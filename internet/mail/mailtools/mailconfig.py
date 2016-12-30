#!/usr/bin/python3

MYEMAIL = '1150712418@qq.com'
popservername = 'pop.qq.com'
popusername = MYEMAIL
popport = 995

smtpservername = 'smtp.qq.com'
smtport = 465
smtpusername = MYEMAIL

myaddress = MYEMAIL
mysignature = ('Thanks, \n--LBlue')
mypassword = 'yarqzodyzfakggja'

# yarqzodyzfakggja
pwdfile = './password.txt'
smtppasswdfile = pwdfile
poppasswdfile = pwdfile
sentmailfile = './mailconfig.py'
savemailfile = './savemail.txt'

fetchEncoding = 'utf8'
headersEncodeTo = None

fetchlimit = 25

