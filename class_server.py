""" 
    handles the requests and method calls from the server.
"""
import os
import datetime
import time
from logic_server import Services

#This is a server class

class Properties:
    """
    This class consists of methods for file management.
    Methods:
        i) __init__(self)
        ii)get_password(self, user_name)
        iii)login(self, split_message)
        iv)register(self, user_name, password)
        v)start_register(self)
        vi)analyze(self, cmd)
    """

    def __init__(self):
        """
        Initializes all the variables
        """
        self.root = os.getcwd()
        self.current = ''
        self.usrname = ''
        self.msg = ''
        self.psswrd = ''

    def get_password(self, user_name):
        """
        This method returns the password.
        Parameters:
            user_name : string
                stores the username from the user
                 where the password is returned.
        """
        usr_log = 'log.txt'
        usr_file = open(usr_log, 'r')
        lines_in_file = usr_file.readlines()
        line_count = sum(1 for line in open('log.txt'))
        usr_num =[ ]
        names =[ ]
        usr_pass =[ ]
        for i in range(line_count):
            line = lines_in_file[i].strip()
            found = line.find(",")
            usr_num.append(found)
            names.append(line[:usr_num[i]])
            usr_pass.append(line[usr_num[i]+1:])
        len_names=len(names)
        for j in range(0, len_names):
            if user_name == names[j]:
                msg = str(f'{names[j]} {usr_pass[j]} user')
                return msg
        msg = 'failed'
        return msg



    def login(self, split_message):
        """
        This method is used for the login to the clients and returns
        loggedin if correct or else returns fail.
        Parameters:
            split_message : string
                used to split the username

        """
        answer=False
        username = split_message[1]
        log_file = 'loginlog.txt'
        with open(log_file) as f_r:
            if username in f_r.read():
                answer= True
        if answer==True:
            return 'loggedin'
        password = split_message[2]
        reply = self.get_password(username)
        message_reply = reply.split(' ', 2)
        check_username = message_reply[0]
        if check_username == 'failed':
            return 'failed'

        check_password = message_reply[1]
        if check_username == username:
            if check_password == password:
                check_reply= 'successful'
            else:
                check_reply='failed'
        else:
            check_reply= 'failed'
        if check_reply == 'successful':
            current_working_direc = os.path.join(self.root, username)
            self.current = current_working_direc
            self.usrname = username
            self.psswrd = password
            self.client = Services(self.root,self.current,self.usrname)
            txt='loginlog.txt'
            file_name = str(f'{self.root}\\{txt}')
            file = open(file_name, 'a+')
            user_data = [self.usrname, "\n"]
            file.writelines(user_data)
            file.close()
            return 'successful'
        elif check_reply == 'failed':
            return 'failed'


    def register(self, user_name, password):
        """
        This method registers the clients in the server.
        Parameters:
            user_name : string
               stores username
            password : string
                stores password 
        """
        file_path = open(str(f'{self.root}\\log.txt'), "a+")
        data = str(f'\n{user_name},{password}')
        file_path.writelines(data)
        file_path.close()
        path = os.path.join(self.root, user_name)
        os.mkdir(path)
        file_name = str(f'{path}\\log.txt')
        file_o = open(file_name, "w")
        data = user_name
        user_data = [data, "\n"]
        file_o.writelines(user_data)
        file_o.close()

    def start_register(self):
        """
        This method checks the credentials provided by the client
        are valid.

        """
        splitted_msg = self.msg.split(' ', 3)
        username = splitted_msg[1]
        password = splitted_msg[2]
        try:
            login_file = 'log.txt'
            file_name = str(f'{self.root}\\{login_file}')
            op_file = open(file_name, 'r')
            lines_in_file = op_file.readlines()
            sum_lines = sum(1 for line in open(file_name, 'r'))
            numbers = []
            names = []
            for i in range(sum_lines):
                file = lines_in_file[i].strip()
                found = file.find(",")
                numbers.append(found)
                names.append(file[:numbers[i]])
            if username in names:
                reply= 'exist'
            reply= 'ok'
        except:
            reply= 'error occured'
        if reply == 'exist':
            return reply
        self.register(username, password)
        splitted_msg = ['login', username, password]
        reply = self.login(splitted_msg)
        return reply

    def analyze(self, cmd):
        """
        This method takes the requests from the file and handles the
        file by file handling methods in an requested order.
        Parameters:
            cmd : list(str,str,str)
                The given arguments are stored in a list.
        """
        command = cmd[0]
        try:
            if self.usrname == '':
                if command == 'login':
                    try:
                        reply = self.login(cmd)
                    except:
                        reply = 'error occurred'
                    return reply
                elif command == 'register':
                    try:
                        reply = self.start_register()
                    except:
                        reply = 'error occurred'
                    return reply
                return 'failed'
            else:
                if command == 'list':
                    try:
                        path = self.client.current_directory
                        files = list(os.listdir(path))
                        data = {}
                        size_date = ['', '']
                        reply = ''
                        for file in files:
                            file_path = os.path.join(path, file)
                            date_created = os.stat(file_path).st_ctime
                            date_format = str("{}".format(datetime.datetime.strptime(time.ctime(date_created), "%a %b %d %H:%M:%S %Y")))
                            thestats = os.stat(file_path)
                            data[file] = size_date.copy()
                            data[file][0] = thestats.st_size
                            data[file][1] = date_format
                        reply += '{:25}\t{:10}\t{:10}'.format('Name of the file', 'Size in Bytes', 'Date of Creation \n')
                        reply += '-------------------------------------------------------------------\n'
                        for key in data:
                            reply += str('{:20s}\t{:10} Bytes\t{:10}\n'.format(key, data[key][0], data[key][1]))
                    except:
                        reply = 'error occured'
                    return reply

                elif command == 'change_folder':
                    try:
                        argument_1 = cmd[1]
                        reply = self.client.change_directory(argument_1)
                    except:
                        reply = 'Failed'
                    return reply

                elif command == 'read_file':
                    try:
                        argument_1 = cmd[1]
                        reply = self.client.file_read(argument_1)
                    except IndexError:
                        reply = self.client.file_read(None)
                    except:
                        reply = 'error occured'
                    return reply
                elif command == 'write_file':
                    try:
                        argument_1 = cmd[1]
                    except IndexError:
                        reply = 'invalid Argument'
                        return reply
                    try:
                        argument_2 = cmd[2]
                        path = os.path.join(self.client.current_directory, argument_1)
                        if argument_2 is None:
                            file_open = open(path, 'w')
                            file_open.close()
                            reply = 'File cleared'
                        else:
                            file_open = open(path, 'a')
                            user_data = [argument_2, "\n"]
                            file_open.writelines(user_data)
                            file_open.close()
                            reply = 'file edited successfully'
                    except IndexError:
                        path = os.path.join(self.client.current_directory, argument_1)
                        if argument_2 is None:
                            file_open = open(path, 'w')
                            file_open.close()
                            reply = 'File cleared'
                        else:
                            file_open = open(path, 'a')
                            user_data = [argument_2, "\n"]
                            file_open.writelines(user_data)
                            file_open.close()
                            reply = 'file edited successfully'
                    except:
                        reply = 'error occured'
                    return reply
                elif command == 'create_folder':
                    try:
                        argument_1 = cmd[1]
                        reply=self.client.create_folder(argument_1)
                    except:
                        reply = 'error occured'
                    return reply
                else:
                    return 'Invalid input'
        except RuntimeError:
            print("RuntimeError")