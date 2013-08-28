import re, urllib2
from bs4 import BeautifulSoup


class ForresterScrap():
	
	def __init__( self ):
		self.baseurl = 'http://blogs.forrester.com' 


	def connectDatabase(self):
		pass
	
	def downloadPage( self  ):
		#Run a infinite loop and maintain the node id in Map/Hash. If it's repeating then stop loop. 
		counter = 0
		while ( counter <= 0 ):
			url = ''.join( [ self.baseurl, '/?page', str ( counter ) ] )
			page = urllib2.urlopen(url).read()
			soup = BeautifulSoup ( page, 'lxml' ) 
			pagelist = soup.findAll ( 'div', attrs = { 'id' : re.compile ( r'node-[0-9]{1,}' ) } )
			for page in pagelist:
				self.parseStatement( page  )
				print '\n\n'
			counter += 1
			
	def parseStatement( self, page ):
		#print 'Start of a tag\n'

		atag = page.findAll('a')
		url = ''.join ( [ self.baseurl, atag[0]['href'] ] )
		#print url
		info = ' # '.join ( [ tag.renderContents() for tag in atag ] )
		print ' # '.join( ['Blog', url, info ])
		#for tag in atag:
		#	print tag.renderContents()
		#print 'End of a tag\n'
		#print 'Start of ptag\n'
		#ptag = page.findAll('p')
		#for tag in ptag:
		#	print tag
		#print 'End of ptag'



if __name__=='__main__':

	forrester = ForresterScrap()
	forrester.downloadPage()


