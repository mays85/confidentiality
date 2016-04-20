'''

This file is the main program for implementing confidentiality.
This program will take a movie file and encrypt it using AES symmetric key encryption.
This program will also take an encrypted file and, using the same symmetric key, reproduce the original movie file.

Imports are:
- argparse
- AESCipher class (AESCipher.py)

The arguments for the program are
- a file (the movie file you're sending)
- the symmetric key (pre-shared) to encrypt the file.
- output file name (not required, default = "file_out.encrypted")
- d option to decrypt

The result of the program is: 
- if encrypting, the program produces an encrypted file
- if decrypting, the program reproduces the original movie file                                                                                                                                                           




'''

import argparse
from AESCipher import *


def parse_args():
	parser = argparse.ArgumentParser(description = 'Encrypt movie file with a key')
	parser.add_argument('-d', '--decrypt', help = 'decypt the given filename with key', action = 'store_true', default = False)
	parser.add_argument ('-f', '--file', help = 'file name to be encrypted')
	parser.add_argument ('-k', '--key', help = 'the key used to encrypt (and decrypt)')
	#parser.add_argument ('-h', '--help', help = 'show help')                                                                                                                                                             
	parser.add_argument ('-o', '--output', help = 'the name of the output file', default = 'file_out.encrypted')
	args = parser.parse_args()
	return args


# Main will: 
# 1) parse the arguments
# 2) encrypt the file useing the key (both of which came from the arguments)
# 3) write the encrypted file.

def main():
	# first things first, get the arguments. what are they...probably a 
	# filename (movie file) and a symmetric key, yea?
	args = parse_args()
	__input_filename__ = args.file
	__key__ = args.key
	__output_filename__ = args.output
	__opt_decrypt = args.decrypt


	# if the decrypt flag is set, then...decrypt!
	if __opt_decrypt:

		# open the encrypted file
		f_in = open(__input_filename__, 'r')
		# read the data
		encrypted_data = f_in.read()
		# create a new AESCipher object
		aes = AESCipher(__key__)
		# use the AESCipher object to decrypt file data
		raw_data = aes.decrypt(encrypted_data)
		# open the output file and write the decrypted data to it.
		f_out = open(__output_filename__, 'w')
		f_out.write(raw_data)

	# if we're not decrypting, then we're...encrypting!
	else:
		# open the input file
		f_in = open(__input_filename__, 'r')
		# read the raw data
		raw_data = f_in.read()
		# create a new AESCipher object
		aes = AESCipher(__key__)
		# use AESCipher object to encrypt raw_data
		encrypted_data = aes.encrypt(raw_data)
		# open the outpt file
		f_out = open (__output_filename__, 'w')
		# write encrypted data to the output file
		f_out.write(encrypted_data)
		print "File written to: ", __output_filename__


if __name__ == "__main__":
	main()

