#! python3
import os

def get_size(path):
	"""Calculates size of folder/file, returns the same."""
	total_size = 0

	if(os.path.isfile(path)):
		total_size = os.path.getsize(path)
	elif(os.path.isdir(path)):
	    for dirpath, dirnames, filenames in os.walk(path):
	        for f in filenames:
	            fp = os.path.join(dirpath, f)
	            total_size += os.path.getsize(fp)

	return total_size


class Tree:
	"""Gets all folders, files and file_types in a folder."""
	def __init__(self, path): 
		self.path = path  
		self.folders = []
		self.files = []
		self.file_types = {}


	def get_folders(self):
		return self.folders

	def get_files(self):
		return self.files

	def get_file_types(self):
		return self.file_types

	def total_size(self):
		return sum(self.files[1])+sum(self.folders[1])

	def make_tree(self):
		"""Searches for files/folders and file types, stores in folders,files,file_types"""
		folders = next(os.walk(self.path))[1]
		folder_labels = []
		folder_values = []


		files = next(os.walk(self.path))[2]
		file_labels = []
		file_values = []

		for folder in folders:
			folder_path = os.path.join(self.path,folder)

			folder_labels.append(folder)
			folder_values.append(get_size(folder_path))


		for file in files:
			file_path = os.path.join(self.path,file)
			file_name, file_extension = os.path.splitext(file)

			file_labels.append(file)
			file_values.append(get_size(file_path))

			if(file_extension in self.file_types):
				self.file_types[file_extension]+=1
			else:
				self.file_types[file_extension]=1

		self.folders.append(
			folder_labels
		)
		self.folders.append(
			folder_values
		)

		self.files.append(
			file_labels
		)
		self.files.append(
			file_values
		)

