import requests
import yaml, os,logging,time
import mysql.connector

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
