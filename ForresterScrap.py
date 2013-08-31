import re, urllib2
from bs4 import BeautifulSoup


class ForresterScrap():
	
	def __init__( self ):
		self.baseurl = 'http://blogs.forrester.com' 
		self.n = 0

	def connectDatabase(self):
		pass
	
	#don't catch exception here and let the program die. It's fetch the total number of pages so if there is error then die.
	def numberofPages( self ):
			page = urllib2.urlopen( self.baseurl ) . read()
			soup = BeautifulSoup ( page , 'lxml' )
			return int ( soup.find( 'li', attrs = { 'class' :'pager-last last' } ).find( 'a' )['href'].split('=')[-1] )
		
	#don't catch erros here. It's error mode run so it's should be error free otherwise we will have lot of duplicate data. 
	def downloadErrorMode ( self ):
		with open('forrester.dat', 'a' ) as f ,  open ('pagedownloaderror.dat', 'r' ) as p :
			for counter in p:
				url = ''.join( [ self.baseurl, '/?page=',  counter ] )
				pagelist = self.downloadUrl( url )
				f.write( '\n'.join ( [ page for page in pagelist  ] ) )
		#If every thing is correct then delete the file or make it empty.
		with open ('pagedownloaderror.dat', 'w' ) as p :
			p.write('')
			

				
	def downloadPage( self  ):
		counter = 0
		self.n = self.numberofPages( )
		print ''.join ( [ 'Total number of pages = ', str ( self.n ) ] )
		with open('forrester.dat', 'a' ) as f ,  open ('pagedownloaderror.dat', 'a+' ) as p :
			while ( counter <= self.n ):
				try:
					url = ''.join( [ self.baseurl, '/?page=', str ( counter ) ] )
					pagelist =  self.downloadUrl( url ) 
					f.write ( '\n'.join ( [ page for page in pagelist  ] ) )
				except urllib2.HTTPError as e:
					print ''.join ( [ self.baseurl, '  ', str ( e ) ] )
					p.write( ''.join ( [ str ( counter ), '\n' ] ) ) 
				except urllib2.URLError as e:
					print ''.join ( [ self.baseurl, '  ', str ( e ) ] ) 
					p.write( ''.join ( [ str ( counter ), '\n' ] ) )
				except Exception as e:
					print ''.join ( [ self.baseurl, '  ', str ( e ) ] ) 
					p.write( ''.join ( [ str ( counter ), '\n' ] ) )
				print ''.join( [ 'Downloaded page ', str ( counter ) ] )
				counter += 1
			
	def downloadUrl( self, url ):
		page = urllib2.urlopen(url).read()
		soup = BeautifulSoup ( page, 'lxml' ) 
		pagelist = soup.findAll ( 'div', attrs = { 'id' : re.compile ( r'node-[0-9]{1,}' ) } )
		return [ self.parseStatement ( page ) for page in pagelist ]


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
			return ' # '.join ( [ 'Blog', url, fpart, ' ' ] )
		else: 
			return '\n'.join ( [ ' # '.join ( [ 'Blog', url, fpart , category ] ) for category in afterreadmore ] )


if __name__=='__main__':

	forrester = ForresterScrap()
	forrester.downloadPage()


