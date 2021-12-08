import copy

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