#!/usr/bin/python3

from server import Server
import os
import sys

from pyhtml import html

server = Server("", 8080)

def myroute(addr, head):
	return True

def myservice(addr, head, sock):
	#print(addr)
	print(head)
	req = head[0].split(' ')
	print(req)
	path = '.' + req[1].replace('../', '')

	try:
		fptr = open(path, 'r')

		out_head = [
			'HTTP/1.0 200 OK',
			'Content-type: text/html; charset=UTF-8'
		]

		output = '\n'.join(out_head) + '\n\n'

		output += fptr.read()
		fptr.close()
	except:
		out_head = [
			'HTTP/1.0 404 Not Found',
		]

		output = '\n'.join(out_head) + '\n\n'

	return output

def route1(addr, head):
	return True

def service1(addr, head, sock):
	out_head = [
		'HTTP/1.0 200 OK',
		'Content-type: text/html; charset=UTF-8'
	]

	output = '\n'.join(out_head) + '\n\n'

	doc = html.Html()
	doc << html.Head()
	body = html.Body()
	body << "Hello World"
	doc << body

	output += str(doc)

	return output

server.addService(route1, service1)

server.run()
