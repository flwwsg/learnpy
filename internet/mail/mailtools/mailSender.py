import mailconfig
import smtplib, os, mimetypes
import email.utils, email.encoders
from mailTool import MailTool, SilentMailTool

from email.message 			import Message
from email.mime.multipart 	import MIMEMultipart
from email.mime.audio 		import MIMEAudio
from email.mime.image 		import MIMEImage
from email.mime.text 		import MIMEText
from email.mime.base 		import MIMEBase
from email.mime.application import MIMEApplication

def fix_encode_base64(msgobj):
	linelen = 76
	from email.encoders import encode_base64

	encode_base64(msgobj)
	text = msgobj.get_payload()
	if isinstance(text, bytes):
		text = text.decode('utf-8')

	lines = []
	text = text.replace('\n', '')
	while text:
		line, text = text[:linelen], text[linelen:]
		lines.append(line)
	msgobj.set_payload('\n'.join(lines))

def fix_text_required(encodingname):
	from email.charset import Charset, BASE64, QP

	charset = Charset(encodingname)
	bodyenc = charset.body_encoding
	return bodyenc in (None, QP)

class MailSender(MailTool):
	def __init__(self, smtpserver=None, tracesize=256):
		self.smtpServerName = smtpserver or mailconfig.smtpservername
		self.tracesize = tracesize

	def sendMessage(self, From, To, Subj, extrahdrs, bodytext, attaches,
					saveMailSeparator=(('='*80) + 'PY\n'),
					bodytextEncoding = 'utf-8',
					attachesEncodings = None):
		if fix_text_required(bodytextEncoding):
			if not isinstance(bodytext, str):
				bodytext = bodytext.decode(bodytextEncoding)
		else:
			if not isinstance(bodytext, bytes):
				bodytext = bodytext.encode(bodytextEncoding)

		if not attaches:
			msg = Message()
			msg.set_payload(bodytext, charset=bodytextEncoding)
		else:
			msg = MIMEMultipart()
			self.addAttachments(msg, bodytext, attaches,
									 bodytextEncoding, attachesEncodings)
		hdrenc = mailconfig.headersEncodeTo or 'utf-8'
		Subj = self.encodeHeader(Subj, hdrenc)
		From = self.encodeAddrHeader(From, hdrenc)
		To = [self.encodeAddrHeader(T, hdrenc) for T in To]
		Tos = ', '.join(To)

		msg['From'] = From
		msg['To'] = Tos
		msg['Subject'] = Subj
		msg['Date'] = email.utils.formatdate()
		recip = To
		for name, value in extrahdrs:
			if value:
				if name.lower() not in ['cc', 'bcc']:
					value = self.encodeHeader(value,hdrenc)
					msg[name] = value
				else:
					value = [self.encodeAddrHeader(V, hdrenc) for V in value]
					recip += value

					if name.lower() != 'bcc':
						msg[name] = ', '.join(value)
		recip = list(set(recip))
		fullText = msg.as_string()

		self.trace('Sending to...'+str(recip))
		self.trace(fullText[:self.tracesize])
		server = smtplib.SMTP_SSL(self.smtpServerName, 465)
		self.getPassword()
		self.authenticateServer(server)

		try:
			failed = server.sendmail(From, recip, fullText)
		except:
			server.close()
			raise
		else:
			server.quit()
		self.saveSentMessage(fullText, saveMailSeparator)
		if failed:
			class SomeAddrsFailed(Exception): pass
			raise SomeAddrsFailed('Failed addrs:%s\n' % failed)

	def addAttachments(self, mainmsg, bodytext, attaches,
							 bodytextEncoding, attachesEncodings):	
		msg = MIMEText(bodytext, _charset=bodytextEncoding)
		mainmsg.attach(msg)

		encodings = attachesEncodings or (['utf-8'] * len(attaches))
		for (filename, fileencode) in zip(attaches, encodings):
			if not os.path.isfile(filename):
				continue
			contype, encoding = mimetypes.guess_type(filename)
			if contype is None or encoding is not None:
				contype = 'application/octet-stream'
			self.trace('Adding '+contype)

			maintype, subtype = contype.split('/', 1)
			if maintype == 'text':
				if fix_text_required(fileencode):
					data = open(filename, 'r', encoding=fileencode)
				else:
					data = open(filename, 'rb')
				msg = MIMEText(data.read(), _subtype=subtype, _charset=fileencode)
				data.close()
			elif maintype == 'image':
				data = open(filename, 'rb')
				msg = MIMEImage(data.read(), _subtype=subtype, 
								_encoder=fix_encode_base64)
				data.close()
			elif maintype == 'audio':
				data = open(filename, 'rb')
				msg = MIMEAudio(data.read(), _subtype=subtype,
								_encoder=fix_encode_base64)
				data.close()
			elif maintype == 'application':
				data = open(filename, 'rb')
				msg = MIMEApplication(data.read(), _subtype=subtype,
								_encoder=fix_encode_base64)
				data.close()
			else:
				data = open(filename, 'rb')
				msg = MIMEBase(maintype,subtype)
				msg.set_payload(data.read())
				fix_encode_base64(msg)

			basename = self.encodeHeader(os.path.basename(filename))
			msg.add_header('Content-Disposition', 'attachment', filename=basename)
			mainmsg.attach(msg)

		# text outside mime structure, seen by non-MIME mail readers
		mainmsg.preamble = 'A multi-part MIME format message.\n'
		mainmsg.epilogue = ''

	def saveSentMessage(self, fullText, saveMailSeparator):
		try:
			sentfile = open(mailconfig.sentmailfile, 'a', encoding=mailconfig.fetchEncoding)
			if fullText[-1] != '\n': fullText += '\n'
			sentfile.write(saveMailSeparator)
			sentfile.write(fullText)
			sentfile.close()
		except:
			self.trace('Could not save sent message')

	def encodeHeader(self, headertext, unicodeencoding='utf-8'):
		try:
			headertext.encode('utf-8')
		except:
			try:
				hdrobj = email.header.make_header([(headertext, unicodeencoding)])
				headertext = hdrobj.encode()
			except:
				pass
		return headertext

	def encodeAddrHeader(self, headertext, unicodeencoding='utf-8'):
		try:
			pairs = email.utils.getaddresses([headertext])
			encoded = []
			for name, addr in pairs:
				try:
					name.encode('ascii')
				except UnicodeError:
					try:
						uni = name.encode(unicodeencoding)
						hdr = email.header.make_header([(uni, unicodeencoding)])
						name = hdr.encode()
					except:
						name = None
				joined = email.utils.formataddr(name, addr)
				encoded.append(joined)

			fullhdr = ', '.join(encoded)
			if len(fullhdr) > 72 or '\n' in fullhdr:
				fullhdr = ',\n '.join(encoded)
			return fullhdr
		except:
			return self.encodeHeader(headertext)

	def authenticateServer(self, server):
		pass

	def getPassword(self):
		pass

class MailSenderAuth(MailSender):
	smtpPassword = None
	def __init__(self, smtpserver=None, smtpuser=None):
		MailSender.__init__(self, smtpserver)
		self.smtpuser = smtpuser or mailconfig.smtpuser

	def authenticateServer(self, server):
		server.login(self.smtpuser, self.smtpPassword)

	def getPassword(self):
		if not self.smtpPassword:
			try:
				localfile = open(mailconfig.smtppasswordfile)
				MailSenderAuth.smtpPassword = localfile.read().strip()
				self.trace('local file password'+repr(self.smtpPassword))
			except:
				MailSenderAuth.smtpPassword = self.askSmtpPassword()

	def askSmtpPassword(self):
		assert False, 'Subclass must define method'

class MailSenderAuthConsole(MailSenderAuth):
	def askSmtpPassword(self):
		import getpass
		prompt = 'Password for %s on %s?' % (
				self.smtpuser, self.smtpServerName)
		return getpass.getpass(prompt)

class SilentMailSender(SilentMailTool, MailSender):
	pass

