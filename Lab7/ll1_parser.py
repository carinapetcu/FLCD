import copy

from parser_output import ParserOutput

EPSILON = 'epsilon'


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar

        self.first = dict(list())
        self.initialize_first()
        self.first_function()

        self.follow = dict(list())
        self.initialize_follow()
        self.follow_function()

        self.parsing_table = dict()
        self.create_parsing_table()

        self.parser_output = None

    def concatenate(self, first, second):
        result = []
        for elementFirst in first:
            for elementSecond in second:
                if elementFirst == EPSILON:
                    result.append(elementSecond)
                elif elementSecond == EPSILON:
                    result.append(elementFirst)
                else:
                    result.append(elementFirst)

        result = list(set(result))
        return result

    def initialize_first(self):
        non_terminal_symbols = self.grammar.non_terminal_symbols
        productions = self.grammar.productions
        terminal_symbols = self.grammar.terminal_symbols

        for symbol in non_terminal_symbols:
            self.first[symbol] = []

        for symbol in productions:
            productions_for_symbol = productions[symbol]
            for production in productions_for_symbol:
                if production[0] in terminal_symbols and production[0] not in self.first[symbol]:
                    self.first[symbol].append(production[0])
                if production[0] == EPSILON:
                    self.first[symbol].append(EPSILON)

    def first_function(self):
        current = dict(list())
        non_terminal_symbols = self.grammar.non_terminal_symbols

        for symbol in self.first:
            value = copy.deepcopy(self.first[symbol])
            productions_for_symbol = self.grammar.productions[symbol]
            for production in productions_for_symbol:
                non_terminal_symbols_first = []
                nonEmpty = True

                if production[0] in non_terminal_symbols:
                    for element in production:
                        if element in non_terminal_symbols:
                            if not self.first[element]:
                                nonEmpty = False
                                continue
                            non_terminal_symbols_first.append(element)

                    if nonEmpty and len(non_terminal_symbols_first) >= 2:
                        result = self.concatenate(self.first[non_terminal_symbols_first[0]],
                                                  self.first[non_terminal_symbols_first[1]])

                        for index in range(2, len(non_terminal_symbols_first)):
                            result = self.concatenate(result, self.first[non_terminal_symbols_first[index]])

                        value.extend(result)
                        value = list(set(value))
                    elif nonEmpty and len(non_terminal_symbols_first) == 1:
                        value = self.first[non_terminal_symbols_first[0]]

            current[symbol] = value

        if self.first != current:
            self.first = current
            self.first_function()

    def initialize_follow(self):
        non_terminal_symbols = self.grammar.non_terminal_symbols
        start_symbol = self.grammar.start_symbol

        for symbol in non_terminal_symbols:
            if symbol == start_symbol:
                self.follow[symbol] = [EPSILON]
            else:
                self.follow[symbol] = []

    def follow_function(self):
        current = dict(list())
        non_terminal_symbols = self.grammar.non_terminal_symbols
        terminal_symbols = self.grammar.terminal_symbols

        for symbol in non_terminal_symbols:
            current_value = copy.deepcopy(self.follow[symbol])
            # tuple of the form (left side, right side)
            matching_productions = self.grammar.get_productions_with_symbol(symbol)

            for prod in matching_productions:
                left_side = prod[0]
                right_side = prod[1]

                index_of_symbol = right_side.index(symbol)
                if index_of_symbol < len(right_side) - 1:
                    # this means that there is another symbol after our current symbol
                    value_after_symbol = right_side[index_of_symbol + 1]
                    if value_after_symbol in terminal_symbols:
                        current_value.append(value_after_symbol)
                    else:
                        neighbour_first_value = self.first[value_after_symbol]
                        found_epsilon = False
                        for value in neighbour_first_value:
                            if value == EPSILON:
                                found_epsilon = True
                            else:
                                current_value.append(value)

                        if found_epsilon:
                            current_value.extend(self.follow[left_side])

                elif index_of_symbol == len(right_side) - 1:
                    current_value.extend(self.follow[left_side])

            current_value = list(set(current_value))
            current[symbol] = current_value

        if not self.compare_dictionaries(self.follow, current):
            self.follow = current
            self.follow_function()

    def compare_dictionaries(self, firstDictionary, secondDictionary):
        first_keys = firstDictionary.keys()
        second_keys = secondDictionary.keys()

        if set(first_keys).issubset(second_keys) and set(second_keys).issubset(first_keys):
            for symbol in firstDictionary:
                first_value = firstDictionary[symbol]
                second_value = secondDictionary[symbol]

                if not set(first_value).issubset(second_value) or not set(second_value).issubset(first_value):
                    return False

            return True
        else:
            return False

    def create_parsing_table(self):
        non_terminal_symbols = self.grammar.non_terminal_symbols
        terminal_symbols = self.grammar.terminal_symbols
        numbered_productions = self.grammar.productions_with_numbers

        rows = non_terminal_symbols + terminal_symbols + ['$']
        columns = terminal_symbols + ['$']

        # initialization
        for row in rows:
            for column in columns:
                if row == column:
                    if row == '$':
                        self.parsing_table[(row, column)] = ("acc", None)
                    else:
                        self.parsing_table[(row, column)] = ("pop", None)

        for index in range(len(numbered_productions)):
            current_production = numbered_productions[index]
            left = current_production[0]
            right = current_production[1]

            if right[0] in terminal_symbols:
                self.parsing_table[(left, right[0])] = (right, index + 1)
            elif right[0] in non_terminal_symbols:
                result = [EPSILON]

                for element in right:
                    if element in non_terminal_symbols:
                        result = self.concatenate(result, self.first[element])
                    elif element in terminal_symbols:
                        result = self.concatenate(result, [element])

                for element in result:
                    key_value = element if element != EPSILON else '$'
                    if (left, key_value) not in self.parsing_table:
                        self.parsing_table[(left, key_value)] = (right, index + 1)
                    else:
                        raise Exception(f'There is a conflict at row {left} and column {key_value}. \n'
                                        f'The current value is {self.parsing_table[(left, key_value)]}\n')

            elif right[0] == EPSILON:
                follow_values = self.follow[left]
                for value in follow_values:
                    key_value = value if value != EPSILON else '$'
                    if (left, key_value) not in self.parsing_table:
                        self.parsing_table[(left, key_value)] = (right, index + 1)
                    else:
                        raise Exception(f'There is a conflict at row {left} and column {key_value}.\n'
                                        f'The current value is {self.parsing_table[(left, key_value)]}\n')

    def parse_algorithm_start(self, sequence):
        input_stack = copy.deepcopy(sequence) + ['$']
        working_stack = [self.grammar.start_symbol, '$']
        output_stack = [EPSILON]

        output_stack = self.parse_algorithm(input_stack, working_stack, output_stack)
        print(output_stack)
        self.parser_output = ParserOutput(output_stack, self.grammar, 'out.txt')
        print(self.parser_output)

    def parse_algorithm(self, input_stack, working_stack, output_stack):
        first_input = input_stack[0]
        first_working = working_stack[0]
        try:
            table_value = self.parsing_table[(first_working, first_input)]
            if table_value[0] == "pop":
                input_stack = input_stack[1:]
                working_stack = working_stack[1:]
            elif table_value[0] == "acc":
                return output_stack
            else:
                working_stack = working_stack[1:]

                if table_value[0][0] != EPSILON:
                    value = copy.deepcopy(table_value[0])
                    value.extend(working_stack)
                    working_stack = copy.deepcopy(value)

                if len(output_stack) == 1 and output_stack[0] == EPSILON:
                    output_stack = [table_value[1]]
                else:
                    output_stack += [table_value[1]]

        except Exception as error:
            print(f'The sequence has an error! ({first_working, first_input}) key does not exist '
                  f'in the parsing table.')
            return None

        return self.parse_algorithm(input_stack, working_stack, output_stack)
