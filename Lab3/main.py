from lexical_analyzer import LexicalAnalyzer

if __name__ == "__main__":
    lexical_analyzer = LexicalAnalyzer()
    lexical_analyzer.scan('p1.txt')
    lexical_analyzer.print_to_files('p1')
