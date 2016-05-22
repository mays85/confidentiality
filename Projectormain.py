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
import RSA_api
import cPickle

RSA_kp = 0

def secure_wipe():
	print '\n[*] SECURE DESTROY IN PROGRESS'
	global RSA_kp
	srsa = sys.getsizeof(RSA_kp)
	RSA_kp = bytearray(os.urandom(sys.getsizeof(srsa)))
	print '[*] COMPLETE!'

def parse_args():
	parser = argparse.ArgumentParser(description = 'Connect to server and download file')
	parser.add_argument ('-i', '--IP', help = 'IP address of the server')                                                                                                                                                             
	parser.add_argument ('-o', '--output', help = 'the name of the output file', default = 'file_out.encrypted')
	args = parser.parse_args()
	return args

def main():
	global RSA_kp

	# need the arguments for some important information
	args = parse_args()

	# Grab ONLY the public key 
	# from the key pair obj
	pubkey = RSA_kp.publickey()
	# serialize pubkey for socket
	to_send=cPickle.dumps(pubkey) 

	# setup the connection to the server
	serverName = args.IP
	serverPort = 12000
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((serverName,serverPort))

	#Immediately send the public key
	print "[*] Sending RSA public key to server => ", pubkey
	clientSocket.send(to_send)
	
	# Transfer ready, now get the size of 
	# the data to be received (it's big)
	cSize = int(clientSocket.recv(1024))
	clientSocket.send('1')

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
	print "[*] file transfer complete!"
	clientSocket.close()

	# use cPickle to unpack the 
	# data in to Payload object
	payload = cPickle.loads(recieved)

	#For demo purposes
	print "\n\n++++++ BEGIN ENCRYPTED KEY +++++++\n"
	print payload.key
	print "\n++++++ END ENCRYPTED KEY +++++++\n"
	payload.key = RSA_kp.decrypt(payload.key)
	print "DECRYPTED b64 KEY => ",payload.key
	

	print "\n\n++++++ BEGIN ENCRYPTED SHA-256 +++++++\n"
	print payload.fhash
	print "\n++++++ END ENCRYPTED SHA-256 +++++++\n"
	payload.fhash = RSA_kp.decrypt(payload.fhash)
	print "DECRYPTED SHA-256 => ",payload.fhash
	
	# using, the b64decoded key that we received, 
	# decrypt the data, then calculate the hash.
	aes = AESCipher(base64.b64decode(payload.key))
	raw_data = aes.decrypt(payload.movData)
	calcHash = SHA256.new(raw_data).hexdigest()

	# if the calculated hash matches the received has, 
	if calcHash == payload.fhash:
		print "\n\n[*] hashes matched, writing data to output file"
		f_out = open(args.output, "w")
		f_out.write(raw_data)
		f_out.close()
		os.system("xdg-open " + args.output)
		secure_wipe()
	else:
		print "\n\n[!] hashes did not match, possibly malicious..begin secure kill"
		secure_wipe()
		sys.exit(1)

if __name__ == "__main__":
	try:
		# RSA_init goes in search of its keystore file
		# if found simply pulls the RSA key pair and returns the obj
		# else, generates RSA key pair, saves it to key store, then returns obj
		global RSA_kp
		RSA_kp = RSA_api.RSA_init() 
		print RSA_kp
		main()		
	except KeyboardInterrupt:
		# if a keyboard interupt is detected, 
		# we wipe RSA key pair from ram
		# and tell the OS to clean up our proc
		print "\n\nDetected Keyboard Interrupt!\n"
		secure_wipe()
		sys.exit(1)
