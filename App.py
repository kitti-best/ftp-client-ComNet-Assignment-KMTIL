from FTP import FTP
from Status import Status

class App:
    def __init__(self):
        self.ftp = FTP()
        self.command_mapper = {
            "ascii": self.ftp.ascii, # check
            "binary": self.ftp.binary, # check
            "bye": self.ftp.quit, # check
            "cd": self.ftp.cd, # check
            "close": self.ftp.disconnect, # check
            "delete": self.ftp.delete, # check
            "disconnect": self.ftp.disconnect, # check
            "get": self.ftp.get, # check
            "ls": self.ftp.ls, # what about ls /pub
            "open": self.ftp.open, # check
            "put": self.ftp.put,
            "pwd": self.ftp.pwd, # check
            "quit": self.ftp.quit, # check
            "rename": self.ftp.rename, # check
            "user": self.ftp.user, # check
            "__not_connected__": self.__not_connect_handler,
            "__return__": lambda: None, # do nothing
            "__param_incomplete__": lambda: None, # do nothing
        }
        self.input_hint = {
            "open": lambda: self.__give_hint("To", usage="Usage: open host name [port]"),
            "user": lambda: self.__give_hint("Username", usage="Usage: user username [password] [account]"),
            "cd": lambda: self.__give_hint("Remote directory", usage="cd remote directory."),
            "delete": lambda: self.__give_hint("Remote file", usage="delete remote file."),
            "get": lambda: self.__give_hint("Remote file", usage="Remote file get [ local-file ]."),
            "rename": lambda: self.__give_hint("From name", "To name", usage="rename from-name to-name."),
            "put": lambda: self.__give_hint("Local file", "Remote file", usage="Local file put: remote file.")
        }

    def run(self):
        while True:
            user_input = input("ftp> ")
            command, params = self.input_parser(user_input)
            if command in self.command_mapper:
                self.command_mapper[command](*params)

    def input_parser(self, user_input):
        user_input = user_input.split()
        if len(user_input) == 0:
            command, params = "__return__", ""
            return command, params
        else:
            command, params = user_input[0], user_input[1:]

        if not command in self.command_mapper:
            print("Invalid command.")
        elif command not in ["open", "quit"] and not self.ftp.get_connection():
            command = "__not_connected__"
        elif len(params) == 0 and command in self.input_hint:
            params = self.input_hint[command]()
            if not params:
                command = "__param_incomplete__"

        return command, params

    def __give_hint(self, *args, usage=""):
        """
        :param args: prompt, each prompt for each params
        :return: list of params
        """
        params = []
        for hint in args:
            param = input(hint + " ")
            if param == "":
                print(usage)
                params = []
                break
            params.append(param)
        return params

    def __not_connect_handler(self, *args):
        print("Not connected.")
