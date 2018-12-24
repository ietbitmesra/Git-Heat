from diffiehellman.diffiehellman import DiffieHellman
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import socket, json, _thread, sys, time


def receiveData(s, length):
	'''
		This function receives 'length' bytes of data from network stream 'conn'.
		The function waits infinitely before all the data is received. There is no timeout
	'''
	data = b''
	ldata = 0
	while ldata < length:
		receivedData = s.recv(1024)
		ldata += len(receivedData)
		data += receivedData
	return data

def getHoursMinutesSeconds(time):
	'''
		Converts seconds to hours, minute and seconds
	'''
	time = int(time)
	minutes = time // 60
	hours = minutes // 60
	seconds = time % 60
	minutes = minutes - 60*hours
	return [str(hours), str(minutes), str(seconds)]

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


progress = 0

def showProgress():
	'''
		This function runs on a separate thread and uses the main thread variable 'progress' to show 
		download progress.
	'''
	global progress
	lastTime = time.time()
	lastProgress = progress
	speed = 0
	timeLeft = -1
	time.sleep(1)
	while progress < fileSize:
		pc = (progress*100)//fileSize
		i = 0
		print("\r"+"[", end='')
		while i < (pc//2):
			print("\u2588", end='')
			i += 1
		while i < 50:
			print(" ", end='')
			i += 1
		print("] ", end='')
		print(str(pc), end='')
		print("% Complete\t", end='')
		print(str(round(speed, 2)), end='')
		print(" KB/s,\tTime Left: ", end='')
		print(':'.join(getHoursMinutesSeconds(timeLeft)), end='')
		print("      ", end='')
		bytesTransferred = progress - lastProgress
		currentTime = time.time()
		timeTaken = currentTime - lastTime
		speed = bytesTransferred / (1024 * timeTaken)
		if speed == 0.0:
			timeLeft = -1
		else:
			timeLeft = (fileSize - progress) / (1024 * speed)
		lastProgress = progress
		lastTime = currentTime
		time.sleep(1)


# First generate a public-private key pair

dh = DiffieHellman()
dh.generate_public_key()
publicKey = dh.public_key

# Create a socket to connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)

ip = input("Enter the IP address of the server: ")

try:
	s.connect((ip, 23548))
except Exception as e:
	print("Connections Failed.")
	exit(0)

# Receive the server public key using KEY_EXCHANGE

data = receiveData(s, 2479)

messageType = data.decode('utf-8', errors='ignore').split('\n')[0]

if messageType != 'KEY_EXCHANGE':
	print("The server sent an illegal response. Closing connection..")
	s.close()
	exit(0)

serverPublicKey = int(data.decode('utf-8', errors='ignore').split('\n')[1])

# Send the client public key
s.sendall(('KEY_EXCHANGE\n' + str(publicKey)).encode('utf-8', errors='ignore'))

# Generate the shared key using Diffie Hellman algorithm and the public key of client and server

sharedKey = ''
try:
	dh.generate_shared_secret(serverPublicKey)
	sharedKey = bytes.fromhex(dh.shared_key)
except Exception as e:
	print("The server sent an illegal response. Closing connection..")
	s.close()
	exit(0)

print('Key exchange successful: ' + dh.shared_key)

# Generate a cipher which will use the shared key to decrypt all incoming data

print('Generating Ciphers..')

cipher = AES.new(sharedKey, AES.MODE_CBC, 'jdirlfhixhtkwlif'.encode('utf-8'))

print('Waiting for file list..')

# Receive the file list size

data = receiveData(s, 29).decode('utf-8', errors='ignore').split('\n');

if(data[0] != 'FILELIST'):
	print("The server sent an illegal response. Closing connection..")
	s.close()
	exit(0)

fileListSize = int(data[1])

# Send READY signal
s.send("READY".encode('utf-8', errors='ignore'))

# Receive the encrypted file list
encryptedFileList = receiveData(s, fileListSize)

print('File list received successful..')
	
print('Sending Acknowledgement..')

# Send acknowledgement
s.send("ACK".encode('utf-8', errors='ignore'))

# Decrypt the file list
fileList = unpad(cipher.decrypt(encryptedFileList), AES.block_size)
sharedFiles = fileList.decode('utf-8').split('\n')

print("Listing..")

# Ask the user for the file to download
print("\nChoose a file to Download: ")
j = 0
for i in sharedFiles:
	print(str(j+1)+'. '+i)
	j += 1

x = ''
while True:
	x = int(input())
	if x<1 or x>len(sharedFiles):
		print('Invalid choice.. Try again..')
	else:
		break

# Send the request
s.send(("REQUEST\n"+padInteger(x-1, 20)).encode('utf-8', errors='ignore'))

print('The file has been requested. Waiting for the server to send back headers..')

# Receive the file size in FILE segment

data = receiveData(s, 25).decode('utf8', errors='ignore').split('\n')

if(data[0] != 'FILE'):
	print("The server sent an illegal response. Closing connection..")
	s.close()
	exit(0)

fileName = sharedFiles[x-1].split('/')[len(sharedFiles[x-1].split('/'))-1]
fileSize = int(data[1])
encryptedFileData = b''

# Send the READY signal

s.send("READY".encode('utf-8', errors='ignore'))

print('Your file is being downloaded..\n0% Complete', end='')

# Download the file and show progress on a separate thread

file = open(fileName, 'wb')

_thread.start_new_thread(showProgress,())
while progress < fileSize:
	receivedData = s.recv(1024)
	file.write(receivedData)
	progress += len(receivedData)
file.close()

i = 0
print("\r"+"[", end='')
while i < 50:
	print("\u2588", end='')
	i += 1
print("] ", end='')
print("100% Complete", end='')
print('\n\nFile download complete..')

# Decrypt the downloaded file

file = open(fileName, 'rb')
encryptedData = file.read()
file.close()

print('Decrypting File..')

file = open(fileName, 'wb')

try:
	# If decryption is successful, then the file was successfully downloaded, send acknowledgement
	cipher = AES.new(sharedKey, AES.MODE_CBC, 'jdirlfhixhtkwlif'.encode('utf-8'))
	decryptedData = unpad(cipher.decrypt(encryptedData), AES.block_size)
	file.write(decryptedData)
	file.close()
	s.send("ACK".encode('utf-8', errors='ignore'))
	print('Your file has been saved successfully in the current working directory..')
except Exception as e:
	# If decryption is unsucessful. Print the error and send failed segment
	print('File decryption error occured. Please re-download the file')
	s.send("FAILED".encode('utf-8', errors='ignore'))

s.close()
