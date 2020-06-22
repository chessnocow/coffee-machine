from collections import deque


class smart_calc:
    error_message = ""
    action = ""
    expression = ""
    values = {}
    operations = []
    operations_que = deque()
    operation_dict = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
        "^": lambda a, b: a ^ b
    }
    precedence = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "^": 3
    }

    def __init__(self):
        pass

    # fill action and expression attributes from the string
    def input_exp(self, str_in):
        if len(str_in) == 0:
            self.action = "empty"
            self.expression = ""
        elif str_in[0] == '/':
            self.action = "command"
            self.expression = str_in
        elif '=' in str_in:
            self.action = 'assign'
            self.expression = str_in
        elif self.values.get(str_in):
            self.action = "calc"
            self.expression = str_in
        else:
            self.action = "calc"
            self.expression = str_in

    # return True or False, fill error_message
    def check_assignment(self):
        if self.action == 'assign':
            self.expression = self.expression.replace('=', ' = ')
            self.operations = self.expression.split()
            if len(self.operations) != 3:
                self.error_message = "Invalid assignment"
                return False
            elif not self.operations[0].isalpha():
                self.error_message = "Invalid identifier"
                return False
            elif not (self.operations[2].isalpha() or self.operations[2].isnumeric()):
                self.error_message = "Invalid assignment"
                return False
            elif self.values.get(self.operations[2]) is None and self.operations[2].isalpha():
                self.error_message = "Unknown variable"
                return False
            return True

    # return string without +- repetitions
    def reduce_add_sub(self, str_in):
        if any([True for ch in str_in if ch not in "+-="]):
            return str_in
        elif len(str_in) == 1:
            return str_in
        else:
            str_in = str_in.replace("++", "+")
            str_in = str_in.replace("+-", "-")
            str_in = str_in.replace("-+", "-")
            str_in = str_in.replace("--", "+")
            return self.reduce_add_sub(str_in)

    # brush expression string
    def parse_expression(self):
        if self.expression != "":
            if "**" in self.expression or "//" in self.expression:
                self.error_message = "Invalid expression"
                return False
            self.expression = self.expression.replace("*", " * ")
            self.expression = self.expression.replace("/", " / ")
            self.expression = self.expression.replace("(", " ( ")
            self.expression = self.expression.replace(")", " ) ")
            self.operations = [self.reduce_add_sub(st) for st in self.expression.split()]
        return True

    # check validity of parenthesis in operations list
    def check_parenthesis(self):
        brackets_stack = deque()
        for ch in self.operations:
            if ch == "(":
                brackets_stack.append(ch)
            elif ch == ")":
                if len(brackets_stack) == 0:
                    return False
                brackets_stack.pop()
        if len(brackets_stack) == 0:
            return True
        return False

    # transform operations list in postfix operations_que
    def transform_operations(self):
        if self.check_parenthesis():
            que = deque()
            for op in self.operations:
                if op.isnumeric():
                    self.operations_que.append(int(op))
                elif op == "(":
                    que.append("(")
                elif op == ")":
                    while que[-1] != "(":
                        self.operations_que.append(que.pop())
                    que.pop()
                elif self.operation_dict.get(op):
                    if len(que) == 0 or que[-1] == "(":
                        que.append(op)
                    elif self.precedence[op] > self.precedence[que[-1]]:
                        que.append(op)
                    elif self.precedence[op] <= self.precedence[que[-1]]:
                        while len(que) > 0:
                            if que[-1] != "(":
                                self.operations_que.append(que.pop())
                            else:
                                break
                        que.append(op)
            for _ in range(len(que)):
                self.operations_que.append(que.pop())
            return True
        else:
            self.error_message = "Invalid expression"
            return False

    # assign variable value
    def assign_value(self):
        if len(self.operations) == 3 and self.operations[1] == '=':
            self.values[self.operations[0]] = self.operations[2]

    # substitute variable values in operations list
    def values_substitution(self):
        for i in range(len(self.operations)):
            if self.values.get(self.operations[i]) is not None:
                self.operations[i] = self.values[self.operations[i]]
            elif self.operations[i].isalpha():
                self.error_message = "Unknown variable"
                return False
        return True

    # calculate postfix expression
    def calculate_operations(self):
        que = deque()
        for _ in range(len(self.operations_que)):
            op = self.operations_que.popleft()
            if type(op) == int:
                que.append(op)
            elif self.operation_dict.get(op):
                a = que.pop()
                b = que.pop()
                res = self.operation_dict[op](b, a)
                res = self.operation_dict[op](b, a)
                que.append(res)
        return que[-1]

    # process the string / main method
    def process(self, str_in):
        self.input_exp(str_in)
        if self.action == "command":
            if self.expression == "/exit":
                print('Bye!')
                return False
            elif self.expression == "/help":
                print('The program calculates the expression from input string. You can use variables.')
            else:
                self.error_message = "Unknown command"
                print(self.error_message)
        elif self.action == "assign":
            if self.check_assignment():
                self.assign_value()
            else:
                print(self.error_message)
        elif self.action == "calc":
            if self.parse_expression() and self.values_substitution():
                try:
                    if self.transform_operations():
                        print(int(self.calculate_operations()))
                    else:
                        print(self.error_message)
                except ValueError:
                    self.error_message = "Invalid expression"
                    print(self.error_message)
                else:
                    return True
            else:
                print(self.error_message)
        return True


calc_obj = smart_calc()
while calc_obj.process(input()):
    pass
