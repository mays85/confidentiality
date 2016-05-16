'''
Projector main is the projector (client) that will eventually ask the theater server
for a file.
'''

import argparse
import sys, os
from Crypto.Hash import SHA256
from AEScipher import *
from Payload import *
from socket import *
import cPickle

def parse_args():
	parser = argparse.ArgumentParser(description = 'Connect to server and download file')
	parser.add_argument ('-i', '--IP', help = 'IP address of the server')                                                                                                                                                             
	parser.add_argument ('-o', '--output', help = 'the name of the output file', default = 'file_out.encrypted')
	args = parser.parse_args()
	return args

def main():
	# need the arguments for some important information
	args = parse_args()

	# setup the connection to the server
	serverName = args.IP
	serverPort = 12000
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((serverName,serverPort))

	# connection ready, now get the size of the data to be received (it's big)
	readySize = raw_input("connection established, ready for cPickle size? y/n: ")
	clientSocket.send(readySize)
	cSize = int(clientSocket.recv(1024))
	# print cSize

	# now we know how much data to expect, tell server that we're ready for the data...
	readyFile = raw_input("size received, ready for file? y/n: ")
	clientSocket.send(readySize)

	# recieved keeps track of total data
	# data is the intermediate received in each step
	# at the completion of the loop, all data is transfered.
	recieved = ''
	while cSize >= int(sys.getsizeof(recieved)):
		#clientSocket.recv(int(fileSize))
		data = clientSocket.recv(1024)
		if not data:
			break
		recieved += data
		# print sys.getsizeof(recieved)
		if cSize == sys.getsizeof(recieved):
			# print "got here"
			break
	print "file transfer complete"
	clientSocket.close()

	# use cPickle to unpack the data in to Payload object
	payload = cPickle.loads(recieved)
	print payload.key

	# using, the b64decoded key that we received, decrypt the data, then calculate the hash.
	aes = AESCipher(base64.b64decode(payload.key))
	raw_data = aes.decrypt(payload.movData)
	calcHash = SHA256.new(raw_data).hexdigest()

	# print calcHash
	# print payload.fhash

	# if the calculated hash matches the received has, 
	if calcHash == payload.fhash:
		print "hashes matched, writing data to output file"
		f_out = open(args.output, "w")
		f_out.write(raw_data)
		f_out.close()
		os.system("xdg-open " + args.output)
	else:
		print "hashes did not match, exiting"

if __name__ == "__main__":
	main()


