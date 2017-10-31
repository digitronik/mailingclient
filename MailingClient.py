#------------------------------------------------------------------------------
#    Platform        : AMO Mailing Client
#    Project Name    : AMO
#    Author          : Nikhil Dhandre
#    Start Date      : 03-04-2017
#    Last Modified   : 03-04-2017
#------------------------------------------------------------------------------

#-----------------------------import lib---------------------------------------
import os
import datetime
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from base64 import b64decode as dc
import urllib2

#------------------------------------------------------------------------------
def check_int_conn():
    try:
        urllib2.urlopen("http://live.com", timeout = 5)
        return True
    except:
        return False
#------------------------------------------------------------------------------
def fetch_path():
    try:
        dt_2hr_back = datetime.datetime.now() - datetime.timedelta(hours = 1)
        conf_f = open("conf.db", "r")
        searchlines = conf_f.readlines()
        conf_f.close()
        for line in searchlines:
            if line.split("%")[0] == "$dirc":
                dirc = line.split("%")[1]
        pth_yr = str(dt_2hr_back.year)
        pth = os.path.join(dirc, pth_yr)
        pth_month = str(dt_2hr_back.strftime("%b"))
        pth = os.path.join(pth, pth_month)
    except:
        print("Error: Directory not set or fail")
        return None
    else:
        return pth

#------------------------------------------------------------------------------
def search_files():
    try:
        pth = fetch_path()
        if pth:
            #print pth
            all_file = os.listdir(pth)
            #newest = max(glob.iglob(os.path.join(pth, '*.txt')), key=os.path.getctime)
        else:
            print("Path not found")
            return None
    except:
        print("Error: search file fail")
        return None
    else:
        return [all_file, pth]

#------------------------------------------------------------------------------
def login():
    try:
        conf_f = open("conf.db", "r")
        searchlines = conf_f.readlines()
        for line in searchlines:
            if line.split("%")[0] == "$c_user":
                usr = dc(line.split("%")[1])
            if line.split("%")[0] == "$c_pass":
                pas =  dc(line.split("%")[1])
            if line.split("%")[0] == "$s_user":
                to_string = line.split("%")[1]
            if line.split("%")[0] == "$amo":
                amo = line.split("%")[1]

        to_list = to_string.split(",")
        to_send = []

        for to in to_list:
            to_send.append(dc(to))
        conf_f.close()

        #print to_send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(usr, pas)
    except:
        print("Error: fail to login")
        return None
    else:
        print "Email Client Status : Login "
        return [server, usr, to_send, amo]
#------------------------------------------------------------------------------
def email(f_path):
    try:
        log = login()

        if None not in log:
            server = log[0]
            path, file_tel = os.path.split(f_path)
            msg = MIMEMultipart()
            msg['Subject'] = "AMO-"+ log[3] +":" + file_tel
            msg['From'] = log[1]
            msg['To'] = recipients = ", ".join(log[2])

            try:
                f = file(f_path)
                attachment = MIMEText(f.read())
                attachment.add_header('Content-Disposition','attachment', filename=file_tel)
                msg.attach(attachment)
            except:
                print("Error: Attaching file fail")
                return None

            try:
                # The actual mail send
                server.sendmail(log[1], log[2], msg.as_string())
            except:
                print("Email Service not responding")
                return None
            else:
                print("Email Send successfully")

            if server:
                server.quit()
                print("Email Client Status : Logout")
        #else:
            #print("Error: returning log fail")
    except:
        print("Mailing fuction fail")
        return None
    else:
        return True
#------------------------------------------------------------------------------

#---------------------------Main-----------------------------------------------

if __name__ == "__main__":
    while True:
        if check_int_conn():
            #print("Internet Connected")
            log_name = os.path.join("Logs","log.txt")
            try:
                l_r = open(log_name,'r')
            except:
                l_w = open(log_name,'w+')
                l_w.write("Sended files \n")
                l_w.close()
                l_r = open(log_name,'r')

            log_lines = l_r.readlines()
            #print log_lines
            l_r.close()

            fetch_data = search_files()
            if fetch_data[0]:
                for d in fetch_data[0]:
                    h,t = os.path.splitext(d)
                    file_dt = datetime.datetime.strptime(h, "%d.%m.%Y")
                    file_d = datetime.datetime.date(file_dt)
                    current_d = datetime.date.today()

                    if file_d != current_d:
                        if log_lines:
                            if d + "\n" in log_lines:
                                pass
                            else:
                                #print(d + " sending to server")
                                f_path = os.path.join(fetch_data[1], d)
                                #print f_path
                                status = email(f_path)
                                #print login()
                                #status = False
                                if status:
                                    log_w = open(log_name, "a")
                                    log_w.write(d + "\n")
                                    log_w.close()
                                    time.sleep(30)
            else:
                pass
        else:
            pass
            print("Internet disconnected")
        time.sleep(120)
