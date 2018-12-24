import os, sys, socket, _thread, json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from diffiehellman.diffiehellman import DiffieHellman


def receiveData(conn, length):
	'''
		This function receives 'length' bytes of data from network stream 'conn'.
		The function waits infinitely before all the data is received. There is no timeout
	'''
	data = b''
	ldata = 0
	while ldata < length:
		receivedData = conn.recv(1024)
		ldata += len(receivedData)
		data += receivedData
	return data

def padInteger(i, length):
	'''
		This function converts a integer to string and pads additional zeros in the beginning
		to make its length equal to 'length'
	'''
	i = str(i)
	i = i[::-1]
	j = len(i)
	while j < length:
		i += '0'
		j += 1

	return i[::-1]


def requestHandler(conn, addr):
	'''
		This method handles a new download request
	'''

	# First generate a public-private key pair
	dh = DiffieHellman()
	dh.generate_public_key()
	publicKey = dh.public_key

	# Next, send the public key using KEY_EXCHANGE. The segment size is 2479.
	conn.sendall(('KEY_EXCHANGE\n' + str(publicKey)).encode('utf-8', errors='ignore'))
	
	# Receive a similar segment from client. This segment contains the client's public key.
	data = receiveData(conn, 2479)

	messageType = data.decode('utf-8', errors='ignore').split('\n')[0]
	if messageType != 'KEY_EXCHANGE':
		print("The client sent an illegal response. Closing connection..")
		conn.close()
		return

	clientPublicKey = int(data.decode('utf-8', errors='ignore').split('\n')[1])
	sharedKey = ''

	# Generate the shared key using Diffie Hellman algorithm and the public key of client and server
	try:
		dh.generate_shared_secret(clientPublicKey)
		sharedKey = bytes.fromhex(dh.shared_key)
	except Exception as e:
		print("The client sent an illegal response. Closing connection..")
		conn.close()
		return

	print('Key exchange successful: ' + dh.shared_key)
	
	print('Generating Ciphers..')
	
	# Generate a cipher which will use the shared key to encrypt all outgoing data

	cipher = AES.new(sharedKey, AES.MODE_CBC, 'jdirlfhixhtkwlif'.encode('utf-8'))

	print('Encrypting File list..')

	# Encrypt the file list with the cipher

	sharedFilesList = []
	
	for i in sharedFiles:
		sharedFilesList.append(i)

	fileList = ('\n'.join(sharedFilesList)).encode('utf-8')
	encryptedFileList = cipher.encrypt(pad(fileList, AES.block_size))
	requiredSize = len(encryptedFileList)
	
	# Send the file list size. We use FILELIST to send the file list size
	print('Sending File List..')
	
	conn.sendall(('FILELIST\n'+padInteger(requiredSize, 20)).encode('utf-8', errors='ignore'))
	
	# Wait till the server doesn't receive READY signal indicating that the client is ready to take the data
	data = receiveData(conn, 5).decode('utf-8', errors='ignore')

	if data != 'READY':
		print('Client is not ready to receive file list..')
		conn.close()
		return

	# Send the encrypted file list now. The segments contain only body and no header
	conn.sendall(encryptedFileList)

	# Wait for acknowloedgement
	data = receiveData(conn, 3).decode('utf-8', errors='ignore')
	if data == 'ACK':
		print('File list was received successfully by client..')
	else:
		print('No Acknowledgement received..')
		conn.close()
		return

	# Wait for a file request
	print('Waiting for request..')

	data = receiveData(conn, 28).decode('utf-8', errors='ignore').split('\n')
	idx = int(data[1])
	if data[0] != 'REQUEST':
		print('The client sent an illegal response. Closing connection..')
		conn.close()
	else:
		if idx < 0 or idx >= len(sharedFilesList):
			print('\n\nThe client sent an illegal response. Closing connection..')
			conn.close()
			return
		else:
			# Open the requested file. Encrypt it with the cipher and send it.
			fileName = sharedFilesList[idx].split('/')
			fileName = fileName[len(fileName) - 1]
			file = open(sharedFilesList[idx], 'rb')
			unencryptedData = file.read()
			file.close()
			cipher = AES.new(sharedKey, AES.MODE_CBC, 'jdirlfhixhtkwlif'.encode('utf-8'))
			encryptedData = cipher.encrypt(pad(unencryptedData, AES.block_size))
			requiredPackets = len(encryptedData)

			# Send the file size. We use FILE to send the file size
			conn.sendall(('FILE\n'+padInteger(requiredPackets, 20)).encode('utf-8', errors='ignore'))

			# Wait for the ready signal
			data = receiveData(conn, 5).decode('utf-8', errors='ignore')
			if data != 'READY':
				print('Client is not ready to receive the file..')
				conn.close()
				return
			print("Sending the file '"+fileName+"'.")
			
			# Sent the encrypted file
			conn.sendall(encryptedData)
			print("Sent! Awaiting Acknowledgement..")
			
			# Wait for acknowledgement
			data = receiveData(conn, 3).decode('utf-8', errors='ignore')
			if data == 'ACK':
				print('Client received the file successfully')
				conn.close()
			else:
				print('An unknown error occured in file transfer')
				conn.close()


sharedFiles = set()
sys.stdin = open(".config", "r")

# Read the file list from .config file
while True:
	file = ''
	try:
		file = input()
		file = file.replace('\\','/')
		if not os.path.isfile(file):
			print('File \"' + file + '\" was not found. Skipping..')
		else:
			sharedFiles.add(file)
	except EOFError as e:
		break

sys.stdin.close()


# Open the server socker and listen indefinitely on port 23548

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 23548))
s.listen(5)
print('Listening on port 23548...')

while True:
	conn, addr = s.accept()
	_thread.start_new_thread(requestHandler, (conn, addr));
