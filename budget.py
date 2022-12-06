class Category:

    def __init__(self, name):
        self.total = 0.0
        self.ledger = []
        self.name = name
        self.total_withdraws = 0
        self.percent = 0

    def __str__(self):
        string = f'*************{self.name}*************\n'
        for expense in self.ledger:
            if len(expense['description']) > 23:
                string += f'{expense["description"][0:23]} {expense["amount"]:.2f}\n'
            else:
                string += f'{expense["description"]}{" " * (24 - len(expense["description"]))}{expense["amount"]:.2f}\n'
        string += f'Total: {self.total}'
        return string

    def deposit(self, amount, description=''):
        self.total += amount
        self.ledger.append({'amount': amount, 'description': description})
        return True

    def withdraw(self, amount, description=''):
        if amount > self.total:
            return False
        self.total -= amount
        self.total_withdraws = amount
        self.ledger.append({'amount': -amount, 'description': description})
        return True

    def transfer(self, amount, category):
        if amount > self.total:
            return False
        category.deposit(amount, f'Transfer from {self.name}')
        self.withdraw(amount, f'Transfer to {category.name}')
        return True

    def get_balance(self):
        return self.total

    def check_funds(self, amount):
        if amount > self.total:
            return False
        else:
            return True


def create_spend_chart(categories):
    total_amount = 0
    y_axis = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    y_percent = ['  0| ', ' 10| ', ' 20| ', ' 30| ', ' 40| ', ' 50| ', ' 60| ', ' 70| ', ' 80| ', ' 90| ', '100| ']
    for category in categories:
        total_amount += category.total_withdraws

    for category in categories:
        category.percent = (100 * category.total_withdraws) / total_amount
        category.percent = round(category.percent)
        for y in y_axis:
            index = round(y / 10)
            if category.percent >= y:
                y_percent[index] += 'o  '
            else:
                y_percent[index] += '   '
    y_percent.reverse()
    result = 'Percentage spent by category\n'
    for y in y_percent:
        result += f'{y}\n'
    result += f'    {"---" * len(categories)}-\n'
    larger_category_name = 0
    for category in categories:
        if len(category.name) > larger_category_name:
            larger_category_name = len(category.name)
    for x in range(larger_category_name):
        result += '     '
        for category in categories:
            try:
                result += f'{category.name[x]}  '
            except:
                result += '   '
        result += '\n'
    return result[:-1]
