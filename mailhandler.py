import gmail
import random

 
mail_id=''   #your gmail id
app_pwd=''   #app pass of gmail id

def send_openacn_email(to,name,acn,pwd):
    con=gmail.GMail(mail_id,app_pwd)
    text=f'''Hello,{name},
We have successfully opened your account with following credentials
Account No = {acn}
Password ={pwd}

Kindly change your password on first login

Thanks
ABC Bank
Noida
'''
    msg=gmail.Message(to=to,text=text,subject='Account Opened')
    con.send(msg)

def send_closeacn_email(to,name,otp):
    con=gmail.GMail(mail_id,app_pwd)
    text=f'''Hello,{name},
Here is the OTP to close your account
OTP = {otp}

Kindly share with Bank Admin

Thanks
ABC Bank
Noida
'''
    msg=gmail.Message(to=to,text=text,subject='Account Closing OTP')
    con.send(msg)   

def send_fpotp_email(to,name,otp):
    con=gmail.GMail(mail_id,app_pwd)
    text=f'''Hello,{name},
Here is the OTP to recover your password
OTP = {otp}

Kindly share with Bank Admin

Thanks
ABC Bank
Noida
'''
    msg=gmail.Message(to=to,text=text,subject='Password Recover OTP')
    con.send(msg)  
