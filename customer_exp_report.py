# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader,select_autoescape
from jinja_markdown import MarkdownExtension
import os
import time
from helpers import *
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cephQeInfra import commonFunctions
from datetime import datetime, date, timedelta
import pytz

import sys

target=""

UTC = pytz.utc
IST = pytz.timezone('Asia/Kolkata')
datetime_ist = datetime.now(IST)
start_time=datetime_ist.strftime("%d %b %Y %H:%M")

end_date =  date.today()
start_date = date.today() - timedelta(7)
period = str(start_date)+" To "+str(end_date)

sender = "mobisht@redhat.com"
recipients = ["mobisht@redhat.com"]

msg = MIMEMultipart("mixed")
msg["Subject"] = "Customer Experience Report : "+period
msg["From"] = sender
msg["To"] = ", ".join(recipients)

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir=os.path.join(project_dir, "bugzilla-reports-tool/html_template")

bugs=get_customer_bug_reported()

items_count={"Bugs Reported":len(bugs),"Customer Escalation":len(get_customer_ex_escalation()),"Hotfix Request":len(get_hotfix_count()),
            "RFE Bugs":len(get_customer_ex_rfe_bug()),"Needinfo Requested":len(get_customer_ex_needinfo_req()),
            "QE_Test_Flag +":len(get_customer_ex_qe_test_flag_plus()),"QE_Test_Flag -":len(get_customer_ex_qe_test_flag_minus()),
            "Customer Opened Document Bugs":len(get_customer_ex_document_bugs_count()),"General Trend/Pattern":""}

jinja_env = Environment(extensions=[MarkdownExtension],
    loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )
template = jinja_env.get_template("customer_exp_report.html")
html1 = template.render(items_count=items_count)
table1 = MIMEText(html1, "html")
msg.attach(table1)

if items_count["Bugs Reported"]>0:
    items=[]
    for  idx, bug in enumerate(bugs):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        hotfix_request=commonFunctions.get_hotfix_status(bug.flags)
        an_item = dict(bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items.append(an_item)
    jinja_env = Environment(extensions=[MarkdownExtension],
        loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
    template = jinja_env.get_template("customer_ex_bug_reported.html")
    html2 = template.render(items=items)
    table2 = MIMEText(html2, "html")
    msg.attach(table2)

if items_count["Customer Escalation"]>0:
    bugs_esc=get_customer_ex_escalation()
    items1=[]
    for  idx, bug in enumerate(bugs_esc):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        hotfix_request=commonFunctions.get_hotfix_status(bug.flags)
        an_item1 = dict(bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items1.append(an_item1)
    jinja_env = Environment(extensions=[MarkdownExtension],
        loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
    template = jinja_env.get_template("customer_ex_cus_esc.html")
    html3 = template.render(items1=items1)
    table3 = MIMEText(html3, "html")
    msg.attach(table3)

if items_count["Hotfix Request"]>0:
    bugs_hotfix=get_hotfix_count()
    items2=[]
    for  idx, bug in enumerate(bugs_hotfix):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        hotfix_request=commonFunctions.get_hotfix_status(bug.flags)
        an_item2 = dict(bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items2.append(an_item1)
    jinja_env = Environment(extensions=[MarkdownExtension],
        loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
    template = jinja_env.get_template("customer_ex_cus_hotfix.html")
    html4 = template.render(items2=items2)
    table4 = MIMEText(html4, "html")
    msg.attach(table4)

if items_count["RFE Bugs"]>0:
    bugs_rfe = get_customer_ex_rfe_bug()
    items3=[]
    for  idx, bug in enumerate(bugs_rfe):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        an_item3 = dict(bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items3.append(an_item3)
    jinja_env = Environment(extensions=[MarkdownExtension],
        loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
    template = jinja_env.get_template("customer_ex_cus_rfe.html")
    html5 = template.render(items3=items3)
    table5 = MIMEText(html5, "html")
    msg.attach(table5)

if items_count["Needinfo Requested"]>0:
    bugs_needinfo = get_customer_ex_needinfo_req()
    items4=[]
    for  idx, bug in enumerate(bugs_needinfo):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        hotfix_request=commonFunctions.get_hotfix_status(bug.flags)
        an_item4 = dict(bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items4.append(an_item4)
    jinja_env = Environment(extensions=[MarkdownExtension],
        loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
    template = jinja_env.get_template("customer_ex_cus_needinfo.html")
    html6 = template.render(items4=items4)
    table6 = MIMEText(html6, "html")
    msg.attach(table6)

if items_count["QE_Test_Flag +"]>0:
    bugs_qe_plus = get_customer_ex_qe_test_flag_plus()
    items5=[]
    for  idx, bug in enumerate(bugs_qe_plus):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        hotfix_request=commonFunctions.get_hotfix_status(bug.flags)
        an_item5 = dict(bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items5.append(an_item5)
    jinja_env = Environment(extensions=[MarkdownExtension],
        loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
    template = jinja_env.get_template("customer_ex_cus_qe_plus.html")
    html7 = template.render(items5=items5)
    table7 = MIMEText(html7, "html")
    msg.attach(table7)

if items_count["QE_Test_Flag -"]>0:
    bugs_qe_minus = get_customer_ex_qe_test_flag_minus()
    items6=[]
    for  idx, bug in enumerate(bugs_qe_minus):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        hotfix_request=commonFunctions.get_hotfix_status(bug.flags)
        an_item6 = dict(bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items6.append(an_item6)
    jinja_env = Environment(extensions=[MarkdownExtension],
        loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
    template = jinja_env.get_template("customer_ex_cus_qe_minus.html")
    html8 = template.render(items6=items6)
    table8 = MIMEText(html8, "html")
    msg.attach(table8)

if items_count["Customer Opened Document Bugs"]>0:
    bugs_doc = get_customer_ex_document_bugs_count()
    items7=[]
    for  idx, bug in enumerate(bugs_doc):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        hotfix_request=commonFunctions.get_hotfix_status(bug.flags)
        an_item7 = dict(bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items7.append(an_item7)
    jinja_env = Environment(extensions=[MarkdownExtension],
        loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
    template = jinja_env.get_template("customer_ex_cus_doc.html")
    html9 = template.render(items7=items7)
    table9 = MIMEText(html9, "html")
    msg.attach(table9)

try:
            s = smtplib.SMTP("localhost")
            s.sendmail(sender, recipients, msg.as_string())
            s.quit()
            print(
                "Results have been emailed to {recipients}".format(
                    recipients=recipients
                )
            )

except Exception as e:
            print("\n")
            log.exception(e)
            print(e)
print("done")
