# Final project
This project is the final code for CSCE 600 Data Security project. 

Overview
- These files set up a client/server system where the server gives an AES encrypted file, along with RSA encrypted AES key and file hash.
-- The server starts running and immediately performs a SHA hash of the file, creates an AES key and encryptes the original movie file using the key.
-- The server then waits for a connection and receives an RSA public key from the client. 
-- Using the RSA public key, the server encrypts the AES key and the file hash, ensuring that only the client can decrypt the key and the hash.
-- The server then sends the client the payload, which consists of the AES encrypted file, RSA encrypted AES key and SHA hash.
-- Once the client receives the payload, the client uses it's private key to decrypt the AES key and file hash.
-- With the AES key now in hand, the client decrypts the movie file.
-- With the original file now decyrpted, the client hashes the file and compares the calculated hash with the received hash.
-- If the hashes match, the client writes the file to the disk. If the hashes don't match, the client will not write the file.


Confidentiality
- The confidentiality portion of this project is handled by using AES encryption.  The movie file is encrypted
  using a generated key. 

Authentication
- The authentication portion of this project is handled by using RSA public/private key encyprtion.
  The client generates a public/private key pair and shares the public key with the server.  The server 
  uses the public key to encrypt the AES key for confidentiality, along with the hash of the original movie(see message integrity below).

Integrity
- The integrity portion of this project is handled using SHA-256 hashing. The original movie is hashed. The hash is 
  encrypted using the clients public RSA key.  The client uses the received hash  to compare that value with a calculated 
  hash of the file once decryption is complete.


Set up the server
./Moviemain1.py -f [filename]

Client process to go get the file
./Projectormain.py -o [outputfile name] -i [IP address of the server]
