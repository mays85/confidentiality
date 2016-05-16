'''
Moviemain1 will become the movie company's server. theaters will connect to it and download
movie files.
'''

import argparse
import sys
from Crypto.Hash import SHA256
from AEScipher import *
from Payload import *
from socket import *
import cPickle

def parse_args():
	# MODIFIED ARGUMENTS FROM MOVIEMAIN
	# for this file, we only need to know which movie file we're going to serve up.
	parser = argparse.ArgumentParser(description = 'Serve up an encrypted movie')
	parser.add_argument ('-f', '--file', help = 'file name to be served')
	args = parser.parse_args()
	return args

def main():
	# parse arguments (that's important)
	args = parse_args()

	# open the input file
	__input_filename__ = args.file
	f_in = open(__input_filename__, 'r')

	# read the raw data
	raw_data = f_in.read()

	#create a hash from the data
	dataHash = SHA256.new(raw_data).hexdigest()
	print "Sha-256: %s" % str(dataHash)

	# create a new AESCipher object
	# creating an object creates a new key as well
	aes = AESCipher()
	print "Block size: %d-bit" % (aes.BLOCK_SIZE*8)
	print "Key size: %d-bit" % (aes.KEY_SIZE*8)

	# b64 encode the key (good for sending)
	b64KEY = base64.b64encode(aes.key)  
	print "b64 Key: " + b64KEY + "\n"
	# use AESCipher object to encrypt raw_data
	encryptedData = aes.encrypt(raw_data)
	# encryptedSize = sys.getsizeof(encryptedData)
	# print "Encrypted data size: %.2f MB" % (encryptedSize / 1000000.0)
	
	# Payload object contains the necessary information for symmetric encryption.
	pay = Payload(b64KEY, dataHash, encryptedData)

	#using cPickle to serialize the data
	to_send = cPickle.dumps(pay)

	#because the data is large (movies are big), we need to know how much data we're sending
	toSize = sys.getsizeof(to_send)
	print "to_size = %d" %toSize
	

	# now, create the server socker and listen.
	serverPort = 12000
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind(('',serverPort))
	serverSocket.listen(1)

	# listening for connections
	while 1:
		print "The server is ready to receive"
		connectionSocket, addr = serverSocket.accept()

		# client needs to know size of the data.
		ready = connectionSocket.recv(1024)	
		if ready is 'y' or 'Y':
			connectionSocket.send(str(toSize))

		# client is now ready to accept the data.
		ready = connectionSocket.recv(1024)
		if ready is 'y' or 'Y':
			# sending the data
			connectionSocket.send(to_send)


if __name__ == "__main__":
	main()