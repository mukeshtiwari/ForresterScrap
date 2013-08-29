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

		atag = page.findAll('a')
		url = ''.join ( [ self.baseurl, atag[0]['href'] ] )
		#print url
		info = [ tag.renderContents() for tag in atag ] 
		beforetweet = ' # '.join ( info [ 0 : info.index('Tweet') ] )
		afterreadmore = []
		#beware some article may not have Read more
		try:
			afterreadmore = info [ info.index('Read more')+1 : ]
		except ValueError:
			afterreadmore = []

		blogtime = ' '.join ( page.find('p').renderContents().split('</a>')[-1].strip().split(' ')[2:] )
		recom = ' '.join ( [ page.find ( 'span' , attrs = { 'class':'recommCount'} ).renderContents() , 'recommendation' ] )
		fpart = ' # '.join ( [ beforetweet, blogtime, recom ] )

		if afterreadmore == [] :
			print ' # '.join ( [ 'Blog', url, fpart, ' ' ] )
		else: 
			for category in afterreadmore:
				print ' # '.join ( [ 'Blog', url, fpart , category ] ) 



if __name__=='__main__':

	forrester = ForresterScrap()
	forrester.downloadPage()


