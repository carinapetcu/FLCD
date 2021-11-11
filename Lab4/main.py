from lexical_analyzer import LexicalAnalyzer

if __name__ == "__main__":
    lexical_analyzer = LexicalAnalyzer()
    fileName = 'p1'
    lexical_analyzer.scan(fileName + '.txt')
    lexical_analyzer.print_to_files(fileName)
