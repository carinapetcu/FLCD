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
            print(self.hash_table)

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


if __name__ == "__main__":
    st = SymbolTable(5)
    st.add_element('mere')
    print(st.add_element('mere'))
    st.add_element('3')
    print(st.add_element('3'))
