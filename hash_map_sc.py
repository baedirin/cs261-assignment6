# Name: Brittaney Nico Davis
# OSU Email: davisbr2@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 12/2/2022 (However I requested 2 extra days, so 12/4/2022)
# Description: A hashmap using chaining, with a dynamic array
#              and linked list.


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

        # TODO - comments, fix

        if self.table_load() >= 1:
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)

        hash_function = self._hash_function(key)
        hash_index = hash_function % self.get_capacity()

        if self._buckets.get_at_index(hash_index).contains(key) is not None:
            self._buckets.get_at_index(hash_index).remove(key)
            self._buckets.get_at_index(hash_index).insert(key, value)

            self._size = self._size - 1

        elif self._buckets.get_at_index(hash_index).contains(key) is None:
            self._buckets.get_at_index(hash_index).insert(key, value)

        self._size = self._size + 1

    def empty_buckets(self) -> int:
        """
        A function which returns the number
        of empty buckets in the hash table.
        """

        # TODO - comments, fix

        empty_count = 0
        hash_capacity = self._capacity

        for i in range(hash_capacity):
            if self._buckets.get_at_index(i).length() == 0:
                empty_count += 1

        return empty_count

    def table_load(self) -> float:
        """
        A function which returns the
        hash table load factor.
        """

        # Return the size divided by the capacity for the load factor.

        return self._size / self._capacity

    def clear(self) -> None:
        """
        A function that clears all contents
        in the hash table without
        modifying the underlying hash
        table capacity.
        """

        # TODO - comments, fix

        ll = LinkedList()
        capacity = self._capacity

        for i in range(0, capacity):
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

        # TODO - comments, fix

        ll = LinkedList()
        da = DynamicArray()

        if new_capacity < 1:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        for i in range(new_capacity):
            da.append(LinkedList())

        for j in range(self._capacity):
            node = self._buckets.get_at_index(j)

            if self._buckets.get_at_index(j) is None:
                continue
            elif self._buckets.get_at_index(j) is not None:
                for k in node:
                    ll.insert(k.key, k.value)

        self._capacity = new_capacity
        self._buckets = da
        self._size = 0

        for q in ll:
            self.put(q.key, q.value)

    def get(self, key: str):
        """
        A function that returns the value
        associated with the passed key. If
        that value is not in the hash table,
        the function returns None.
        """

        # TODO - comments, fix

        hash_function = self._hash_function(key)
        hash_index = hash_function % self._capacity

        if not self.contains_key(key):
            return None

        else:
            return self._buckets.get_at_index(hash_index).contains(key).value

    def contains_key(self, key: str) -> bool:
        """
        A function that returns True or False,
        depending upon whether the passed
        key is in the hash table. An empty
        hash table will not contain any keys.
        """

        # TODO - comments, fix

        hash_function = self._hash_function(key)
        hash_index = hash_function % self._capacity

        if self._capacity == 0:
            return False

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

        # TODO - comments, fix

        hash_function = self._hash_function(key)
        hash_index = hash_function % self._capacity

        if not self.contains_key(key):
            return

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

        # TODO - comments, fix

        da = DynamicArray()

        for i in range(self._buckets.length()):
            buckets = self._buckets[i]
            for j in buckets:
                da.append((j.key, j.value))
        return da

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    TODO: Write this implementation
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    # TODO - comments, write function

    # Write a standalone function outside the HashMap class that receives a dynamic array
    # (that is not guaranteed to be sorted). This function will return a tuple containing, in this
    # order, a dynamic array comprising the mode (most occurring) value/s of the array, and an
    # integer that represents the highest frequency (how many times they appear).
    # If there is more than one value with the highest frequency, all values at that frequency
    # should be included in the array being returned (the order does not matter). If there is only
    # one mode, the dynamic array will only contain that value.
    # You may assume that the input array will contain at least one element, and that all values
    # stored in the array will be strings. You do not need to write checks for these conditions.
    # For full credit, the function must be implemented with O(N) time complexity. For best
    # results, we recommend using the separate chaining hash map provided for you in the
    # function’s skeleton code.

    pass


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
