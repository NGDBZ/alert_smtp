import os
import smtplib
from email.mime.text import MIMEText
from time import sleep
# 远程电脑的 IP 地址列表
ip_addresses = ["10.16.62.66", "10.16.62.84"]

# 报警通知的电子邮件配置
smtp_server = "smtp.qq.com"#SMTP服务器地址，这里使用的是QQ邮箱的SMTP服务器。
smtp_port = 587#SMTP服务器端口，这里使用的是587端口。
smtp_username = "2284277906@qq.com"#发送邮件的邮箱地址。
smtp_password = "dcftlkhrmtngdjbd"  # 注意，这里需要使用授权码，而不是QQ邮箱的登录密码
from_email = "2284277906@qq.com"#发送邮件的邮箱地址（与smtp_username相同）
to_email = "2284277906@qq.com"#接收邮件的邮箱地址
def is_computer_online(ip):
    response = os.system(f"ping -c 1 {ip}")#使用os.system执行ping命令，检查目标IP地址是否有响应。-c 1表示只发送一次ping请求。
    return response == 0#如果ping命令返回0，表示目标IP地址在线，否则不在线
def send_alert(ip):
    print(f"Sending alert for {ip}")
    subject = f"Alert: {ip} is offline"
    body = f"The computer with IP address {ip} is offline."
    msg = MIMEText(body)#创建一个 MIMEText 对象，用于构建电子邮件的文本内容。将邮件正文 body 作为参数传递给 MIMEText，生成包含邮件内容的对象 msg。
    msg['Subject'] = subject#设置邮件的主题为前面定义的 subject。
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:#使用 smtplib.SMTP 类连接到指定的 SMTP 服务器。smtp_server 和 smtp_port 分别是服务器地址和端口号。
            server.starttls()#启动 TLS（传输层安全）加密，以确保电子邮件的传输过程是安全的。
            server.login(smtp_username, smtp_password)#使用提供的用户名 smtp_username 和密码 smtp_password 登录到 SMTP 服务器。这些凭据是在之前的配置中定义的。
            server.sendmail(from_email, to_email, msg.as_string())#将 MIMEText 对象 msg 转换为字符串格式，以便 sendmail 方法可以发送它。
        print(f"Alert sent for {ip}")
    except Exception as e:
        print(f"Failed to send alert for {ip}: {e}")

def monitor():
    while True:
        for ip in ip_addresses:
            if not is_computer_online(ip):
                send_alert(ip)
        sleep(300)  # 每 5 分钟检查一次
if __name__ == "__main__":
    monitor()

