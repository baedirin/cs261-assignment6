# Name: Brittaney Nico Davis
# OSU Email: davisbr2@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 12/2/2022  (However I requested 2 extra days, so 12/4/2022)
# Description: A hashmap using opening addressing, with a
#              dynamic array and linked list.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        A function which updates the
        key/value pair in a hash map.
        If a value already exists in the
        hash map, it must be replaced. If a
        key is not present, it must be
        put into the hash map.
        """

        # TODO - comments

        if self.table_load() >= 0.5:
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)

        hash_index = self._hash_function(key) % self.get_capacity()
        counter = 0

        while self._buckets[hash_index]:
            if self._buckets[hash_index].key == key or \
                    self._buckets[hash_index].is_tombstone is True:
                break
            counter += 1
            index = hash_index
            hash_index = (index + (counter * counter)) % self.get_capacity()

        if self._buckets[hash_index] is None:
            self._buckets[hash_index] = HashEntry(key, value)
            self._size += 1

        elif self._buckets[hash_index] is not None:
            if self._buckets[hash_index].key == key:
                self._buckets[hash_index].value = value
            if self._buckets[hash_index].is_tombstone is True:
                self._buckets[hash_index] = HashEntry(key, value)

        # hash_func = self._hash_function(key)
        # empty = False
        # counter = 0
        #
        # while not empty:
        #     quadratic_probe = ((hash_func + (counter * counter)) % self.get_capacity())
        #     if self._buckets.get_at_index(quadratic_probe) is None:
        #         empty = True
        #         self._buckets.set_at_index(quadratic_probe, (HashEntry(key, value)))
        #         self._size += 1
        #     elif self._buckets.get_at_index(quadratic_probe).key == key:
        #         empty = True
        #         tombstone = self._buckets.get_at_index(quadratic_probe).is_tombstone
        #         if tombstone is True:
        #             self._size += 1
        #
        #         self._buckets.set_at_index(quadratic_probe, (HashEntry(key, value)))
        #
        #     counter += 1

    def table_load(self) -> float:
        """
        A function that returns the
        hash table load factor.
        """

        # Return the size divided by the capacity for the load factor.

        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        A function that returns the
        number of empty buckets in the
        hash table.
        """

        # TODO - comments

        empty_count = 0
        hash_capacity = self._capacity

        for index in range(hash_capacity):
            if self._buckets.get_at_index(index) is None or \
                    self._buckets[index].is_tombstone is True:
                empty_count += 1
        return empty_count

    def resize_table(self, new_capacity: int) -> None:
        """
        A function that changes the
        internal capacity of the hash table.
        All key/value pairs must remain in
        the new hash map and the links must
        be rehashed.
        """

        # TODO - comments

        if new_capacity < self._size:
            return

        prime_capacity = self._is_prime(new_capacity)
        next_prime = self._next_prime(new_capacity)

        if prime_capacity is not True:
            new_capacity = next_prime

        self._capacity = new_capacity
        buckets = self._buckets
        self._buckets = DynamicArray()
        self._size = 0

        for index in range(new_capacity):
            self._buckets.append(None)

        for index in range(buckets.length()):
            element = buckets.get_at_index(index)
            if element is not None:
                self.put(element.key, element.value)

    def get(self, key: str) -> object:
        """
        A function that returns the value
        of the key passed. If the key is
        not present in the hash map, it
        returns None.
        """

        # TODO - comments

        # This method returns the value associated with the given key. If the key is not in the hash
        # map, the method returns None.

        hash_function = self._hash_function(key)
        hash_index = hash_function % self._capacity

        if not self.contains_key(key):
            return None

        if self._buckets[hash_index].is_tombstone is True:
            return None
        elif self._buckets[hash_index].is_tombstone is False and \
                self._buckets[hash_index] is not None:
            return self._buckets.get_at_index(hash_index)

    def contains_key(self, key: str) -> bool:
        """
        A function that returns True if
        a passed key is present in the
        hash map. Otherwise, it returns
        False. If the hash map is empty.
        it returns no keys.
        """

        # TODO - comments

        # This method returns True if the given key is in the hash map, otherwise it returns False. An
        # empty hash map does not contain any keys.

        capacity = self._capacity

        if self._capacity == 0:
            return False

        for index in range(capacity):
            hash_function = self._hash_function(key)
            hash_index = hash_function % self._capacity
            if self._buckets.get_at_index(hash_index) == key and\
                    self._buckets[hash_index].is_tombstone is False:
                return True
            else:
                return False

    def remove(self, key: str) -> None:
        """
        A function that removes the key
        passed, plus the value associated
        with that key. If the key passed
        is not present in the hash map,
        the function does nothing.
        """

        # TODO - comments

        hash_function = self._hash_function(key)
        hash_index = hash_function % self._capacity

        if not self.contains_key(key):
            return None

        if self._buckets.get_at_index(hash_index) == key:
            if self._buckets[hash_index].is_tombstone is True:
                return None
            if self._buckets[hash_index].is_tombstone is False:
                self._buckets.set_at_index(hash_index, None)
                self._buckets[hash_index].is_tombstone = True
                self._size -= 1

    def clear(self) -> None:
        """
        A function that clears the
        contents of the underlying
        hash map, without changing the
        underlying capacity.
        """

        # TODO - comments

        da = DynamicArray()
        capacity = da.length()

        for i in range(0, capacity):
            self._buckets.set_at_index(i, da)
            self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        A function that returns a
        dynamic array where each element
        contains a tuple containing a
        key/value pair. Order does not
        matter.
        """

        # TODO - comments

        # This method returns a dynamic array where each index contains a tuple of a key/value pair
        # stored in the hash map. The order of the keys in the dynamic array does not matter.

        da = DynamicArray()

        for i in range(self._buckets.length()):
            bucket = self._buckets[i]
            if bucket is not None and bucket.is_tombstone is False:
                da.append((bucket.key, bucket.value))
        return da

    def __iter__(self):
        """
        A function that allows the hash
        map to iterate across itself.
        """

        # TODO - comments

        # This method enables the hash map to iterate across itself. Implement this method in a
        # similar way to the example in the Exploration: Encapsulation and Iterators.
        # You ARE permitted (and will need to) initialize a variable to track the iterator’s progress
        # through the hash map’s contents.
        # You can use either of the two models demonstrated in the Exploration - you can build the
        # iterator functionality inside the HashMap class, or you can create a separate iterator class.

        pass

    def __next__(self):
        """
        A function that returns the next
        item in the hash map, based upon
        the current location of the iterator.
        """

        # TODO - comments

        # This method will return the next item in the hash map, based on the current location of the
        # iterator. Implement this method in a similar way to the example in the Exploration:
        # Encapsulation and Iterators. It will need to only iterate over active items.

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

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
