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
import RSA_api
import cPickle

Client_RSApk = 0

def secure_wipe():
	print '\n[*] SECURE DESTROY IN PROGRESS'
	global Client_RSApk
	srsa = sys.getsizeof(Client_RSApk)
	Client_RSApk = bytearray(os.urandom(sys.getsizeof(srsa)))
	print '[*] COMPLETE!'

def parse_args():
	# MODIFIED ARGUMENTS FROM MOVIEMAIN
	# for this file, we only need to know 
	# which movie file we're going to serve up.
	parser = argparse.ArgumentParser(description = 'Serve up an encrypted movie')
	parser.add_argument ('-f', '--file', help = 'file name to be served')
	args = parser.parse_args()
	return args

def main():
	global Client_RSApk

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
	encryptedSize = sys.getsizeof(encryptedData)
	print "Encrypted data size: %.2f MB" % (encryptedSize / 1000000.0)
	
	# Payload object contains encrypted movie and 
	# the necessary information for symmetric encryption.
	pay = Payload(b64KEY, dataHash, encryptedData)

	# now, create the server socker and listen.
	serverPort = 12000
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind(('',serverPort))
	serverSocket.listen(1)

	# listening for connections
	while 1:
		#accept inbound tcp connections
		print "The server is ready to receive connections"
		connectionSocket, addr = serverSocket.accept()

		#Receive the projectors public key obj
		print '[*] Receiving projector public RSA key'
		cRSA = connectionSocket.recv(1024)
		Client_RSApk = cPickle.loads(cRSA) 
		#print our obj for verification
		print '[*] Projector RSA Public Key => ', Client_RSApk
		
		pay.key = Client_RSApk.encrypt(pay.key, '')[0]
		pay.fhash = Client_RSApk.encrypt(pay.fhash, '')[0]
		to_send = cPickle.dumps(pay)
		#get size of encrypted and pickled payload obj
		toSize = sys.getsizeof(to_send)
		print "Size of Payload = %d Bytes" %toSize

		# client needs to know size of the data.
		connectionSocket.send(str(toSize))
		connectionSocket.recv(1)

		# client is now ready to accept the data.
		connectionSocket.send(to_send)
		
		secure_wipe()
		sys.exit(1)

if __name__ == "__main__":
	try:
		main()		
	except KeyboardInterrupt:
		# if a keyboard interupt is detected, 
		# we wipe RSA key pair from ram
		# and tell the OS to clean up our proc
		print "\n\nDetected Keyboard Interrupt!\n"
		secure_wipe()
		sys.exit(1)
