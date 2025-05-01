# Copyright (C) 2025 Kumo inc.
# Author: Jeff.li lijippy@163.com
# All rights reserved.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https:#www.gnu.org/licenses/>.
#
# distutils: language = c++

from libcpp.utility cimport pair

cdef extern from "turbo/container/flat_hash_map.h" namespace "turbo" nogil:
    cdef cppclass CFlatHashMap "turbo::flat_hash_map"[K, V, HASH=*, PRED=*, ALLOCATOR=*] :
        ctypedef K key_type
        ctypedef V mapped_type
        ctypedef pair[const K, V] value_type
        ctypedef ALLOCATOR allocator_type

        # these should really be allocator_type.size_type and
        # allocator_type.difference_type to be true to the C++ definition
        # but cython doesn't support deferred access on template arguments
        ctypedef size_t size_type
        ctypedef ptrdiff_t difference_type

        cppclass iterator
        cppclass iterator:
            iterator() except +
            iterator(iterator&) except +
            # correct would be value_type& but this does not work
            # well with cython's code gen
            pair[K, V]& operator*()
            iterator operator++()
            iterator operator--()
            iterator operator++(int)
            iterator operator--(int)
            bint operator==(iterator)
            bint operator==(const_iterator)
            bint operator!=(iterator)
            bint operator!=(const_iterator)
        cppclass const_iterator:
            const_iterator() except +
            const_iterator(iterator&) except +
            operator=(iterator&) except +
            # correct would be const value_type& but this does not work
            # well with cython's code gen
            const pair[K, V]& operator*()
            const_iterator operator++()
            const_iterator operator--()
            const_iterator operator++(int)
            const_iterator operator--(int)
            bint operator==(iterator)
            bint operator==(const_iterator)
            bint operator!=(iterator)
            bint operator!=(const_iterator)

        CFlatHashMap() except +
        CFlatHashMap(CFlatHashMap&) except +
        #CFlatHashMap(key_compare&)
        V& operator[](const K&)
        #CFlatHashMap& operator=(CFlatHashMap&)
        bint operator==(CFlatHashMap&, CFlatHashMap&)
        bint operator!=(CFlatHashMap&, CFlatHashMap&)
        bint operator<(CFlatHashMap&, CFlatHashMap&)
        bint operator>(CFlatHashMap&, CFlatHashMap&)
        bint operator<=(CFlatHashMap&, CFlatHashMap&)
        bint operator>=(CFlatHashMap&, CFlatHashMap&)
        V& at(const K&) except +
        const V& const_at "at"(const K&) except +
        iterator begin()
        const_iterator const_begin "begin"()
        const_iterator cbegin()
        void clear()
        size_t count(const K&)
        bint empty()
        iterator end()
        const_iterator const_end "end"()
        const_iterator cend()
        pair[iterator, iterator] equal_range(const K&)
        pair[const_iterator, const_iterator] const_equal_range "equal_range"(const K&)
        iterator erase(iterator)
        iterator const_erase "erase"(const_iterator)
        iterator erase(const_iterator, const_iterator)
        size_t erase(const K&)
        iterator find(const K&)
        const_iterator const_find "find"(const K&)
        pair[iterator, bint] insert(const pair[K, V]&) except +
        iterator insert(const_iterator, const pair[K, V]&) except +
        void insert[InputIt](InputIt, InputIt) except +
        #key_compare key_comp()
        iterator lower_bound(const K&)
        const_iterator const_lower_bound "lower_bound"(const K&)
        size_t max_size()
        size_t size()
        void swap(CFlatHashMap&)
        iterator upper_bound(const K&)
        const_iterator const_upper_bound "upper_bound"(const K&)
        #value_compare value_comp()
        void max_load_factor(float)
        float max_load_factor()
        float load_factor()
        void rehash(size_t)
        void reserve(size_t)
        size_t bucket_count()
        size_t max_bucket_count()
        size_t bucket_size(size_t)
        size_t bucket(const K&)
        # C++20
        bint contains(const K&)

    cdef cppclass unordered_multimap[K, V, HASH=*, PRED=*, ALLOCATOR=*]:
        ctypedef K key_type
        ctypedef V mapped_type
        ctypedef pair[const K, V] value_type
        ctypedef ALLOCATOR allocator_type

        # these should really be allocator_type.size_type and
        # allocator_type.difference_type to be true to the C++ definition
        # but cython doesn't support deferred access on template arguments
        ctypedef size_t size_type
        ctypedef ptrdiff_t difference_type

        cppclass const_iterator
        cppclass iterator:
            iterator() except +
            iterator(iterator&) except +
            # correct would be value_type& but this does not work
            # well with cython's code gen
            pair[K, V]& operator*()
            iterator operator++()
            iterator operator++(int)
            bint operator==(iterator)
            bint operator==(const_iterator)
            bint operator!=(iterator)
            bint operator!=(const_iterator)
        cppclass const_iterator:
            const_iterator() except +
            const_iterator(iterator&) except +
            operator=(iterator&) except +
            # correct would be const value_type& but this does not work
            # well with cython's code gen
            const pair[K, V]& operator*()
            const_iterator operator++()
            const_iterator operator++(int)
            bint operator==(iterator)
            bint operator==(const_iterator)
            bint operator!=(iterator)
            bint operator!=(const_iterator)

        unordered_multimap() except +
        unordered_multimap(const unordered_multimap&) except +
        #unordered_multimap(key_compare&)
        #CFlatHashMap& operator=(unordered_multimap&)
        bint operator==(const unordered_multimap&, const unordered_multimap&)
        bint operator!=(const unordered_multimap&, const unordered_multimap&)
        bint operator<(const unordered_multimap&, const unordered_multimap&)
        bint operator>(const unordered_multimap&, const unordered_multimap&)
        bint operator<=(const unordered_multimap&, const unordered_multimap&)
        bint operator>=(const unordered_multimap&, const unordered_multimap&)
        iterator begin()
        const_iterator const_begin "begin"()
        const_iterator cbegin()
        #local_iterator begin(size_t)
        #const_local_iterator const_begin "begin"(size_t)
        void clear()
        size_t count(const K&)
        bint empty()
        iterator end()
        const_iterator const_end "end"()
        const_iterator cend()
        #local_iterator end(size_t)
        #const_local_iterator const_end "end"(size_t)
        pair[iterator, iterator] equal_range(const K&)
        pair[const_iterator, const_iterator] const_equal_range "equal_range"(const K&)
        iterator erase(iterator)
        iterator const_erase "erase"(const_iterator)
        iterator erase(const_iterator, const_iterator)
        size_t erase(const K&)
        iterator find(const K&)
        const_iterator const_find "find"(const K&)
        iterator insert(const pair[K, V]&) except +
        iterator insert(const_iterator, const pair[K, V]&) except +
        void insert[InputIt](InputIt, InputIt) except +
        #key_compare key_comp()
        iterator lower_bound(const K&)
        const_iterator const_lower_bound "lower_bound"(const K&)
        size_t max_size()
        size_t size()
        void swap(unordered_multimap&)
        iterator upper_bound(const K&)
        const_iterator const_upper_bound "upper_bound"(const K&)
        #value_compare value_comp()
        void max_load_factor(float)
        float max_load_factor()
        float load_factor()
        void rehash(size_t)
        void reserve(size_t)
        size_t bucket_count()
        size_t max_bucket_count()
        size_t bucket_size(size_t)
        size_t bucket(const K&)
        # C++20
        bint contains(const K&)
