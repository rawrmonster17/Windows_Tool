import string
import os
import fnmatch

class Health:

    def __init__(self) -> None:
        pass

    def get_event_logs(self):
        # I don't have time to look at this yet but this seems promising https://www.blog.pythonlibrary.org/2010/07/27/pywin32-getting-windows-event-logs/
        pass

class Malicious:

    def __init__(self) -> None:
        self.list_of_all_connected_drives = []
        self.important_file_extensions = [".jpg", ".txt"]
        self.folders_to_exclude_in_data_collection = [r"c:\Windows", r"c:\Users\*\AppData"]
        self.files_to_collect = []

    def find_all_important_files(self):
        # This works but I need to filter some files so it will not pull files from c:\windows and file paths like that. 
        for drive in self.list_of_all_connected_drives:
            for root, dirs, files in os.walk(drive):
                for file in files:
                    for file_extension in self.important_file_extensions:
                        if (file.endswith(file_extension)):
                            full_file_path = os.path.join(root, file)
                            iteration_count_max = len(self.folders_to_exclude_in_data_collection)
                            iteration_count = 0
                            # This does not work correctly
                            for folder_to_exclude in self.folders_to_exclude_in_data_collection:
                                if fnmatch.filter(full_file_path, folder_to_exclude):
                                    print("{} matched the string".format(full_file_path))
                                    break
                                iteration_count = iteration_count + 1
                                if iteration_count == iteration_count_max:
                                    self.files_to_collect.append(full_file_path)  
                                print(iteration_count_max)
                                print(iteration_count)                 
        for item in self.files_to_collect:
            print("\n {} \n".format(item))

    def find_all_connected_drives(self):
        all_lower_case_letters_list = list(string.ascii_lowercase)
        for letter in all_lower_case_letters_list:
            letter = letter + ":\\"
            does_drive_exist = os.path.isdir(letter)
            if does_drive_exist:
                if letter in self.list_of_all_connected_drives:
                    continue
                else:
                    self.list_of_all_connected_drives.append(letter)
                    

obj = Malicious()
obj.find_all_connected_drives()
obj.find_all_important_files()