#!/usr/bin/python
#
# Copyright (c) 2020 Fred-sun, <v-xisu@microsoft.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import smtplib
import sys
from email.mime.text import MIMEText
from email.header import Header

from_addr = sys.argv[1]
password = sys.argv[2]
to_addr = ['xiuxi.sun@qq.com', ]

smtp_server = 'smtp.qq.com'

msg = MIMEText('DEV ver pipeline test fail，detail info as Link：*******', 'plain', 'utf-8')

msg['From'] = Header(from_addr)
msg['Subject'] = Header('ansible-collection DEV TEST')

server = smtplib.SMTP_SSL()
server.connect(smtp_server, 465)
server.login(from_addr, password)
for mail_box in to_addr:
    msg['To'] = Header(mail_box)
    server.sendmail(from_addr, mail_box, msg.as_string())
server.quit()
