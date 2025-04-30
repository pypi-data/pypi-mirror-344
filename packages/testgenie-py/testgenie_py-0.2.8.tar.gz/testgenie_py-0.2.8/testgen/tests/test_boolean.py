import pytest

import testgen.code_to_test.boolean as boolean

def test_bin_and_0():
   args = (False, False)
   expected = False
   result = boolean.bin_and(*args)
   assert result == expected

def test_bin_and_1():
   args = (True, True)
   expected = True
   result = boolean.bin_and(*args)
   assert result == expected

def test_bin_and_2():
   args = (True, False)
   expected = False
   result = boolean.bin_and(*args)
   assert result == expected

def test_bin_xor_3():
   args = (False, True)
   expected = True
   result = boolean.bin_xor(*args)
   assert result == expected

def test_bin_xor_4():
   args = (False, False)
   expected = False
   result = boolean.bin_xor(*args)
   assert result == expected

def test_bin_xor_5():
   args = (True, True)
   expected = False
   result = boolean.bin_xor(*args)
   assert result == expected

def test_bin_xor_6():
   args = (True, False)
   expected = True
   result = boolean.bin_xor(*args)
   assert result == expected

def test_status_flags_7():
   args = (True, False, True)
   expected = 'admin-unverified'
   result = boolean.status_flags(*args)
   assert result == expected

def test_status_flags_8():
   args = (True, True, False)
   expected = 'user-verified'
   result = boolean.status_flags(*args)
   assert result == expected

def test_status_flags_9():
   args = (False, True, True)
   expected = 'admin-verified'
   result = boolean.status_flags(*args)
   assert result == expected

def test_status_flags_10():
   args = (True, True, True)
   expected = 'admin-verified'
   result = boolean.status_flags(*args)
   assert result == expected

def test_status_flags_11():
   args = (True, False, False)
   expected = 'user-unverified'
   result = boolean.status_flags(*args)
   assert result == expected

def test_status_flags_12():
   args = (False, True, False)
   expected = 'inactive'
   result = boolean.status_flags(*args)
   assert result == expected
