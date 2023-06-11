#!/usr/bin/env python3

import os

import aws_cdk as cdk
from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as events_targets
from aws_cdk import aws_iam as iam
from aws_cdk import aws_logs as logs
from aws_cdk import aws_stepfunctions as sfn
from aws_cdk import aws_stepfunctions_tasks as tasks
from constructs import Construct

import constants as c

STACK_NAME = "rent-spider"
MEMORY_RESERVATION_MIB = 8192
VPC_ID = {"us-east-1": "vpc-145a3a6e", "us-west-2": "vpc-01f42463bab73d1ef"}
STACK_NAME_MAP = {"us-east-1": STACK_NAME, "us-west-2": STACK_NAME + "-us-west-2"}


class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        region = kwargs["env"]["region"]

        # ECS
        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=VPC_ID[region])
        cluster = ecs.Cluster(self, "Cluster", cluster_name=STACK_NAME, vpc=vpc)
        execution_role = iam.Role(
            self,
            "EcsExecutionRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AmazonECSTaskExecutionRolePolicy"
                )
            ],
        )
        task_definition = ecs.FargateTaskDefinition(
            self,
            "TaskDef",
            memory_limit_mib=MEMORY_RESERVATION_MIB,
            cpu=2048,
            runtime_platform=ecs.RuntimePlatform(
                operating_system_family=ecs.OperatingSystemFamily.LINUX,
            ),
            execution_role=execution_role,
        )
        repository = ecr.Repository(
            self,
            "Repository",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            repository_name=STACK_NAME,
            lifecycle_rules=[
                ecr.LifecycleRule(
                    description="Expire after 3 images",
                    max_image_count=3,
                )
            ],
        )
        image = ecs.ContainerImage.from_ecr_repository(repository)
        log_group = logs.LogGroup(
            self,
            "ECS Log Group",
            log_group_name=f"/ecs/{STACK_NAME}",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        # Step Function
        sfn_map = sfn.Map(
            self, "Map", max_concurrency=1, items_path=sfn.JsonPath.string_at("$.websites")
        )
        ecs_run_task = tasks.EcsRunTask(
            self,
            "EcsRunTask",
            integration_pattern=sfn.IntegrationPattern.RUN_JOB,
            cluster=cluster,
            task_definition=task_definition,
            assign_public_ip=True,
            subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            container_overrides=[
                tasks.ContainerOverride(
                    container_definition=ecs.ContainerDefinition(
                        self,
                        "ContainerDefinition",
                        container_name=STACK_NAME,
                        task_definition=task_definition,
                        image=image,
                        logging=ecs.LogDrivers.aws_logs(stream_prefix="ecs", log_group=log_group),
                        memory_reservation_mib=MEMORY_RESERVATION_MIB,
                        entry_point=["sh", "-c"],
                    ),
                    command=sfn.JsonPath.list_at("$.commands"),
                )
            ],
            launch_target=tasks.EcsFargateLaunchTarget(
                platform_version=ecs.FargatePlatformVersion.LATEST
            ),
        )
        ecs_run_task.add_catch(sfn.Pass(self, "EcsRunTaskCatch"), errors=["States.ALL"])
        wait = sfn.Wait(self, "Wait", time=sfn.WaitTime.duration(cdk.Duration.seconds(30)))
        sfn_map.iterator(wait.next(ecs_run_task))
        definition = sfn_map
        sfn_role = iam.Role(
            self,
            "StepFunctionRole",
            assumed_by=iam.ServicePrincipal("states.amazonaws.com"),
            inline_policies={
                "ecs": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=["ecs:*"],
                            resources=["*"],
                        )
                    ]
                )
            },
        )
        state_machine = sfn.StateMachine(self, "StateMachine", definition=definition, role=sfn_role)

        # Scheduler
        mid = len(c.WEBSITES) // 3
        websites = c.WEBSITES[:mid] if region == "us-west-2" else c.WEBSITES[mid:]
        sfn_input = {
            "websites": [
                {
                    "commands": [
                        f"cd rent_spider; git pull; xvfb-run -- python3 main.py -u -r -p AWS -i {website['class_name']}"
                    ]
                }
                for website in websites
                if website["platform"] == c.Platform.AWS
            ]
        }
        rule = events.Rule(
            self,
            "Rule",
            schedule=events.Schedule.cron(minute="0", hour="11,23"),
        )
        events_role = iam.Role(
            self,
            "EventsRole",
            assumed_by=iam.ServicePrincipal("events.amazonaws.com"),
            inline_policies={
                "ecs": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=["states:StartExecution"],
                            resources=[state_machine.state_machine_arn],
                        )
                    ]
                )
            },
        )
        rule.add_target(
            events_targets.SfnStateMachine(
                state_machine,
                input=events.RuleTargetInput.from_object(sfn_input),
                role=events_role,
            ),
        )


app = cdk.App()
for region in ["us-east-1", "us-west-2"]:
    InfraStack(
        app,
        STACK_NAME_MAP[region],
        env={"account": os.environ["CDK_DEFAULT_ACCOUNT"], "region": region},
    )


app.synth()
