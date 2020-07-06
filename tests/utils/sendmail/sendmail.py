# smtplib 用于邮件的发信动作
import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header
# 用于构建邮件头
  
# 发信方的信息：发信邮箱，QQ 邮箱授权码
from_addr = 'xiuxi.sun@qq.com'
password = 'jdvtetkivptobeja'
  
# 收信方邮箱
to_addr = ['v-xisu@microsoft.com', 'xiuxi.sun@qq.com']
    
# 发信服务器
smtp_server = 'smtp.qq.com'
 
# 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
msg = MIMEText('DEV 版本pipeline 测试失败，详细信息请参考 Link：*******','plain','utf-8')
     
# 邮件头信息
msg['From'] = Header(from_addr)
msg['Subject'] = Header('ansible-collection DEV TEST')
    
# 开启发信服务，这里使用的是加密传输
server = smtplib.SMTP_SSL()
server.connect(smtp_server,465)
# 登录发信邮箱
server.login(from_addr, password)
# 发送邮件
for mail_box in to_addr:
    msg['To'] = Header(mail_box)
    server.sendmail(from_addr, mail_box, msg.as_string())
# 关闭服务器
server.quit()
