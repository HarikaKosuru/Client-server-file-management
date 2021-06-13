"""
Contains class named as Services, this class consists of some 
of the services provided by the server.
"""
import os

class Services:
    """
    This class consists some of services provided by the server.

    Methods:
    --------------
        i) __init__(self)
        ii) file_read(self, register_name)
        iii)change_directory(self, folder_name)

    """
    def __init__(self, root_directory, current_directory, user_name):
        """
        Initializing variables
        """
        self.user_name = user_name
        self.root_directory = root_directory
        self.current_directory = current_directory
        self.input = ''
        self.starting = 0
    
    def create_folder(self, folder_name):
        """Creating a folder
        Parameters:
            folder_name : string
                name of the folder to create
        """
        try:
            path = os.path.join(self.current_dir, folder_name)
            os.mkdir(path)
        except:
            reply = 'failed to create folder'
            return reply
        reply = 'folder created'
        return reply


    def file_read(self, register_name):
        """
        This method reads the contents from a given file register_name and returns the starting
        100 characters from the file. This method checks if the newfile matches the previous 
        file, saves the created filename. If the files atre similar it returns next 100 characters.
        
        Parameters:
            register_name : string
                Reads the file name that has to stored.
        """
        if register_name is None:
            if self.input != '':
                self.input = ''
                reply = 'File Closed'
                return reply
            reply = 'Invalid argument'
            return reply
        elif self.user_name=="uSerNamE":
            print("uSerNamE")
        path = os.path.join(self.current_directory, register_name)
        try:
            if os.path.exists(path):
                if self.input == register_name:
                    self.starting = self.starting+100
                    strt = self.starting+100
                    file_open = open(path, "r")
                    read_value = file_open.read()
                    if strt >= len(read_value):
                        self.starting = 0
                    reply= str(read_value[self.starting:strt])
                    return reply
                self.input = register_name
                self.starting = 0
                strt = self.starting+100
                file_open = open(path, "r")
                read_value = file_open.read()
                if strt >= len(read_value):
                    self.starting = 0
                reply= str(read_value[self.starting:strt])
                return reply
            reply = 'file doesnot exist'
            return reply
        except PermissionError:
            reply = 'Requested file is a folder'
            return reply
        except:
            reply = 'error occured'
            return reply

    def change_directory(self, folder_name):
        """
        This method is used to change the directory.
        Parameters:
            folder_name : string
                This changes the name of the folder.
        """
        reverse = ""
        for i in self.root_directory:
            reverse = i + reverse
        path=reverse
        num = path.find('\\')+1
        final_directory = path[num:]
        print(final_directory)
        inp = '..'
        try:
            if folder_name == inp:
                reverse = ""
                for i in self.current_directory:
                    reverse = i + reverse
                inverse=reverse
                num = inverse.find('\\')+1
                new_directory = inverse[num:]
                reverse = ""
                for i in new_directory:
                    reverse= i + reverse
                updated_path= reverse
                reverse = ""
                for i in final_directory:
                    reverse = i + reverse
                last_path= reverse
                if updated_path == last_path:
                    return 'Not autorized'
                reverse = ""
                for i in new_directory:
                    reverse = i + reverse
                self.current_directory= reverse
                reply = 'New directory -> '+self.current_directory
                return reply
            user_directory = os.path.join(self.current_directory, folder_name)
            if os.path.isdir(user_directory):
                self.current_directory = user_directory
                reply = 'New directory -> '+self.current_directory
                return reply
            return 'file not found in this directory '
        except Exception as error:
            reply = f'Exception occured : {error}'
            return reply
        return 'error'
