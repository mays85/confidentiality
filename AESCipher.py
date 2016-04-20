'''
This is the AESCipher class which implements AES encryption for the confidentiality portion of the project.
This class is used as an object in the confidentiality_main program.

This code was taken from:
http://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
'''

from Crypto import Random
from Crypto.Cipher import AES
import base64

BLOCK_SIZE = 32
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s)-1:])]


#This constructor initializes the AESCipher object and sets the key value for the object. The key is given as an argument 
#for the constructor.

class AESCipher:
	def __init__(self , key):
		self.key = key


#The encrypt function takes the raw movie data and returns the encrypted version using the key value. 
#Finally, the function encodes the data in base64 encoding -- IS THAT REQUIRED???

	def encrypt (self , raw):
		raw = pad (raw)
		iv = Random.new().read( AES.block_size )
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return base64.b64encode (iv + cipher.encrypt(raw))


#The decrypt function takes the encoded, encrypted data and first decodes it, then decrypts it using the AESCipher.key value.
	def decrypt (self, enc):
		enc = base64.b64decode(enc)
		iv = enc[:16]
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return unpad(cipher.decrypt(enc[16:]))