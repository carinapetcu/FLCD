from collections import deque


class SymbolTable:
    def __init__(self, number_buckets):
        self.number_buckets = number_buckets
        self.position = 0
        # the hash table is represented as a list of deques, such that the complexity is O(1)
        self.hash_table = list(deque() for _ in range(self.number_buckets))

    def add_element(self, element):
        # we search for the element in hash table
        # if it exists, we return the position
        found_element_position = self.search_element(element)
        if found_element_position != -1:
            return found_element_position
        else:
            # if the element does not exist, then we add it in the symbol table, taking into account the has value
            hash_value = self.hash(element)
            self.hash_table[hash_value].append((element, self.position))
            self.position += 1
            return self.position - 1

    def search_element(self, element):
        # we will search the element coresponding to the hash value
        hash_value = self.hash(element)
        for index in range(len(self.hash_table[hash_value])):
            hash_table_value = self.hash_table[hash_value][index]
            if hash_table_value[0] == element:
                return hash_table_value[1]
        return -1

    def hash(self, element):
        ascii_sum = 0
        for character in element:
            ascii_sum += ord(character)
        return ascii_sum % self.number_buckets

    def __str__(self):
        required_string = "The symbol table was represented using a hash table, " + \
                          "where each bucket was represented as a deque. The number of buckets is " + \
                          str(self.number_buckets) + ". The has function is calculated by summing up the ascii codes " \
                          + "of the characters and the number of buckets (it is the modulo between these 2 values).\n\n"

        elements = ["" for _ in range(0, self.position)]
        # I will iterate through the hash table and then add the corresponding positions to the array
        for bucket in self.hash_table:
            for element in bucket:
                elements[element[1]] = element[0]

        required_string += "Token | position\n"
        for index in range(0, self.position):
            element = elements[index]
            required_string += element + " | " + str(index) + "\n"

        return required_string
