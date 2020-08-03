import smtplib
from email.mime.text import MIMEText
from email.header import Header
import argparse,os,sys
def prompt(prompt):
    sys.stdout.write(prompt + ": ")
    sys.stdout.flush()
    return sys.stdin.readline().strip()
def generate_parser():
    parser=argparse.ArgumentParser()
    parser.add_argument("-f","--from",help="send from")
    parser.add_argument("-t","--to",help="send to")
    parser.add_argument("-s","--server",help="mail server")
    parser.add_argument("-xu","--user",help="user at the mail server")
    parser.add_argument("-xp","--password",help="password at the mail server")
    parser.add_argument("-u","--subject","-theme","--title",help="head of the message")
    parser.add_argument("-m","--message","--body",help="message body of the message")
    return parser
def complete_args(args):
    for key,value in args.__dict__.items():
        while not value:
            args.__dict__[key]=value=prompt(key)
def mail(args):
    error_count=0
    while True:
        try :
            #ssl登录
            smtp = smtplib.SMTP_SSL(args.server)
            #set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
            smtp.set_debuglevel(0)
            smtp.ehlo(args.server)
            smtp.login(args.user,args.password)

            msg = MIMEText(args.message, "plain", 'utf-8')
            msg["Subject"] = Header(args.subject, 'utf-8')
            # print(args._)
            msg["From"] = args.__dict__['from']
            msg["To"] = args.to
            smtp.sendmail(args.__dict__['from'], args.to, msg.as_string())
        except Exception:
            error_count+=1
            print("Eroor at the "+str(error_count)+" try:")
            if error_count==10:
                print("error occured "+str(error_count)+" times")
                print("giving up")
                return 1
        else:
            smtp.quit()
            print("successfully sent")
            return 0
if __name__=="__main__":
    parser=generate_parser()
    args=parser.parse_args(sys.argv[1:])
    complete_args(args)
    mail(args)


