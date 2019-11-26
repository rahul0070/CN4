from dijsktra import Algorithm
import topology as tp 
import sqlite3

class Activate:
	def __init__(self, routerName):
		print('here')
		self.routerName = routerName
		self.data = {}
		self.costs = []
		self.routes = []
		self.dk = Algorithm()
		self.initialize()

	def initialize(self):
		ip = tp.ipAddress[self.routerName]
		self.data = {'Name': self.routerName, 'ipAddress': ip}
		self.runAlgorithm()

	def runAlgorithm(self):
		self.dk.run(self.routerName)
		self.costs = self.dk.shortestPath
		self.routes = self.dk.routes.paths
		self.buildTable()

	def getCost(self, routerName):
		for i in self.costs:
			if i[0] == routerName:
				cost = i[1]
				return cost

	def getPortNumber(self, origin, destination):
		ports = tp.portNumber
		index = origin +','+ destination
		if origin == destination:
			return 0
		else:
			return ports[index]


	def getData(self, router):
		data = []
		path = self.dk.routes.paths[router]
		cost = self.getCost(router)
		portNumber = self.getPortNumber(self.routerName, path[1])
		return path[1], cost, portNumber

	def buildTable(self):
		connection = sqlite3.connect('routerInformation_'+self.routerName+'.db')
		db = connection.cursor()
		try:
			db.execute('CREATE TABLE information(routerName text, ipAddress text)')
			info = [self.routerName, tp.ipAddress[self.routerName]]
			db.execute('INSERT INTO information VALUES(?, ?)',info)
			connection.commit()
		except:
			pass

		try:
			db.execute('CREATE TABLE routingTable(destination char, nextHop text, cost integer, interface integer)')
			connection.commit()
			routerList = tp.routers
			for i in routerList:
				nextHop, cost, interface = self.getData(i)
				print(i, nextHop, cost, interface)
				parameters = [i, nextHop, cost, interface]
				db.execute('INSERT INTO routingTable VALUES(?, ?, ?, ?)', parameters)
				connection.commit()
		except:
			pass





#r = Activate('C')