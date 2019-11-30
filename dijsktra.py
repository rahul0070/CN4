import topology as tp

class Routes:
	def __init__(self):
		self.paths = {
			'A' : [],
			'B' : [],
			'C' : [],
			'D' : [],
			'E' : [],
			'F' : [],
			'G' : [],
			}


class Algorithm:

	def initialize(self):
		self.shortestPath = []
		self.startingRouter = ''
		self.startingRouterIndex = 0
		self.routerIndex = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H'}
		self.spList = []
		self.spRoute = []
		self.route =[]
		self.routes = Routes()

	def compareCost(self, one, two):
		if one == two:
			return 0
		elif one == 'X':
			return 2
		elif two == 'X':
			return 1
		elif one == 'n':
			return 1
		elif two == 'n':
			return 2
		elif one > two:
			return 1
		elif two > one:
			return 2


	def replaceCost(self, routerName):
		for i in range(len(tp.routers)):
			#print(routerName, tp.routers[i])
			if tp.routers[i] == routerName:
				self.spList[i] = 'X'


	def splitPoints(self, stringInput):
		listOfPoints = stringInput.split(',')
		return listOfPoints[0], listOfPoints[1]


	def checkList(self, list):
		for i in list:
			if i != 'X':
				return 0
		return 1

	def get_key(self, val): 
	    for key, value in self.routerIndex.items(): 
	         if val == value: 
	             return key


	def addRoute(self, routerName):
		self.routes.paths[routerName] = self.spRoute[self.get_key(routerName)]


	def findCost(self, existingCost, pointA, pointB):
		value, ifExists = self.calculateCost(pointA, pointB)
		if ifExists == False:
			return 'n'
		else:
			return value + existingCost

	def findRoute(self, existingRoute, pointA, pointB):
		tempRoute = []
		tempRoute.append(pointA)
		tempRoute.append(pointB)
		return tempRoute


	def form_spList(self, startingPoint, costs):
		spList = []
		existingRoute = []
		routerList = tp.routers
		for i in routerList:
			value = self.findCost(0, startingPoint, i)
			spList.append(value)

			valueRoute = self.findRoute(existingRoute, startingPoint, i)
			self.spRoute.append(valueRoute)

		return spList


	def calculateCost(self, pointA, pointB):
		flag = 0
		value = 0
		ifExists = False
		for route,cost in tp.costs.items():
			first, second = self.splitPoints(route)
			if pointA == pointB:
				flag = 1
				value = 0
			if first == pointA and second == pointB or first == pointB and second == pointA:
				flag = 1
				value = cost

		if flag == 1:
			ifExists = True 

		return value, ifExists



	def findNearest(self, listOfCost):
		small = 'n'
		router = self.routerIndex[0]
		for i in range(0,len(listOfCost)):
			if listOfCost[i] == 'X':
				continue
			if self.compareCost(small, listOfCost[i]) == 1:
				small = listOfCost[i]
				router = self.routerIndex[i]

		return router, small


	def updateRoute(self, basePoint, routerName):
		tempRoute = []

		for i in self.spRoute[self.get_key(basePoint)]:
			tempRoute.append(i)
		tempRoute.append(routerName)

		self.routes.paths[routerName] = tempRoute
		self.spRoute[self.get_key(routerName)] = tempRoute


	def relaxation(self, point, existingCost):
		index = 0
		for i in tp.routers:
			cost = self.findCost(existingCost, point, i)
			if self.compareCost(self.spList[index], cost) == 1:
				self.spList[index] = cost
				self.updateRoute(point, i)
			index = index + 1


	def dijkstra(self, costs):
		self.spList = self.form_spList(self.startingRouter, costs)
		while self.checkList(self.spList) != 1:
			point, cost = self.findNearest(self.spList)
			self.shortestPath.append([point, cost])
			self.addRoute(point)
			self.replaceCost(point)
			self.relaxation(point, cost)

	
	def run(self, startingRouter):
		self.initialize()
		self.startingRouter = startingRouter
		self.dijkstra(tp.costs)
