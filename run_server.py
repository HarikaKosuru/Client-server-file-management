""" 
Server creation
"""
import asyncio
import signal
import os
from class_server import Properties

signal.signal(signal.SIGINT, signal.SIG_DFL)
client_details = {}

async def handle_echo(reader, writer):
    """
    Basic TCP/IP application for client and server.
    """
    root=os.getcwd()
    connection_details = writer.get_extra_info('peername')
    
    #server is connected to the client
    cmd = f"{connection_details} is connected :)"

    #this dictionary stores the client details
    client_details[connection_details[1]] = Properties()
    print(cmd)
    while True:
        read_input = await reader.read(10000)
        cmd = read_input.decode().strip()
        if cmd == 'quit':
            log_in_log = os.path.join(root, 'loginlog.txt')
            file_open = open(log_in_log, 'r')
            lines_in_file = file_open.readlines()
            for i in range(len(lines_in_file)):
                while lines_in_file:
                    if client_details[connection_details[1]].usrname in lines_in_file[i]:
                        pos = i
                    break
            file_open.close()
            file_open = open(log_in_log, 'w')
            for i in range(len(lines_in_file)):
                if pos != i:
                    file_open.writelines(lines_in_file[i])
            file_open.close()
            break
        print(f"Received command < {cmd} > from {connection_details}")
        client_details[connection_details[1]].msg=cmd
        reply_message = cmd.split(' ', 2)
        print('command splitted as: ', reply_message)
        reply = client_details[connection_details[1]].analyze(reply_message)
        print('command execution: ', reply)
        print(f"Sent message: {reply}")
        if reply != '' or reply != 'None':
            writer.write(reply.encode())
        else:
            reply = '.'
            writer.write(reply.encode())
        await writer.drain()
    print("Close the connection")
    writer.close()

async def main():
    """
    Here the main server starts its execution.
    """
    ip_server = '127.0.0.1'
    port_number = 8080
    log_file = open('loginlog.txt', 'w')
    log_file.close()
    server = await asyncio.start_server(handle_echo, ip_server, port_number)

    get_socketname = server.sockets[0].getsockname()
    print(f'Serving on {get_socketname}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
