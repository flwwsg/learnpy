#-*- coding: utf-8 -*-
'''
file:sendmail.py
desc: using 1150712418@qq.com to send email
'''

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from code.misc import DEBUG

if DEBUG:
	MYRECEIVER = ['2319406132@qq.com']
else:
	MYRECEIVER = ['190971120@qq.com','2319406132@qq.com']

SUCCSUBJECT = '打包完成'
SUCCBODY = '打包%s完成, 本次打包开始时间为%s, %s完成打包 '
SUCCBODYEXP = '打包%s完成, 本次打包开始时间为%s, %s完成打包, 但是出现错误，详见日志'
SVNOTFOUND = '在svn.txt地址中无法找到类型为 %s-%s 位于 %s 名为 %s 的swf文件 '
LASTOPNOTCLEAN = '上次运行时程序意外中止，请查看tmp目录 '

def sendMail(receiver,subject,fname=None,mbody=None,server=None):
	if not server:
		server=dict()
		server['host'] ='smtp.qq.com'
		server['usr'] = '1150712418@qq.com'
		server['pwd'] = 'yarqzodyzfakggja'
		server['port'] = 465

	encode = 'utf-8'
	msg = MIMEMultipart()
	if not mbody:
		mbody = MIMEText('Python email', 'plain', encode)
	else:
		mbody = MIMEText(mbody,'plain',encode)
	msg.preamble = 'You will not see this in a MIME-aware mail reader'
	msg['From'] = server['usr']
	msg['To'] = receiver
	msg['Subject'] = subject
	
	if fname:
		att = MIMEText(open(fname,'rb').read(),'base64',encode)
		att.add_header('Content-Disposition', 'attachment', filename=fname)
		msg.attach(att)

	msg.attach(mbody)

	try:
		smail = smtplib.SMTP_SSL(server['host'], 465)
		smail.login(server['usr'], server['pwd'])
		# smail.send_message(msg)
		smail.sendmail(server['usr'], receiver, msg.as_string())
		# print('Email send successful')
	except smtplib.SMTPException:
		print('Failing to send email' )
	finally:
		smail.quit()



