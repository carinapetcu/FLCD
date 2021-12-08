class Grammar:
    def __init__(self, file_name):
        self.non_terminal_symbols = list()
        self.terminal_symbols = list()
        self.productions = dict(list())
        self.start_symbol = None
        self.read_from_file(file_name)

    def read_from_file(self, file_name):
        file = open(file_name, "r")
        lines = file.readlines()

        self.non_terminal_symbols = lines[0].strip().split(',')
        self.terminal_symbols = lines[1].strip().split(',')
        self.start_symbol = lines[2].strip()

        for index in range(3, len(lines)):
            elements = lines[index].strip().split(',')
            non_terminal_symbol = elements[0]
            productions_for_symbol_not_split = elements[1:]
            productions_for_symbol = [production.split('.') for production in productions_for_symbol_not_split]
            self.productions[non_terminal_symbol] = productions_for_symbol

    def get_productions_with_symbol(self, symbol):
        result = []
        for production_key in self.productions:
            production_values = self.productions[production_key]
            for right_side in production_values:
                if symbol in right_side:
                    result.append((production_key, right_side))

        return result

    def check_if_cfg(self):
        # we will go through all the productions and check if the terminal node is on the left side
        for symbol in self.productions:
            productions = self.productions[symbol]
            for production in productions:
                if len(production) >= 2:
                    if production[0] in self.terminal_symbols and production[1] in self.terminal_symbols:
                        return False
        return True

    def print_menu(self):
        print('Please choose an option: \n'
              '\t1. show non terminals\n'
              '\t2. show terminals\n'
              '\t3. show starting symbol\n'
              '\t4. show all productions\n'
              '\t5. show productions for symbol \n'
              '\t6. check if grammar is context free\n'
              '\tx. quit\n')

    def menu(self):
        isDone = False
        print('Hello!\n')
        while not isDone:
            self.print_menu()
            option = input('Your choice is: ')
            if option == '1':
                print('The non terminals: ' + str(self.non_terminal_symbols))
            elif option == '2':
                print('The terminals: ' + str(self.terminal_symbols))
            elif option == '3':
                print('The starting symbol: ' + str(self.start_symbol))
            elif option == '4':
                toPrint = ""
                for symbol in self.productions:
                    productions_for_symbol = self.productions[symbol]
                    toPrint += symbol + " -> "
                    for production in productions_for_symbol:
                        toPrint += ' '.join(production) + " | "
                    toPrint = toPrint[:-2]
                    toPrint += "\n\t"
                print('The productions: \n\t' + toPrint)
            elif option == '5':
                symbol = input('The given symbol is: ')
                toPrint = ""
                productions_for_symbol = self.productions[symbol]
                for production in productions_for_symbol:
                    toPrint += symbol + " -> " + ' '.join(production) + "\n\t"
                print('The productions for symbol ' + symbol + ' : \n\t' + toPrint)
            elif option == '6':
                result = self.check_if_cfg()
                isCFG = "is" if result else "is not"
                print('The given grammar ' + isCFG + ' a cfg')

            elif option == 'x':
                print('Goodbye!')
                isDone = True
            else:
                print('Wrong option! Please try again!')


if __name__ == '__main__':
    grammar = Grammar('g2.txt')
    grammar.menu()
