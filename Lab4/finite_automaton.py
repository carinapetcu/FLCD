class FiniteAutomaton:
    def __init__(self, file_name):
        self.states = list()
        self.alphabet = list()
        self.transitions = dict()
        self.initial_state = None
        self.final_states = list()
        self.neighbours = dict(list())
        self.read_from_file(file_name)

    def read_from_file(self, file_name):
        file = open(file_name, "r")
        lines = file.readlines()

        self.states = lines[0].strip().split(',')

        for state in self.states:
            self.neighbours[state] = []

        self.alphabet = lines[1].strip().split(',')

        self.initial_state = lines[2].strip()

        self.final_states = lines[3].strip().split(',')

        for index in range(4, len(lines)):
            elements = lines[index].strip().split(',')
            first = elements[0]
            second = elements[1]
            values = elements[2:]
            self.neighbours[first].append(second)
            self.transitions[(first, second)] = values

        file.close()

    def check_if_sequence_accepted(self, sequence, current_state):
        if len(sequence) == 0:
            return current_state in self.final_states

        for neighbor in self.neighbours[current_state]:
            values = self.transitions[(current_state, neighbor)]
            if sequence[0] in values:
                if self.check_if_sequence_accepted(sequence[1:], neighbor):
                    return True

        return False

    def check_sequence(self, sequence):
        return self.check_if_sequence_accepted(sequence, self.initial_state)

    def print_menu(self):
        print('Please choose an option: \n'
              '\t1. show states\n'
              '\t2. show alphabet\n'
              '\t3. show transitions\n'
              '\t4. show initial state\n'
              '\t5. show final states\n'
              '\t6. check if sequence is accepted\n'
              '\tx. quit\n')

    def menu(self):
        isDone = False
        print('Hello!\n')
        while not isDone:
            self.print_menu()
            option = input('Your choice is: ')
            if option == '1':
                print('The states are: ' + str(self.states))
            elif option == '2':
                print('The alphabet is: ' + str(self.alphabet))
            elif option == '3':
                print('The transitions are: ' + str(self.transitions))
            elif option == '4':
                print('The initial state is: ' + str(self.initial_state))
            elif option == '5':
                print('The final states are: ' + str(self.final_states))
            elif option == '6':
                sequence = input('The sequence to be checked: ')
                isAccepted = self.check_sequence(sequence)
                action = ' is ' if isAccepted else ' is not '
                result = 'The sequence ' + sequence + action + 'accepted by the current FA\n'
                print(result)

            elif option == 'x':
                print('Goodbye!')
                isDone = True
            else:
                print('Wrong option! Please try again!')


if __name__ == '__main__':
    fa = FiniteAutomaton('fa_integer_constants.in')
    fa.menu()

