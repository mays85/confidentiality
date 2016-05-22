import base64
import os

# key is AES key stored in base64 format for readability
# fhash is hash of UN-ENCRYPTED movie data
# movData is not a file, but rather the encrypted data

class Payload:
	def __init__(self , key, fhash=None, movData=None):
		self.key = key
		self.fhash = fhash
		self.movData = movData
