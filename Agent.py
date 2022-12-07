import string
import os
import fnmatch

class Logging:

    def __init__(self) -> None:
        self.logfile_location = None
    
    def set_logging_location(self):
        pass

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
        self.folders_to_exclude_in_data_collection = [r"c:\Windows\*", r"c:\Users\*\AppData\*"]
        self.files_to_collect = []

    def find_all_important_files(self):
        # This works but I need to filter some files so it will not pull files from c:\windows and file paths like that. 
        for drive in self.list_of_all_connected_drives:
            for root, dirs, files in os.walk(drive):
                for file in files:
                    for file_extension in self.important_file_extensions:
                        if (file.endswith(file_extension)):
                            full_file_path = os.path.join(root, file)
                            print(full_file_path)
                            iteration_count = 0
                            iteration_max = len(self.folders_to_exclude_in_data_collection)
                            # This does not work correctly
                            for folder_to_exclude in self.folders_to_exclude_in_data_collection:
                                iteration_count = iteration_count + 1
                                if fnmatch.fnmatch(full_file_path, folder_to_exclude):
                                    print("{} Matches and is going to be excluded".format(full_file_path))
                                    break
                                elif not fnmatch.fnmatch(full_file_path, folder_to_exclude) and iteration_count == iteration_max:
                                    print("adding file to list")
                                    self.files_to_collect.append(full_file_path)
                                elif not fnmatch.fnmatch(full_file_path, folder_to_exclude) and iteration_count != iteration_max:
                                    continue
                                else:
                                    print("")
                                
                                                  
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