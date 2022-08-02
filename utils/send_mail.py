import configparser
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr

import constants as c


def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))


def generate_header():
    header = ""
    for column_name in c.ROOM_TABLE_COLUMNS_NAME:
        header += f"""<th style="border: 1px solid #dddddd;text-align: center;padding: 8px; min-width: 100px;">{column_name}</th>"""
    header = "<tr>" + header + "</tr>"
    return header


def generate_table(rooms):
    content = generate_header()
    for room in rooms:
        is_room_updated = isinstance(room, tuple)
        if is_room_updated:
            prev_room, room = room
        room_content = ""
        for column_name in c.WEBSITE_ROOM_VIEW_COLUMNS:
            if column_name in c.WEBSITE_ROOM_VIEW_ADDITIONAL_COLUMNS:
                continue
            cell_content = room[column_name]
            if column_name == c.ROOM_WEBSITE_NAME_COLUMN:
                cell_content = f"""<a href="{room[c.WEBSITE_URL_COLUMN]}">[{room[c.WEBSITE_PRIORITY_COLUMN]}] {room[c.ROOM_WEBSITE_NAME_COLUMN]}</a>"""
            elif is_room_updated and room[column_name] != prev_room[column_name]:
                cell_content = f"<del>{prev_room[column_name]}</del> {room[column_name]}"
            room_content += f"""<td style="border: 1px solid #dddddd;text-align: center;padding: 8px;">{cell_content}</td>"""
        content += "<tr>" + room_content + "</tr>"
    return """<table style="border-collapse: collapse;">""" + content + "</table>"


def send_email(receivers, receivers_cc, subject, content):
    username = c.EMAIL_SENDER
    mail_from = c.EMAIL_SENDER
    config = configparser.ConfigParser()
    config.read("secrets.cfg")
    password = config["email"]["password"]
    mail_body = MIMEText(content, "html", "utf-8")
    mimemsg = MIMEMultipart()
    mimemsg["From"] = format_addr(f"{subject} <'{mail_from}'>")
    mimemsg["To"] = ",".join(receivers)
    mimemsg["Subject"] = subject
    mimemsg["Cc"] = ",".join(receivers_cc)
    mimemsg.attach(mail_body)
    connection = smtplib.SMTP(host=c.SMTP_HOST, port=c.SMTP_PORT)
    connection.starttls()
    connection.login(username, password)
    connection.send_message(mimemsg)
    connection.quit()


def send_notification_email(new_rooms, removed_rooms, updated_rooms):
    content = ""
    if new_rooms:
        content += "<h3>新房源:</h3>" + generate_table(new_rooms)
    if removed_rooms:
        content += "<h3>下架房源:</h3>" + generate_table(removed_rooms)
    if updated_rooms:
        content += "<h3>房源信息更新:</h3>" + generate_table(updated_rooms)
    content += f"""<h3>全部房源:<div><a href="{c.WEB_APP_LINK}">{c.WEB_APP_LINK}</a></div></h3>"""
    content = "<html><body>" + content + "</body></html>"

    send_email(c.EMAIL_RECEIVERS, c.EMAIL_RECEIVERS_DEV, c.NOTIFICATION_EMAIL_SUBJECT, content)


def send_error_email(website_name, error):
    content = f"<h3>{website_name}</h3>"
    content += f"<div>{repr(error)}</div>"
    content = "<html><body>" + content + "</body></html>"
    send_email(c.EMAIL_RECEIVERS_DEV, c.EMAIL_RECEIVERS_DEV, c.ERROR_EMAIL_SUBJECT, content)
