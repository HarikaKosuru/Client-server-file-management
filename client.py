"""
Client Initialization.
"""
import asyncio

ISSUED = ''
def start():
    """
    This function helps the client to register and login.
    """
    print('******* client-server application *******')
    while True:
        print('1 : Login & 2 : Register')
        choice = input('Enter Choice(1 or 2): ')
        if choice == '1':
            result = login()
            return result
        elif choice == '2':
            result = register()
            return result
        print('Invalid Input ')

def process(message):
    """
    This function process the commands that are sent to server.

    """
    split_message = message.split(' ', 1)
    command = split_message[0]
    count_arguments = len(split_message)
    global ISSUED
    if command == 'commands':
        if count_arguments == 1:
            c_file = open('commands.txt', 'r')
            content = c_file.read()
            print(content)
            return False
        elif count_arguments == 2:
            argument = split_message[1]
            if argument == 'issued':
                print(ISSUED)
                return False
            elif argument == 'clear':
                ISSUED = ''
                print('Cleared')
                return False
            print('Invalid command')
            return False
        print('invalid arguments')
        return False
    ISSUED += str('\n'+message)
    return True

def login():
    """
    This function returns the login credentials.

    """
    
    print('*************** USER LOGIN ****************')
    login = input("login <username> <password> :")
    result = str(f'{login}')
    return result

def register():
    """
    This function returns and prints the registered credentials.

    """
    
    print('*********** USER Registration ************')
    sign_up=input("register <username> <password>: ")
    result = str(f'{sign_up} ')
    print(result)
    return result

async def server_connect():
    """
    This function establishes connection with the server.

    """
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8080)
        recieved = ''
        while True:
            request = start()
            writer.write(request.encode())
            data = await reader.read(10000)
            recieved = data.decode()
            if recieved == 'successful':
                print('Login Successful ')
                break
            elif recieved == 'Created':
                print('New user Created')
                break
            elif recieved == 'exist':
                print('User Already Exist ')
                print('Try again with new Username')
                continue
            elif recieved == 'failed':
                print('Login Failed ')
                print('Try Again')
                continue
            elif recieved == 'invalid':
                print('invalid input ')
                continue
            elif recieved == 'loggedin':
                print('user is already loggedin from another client')
                continue
            else:
                print('Error has Occured, Please Try Again ')
                continue

        while True:
            recieved = input('>>')

            if recieved == 'quit':
                writer.write(recieved.encode())
                break
            elif recieved == '':
                continue
            reply = process(recieved)
            if reply:
                writer.write(recieved.encode())
                data = await reader.read(10000)
                print(f'{data.decode()}')
        print('Close the connection')
        writer.close()
    except RuntimeError:
        print("Runtime error")

try:
    asyncio.run(server_connect())
except ConnectionRefusedError:
    print('Failed to connect to the server')
