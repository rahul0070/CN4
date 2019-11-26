import socket
import sqlite3
import topology as tp
from activateRouter import Activate

class RoutingTable:
	def __init__(self, routerName):
		self.routerName = routerName
		connection = sqlite3.connect('routerInformation_'+self.routerName+'.db')
		self.db = connection.cursor()
		self.db.execute('SELECT destination, nextHop FROM routingTable')
		self.portNumers = self.db.fetchall()

	def getNextHop(self, destination):
		for i in self.portNumers:
			if i[0] == destination:
				nextHop = i[1]

		return nextHop


class Router:
	def __init__(self):
		self.ipAddress = ipAddress
		self.routerName = routerName

def getPorts(routerName):
	ports = []
	for key, value in tp.portNumber:
		if key[0] == routerName:
			ports.append(tp.portNumber[key[2]])

	for element in ports:
		for key, value in tp.ipAddress:
			if key == element:
				ip = value
				portList.append([ip, element])


def getData(routerName):
	portNumber = getPorts(routerName)
	connection = sqlite3.connect('routerInformation_'+self.routerName+'.db')
	db = connection.cursor()


def getIp(routerName):
	fileReader = open('Ip.txt')
	data = fileReader.readlines()
	for i in data:
		row = i.split(' : ')
		if row[0] == routerName:
			ipAddress = row[1]

	return ipAddress


def getIpData(routerName):
	result = [['B', '127.0.0.1', '10001'],
			['F', '127.0.0.1', '10002'],
			['E', '127.0.0.1', '10003']]

	return result


if __name__ == "__main__":
	routerName = input('Enter router name: ')
	router = Activate(routerName)
	table = RoutingTable(routerName)
	#ipAddresses, portNumbers =  getData(routerName)

	ipAddress = getIp(routerName)
	ipData = getIpData(routerName)
	print(ipAddress)

	interface1 = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
	interface1.bind((ipData[0][1], int(ipData[0][2])))

	interface2 = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
	interface2.bind((ipData[1][1], int(ipData[1][2])))

	interface3 = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
	interface3.bind((ipData[2][1], int(ipData[2][2])))

	inputInterface = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
	inputInterface.bind(('127.0.0.1', 10004))



	while True:
		data = "Destination: G, data = Hello"
		#data, senderAddress = inputInterface.recvfrom(4096)
		destination = 'B'
		nextHop = table.getNextHop(destination)
		print(destination, nextHop)
		print(getIp(destination))
		fg = str(getIp(destination))
		print(type(fg))
		interface1.sendto(data.encode(), (fg,20004))
		#data = null

	
