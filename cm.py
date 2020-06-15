class CoffeeMachine:
    water = 0
    milk = 0
    beans = 0
    cups = 0
    money = 0
    coffee_type = [250, 0, 16, 4, 350, 75, 20, 7, 200, 100, 12, 6]

    def __init__(self, water, milk, beans, cups, money):
        self.water = water
        self.milk = milk
        self.beans = beans
        self.cups = cups
        self.money = money

    def show_state(self):
        print("The coffee machine has:")
        print(self.water, "of water")
        print(self.milk, "of milk")
        print(self.beans, "of coffee beans")
        print(self.cups, "of disposable cups")
        print(self.money, "of money")

    def make_smth(self, inp_):
        if inp_ == "buy":
            w2b = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:")
            if w2b != 'back':
                w2b = int(w2b)
                if self.water >= self.coffee_type[(w2b - 1) * 4] and self.milk >= self.coffee_type[
                    (w2b - 1) * 4 + 1] and self.beans >= self.coffee_type[(w2b - 1) * 4 + 2] and self.cups >= 1:
                    self.water -= self.coffee_type[(w2b - 1) * 4]
                    self.milk -= self.coffee_type[(w2b - 1) * 4 + 1]
                    self.beans -= self.coffee_type[(w2b - 1) * 4 + 2]
                    self.cups -= 1
                    self.money += self.coffee_type[(w2b - 1) * 4 + 3]
                    print('I have enough resources, making you a coffee!')
                    return True
                else:
                    print("Not enough supplements")
                    return True
            else:
                return True
        elif inp_ == "fill":
            self.water += int(input("Write how many ml of water do you want to add:"))
            self.milk += int(input("Write how many ml of milk do you want to add:"))
            self.beans += int(input("Write how many grams of coffee beans do you want to add:"))
            self.cups += int(input("Write how many disposable cups do you want to add:"))
            return True
        elif inp_ == "take":
            print("I gave you $", self.money)
            self.money = 0
            return True
        elif inp_ == "exit":
            return False
        elif inp_ == "remaining":
            self.show_state()
            return True
        else:
            print("Error")
            return True


cm = CoffeeMachine(400, 540, 120, 9, 550)
while cm.make_smth(input("Write action (buy, fill, take):")):
    pass
