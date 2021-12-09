class ParserOutput:
    def __init__(self, sequence, grammar, file_name):
        self.sequence = sequence
        self.grammar = grammar
        self.file_name = file_name
        self.info = [self.grammar.start_symbol]
        self.parent = [0]
        self.left_sibling = [0]
        self.create_tree()
        self.write_to_file()

    def create_tree(self):
        productions_numbered = self.grammar.productions_with_numbers

        for production_number in self.sequence:
            left = productions_numbered[production_number - 1][0]
            right = productions_numbered[production_number - 1][1]

            # the parent should be the last unused left symbol
            current_parent_index = self.search_parent(left) + 1

            for _ in range(len(right)):
                self.parent.append(current_parent_index)

            self.info.append(right[0])
            self.left_sibling.append(0)
            for index in range(1, len(right)):
                self.info.append(right[index])
                self.left_sibling.append(len(self.info) - 1)

    def search_parent(self, parent):
        for index in range(len(self.info) - 1, -1, -1):
            if self.info[index] == parent and (index + 1) not in self.parent:
                return index

    def write_to_file(self):
        file = open(self.file_name, "w")
        file.write(str(self))
        file.close()

    def __str__(self):
        s = 'Index | Info | Parent | Left sibling\n'

        for index in range(len(self.info)):
            s += f'{index + 1} | {self.info[index]} | {self.parent[index]} | {self.left_sibling[index]}\n'

        return s
