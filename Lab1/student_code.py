
##################################################################
# Notes:                                                         #
# You can import packages when you need, such as structures.     #
# Feel free to write helper functions, but please don't use many #
# helper functions.                                              #
##################################################################




	# recursion of DFS
	#return testmap
def dfs(testmap):
	for y in range(len(testmap)):
		for x in range(len(testmap[y])):
		    if testmap[y][x] == 2:
		        testmap[y][x] = 5
		        rightroad(testmap,y,x)


def dfs_help(testmap,y,x):
	#put your codes here:
		if testmap[y][x]==3:
			testmap[y][x]=5
			print testmap
			return testmap
		elif testmap[y][x]==1:
			testmap[y][x]=4
			dfs_turn(testmap,y,x)
		elif testmap[y][x]==0:
			testmap[y][x]=5
			rightroad(testmap,y,x)
		elif testmap[y][x]==5:
			rightroad(testmap,y,x)

def rightroad(testmap,y,x):
    if x+1<len(testmap) and testmap[y][x+1] == 0:
		x = x + 1	
		testmap[y][x] = 5
		dfs_help(testmap,y,x)
    elif x+1<len(testmap) and testmap[y][x+1] == 1:
		testmap[y][x+1] = 4
		downroad(testmap,y,x)
    elif x+1 < len(testmap) and testmap[y][x+1] == 3:
		dfs_help(testmap,y,x+1)	
    else:
        downroad(testmap,y,x)

def downroad(testmap,y,x): 
	if y + 1 < len(testmap) and testmap[y+1][x] == 0:
		y = y + 1
		testmap[y][x] = 5
		dfs_help(testmap,y,x)
	elif y+1<len(testmap) and testmap[y+1][x] == 1:
		testmap[y+1][x] = 4
		leftroad(testmap,y,x)
	elif y + 1 < len(testmap) and testmap[y+1][x] == 3:
		dfs_help(testmap,y+1,x)
	else:
		leftroad(testmap,y,x)


def leftroad(testmap,y,x): 
	if x-1>=0 and testmap[y][x-1] == 0:
		x = x - 1
		testmap[y][x] = 5
		dfs_help(testmap,y,x)
	elif x-1>=0 and testmap[y][x-1] == 1:
		testmap[y][x-1] = 4
		uproad(testmap,y,x)
	elif x-1>=0 and testmap[y][x-1] == 3:
		dfs_help(testmap,y,x-1)
	else:
		uproad(testmap,y,x)


def uproad(testmap,y,x):
	if y-1>=0 and testmap[y-1][x]==0 :
		y = y - 1
		testmap[y][x]=5
		dfs_help(testmap,y,x)
	elif y-1>=0 and testmap[y-1][x] == 1:
		testmap[y-1][x] = 4
		dfs_turn(testmap,y,x)
	elif y-1>=0 and testmap[y-1][x] == 3:
		dfs_help(testmap,y-1,x)
	else:
		dfs_turn(testmap,y,x)

def dfs_turn(testmap,y,x):
	testmap[y][x]=4
	if x-1>=0 and testmap[y][x-1] ==5:  
		x=x-1
		dfs_help(testmap,y,x)
	elif y-1>=0 and testmap[y-1][x] ==5 :
		y=y-1
		dfs_help(testmap,y,x)
	elif x+1<len(testmap) and testmap[y][x+1] ==5:
		x=x+1
		dfs_help(testmap,y,x)
	elif y+1<len(testmap) and testmap[y+1][x] ==5:
		y = y+1
		dfs_help(testmap,y,x)



import Queue

class node:
	x =0
	y =0
	def __init__(self,x_p,y_p):
		self.x=x_p
		self.y=y_p

def bfs(testmap):
	#put your codes here:
	# using queue to implement bfs
	points_buffer = Queue.Queue()
	i =0 
	j =0
	height = len(testmap)
	length = len(testmap[0])
	print length
	print height
	path = [[ 0 for y in range (length)] for x in range(height)]
	for row in testmap:
		j=0
		for col in row:
			if col == 2:
				print i
				print "s"
				print j 
				start_point= node(j,i)
			j+=1
		i+=1
	points_buffer.put(start_point)

	while not points_buffer.empty():
		point = points_buffer.get()
		if testmap[point.y][point.x] == 3:
			end_point = node(point.x, point.y)
			break
		testmap[point.y][point.x]=4

		# Find the abjancent point
		#x+1
		if point.x+1< length and testmap[point.y][point.x+1]!=1 and testmap[point.y][point.x+1]!=4: 
			points_buffer.put(node(point.x+1, point.y))
			print point.x,
			print point.y
			path[point.y][point.x+1] = point.x + point.y*length
			
		#y+1
		if point.y+1<height and testmap[point.y+1][point.x]!=1 and testmap[point.y+1][point.x]!=4:
			points_buffer.put(node(point.x, point.y+1))
			print point.x,
			print point.y
			path[point.y+1][point.x] = point.x + point.y*length
			
		#x-1
		if point.x-1>=0 and testmap[point.y][point.x-1]!=1 and testmap[point.y][point.x-1]!=4:
			points_buffer.put(node(point.x -1, point.y))
			print point.x,
			print point.y
			path[point.y][point.x-1] = point.x + point.y*length
		#y-1
		if point.y-1>=0 and testmap[point.y-1][point.x]!=1 and testmap[point.y-1][point.x]!=4:
			points_buffer.put(node(point.x, point.y-1))	
			print point.x,
			print point.y
			path[point.y-1][point.x] = point.x + point.y*length
	# trace back 

	path_x = end_point.x
	path_y = end_point.y	

	while (path_x!=start_point.x or path_y!=start_point.y):		
		testmap[path_y][path_x]=5
		x = path_x
		y = path_y
		path_x = (path[y][x])%length
		path_y = (path[y][x])/length

		
	testmap[start_point.y][start_point.x] = 5

	return testmap



def a_star_search (dis_map, time_map, start,end):

	scores = {}
	#put your codes here:
	for y in range(len(testmap)):


	return scores





















