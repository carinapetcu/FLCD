class Tests:
    def __init__(self, parser):
        self.parser = parser

    def test_concatenateWithoutEpsilon_expectedResult(self):
        first = ['a', 'b']
        second = ['c', 'b']
        expected_result = ['a', 'b']
        actual_result = self.parser.concatenate(first, second)

        assert (set(expected_result).issubset(actual_result) and set(actual_result).issubset(expected_result))

    def test_concatenateWithEpsilonInFirst_expectedResult(self):
        first = ['a', 'epsilon']
        second = ['c', 'b']
        expected_result = ['a', 'b', 'c']
        actual_result = self.parser.concatenate(first, second)

        assert (set(expected_result).issubset(actual_result) and set(actual_result).issubset(expected_result))

    def test_concatenateWithEpsilonInSecond_expectedResult(self):
        first = ['a', 'b']
        second = ['c', 'epsilon']
        expected_result = ['a', 'b']
        actual_result = self.parser.concatenate(first, second)

        assert (set(expected_result).issubset(actual_result) and set(actual_result).issubset(expected_result))

    def test_initializeFirst_expectedResult(self):
        expected_result = {
            'S': [],
            'A': ['+', 'epsilon'],
            'B': [],
            'C': ['*', 'epsilon'],
            'D': ['(', 'a']
        }

        self.parser.initialize_first()
        actual_result = self.parser.first

        assert (self.parser.compare_dictionaries(expected_result, actual_result))

    def test_firstFunction_expectedResult(self):
        expected_result = {
            'S': ['(', 'a'],
            'A': ['+', 'epsilon'],
            'B': ['(', 'a'],
            'C': ['*', 'epsilon'],
            'D': ['(', 'a']
        }

        self.parser.first_function()
        actual_result = self.parser.first

        assert (self.parser.compare_dictionaries(expected_result, actual_result))

    def test_initializeFollow_expectedResult(self):
        expected_result = {
            'S': ['epsilon'],
            'A': [],
            'B': [],
            'C': [],
            'D': []
        }

        self.parser.initialize_follow()
        actual_result = self.parser.follow
        assert (self.parser.compare_dictionaries(expected_result, actual_result))

    def test_followFunction_expectedResult(self):
        expected_result = {
            'S': [')', 'epsilon'],
            'A': [')', 'epsilon'],
            'B': ['+', ')', 'epsilon'],
            'C': ['+', ')', 'epsilon'],
            'D': ['*', '+', ')', 'epsilon']
        }

        self.parser.follow_function()
        actual_result = self.parser.follow

        assert (self.parser.compare_dictionaries(expected_result, actual_result))

    def run(self):
        self.test_concatenateWithoutEpsilon_expectedResult()
        self.test_concatenateWithEpsilonInFirst_expectedResult()
        self.test_concatenateWithEpsilonInSecond_expectedResult()
        self.test_initializeFirst_expectedResult()
        self.test_firstFunction_expectedResult()
        self.test_initializeFollow_expectedResult()
        self.test_followFunction_expectedResult()
