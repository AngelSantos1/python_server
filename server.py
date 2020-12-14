#!/usr/bin/python3

import socket
import subprocess

class Server:
	def __init__(self, host, port):
		self.port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.port.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.port.bind((host, port))
		self.port.listen(1)
		self.api = []

	# read a line in the http header from a socket
	# This specifically looks for the new-line byte
	def readLine(self, sock):
		result = bytearray()
		b = sock.recv(1)
		while b and b != b'\n':
			result.append(b[0])
			b = sock.recv(1)
		if b:
			result.append(b[0])
		return result.decode('utf-8', errors="ignore")

	# read the http headers into a list from a socket
	def readHeader(self, sock):
		head = []
		while len(head) == 0 or head[-1].strip() != "":
			head.append(self.readLine(sock).strip())
		return head

	def addService(self, route, service):
		self.api.append((route, service))

	def run(self):
		while True:
			# wait for a request
			sock, addr = self.port.accept()

			# read the headers of the request
			head = self.readHeader(sock)

			for route, service in self.api:
				if (callable(route) and route(addr, head)) or (not callable(route) and route):
					if callable(service):
						sock.send(service(addr, head, sock).encode('utf-8'))
					else:
						sock.send(str(service).encode('utf-8'))
					break

			sock.close()

