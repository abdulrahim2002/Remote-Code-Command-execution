import socket
import threading
import time
import utility
IP = utility.get_ip_address()

c_obj = threading.Condition()
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMATmsg = "utf-8"
USERNAME = None
PIN = None
client = None
S_PORT = None


def send_message():
    # c_obj.acquire()
    while True:
        msg = input("")
        globals()['client'].send(msg.encode(FORMATmsg))


def recieve_messsage():
    # c_obj.acquire()
    while True:

        msg = globals()['client'].recv(SIZE).decode(FORMATmsg)

        print(f"[SERVER] {msg}")
        pass


def startClient():
    print(f"[CONNECTING] Client connecting to server at {IP}:{PORT}")
    globals()['client'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    globals()['client'].connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")


def main():
    utility.printUI()

    while True:
        startClient()

        # [TAB] for inputting, sending and verifyin username
        if globals()['USERNAME'] == None or globals()['USERNAME'] == "!NOTACCEPTED":
            while True:
                globals()['USERNAME'] = input("[LOGIN] INPUT USERNAME: ")

                globals()['client'].send(
                    globals()['USERNAME'].encode(FORMATmsg))
                temp_msg = globals()['client'].recv(SIZE).decode(FORMATmsg)
                if (temp_msg == globals()['USERNAME']):
                    print(f"[SERVER] Username accepted")
                    break
                else:
                    print("[NAME ERROR] Try another username")
                    continue

        if globals()['PIN'] == None:
            globals()['PIN'] = input("[LOGIN] Input PIN: ")
        globals()['client'].send(globals()['PIN'].encode(FORMATmsg))

        temp_msg = globals()['client'].recv(SIZE).decode(FORMATmsg)
        print(f"[SERVER] {temp_msg}")
        if temp_msg == "try again":
            print(
                '[SERVER]: PIN not accepted:(\n[SERVER]: Connection failed:(\nTerminating:(\n')
            globals()['client'].close()
            exit()

        print(
            f"[AUTHENTICATED] credentials are verified by server at {IP}:{PORT}")

        print(f"[Waiting] Waiting for port number from {IP}:{PORT}")
        globals()['client'].send("PORT".encode(FORMATmsg))
        temp_msg = globals()['client'].recv(SIZE).decode(FORMATmsg)
        globals()['S_PORT'] = int(temp_msg)
        print(f"[SERVER] Your port number is {globals()['S_PORT']}")
        # input("end")
        break

    thread_recv = threading.Thread(target=recieve_messsage, args=())
    thread_recv.start()
    time.sleep(0.1)
    thread_send = threading.Thread(target=send_message, args=())
    thread_send.start()

    pass


if __name__ == "__main__":
    main()
