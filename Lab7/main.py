from tests import *


def get_sequence(file_name):
    file = open(file_name, "r")
    lines = file.readlines()
    sequence = []

    for line in lines:
        elements = line.split("|")
        if elements[0] != 'Token':
            sequence.append(elements[0].strip())

    return sequence


if __name__ == "__main__":
    file_name = 'g3.txt'
    grammar = Grammar(file_name)
    parser = Parser(grammar)
    tests = Tests()
    tests.run()
    if file_name == 'g3.txt':
        parser.parse_algorithm_start(get_sequence('seq.txt'), 'out3.txt')
    elif file_name == 'g2.txt':
        parser.parse_algorithm_start(get_sequence('pif.txt'), 'out2.txt')
