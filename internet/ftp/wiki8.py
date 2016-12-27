'''wiki8.py'''
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.connect(host='localhost', user='wdj', passwd='wdj654321',
						db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute('use wikipedia')

class SolutionFound(RuntimeError):
	def __init__(self, msg):
		self.message = msg

def getLinks(fromPageId):
	cur.execute('select toPageId from links where fromPageId =\'%s\'', (fromPageId))
	if not cur.rowcount:
		return None
	else:
		return [x[0] for x in cur.fetchall()]

def constructDict(currentPageId):
	links = getLinks(currentPageId)
	if links:
		return dict(zip(links,[{}]*len(links)))
	return {}

def searchDepth(targetPageId, currentPageId, linkTree, depth):
	if depth == 0:
		return linkTree
	if not linkTree:
		linkTree = constructDict(currentPageId)
		if not linkTree:
			return {}
	if targetPageId in linkTree.keys():
		print('Target '+str(targetPageId)+' found!')
		raise SolutionFound('Page: '+str(currentPageId))

	for branchKey, branchValue in linkTree.items():
		try:
			linkTree[branchKey] = searchDepth(targetPageId, branchKey, {branchValue}, depth-1)
			# print(linkTree)
		except SolutionFound as e:
			print(e.message)
			raise SolutionFound('page: '+str(currentPageId))
	return linkTree

try:
	searchDepth(1000,1,{}, 4)
	
	print('No solution found')
except SolutionFound as e:
	print(e.message)
