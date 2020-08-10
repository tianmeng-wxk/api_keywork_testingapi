import requests
import yaml, os,logging,time
import mysql.connector
import smtplib
from email.mime.text import MIMEText#支持html格式
from email.mime.multipart import MIMEMultipart
from email.header import Header

def read_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print(data)
        return data

def write_yaml(extract_dict):
    with open("./config/extract.yaml", 'w') as f:
        yaml.dump(extract_dict,f)

def read_yaml_extract(data):
    with open("./config/extract.yaml", 'r') as f:
        cfg = yaml.load(f,Loader=yaml.FullLoader)
        data=cfg[data]
        return data

def connect_mysql(sql):
    ccon=mysql.connector.connect(
        host='localhost',
        user='root',
        password='wxk111',
        database='first'
    )
    print(ccon)
    cmd=ccon.cursor()
    # cmd.execute("show databases;")
    # for x in cmd:
    #     print(x)
    cmd.execute("{}".format(sql))
    res=cmd.fetchall()
    return res[0][0]


def log():
    logger=logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        sh = logging.StreamHandler()
        fh=logging.FileHandler(filename="./log/{}_log".format(time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime())),encoding="utf-8")
        formator=logging.Formatter(fmt="%(asctime)s %(filename)s %(levelname)s %(msg)s", datefmt="%Y-%m-%d %X")
        sh.setFormatter(formator)
        fh.setFormatter(formator)
        logger.addHandler(fh)
        logger.addHandler(sh)
    return logger


#发送附件邮件
def send_email(email_path):
    message = MIMEMultipart()
    #邮件内容
    text = """
    请输入你想说的邮件内容
    """
    message.attach(MIMEText(_text=text, _subtype='plain', _charset="utf-8"))
    #需要发送的附件的路径
    with open(email_path, 'rb') as f:
        content = f.read()
    att1 = MIMEText(content, "base64", "utf-8")
    att1["Content-Type"] = 'application/octet-stream'
    att1['Content-Disposition'] = 'attachment; filename = "report.html"'
    message.attach(att1)

    #邮件主题
    message["Subject"] = Header("主题", "utf-8").encode()
    message["From"] = Header("tianmeng", "utf-8")
    message["To"] = Header('tianmeng_wxk', "utf-8")

    try:
        smtp = smtplib.SMTP()
        #smtp = smtplib.SMTP_SSL('smtp.163.com', 465)
        smtp.connect(host="smtp.qq.com", port=587)
        smtp.login(user="3394788013@qq.com", password="lizceyidpekpdbhd")
        sender = "3394788013@qq.com"
        receiver = ['tianmeng_wxk@163.com']
        smtp.sendmail(sender, receiver, message.as_string())
        log().info("发送邮件成功")
        return email_path
    except smtplib.SMTPException as e:
        log().info("发送邮件失败，失败信息：{}".format(e))

#发送html格式邮件（需要修改报告源码）
def send_mail(email_path):
    with open(email_path, 'rb') as f:
        content = f.read()
    host = "smtp.qq.com"
    port = 587
    sender = "3394788013@qq.com"
    password = "lizceyidpekpdbhd"
    receiver = "tianmeng_wxk@163.com"
    message = MIMEText(content, "HTML", "UTF-8")
    message["Subject"] = "接口测试"
    message["From"] = sender
    message["To"] = receiver
    try:
        smtp = smtplib.SMTP(host, port)
        smtp.login(sender,password)
        smtp.sendmail(sender, receiver, message.as_string())
        log().info("发送邮件成功")
    except smtplib.SMTPException as e:
        log().info("发送邮件失败，失败信息：{}".format(e))