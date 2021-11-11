from finite_automaton import FiniteAutomaton
from symbol_table import SymbolTable
import re


class LexicalAnalyzer:
    def __init__(self):
        self.operators = ["+", "-", "*", "/", "%", "=", "==", "<", "<=", ">=", ">", "<>", "&&", "||", "!", ">>", "<<"]
        self.separators = [":", ";", " ", "\n", "\t", "[", "]", "{", "}"]
        self.reserved_words = ["if", "else", "int", "char", "bool", "while", "@"]
        self.double_defined_token = {
            "<": ["=", ">", "<"],
            ">": ["=", ">"],
            "&": ["&"],
            "|": ["|"],
            "\\": ["n", "t"],
            "=": ["="]
        }
        self.symbol_table_identifiers = SymbolTable(37)
        self.symbol_table_constant = SymbolTable(37)
        self.pif = []
        self.outcome = ""
        self.fa_identifiers = FiniteAutomaton('fa_identifiers.in')
        self.fa_integer_constants = FiniteAutomaton('fa_integer_constants.in')

    def is_of_constant_or_identifier(self, character):
        return re.search("[a-zA-Z0-9+-]", character)

    # def check_identifier(self, token):
    #     return re.search("^[a-zA-Z][a-zA-Z0-9]*$", token)

    def check_character(self, token):
        return re.search("^'[a-zA-Z0-9]'$", token)

    def check_string(self, token):
        return re.search("^\"[a-zA-Z0-9 ]*\"$", token)

    # def check_integer(self, token):
    #     return re.search("^([+-]?[1-9][0-9]*)|0$", token)

    def check_boolean(self, token):
        return re.search("[01]", token)

    def check_constant(self, token):
        return self.check_character(token) \
               or self.check_string(token) \
               or self.fa_integer_constants.check_sequence(token) \
               or self.check_boolean(token)

    def get_line_components(self, line):
        # initially I will try to add spaces in the string such that the default tokens
        # are different from the non default ones
        new_line = []
        # this will be used to mark where in the line we had a space, as they will be missed after altering the line
        spaces = []
        index = 0
        while index < len(line):
            if self.is_of_constant_or_identifier(line[index]):
                # we have some special cases for "-" and "+" since they can also be used for integers
                if line[index] == "-" or line[index] == "+":
                    if index != len(line) - 1 and line[index] != " ":
                        new_line.append(line[index])
                    else:
                        new_line.append(" ")
                        new_line.append(line[index])
                        new_line.append(" ")
                else:
                    new_line.append(line[index])
            else:
                if line[index] == " ":
                    spaces.append(index)
                new_line.append(" ")
                new_line.append(line[index])
                new_line.append(" ")
            index += 1

        new_line_string = "".join(new_line)
        new_line_components = new_line_string.split()
        return spaces, new_line_components

    def get_tokens(self, new_line_components):
        new_line_tokens = []
        # try to solve the issue with the defined tokens with length 2
        while len(new_line_components) > 0:
            current_token = new_line_components[0]
            if current_token in self.double_defined_token:
                values = self.double_defined_token[current_token]
                if len(new_line_components) > 1 and new_line_components[1] in values:
                    combined_token = current_token + new_line_components[1]
                    new_line_tokens.append(combined_token)
                    new_line_components.pop(0)
                else:
                    new_line_tokens.append(current_token)
            else:
                new_line_tokens.append(current_token)
            new_line_components.pop(0)
        return new_line_tokens

    def get_tokens_with_string(self, tokens, separator):
        new_token_array = []
        current_string = ""
        for token in tokens:
            if token == separator:
                if len(current_string) == 0:
                    current_string += separator
                else:
                    current_string = current_string[:-1]
                    current_string += separator
                    new_token_array.append(current_string)
                    current_string = ""
            else:
                if len(current_string) == 0:
                    new_token_array.append(token)
                else:
                    current_string += token + " "
        return new_token_array

    def scan(self, fileName):
        file = open(fileName, "r")
        noOfLines = 0
        for line in file:
            noOfLines += 1
            spaces, new_line_components = self.get_line_components(line)
            new_line_tokens = self.get_tokens(new_line_components)
            new_line_tokens = self.get_tokens_with_string(new_line_tokens, "\"")
            new_line_tokens = self.get_tokens_with_string(new_line_tokens, "\'")

            current_index = 0
            while len(spaces) != 0 and len(new_line_tokens) != 0:
                component_index = line.find(new_line_tokens[0])
                current_token = new_line_tokens[0]
                # now we check the indices and we take into account the smallest one
                if spaces[0] < component_index:
                    # we had a space, we will add the space to the pif
                    self.pif.append([" ", 0])
                    # we will remove the space from the list of spaces and we will increment the current index
                    spaces.pop(0)
                    current_index += 1
                else:
                    # we will check if the current character reserve word, operator or constant
                    if current_token in self.operators or current_token in self.separators \
                            or current_token in self.reserved_words:
                        self.pif.append([current_token, 0])
                        current_index += len(current_token)
                    elif self.fa_identifiers.check_sequence(current_token):
                        position = self.symbol_table_identifiers.add_element(current_token)
                        self.pif.append([current_token, position])
                        current_index += len(current_token)
                    elif self.check_constant(current_token):
                        position = self.symbol_table_constant.add_element(current_token)
                        self.pif.append([current_token, position])
                        current_index += len(current_token)
                    else:
                        self.outcome += "Lexical error on line " + str(noOfLines) + ", column " + str(current_index) + \
                                        ". Token not defined: " + current_token + "\n"
                    new_line_tokens.pop(0)

            while len(spaces) != 0:
                self.pif.append([" ", 0])
                spaces.pop(0)
                current_index += 1

            while len(new_line_tokens) != 0:
                current_token = new_line_tokens[0]
                if current_token in self.operators or current_token in self.separators \
                        or current_token in self.reserved_words:
                    self.pif.append([current_token, 0])
                elif self.fa_identifiers.check_sequence(current_token):
                    position = self.symbol_table_identifiers.add_element(current_token)
                    self.pif.append([current_token, position])
                    current_index += len(current_token)
                elif self.check_constant(current_token):
                    position = self.symbol_table_constant.add_element(current_token)
                    self.pif.append([current_token, position])
                    current_index += len(current_token)
                else:
                    self.outcome += "Lexical error on line " + str(noOfLines) + ", column " + str(current_index) + \
                                    ". Token not defined: " + current_token + "\n"
                new_line_tokens.pop(0)

        if len(self.outcome) == 0:
            self.outcome += "Lexically correct."
        print(self.outcome)

    def print_to_files(self, fileName):
        pif_file = open("PIF_" + fileName + ".out", "w")
        pif_file.write("Token | Position\n")
        for element in self.pif:
            pif_file.write(element[0] + " | " + str(element[1]) + "\n")
        pif_file.close()

        constants_file = open("ST_constants_" + fileName + ".out", "w")
        constants_file.write(str(self.symbol_table_constant))
        constants_file.close()

        identifiers_file = open("ST_identifiers_" + fileName + ".out", "w")
        identifiers_file.write(str(self.symbol_table_identifiers))
        identifiers_file.close()
