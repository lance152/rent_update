from email.header import Header
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import parseaddr,formataddr
import smtplib
import glob
import os

base_path = os.path.abspath('.')+'\\'

def send(number):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    from_addr = input('sender')
    password = input('password:')
    to_addr = input('receiver:')

    info = get_info(number)
    print(info)
    msg = MIMEMultipart()
    msg.attach(MIMEText(info[1],'plain','utf-8'))
    msg['Subject'] = Header(info[0],'utf-8').encode()

    imlist = get_pic_path(number)
    for i in imlist:
        image = MIMEImage(open(i,'rb').read())
        image.add_header('Content-Disposition', 'attachment', filename=os.path.basename(i))
        msg.attach(image)

    server = smtplib.SMTP(smtp_server,smtp_port)
    server.starttls()
    server.set_debuglevel(1)
    server.login(from_addr,password)
    server.sendmail(from_addr,to_addr,msg.as_string())
    server.quit()

def get_pic_path(number):
    path = base_path+number+'\\'
    imlist = glob.glob(path+'*.jpg')
    return imlist

def pics(msg):
    pass

def get_info(number):
    path = base_path+number
    with open(path+'\\info.txt','r',encoding='utf-8') as f:
        lines = f.readlines()
        title = lines[0]
        info = ''.join(lines[1:])
        return [title,info]

if __name__ == '__main__':
    send('66121')