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
from aws_cdk import aws_stepfunctions as sfn
from aws_cdk import aws_stepfunctions_tasks as tasks
from constructs import Construct

import constants as c

STACK_NAME = "rent-spider"


class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ECS
        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id="vpc-145a3a6e")
        cluster = ecs.Cluster(self, "Cluster", cluster_name=STACK_NAME, vpc=vpc)
        task_definition = ecs.FargateTaskDefinition(
            self,
            "TaskDef",
            memory_limit_mib=8192,
            cpu=2048,
            runtime_platform=ecs.RuntimePlatform(
                operating_system_family=ecs.OperatingSystemFamily.LINUX,
            ),
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
        task_definition.add_container("Container", image=image)

        # Step Function
        sfn_map = sfn.Map(
            self, "Map", max_concurrency=1, items_path=sfn.JsonPath.string_at("$.websites")
        )
        sfn_map.iterator(
            tasks.EcsRunTask(
                self,
                "EcsRunTask",
                integration_pattern=sfn.IntegrationPattern.RUN_JOB,
                cluster=cluster,
                task_definition=task_definition,
                subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                container_overrides=[
                    tasks.ContainerOverride(
                        container_definition=ecs.ContainerDefinition(
                            self,
                            "ContainerDefinition",
                            task_definition=task_definition,
                            image=image,
                            entry_point=["sh", "-c"],
                        ),
                        command=sfn.JsonPath.list_at("$.commands"),
                    )
                ],
                launch_target=tasks.EcsFargateLaunchTarget(
                    platform_version=ecs.FargatePlatformVersion.LATEST
                ),
            )
        )
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
        sfn_input = {
            "websites": [
                {
                    "commands": [
                        f"cd rent_spider; git pull; xvfb-run -- python3 main.py -u -r -i {website['class_name']}"
                    ]
                }
                for website in c.WEBSITES
            ]
        }
        rule = events.Rule(
            self,
            "Rule",
            schedule=events.Schedule.cron(minute="0", hour="16,23"),
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
InfraStack(
    app,
    STACK_NAME,
    env={"account": os.environ["CDK_DEFAULT_ACCOUNT"], "region": os.environ["CDK_DEFAULT_REGION"]},
)


app.synth()
