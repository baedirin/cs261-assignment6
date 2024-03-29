# Name: Brittaney Nico Davis
# OSU Email: davisbr2@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 12/2/2022
# Description: A hashmap using chaining, with a HashMap class
#              that interacts with a dynamic array and linked
#              list class, as well as an SLNode class. Several
#              methods interact with one another to build the
#              hash map, using chaining to handle collisions.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        A function which updates a key/value
        pair in the hash table. When the key passed
        already exists in the hashmap, the
        associated value is replaced with the
        new value passed. If the key is not
        present in the hash table, it must be added.
        """

        # Begin by making a check if the table load is greater than
        # or equal to 1. If yes, set the new capacity to twice the
        # size, then resize the hash table according to the new capacity.
        if self.table_load() >= 1:
            new_capacity = self.get_capacity() * 2
            self.resize_table(new_capacity)

        # Create a function for hashing, utilizing the hash function
        # and the passed key. Then, use this function modulo the
        # capacity to create a hash index.
        hash_function = self._hash_function(key)
        hash_index = hash_function % self.get_capacity()

        # Then, make a check to see if the passed key at the hash index is not None.
        # In such a case, we must replace the value by removing the old key, and then
        # inserting the new key and value. Then, decrement the size.
        if self._buckets.get_at_index(hash_index).contains(key) is not None:
            self._buckets.get_at_index(hash_index).remove(key)
            self._buckets.get_at_index(hash_index).insert(key, value)

            self._size = self._size - 1

        # Otherwise, if the passed key at the hash index is None, we simply
        # insert the key and value, without any removal. Increment the size.
        elif self._buckets.get_at_index(hash_index).contains(key) is None:
            self._buckets.get_at_index(hash_index).insert(key, value)

        self._size = self._size + 1

    def empty_buckets(self) -> int:
        """
        A function which returns the number
        of empty buckets in the hash table.
        """

        # Begin by creating a counter for the empty buckets,
        # and a variable for the capacity.
        empty_count = 0
        hash_table_capacity = self.get_capacity()

        # Then, loop through the capacity, checking if the length at
        # each index is 0. If yes, increment the counter. Then, return
        # the counter.
        for i in range(hash_table_capacity):
            if self._buckets.get_at_index(i).length() == 0:
                empty_count += 1

        return empty_count

    def table_load(self) -> float:
        """
        A function which returns the
        hash table load factor.
        """

        # Return the size divided by the capacity for the load factor.

        return self.get_size() / self.get_capacity()

    def clear(self) -> None:
        """
        A function that clears all contents
        in the hash table without
        modifying the underlying hash
        table capacity.
        """

        # Begin by creating linked list and hash table capacity variables.
        ll = LinkedList()
        hash_table_capacity = self.get_capacity()

        # Then, loop through the hash table capacity, setting the index
        # i with the value of the linked list. Set the size to 0 to fully
        # clear the hash table.
        for i in range(hash_table_capacity):
            self._buckets.set_at_index(i, ll)
            self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        A function that alters the capacity
        of the hash table. The key/value
        pairs and links within must be
        maintained via rehashing. Capacity
        must be adjusted depending upon
        whether it is greater than or equal
        to one. If less than 1, nothing
        occurs.
        """

        # Begin by making a check to see if the new capacity
        # passed is less than 1. If yes, return, as this is an
        # invalid capacity to resize.
        if new_capacity < 1:
            return

        # Create variables for a linked list and dynamic array to use.
        ll = LinkedList()
        da = DynamicArray()

        # Make a check if the new capacity is not prime - if it
        # is not, then set the new capacity to the next prime of
        # new capacity.
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Looping through the length of the new capacity, append
        # the linked list to the dynamic array.
        for i in range(new_capacity):
            da.append(LinkedList())

        # Then, loop through the capacity, creating a node to add
        # for each bucket at index of buckets. If the bucket is
        # not None, insert this node into the linked list.
        for bucket in range(self.get_capacity()):
            node_to_add = self._buckets.get_at_index(bucket)
            if node_to_add is not None:
                for node in node_to_add:
                    ll.insert(node.key, node.value)

        # Set size to 0, buckets to da, and capacity to new capacity. Then,
        # put each key and value into each node of the linked list.
        self._size = 0
        self._buckets = da
        self._capacity = new_capacity

        for node in ll:
            self.put(node.key, node.value)

    def get(self, key: str):
        """
        A function that returns the value
        associated with the passed key. If
        that value is not in the hash table,
        the function returns None.
        """

        # Create a function for hashing, utilizing the hash function
        # and the passed key. Then, use this function modulo the
        # capacity to create a hash index.
        hash_function = self._hash_function(key)
        hash_index = hash_function % self.get_capacity()

        # Make a check to see that the key exists. If not,
        # return None, as the key is not in the hash table.
        if not self.contains_key(key):
            return None

        # Otherwise, return the value of the key passed, utilizing the hash
        # index.
        else:
            return self._buckets.get_at_index(hash_index).contains(key).value

    def contains_key(self, key: str) -> bool:
        """
        A function that returns True or False,
        depending upon whether the passed
        key is in the hash table. An empty
        hash table will not contain any keys.
        """

        # Create a function for hashing, utilizing the hash function
        # and the passed key. Then, use this function modulo the
        # capacity to create a hash index.
        hash_function = self._hash_function(key)
        hash_index = hash_function % self.get_capacity()

        # Make a check to see if the capacity is 0. If yes,
        # return False, as no keys are in the hash table.
        if self.get_capacity() == 0:
            return False

        # Otherwise, if the passed key is at the hash index, return True.
        # Otherwise, return False.
        if self._buckets.get_at_index(hash_index).contains(key):
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        A function which removes the passed
        key from the hash table as well as the
        associated value. If the key does not
        exist in the hash table, nothing occurs.
        """

        # Create a function for hashing, utilizing the hash function
        # and the passed key. Then, use this function modulo the
        # capacity to create a hash index.
        hash_function = self._hash_function(key)
        hash_index = hash_function % self.get_capacity()

        # Make a check to see if the key is within the hash
        # table to remove. If no, then return.
        if not self.contains_key(key):
            return
        # In the case that the passed key is at the hash index,
        # remove that key and decrease the size by 1.
        if self._buckets.get_at_index(hash_index).contains(key):
            self._buckets.get_at_index(hash_index).remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        A function that returns a dynamic array
        in which each index contains a tuple
        of key/value pairs within the hash
        table. Order does not matter.
        """

        # Create a new dynamic array to append to and return.
        da = DynamicArray()

        # Then, looping through the length of the buckets,
        # set a variable buckets to the index of each. Looping again
        # through the buckets, append each key and corresponding value to
        # the dynamic array, which will be returned.
        for i in range(self._buckets.length()):
            buckets = self._buckets[i]
            for j in buckets:
                da.append((j.key, j.value))
        return da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    A function that tracks multiple modes
    within a hash map. The function will
    track multiple modes via their values,
    and return a tuple an array populated
    with those modes, as well as the
    frequency of the modes. This function
    must use O(N) runtime complexity.
    """

    # This code was written referencing my find_mode from assignment 2.

    # First, create variables for the highest frequency, a new dynamic array
    # to populate with modes and return, and a hash map with the input array
    # passed.
    highest_frequency = 0
    return_da = DynamicArray()
    map = HashMap(da.length())

    # Then, looping through the length of the input dynamic array, create a key
    # and value based upon the dynamic array. If the value exists, place the key
    # and value plus 1 into the map. This map will serve as a "clip board" to track
    # the occurrences plus frequency.
    for index in range(da.length()):

        key = da.get_at_index(index)
        value = map.get(key)

        if value:
            value += 1
            map.put(key, value)
    # Otherwise, set the value to 1 and place the key and value into the map.
        else:
            value = 1
            map.put(key, value)

    # Now, make comparisons to append to the dynamic array to be returned. If the
    # value is greater than the highest frequency, reset the highest frequency to the
    # value, as I did in assignment 2 find_mode. Create the dynamic array and append the
    # key to it. If the value is equal to the highest frequency, simply append the key
    # to the return dynamic array.
        if value > highest_frequency:
            highest_frequency = value
            return_da = DynamicArray()
            return_da.append(key)
        elif value == highest_frequency:
            return_da.append(key)

    return return_da, highest_frequency


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
