import random
import socket
import sys
from Status import Status

class FTP:
    def __init__(self):
        self.rcv_buffer = []
        self.client_socket = None
        self.__connected = False

    def __display_response(self, buff_size=4096):
        while True:
            recv = self.client_socket.recv(buff_size).decode()
            print(recv.strip())
            try:
                status = Status(int(recv[:3]))
            except (TypeError, IndexError) as e:
                status = None
                return status
            if len(recv) < buff_size:
                break

        return status

    def __prepare_command(self, command):
        return (command + "\r\n").encode()

    def get_connection(self):
        return self.__connected

    def open(self, host, port=21, *args):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if host == "":
            print("Usage: open host name [port]")
            return
        try:
            self.client_socket.connect((host, int(port)))
        except socket.gaierror:
            print(f"Unknown host {host}")
            return
        except ConnectionRefusedError:
            print(f"> ftp: connect :Connection refused")
            return
        except TimeoutError:
            print(f"> ftp: connect :Connection timed out")
            return

        print(f"Connected to {host}.")
        status = self.__display_response()
        self.client_socket.send("OPTS UTF8 ON\r\n".encode())
        status = self.__display_response()

        self.__connected = True
        if Status.is_positive_completion(status):
            user_name = input(f"User ({host}:(none)): ")
            self.user(user_name)

        return status

    def user(self, user_name, password="", *args):
        self.client_socket.send(f"USER {user_name}\r\n".encode())
        status = self.__display_response()
        if Status.is_negative5xx(status):
            print("Login failed.")
            return
        elif Status.is_positive_intermediate(status) and not password:
            password = input(f"Password: ")
        if password:
            self.client_socket.send(f"PASS {password}\r\n".encode())
            status = self.__display_response()
            if Status.is_negative5xx(status):
                print("Login failed.")
                return

    def ascii(self, *args):
        self.client_socket.send(f"TYPE A\r\n".encode())
        self.__display_response()

    def binary(self, *args):
        self.client_socket.send(f"TYPE I\r\n".encode())
        self.__display_response()

    def disconnect(self, *args, show_res=True):
        self.client_socket.send(f"QUIT\r\n".encode())
        self.__connected = False
        if show_res:
            self.__display_response()

    def quit(self, *args):
        if self.client_socket:
            self.disconnect(show_res=False)
        sys.exit()

    def __get_passive_port(self, passive_rcv):
        rcv = passive_rcv.split()
        status = Status(int(rcv[0]))
        if status != Status.S227:
            return status

        data = rcv[4].replace("(", "").replace(")", "").split(",")
        port = ".".join(data[:4])
        host = int(data[4]) * 256 + int(data[5])
        return port, host

    def __open_remote_data_connection(self, command, func):
        port = random.randint(0, 65535)  # 0 to 2 ^ 16 - 1
        ip = socket.gethostbyname(socket.gethostname())
        args = ip + "." + str(port // 256) + "." + str(port % 256)
        args = args.replace(".", ",")
        self.client_socket.send(("PORT " + args + "\r\n").encode())
        status1 = self.__display_response()
        if status1 != Status.S200:
            return status1

        self.client_socket.send("PASV\r\n".encode())
        rcv = self.client_socket.recv(1024).decode()
        data_host, data_port = self.__get_passive_port(rcv)
        with socket.create_connection((data_host, data_port)) as data_socket:
            self.client_socket.send(f"{command}\r\n".encode())
            self.__display_response()
            # do the task here
            func(data_socket)

    def ls(self, remote_dir="", *args):
        def show_remote_files(data_socket):
            rcv = data_socket.recv(1024).decode()
            while rcv != "":
                print(rcv.strip())
                rcv = data_socket.recv(1024).decode()

        remote_dir = "x" + remote_dir if remote_dir else ""
        self.__open_remote_data_connection("NLST" + remote_dir, show_remote_files)
        self.__display_response()

    def cd(self, cd_to, *args):
        self.client_socket.send(f"CWD {cd_to}\r\n".encode())
        self.__display_response()

    def get(self, file_name, *args):
        def get_file(data_socket):
            with open(file_name, "w") as file:
                rcv = data_socket.recv(1024).decode()
                while rcv != "":
                    file.write(rcv.replace("\n", ""))
                    rcv = data_socket.recv(1024).decode()

        self.__open_remote_data_connection(f"RETR {file_name}", get_file)
        self.__display_response()

    def put(self, file_name, *args):
        self.__open_remote_data_connection(f"STOR {file_name}", lambda *args: None)

    def delete(self, file_name, *args):
        self.client_socket.send(f"DELE {file_name}\r\n".encode())
        self.__display_response()

    def pwd(self, *args):
        self.client_socket.send("XPWD\r\n".encode())
        self.__display_response()

    def rename(self, from_name, to_name, *args):
        self.client_socket.send(f"RNFR {from_name}\r\n".encode())
        self.__display_response()
        self.client_socket.send(f"RNTO {to_name}\r\n".encode())
        self.__display_response()

