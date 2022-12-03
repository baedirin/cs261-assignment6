# Name: Brittaney Nico Davis
# OSU Email: davisbr2@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 12/2/2022
# Description: A hashmap that includes a HashMap class
#              which interacts with a dynamic array and linked
#              list class, as well as an SLNode class. Several
#              methods interact with one another to build the
#              hash map, using open addressing to handle collisions.

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

        # Set a probe counter to track the count for the quadratic probe function,
        # plus a while loop variable and the hash function with the passed
        # key to use in the quadratic probing function.
        empty = 0
        probe_counter = 0
        hash_func = self._hash_function(key)

        # Begin by making a check if the table load is greater than
        # or equal to 0.5. If yes, set the new capacity to twice the
        # size, then resize the hash table according to the new capacity.
        if self.table_load() >= 0.5:
            new_capacity = self.get_capacity() * 2
            self.resize_table(new_capacity)

        # While empty is 0, set the quadratic probe function using the hash function, probe counter and capacity.
        # Create a bucket available variable for quadratic probe index, and a placement variable for the hash entry.
        while empty == 0:

            quadratic_probe = ((hash_func + (probe_counter * probe_counter)) % self.get_capacity())
            bucket_available = self._buckets.get_at_index(quadratic_probe)
            placement = (HashEntry(key, value))

            # If the bucket at the index of the quadratic probe is None, we can put the
            # key and value into the hash map and increase the size by 1.
            if bucket_available is None:
                empty = 1
                self._buckets.set_at_index(quadratic_probe, placement)
                self._size = self._size + 1

            # If the bucket at the index of the quadratic probe matches the key, then
            # we must make an additional check that the space is a Tombstone value. If
            # yes, increment the size by 1. Then put the key and value into the hash map.
            if key == self._buckets.get_at_index(quadratic_probe).key:
                empty = 1
                if self._buckets.get_at_index(quadratic_probe).is_tombstone is True:
                    self._size = self._size + 1
                self._buckets.set_at_index(quadratic_probe, placement)

            # Increment the probe counter to keep the quadratic probe formula accurate.
            probe_counter += 1

    def table_load(self) -> float:
        """
        A function that returns the
        hash table load factor.
        """

        # Return the size divided by the capacity for the load factor.
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        A function that returns the
        number of empty buckets in the
        hash table.
        """

        # Set a counter for the empty buckets and the capacity to loop through.
        empty_count = 0
        hash_capacity = self.get_capacity()

        # Looping through the capacity, make a check if the index
        # is none or the Tombstone value is True. If yes, increment
        # the empty counter.
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

        # Make a check to see if the new capacity is less than the size.
        # If yes, return.
        if new_capacity < self.get_size():
            return

        # Make a check if the new capacity is not prime - if it
        # is not, then set the new capacity to the next prime of
        # new capacity.
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Set the size to 0, the capacity to the new capacity,
        # buckets to the buckets of the DA, and reset the dynamic array.
        self._size = 0
        self._capacity = new_capacity
        buckets = self._buckets
        self._buckets = DynamicArray()

        # Looping through the new capacity, append None to the buckets, as
        # is shown in the HashMap class.
        for i in range(new_capacity):
            self._buckets.append(None)

        # Then, loop through the length of buckets, creating an element
        # for each index. Then, if that element is not None, and it is not
        # a Tombstone value, put that element into the dynamic array.
        for j in range(buckets.length()):
            element = buckets.get_at_index(j)
            if element:
                if buckets[j].is_tombstone is False:
                    self.put(element.key, element.value)

    def get(self, key: str) -> object:
        """
        A function that returns the value
        of the key passed. If the key is
        not present in the hash map, it
        returns None.
        """

        # Make a check to see if the key is within the dynamic array. If not,
        # return None, as it cannot be obtained.
        if not self.contains_key(key):
            return None

        # Make an additional check to see if the size is less than 1. If yes,
        # return, as there is no key in the hash map to remove.
        if self._buckets.length() < 1:
            return None

        # Set a probe counter to track the count for the quadratic probe function,
        # plus a while loop variable and the hash function with the passed
        # key to use in the quadratic probing function.
        empty = 0
        probe_counter = 0
        hash_func = self._hash_function(key)

        # While empty is 0, set the quadratic probe function using the hash function, probe counter and capacity.
        # Create a bucket available variable for quadratic probe index.
        while empty == 0:

            quadratic_probe = ((hash_func + (probe_counter * probe_counter)) % self.get_capacity())
            bucket_available = self._buckets.get_at_index(quadratic_probe)

            # Make a check if the index is None or the index is a Tombstone value. If yes, increment
            # the probe counter and return None, as there is no value to return at that key.
            if bucket_available is None or \
                    self._buckets.get_at_index(quadratic_probe).is_tombstone is True:
                probe_counter += 1
                return None

            # Otherwise, if the key matches the key passed, increment the probe counter
            # and return the value at that index.
            elif key == self._buckets.get_at_index(quadratic_probe).key:
                probe_counter += 1
                return self._buckets.get_at_index(quadratic_probe).value

            # Increment the probe counter to keep the quadratic probe function accurate.
            probe_counter += 1

    def contains_key(self, key: str) -> bool:
        """
        A function that returns True if
        a passed key is present in the
        hash map. Otherwise, it returns
        False. If the hash map is empty.
        it returns no keys.
        """

        # Set a probe counter to track the count for the quadratic probe function,
        # plus a while loop variable and the hash function with the passed
        # key to use in the quadratic probing function.
        empty = 0
        probe_counter = 0
        hash_func = self._hash_function(key)

        # While empty is 0, set the quadratic probe function using the hash function, probe counter and capacity.
        # Create a bucket available variable for quadratic probe index.
        while empty == 0:

            quadratic_probe = ((hash_func + (probe_counter * probe_counter)) % self.get_capacity())
            bucket_available = self._buckets.get_at_index(quadratic_probe)

            # Make a check to see if the index is None. If yes, increment the probe counter
            # and return False, as the value is not present.
            if bucket_available is None:
                probe_counter += 1
                return False

            # Otherwise, if the key matches the key passed and it is not a Tombstone
            # value, return True, as the key is present within the hash map. Increment the probe counter.
            if key == self._buckets.get_at_index(quadratic_probe).key and \
                    self._buckets.get_at_index(quadratic_probe).is_tombstone is False:
                probe_counter += 1
                return True

            # Increment the probe counter to keep the quadratic probe function accurate.
            probe_counter += 1

    def remove(self, key: str) -> None:
        """
        A function that removes the key
        passed, plus the value associated
        with that key. If the key passed
        is not present in the hash map,
        the function does nothing.
        """

        # Make a check to see that the key is within the hash map
        # to be removed. If not, then return, as a key that is not present
        # cannot be removed from the hash map.
        if not self.contains_key(key):
            return None

        # Make an additional check to see if the size is less than 1. If yes,
        # return, as there is no key in the hash map to remove.
        if self._buckets.length() < 1:
            return None

        # Set a probe counter to track the count for the quadratic probe function,
        # plus a while loop variable and the hash function with the passed
        # key to use in the quadratic probing function.
        empty = 0
        probe_counter = 0
        hash_func = self._hash_function(key)

        # While is 0, set the quadratic probe function using the hash function, probe counter and capacity.
        # Create a bucket available variable for quadratic probe index.
        while empty == 0:

            quadratic_probe = ((hash_func + (probe_counter * probe_counter)) % self.get_capacity())
            bucket_available = self._buckets.get_at_index(quadratic_probe)

            # If the key matches the key passed, and the index is true, return. Set the Tombstone
            # value to true, set the index to the quadratic probe and the value, then decrement the
            # size and return.
            if key == self._buckets.get_at_index(quadratic_probe).key:
                if bucket_available is True:
                    return
                self._buckets.get_at_index(quadratic_probe).is_tombstone = True
                self._buckets.set_at_index(quadratic_probe, self._buckets.get_at_index(quadratic_probe))
                self._size = self._size - 1
                return

            # If the quadratic probe is None, return.
            if bucket_available is None:
                return

            # If the length is less than or equal to the quadratic probe,
            # return.
            if self._buckets.length() <= quadratic_probe:
                return

            # Increment the probe counter to keep the quadratic probe function accurate.
            probe_counter += 1

    def clear(self) -> None:
        """
        A function that clears the
        contents of the underlying
        hash map, without changing the
        underlying capacity.
        """

        # Looping the length of buckets, set the buckets at index
        # to None and the size to 0 to clear the buckets without
        # altering the underlying capacity.
        for index in range(self._buckets.length()):
            self._buckets.set_at_index(index, None)
            self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        A function that returns a
        dynamic array where each element
        contains a tuple containing a
        key/value pair. Order does not
        matter.
        """

        da = DynamicArray()

        # Looping through the length of the buckets, set a variable buckets
        # to the index of each. A check is made to see if the current bucket
        # is not None and is not a Tombstone value. Then, if not None and
        # not a Tombstone, append the key and value of the bucket
        # to the return dynamic array.
        for index in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(index)
            if bucket:
                if bucket.is_tombstone is False:
                    da.append((bucket.key, bucket.value))
        return da

    def __iter__(self):
        """
        A function that allows the hash
        map to iterate across itself.
        """
        # As done in my bag DA assignment, set the index to 0 and return self.
        self._index = 0

        return self

    def __next__(self):
        """
        A function that returns the next
        item in the hash map, based upon
        the current location of the iterator.
        """
        # Taking inspiration from my bag DA assignment, try the value of buckets
        # at index. While this is None or the Tombstone value is True, increment
        # the index. Reset value.
        try:
            value = self._buckets[self._index]
            while value is None or value.is_tombstone is True:
                self._index += 1
                value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration

        # Increment the index and return.

        self._index += 1
        return value

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
