import smtplib
from email.mime.text import MIMEText
from email.header import Header


class SendMail:

    def __init__(self, mail_host):
        self.mail_host = mail_host

    def send(self, title, content, sender, auth_code, receivers):
        message = MIMEText(content, 'html', 'utf-8')
        message['From'] = "{}".format(sender)
        message['To'] = ",".join(receivers)
        message['Subject'] = title
        try:
            smtp_obj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtp_obj.login(sender, auth_code)
            smtp_obj.sendmail(sender, receivers, message.as_string())
            print("ok")

        except Exception as e:
            print(e)


if __name__ == '__main__':
    mail = SendMail("smtp.163.com")
    sender = "15590277678@163.com"
    receivers = ["793655595@qq.com"]
    title = "test email"
    content = """
    可
    <a href="https://baijiahao.baidu.com/s?id=1761421287610998468&wfr=spider&for=pc">more</a>
    """
    auth_code = "NCMOKZTKWKYWFJEV"
    mail.send(title, content, sender, auth_code, receivers)
