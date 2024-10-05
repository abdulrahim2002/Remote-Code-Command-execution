import socket
import threading
import random
import os
import utility
import subprocess
import pyautogui

parentDir = utility.getpath()

# get server IP
IP = utility.get_ip_address()
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMATmsg = "utf-8"

u_name = []     # list of usernames
u_addr = []     # list of ip addresses
u_conn = []     # list of connections
u_pin = []      # list of pins
u_port = []     # list of ports


# server functions
def start():
    global server

    print(f"SERVER IP = {IP}\n")
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

# broadcast connection list
def broadcast(message):
    if message == 'LIST':
        for addr in u_conn:
            msg = str(u_name)
            msg = "[LIST] CONNECTION LIST: " + msg
            addr.send(msg.encode(FORMATmsg))
            msg = str(u_port)
            msg = "[LIST] CONNECTION LIST: " + msg
            addr.send(msg.encode(FORMATmsg))
    else:
        for addr in u_conn:
            addr.send(message.encode(FORMATmsg))

def exec_cmd(msg):
    result = executeCommand(msg)
    print(f'Output: {result}')
    broadcast(result)

def handle_client(conn, addr, u_name):
    print(f"[SERVER] [NEW CONNECTION] {u_name}:{addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMATmsg)

        print('[Incoming request]: ')
        print(f"[{u_name}:{addr}] {msg}")                   # print msg in server console

        print('Executing command...')
        # str = input()
        # print(str)
        str = msg
        # if str == "exit()":
        #     exit()
        if str[0]=="!" and str[1]!="!":
                str = str.replace("`", "\n")
                pyautogui.write(str[1:], interval = 0.05)
                continue
        if str[0]== '!' and str[1 == '!']:
            spl = str[2:].split('~')
            if len(spl)==1:
                pyautogui.hotkey(spl[0])
                continue
            if len(spl)==2:
                pyautogui.hotkey(spl[0], spl[1])
                continue

        Thr = threading.Thread(target=exec_cmd, args=(msg,))
        Thr.start()

    conn.close()

def executeCommand(command):
    result = os.popen(command).read()
    return result

def startVideoStream():
    print('\nStarting video stream...')
    process = subprocess.Popen(['cmd', '/C', 'streamVideo.bat'], creationflags= subprocess.CREATE_NEW_CONSOLE)

    print(f'Video Stream: Path: http://{IP}:5000')

def main():
    utility.printUI()
    start()
    startVideoStream()

    temp_port = PORT+1
    while True:
        conn, addr = server.accept()
        while True:
            temp_name = conn.recv(SIZE).decode(FORMATmsg)
            print(f"[CLIENT] Username: {temp_name}")
            if temp_name in u_name:
                print("[SERVER] Username not accepted")
                conn.send("NOTACCEPTED!".encode(FORMATmsg))
            else:
                print("[SERVER] Username accepted")
                conn.send(temp_name.encode(FORMATmsg))
                break
        
        temp_pin = str(random.randint(1000, 9999))
        print(f"[AUTHENTICATING] Current Pin: {temp_pin}")
        msg_pin = conn.recv(SIZE).decode(FORMATmsg)
        
        if msg_pin != temp_pin:
            print("[SERVER] PIN not accepted")
            conn.send("try again".encode(FORMATmsg))
            continue
        else:
            print("[SERVER] PIN accepted")
            conn.send("!ACCEPTED".encode(FORMATmsg))
        
        
        conn.recv(SIZE).decode(FORMATmsg)
        conn.send(str(temp_port).encode(FORMATmsg))

        print(f"[SERVER] {temp_name} added to network")
        
        
        clientThread = threading.Thread(target=handle_client, args=(conn, addr, temp_name))
        clientThread.start()


        u_pin.append(temp_pin)
        u_name.append(temp_name)
        u_addr.append(addr)
        u_conn.append(conn)
        u_port.append(temp_port)
        temp_port += 1

        # broadcast connection list
        broadcast('LIST')

        print(f"\n[SERVER][ACTIVE CONNECTIONS] {threading.active_count() - 2}")
    pass


if __name__ == "__main__":
    main()
