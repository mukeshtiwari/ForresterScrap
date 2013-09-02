import re, urllib2, os, collections
from bs4 import BeautifulSoup

class OrderedSet(collections.MutableSet):

	def __init__(self, iterable=None):
		        self.end = end = [] 
			end += [None, end, end]         # sentinel node for doubly linked list
			self.map = {}                   # key --> [key, prev, next]
			if iterable is not None:
				self |= iterable
	def __len__(self):
		     	return len(self.map)

	def __contains__(self, key):
		        return key in self.map
	def add(self, key):
		        if key not in self.map:
				end = self.end
				curr = end[1]
				curr[2] = end[1] = self.map[key] = [key, curr, end]
	def discard(self, key):
		        if key in self.map:        
				key, prev, next = self.map.pop(key)
				prev[2] = next
				next[1] = prev

	def __iter__(self):
		        end = self.end
			curr = end[2]
			while curr is not end:
				yield curr[0]
				curr = curr[2]

	def __reversed__(self):
		        end = self.end
			curr = end[1]
			while curr is not end:
				yield curr[0]
				curr = curr[1]
	def pop(self, last=True):
		if not self:
			raise KeyError('set is empty')
		key = self.end[1][0] if last else self.end[2][0]
		self.discard(key)
		return key
	def __repr__(self):
		if not self:
			return '%s()' % (self.__class__.__name__,)
		return '%s(%r)' % (self.__class__.__name__, list(self))
	def __eq__(self, other):
		if isinstance(other, OrderedSet):
			return len(self) == len(other) and list(self) == list(other)
		return set(self) == set(other)

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
		with open('errormode.dat', 'a' ) as f ,  open ('pagedownloaderror.dat', 'r' ) as p :
			for counter in p:
				url = ''.join( [ self.baseurl, '/?page=',  counter ] )
				pagelist = self.downloadUrl( url )
				f.write( '\n'.join ( [ page for page in pagelist  ] ) )
		#If every thing is correct then merge the errormode file with main file forrester.dat and delete both files.
		self.mergeFiles( 'forrester.dat', 'errormode.dat' )
		os.remove( 'pagedownload.dat')

			
	def mergeFiles ( self, firstfile, secondfile ):
		with open ( firstfile, 'r+' ) as first, open ( secondfile, 'r' ) as second:
			combined = iter ( [ set ( first ) , set ( second ) ] )
			final =  ''.join ( sorted ( frozenset().union ( *combined ) ) )
			#f =  OrderedSet ( first ) 
			#s =  OrderedSet ( second ) 
			first.write ( final  ) 
		os.remove ( secondfile )


	def downloadPage( self, numpage = None  ):
		counter = 0
		if numpage is not None: 
			self.n = 2 # numpage
		else:
			self.n = 2 # self.numberofPages( )
		print ''.join ( [ 'Total number of pages = ', str ( self.n ) ] )
		with open('forrester.dat', 'a' ) as f,  open( 'tmpmerging.dat', 'a' ) as t, open ('pagedownloaderror.dat', 'a' ) as p :
			while ( counter <= self.n ):
				try:
					url = ''.join ( [ self.baseurl, '/?page=', str ( counter ) ] )
					pagelist =  self.downloadUrl ( url ) 
					f.write ( '\n'.join ( [ page for page in pagelist  ] ) )
					print ''.join ( [ 'Downloaded page ', str ( counter ) ] )
				except urllib2.HTTPError as e:
					print ''.join ( [ self.baseurl, '  ', str ( e ) ] )
					p.write( ''.join ( [ str ( counter ), '\n' ] ) ) 
				except urllib2.URLError as e:
					print ''.join ( [ self.baseurl, '  ', str ( e ) ] ) 
					p.write( ''.join ( [ str ( counter ), '\n' ] ) )
				except Exception as e:
					print ''.join ( [ self.baseurl, '  ', str ( e ) ] ) 
					p.write( ''.join ( [ str ( counter ), '\n' ] ) )
				counter += 1
			self.mergeFiles( 'forrester.dat', 'tmpmerging.dat' )

			
	def downloadUrl( self, url ):
		page = urllib2.urlopen ( url ).read ( )
		soup = BeautifulSoup ( page, 'lxml' ) 
		pagelist = soup.findAll ( 'div', attrs = { 'id' : re.compile ( r'node-[0-9]{1,}' ) } )
		return [ self.parseStatement ( page ) for page in pagelist ]


	def parseStatement( self, page ):

		atag = page.findAll ( 'a' )
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


