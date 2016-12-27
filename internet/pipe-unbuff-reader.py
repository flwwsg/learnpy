'''pip-unbuff-reader.py'''
import os
for line in os.popen('python3 -u pipe-unbuff-writer.py'):
	print(line, end='')
