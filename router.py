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


def getIp(routerName):
	fileReader = open('Ip.txt')
	data = fileReader.readlines()
	for i in data:
		row = i.split(' : ')
		if row[0] == routerName:
			ipAddress = row[1]

	return ipAddress.rstrip()

def getPort(routerName):
	for item in tp.inputPort:
		if item == routerName:
			return tp.inputPort[item]


def getConnectedRouters(routerName):
	routerList = []
	for key in tp.ports:
		route = key.split(',')
		if route[0] == routerName:
			routerList.append([route[1], getIp(route[1]), tp.ports[key]])

	return routerList


def getIpData(routerName):
	routerList = getConnectedRouters(routerName)
	result = [['B', '127.0.0.1', '10001'],
			['F', '127.0.0.1', '10002'],
			['E', '127.0.0.1', '10003']]

	print(routerList)
	return routerList


def decodePacket(packet):
	destination = packet[13]
	message = packet[23:]

	return destination, message


if __name__ == "__main__":
	routerName = input('Enter router name: ')
	router = Activate(routerName)
	table = RoutingTable(routerName)

	ipAddress = getIp(routerName)
	port = getPort(routerName)
	ipData = getIpData(routerName)
	print(ipAddress)

	interface1 = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
	interface1.bind((ipData[0][1], int(ipData[0][2])))

	interface2 = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
	interface2.bind((ipData[1][1], int(ipData[1][2])))

	interface3 = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
	interface3.bind((ipData[2][1], int(ipData[2][2])))

	inputInterface = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
	inputInterface.bind((ipAddress, port))



	while True:
		data = "Destination: C, data = Hello"
		#data, senderAddress = inputInterface.recvfrom(4096)
		destination, message = decodePacket(data)

		if destination == routerName:
			break

		nextHop = table.getNextHop(destination)
		print(destination, nextHop, message)
		nextIp = getIp(nextHop)
		nextPort = getPort(nextHop)
		interface1.sendto(data.encode(), (nextIp,nextPort))