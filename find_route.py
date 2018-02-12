import sys
# created a City class with attributes city_name as name, depth, parent node, next node and cost
class City:
    def __init__(self,name='',next=None,parent=None,depth=0,cost=0):
        self.city_name = name
        self.next = next
        self.parent = parent
        self.depth = depth
        self.cost = cost
    def __str__(self):
        return self.city_name
    
# a method for finding the adjacent/neighbour nodes          
def findneighbours(city,paths):
    l = [] 
    for i,j in enumerate(paths):
        if j[0]==city:
            l.append(j[1])
        elif j[1]==city:
            l.append(j[0])
    return l

# a method for finding the distance between two nodes
def finddist(a,b,dist):
    l = dist.keys()
    if (a,b) in l:
        return dist[a,b]
    elif (b,a) in l:
        return dist[b,a]

# a method for updating the distance and depth for all the neighbours and return updated list
def updateneighbours(adjacent_cities,current,dist):
    temp = []
    for iCity in adjacent_cities:
        city = City()
        city.city_name = iCity
        city.parent = current
        city.depth = current.depth+1
        city.cost = current.cost+finddist(current.city_name,city.city_name,dist)
        temp.append([city,city.cost])    
    return temp

# a method for printing the full route from source to destination
def printroute(node,dist):
    route = []
    while node:
        route.append(node.city_name)
        node = node.parent 
    print('route:')     
    if len(route)==1:
        print('at destination')
    else:
        route.reverse()
        for i in range(len(route)-1):
            print(route[i]+" to "+route[i+1]+", "+str(finddist(route[i],route[i+1],dist))+" km")

# opening the input file    
filename = 'C:\\Users\\lenovo\\Downloads\\input.txt'
f = open(filename,'r')
s = 'London'
d = 'Manchester'

# closed set for keeping track of visited cities
visited_cities = []

# create an empty fringe 
fringe = []

# a dictionary holding all the links in the given problem
dist = {}

# reading the file and storing the links between cities in a dictionary dist along with the link cost
for i in f:
    if i =="END OF INPUT":
        break
    a,b,c = i.strip().split()
    dist[a,b] = int(c)

# creating a source node and adding it to the fringe
origin = City(s,None,None,0,0)
fringe.append([origin,origin.cost])    
flag = 0
# iterating through the fringe nodes and finding the optimal path
while len(fringe)>0:
    # picking the first value from nondecreasing ordered fringe
    current = fringe.pop(0)[0]
    # printing the full route and total cost if destination is reached
    if current.city_name == d:
        flag = 1
        print('distance: '+str(current.cost)+" km")
        printroute(current,dist)
        break
    # checking if city is in visited cities otherwise continue to next node
    if current.city_name in visited_cities:
        continue
    # find neighbours for the current city
    adjacent_cities = findneighbours(current.city_name,dist)
    visited_cities.append(current.city_name)
    # calling method for node expansion and storing the updated neighbours into list
    l = updateneighbours(adjacent_cities,current,dist)
    # append the fringe with new nodes
    fringe.extend(l)
    # fringe is sorted based on the cost from source to current node
    fringe.sort(key = lambda x:x[1])
    
# checking for destination not in given problem
if flag == 0:
    print('distance: infinity')
    print('route:')
    print('none')    