import os
import pandas as pd


class FileSearch:
	def __init__(self, path):
		self.path = path
		self.slash = "\\"

	def files(self, sub_folders):
		"""
		Method to list all files in the path, returns all files in sub-folders as well if
		sub_folders is True.

		For every file in the path, if a file_path, checks to see whether sub-folders are included
		and then re-runs the method on that path. If not a file_path appends file onto the end of the list.

		:param sub_folders: Return files from sub-folders?
		:return: Returns list of all files in the path
		"""
		result = []
		for file in os.listdir(self.path):
			file_path = self.path + self.slash + file
			if os.path.isdir(file_path):
				if sub_folders:
					sub = FileSearch(file_path)
					subs = sub.files(True)
					result = result + subs
				else:
					result.append(file)
			else:
				result.append(file)

		return result

	def size(self, sub_folders):
		"""
		Method to retrieve all files in specified path along with size of each file, returns files
		in sub-folders as well if sub_folders is True.

		For every file in the path, f a file_path, checks to see whether sub-folders are included
		and then re-runs the method on that path. If not a file_path, creates a dictionary of file path and size
		creates data frame from that dictionary and appends to existing data frame.

		:param sub_folders: Return files from sub-folders?
		:return: Returns data frame of all files and size, files given by paths.
		"""

		lst = {'File': [], 'Size': []}
		data = pd.DataFrame(lst)

		for file in os.listdir(self.path):
			file_path = self.path + self.slash + file
			if os.path.isdir(file_path):
				if sub_folders:
					sub = FileSearch(file_path)
					subs = sub.size(True)
					data = data.append(subs, ignore_index=True)
				else:
					pass
			else:
				size = round((os.path.getsize(file_path))/1000000, 3)
				file_size = {'File': [file_path], 'Size': [size]}
				file_data = pd.DataFrame(file_size)
				data = data.append(file_data, ignore_index=True)

		return data

	def size_sorted(self, sub_folders, number_to_return):
		"""
		Method to retrieve specified number of  files in specified path sorted by descending size, returns files
		in sub-folders as well if sub_folders is True.

		Runs the size method then sorts by descending size and returns number specified.

		:param sub_folders: Return files from sub-folders?
		:param number_to_return: Number of files to return
		:return: Returns data frame of specified number of files by size
		"""
		data_frame = self.size(sub_folders)
		new_data = data_frame.sort_values(by=['Size'], ascending=False)

		return new_data.head(number_to_return)

	def search(self, filename):
		"""
		Method searches for file name specified in self.path

		:param filename: Name of the file searching for
		:return: Path to file name
		"""
		for roots, directories, files in os.walk(self.path):
			if filename in files:
				return os.path.join(roots, filename)








