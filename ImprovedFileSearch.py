import os
import pandas as pd


class FileSearch:
    def __init__(self, path):
        self.path = path
        self.slash = "\\"

    def list_files(self, sub_folders=False):
        if sub_folders:
            files = []
            for file in os.listdir(self.path):
                file_path = self.path + self.slash + file
                if os.path.isdir(file_path):
                    sub_dir = FileSearch(file_path)
                    sub_files = sub_dir.list_files(sub_folders=True)
                    files += sub_files
                else:
                    files.append(file)
        else:
            files = os.listdir(self.path)

        return files

    def file_sizes(self, sub_folders=False):
        diction = {'File':[], 'Size':[]}
        if sub_folders:
            data_frame = pd.DataFrame(diction)
            for file in os.listdir(self.path):
                file_path = self.path + self.slash + file
                if os.path.isdir(file_path):
                    sub_dir = FileSearch(file_path)
                    sub_files = sub_dir.file_sizes(sub_folders=True)
                    data_frame.append(sub_files, ignore_index=True)
                else:
                    pass
        else:
            files = os.listdir(self.path)
            sizes = []
            for file in files:
                file_path = self.path + self.slash + file
                file_size = round(os.path.getsize(file_path)/1000000, 3)
                sizes.append(file_size)
            diction['File'] = files
            diction['Size'] = sizes
            data_frame = pd.DataFrame(diction)
            return data_frame

    def file_size_sorted(self, number=3, sub_folders=False, ascending=False):
        data_frame = self.file_sizes(sub_folders=sub_folders)
        sorted_data_frame = data_frame.sort_values(by=['Size'], ascending=ascending)

        return sorted_data_frame.head(n=number)

    def find_file(self, filename):
        for root, directory, file in os.walk(self.path):
            if filename in file:
                file_path = os.path.join(root, filename)
                return file_path
