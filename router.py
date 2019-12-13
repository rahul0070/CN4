import socket
import sqlite3
import topology as tp
from activateRouter import Activate
import sys

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
	return routerList


def decodePacket(packet):
	destination = packet[13]
	message = packet[23:]

	return destination, message


def getDatafromFile(fileName):
	file = open(fileName, 'r')
	packet = file.read()
	return packet


def getPortNumber(router1, router2):
	for key, value in tp.ports.items():
		if key == router1 + ',' + router2:
			outputPortNumber = value

	return outputPortNumber



def write_log(node,source,inport,destination,outport,forward):
	file = open("log_"+node+".txt","a")
	print(node,source,inport,destination,outport,forward)
	file.write("\n")
	file.write(source+"\t"+str(inport)+"\t"+destination+"\t"+str(outport)+"\t"+"DIJKSTRA"+"\t"+forward+"\n")
	file.write("--------------------------------------------------------------------------------------------------"+"\n")
	file.close()

def forwardPacket(destination, data):
	if destination == routerName:
	    write_log(routerName, 'NA', port,destination,'NA','NA')
	    print('Message Recieved')

	else:
		print('Message Forwarded')
		nextHop = table.getNextHop(destination)
		nextIp = getIp(nextHop)
		nextPort = getPort(nextHop)

		outputPortNumber = getPortNumber(routerName, nextHop)
		print(outputPortNumber)
		for i in range(len(addressList)):
			if addressList[i][1] == outputPortNumber:
				index = i

		write_log(routerName, senderAddress[0], port,destination,outputPortNumber,nextHop)
		interfaceList[index].sendto(data, (nextIp,nextPort))

def getBroadcastList(routerName):
	routerList = tp.routers
	routerList.remove(routerName)
	return routerList

def createPacket(destination):
	data = 'Destination: ' + destination + ', data = Broadcasting'
	return data



if __name__ == "__main__":

	routerName = sys.argv[1]
	serviceType = sys.argv[2] # r- Recieving, s - Sending, b - Broadcasting
	router = Activate(routerName)
	table = RoutingTable(routerName)

	ipAddress = getIp(routerName)
	port = getPort(routerName)
	ipData = getIpData(routerName)
	print(ipAddress)

	interfaceList = []
	addressList = []
	for i in range(len(ipData)):
		interface = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
		address = (ipData[i][1], int(ipData[i][2]))
		interface.bind(address)
		interfaceList.append(interface)
		addressList.append(address)

	inputInterface = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
	inputInterface.bind((ipAddress, port))



	if serviceType == 's':
		data = getDatafromFile('Packet.txt')
		destination, message = decodePacket(data)
		senderAddress = ipAddress
		forwardPacket(destination, data.encode())

	elif serviceType == 'r':
		while True:
			data, senderAddress = inputInterface.recvfrom(4096)
			destination, message = decodePacket(data.decode())

			forwardPacket(destination, data)

	elif serviceType == 'b':
		destinationList = getBroadcastList(routerName)

		for destination in destinationList:
			senderAddress = ipAddress
			data = createPacket(destination)
			forwardPacket(destination, data.encode())
