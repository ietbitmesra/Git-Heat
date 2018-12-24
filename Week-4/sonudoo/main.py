import os

pyt = "python3" #Here is the command that you use to run python. Possible values - python, python3, python27 etc

print('\nMain Menu:\n')
print('1. Download a file')
print('2. Serve your file(s)')


choice = 0
while True:
	try:
		print('\nEnter your choice: ', end = '')
		choice = int(input())

		if choice != 1 and choice != 2:
			raise Exception('Invalid choice..')

		break
	except Exception as e:
		print('Invalid choice. Please try again..')

if choice == 1:
	try:
		os.system(pyt+" client.py")
	except Exception as e:
		print('Error: File missing or permission denied')

else:
	try:
		os.system(pyt+" server.py")
	except Exception as e:
		print('Error: File missing or permission denied')