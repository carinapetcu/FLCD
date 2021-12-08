from grammar import *
from ll1_parser import *
from tests import *

if __name__ == "__main__":
    grammar = Grammar('g3.txt')
    parser = Parser(grammar)
    tests = Tests(parser)
    tests.run()
