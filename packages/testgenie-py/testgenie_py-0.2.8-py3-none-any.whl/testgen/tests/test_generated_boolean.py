import unittest

import testgen.generated_boolean as generated_boolean

class TestNone(unittest.TestCase):  

   def test_bin_and_0(self):
      args = (True, True)
      expected = True
      result = generated_boolean.bin_and(*args)
      self.assertEqual(result, expected)

   def test_bin_and_1(self):
      args = (True, False)
      expected = False
      result = generated_boolean.bin_and(*args)
      self.assertEqual(result, expected)

   def test_bin_and_2(self):
      args = (False, True)
      expected = False
      result = generated_boolean.bin_and(*args)
      self.assertEqual(result, expected)

   def test_bin_xor_3(self):
      args = (True, True)
      expected = False
      result = generated_boolean.bin_xor(*args)
      self.assertEqual(result, expected)

   def test_bin_xor_4(self):
      args = (True, False)
      expected = True
      result = generated_boolean.bin_xor(*args)
      self.assertEqual(result, expected)

   def test_bin_xor_5(self):
      args = (False, True)
      expected = True
      result = generated_boolean.bin_xor(*args)
      self.assertEqual(result, expected)

   def test_status_flags_6(self):
      args = (True, True, True)
      expected = 'admin-verified'
      result = generated_boolean.status_flags(*args)
      self.assertEqual(result, expected)

   def test_status_flags_7(self):
      args = (True, True, False)
      expected = 'user-verified'
      result = generated_boolean.status_flags(*args)
      self.assertEqual(result, expected)

   def test_status_flags_8(self):
      args = (True, False, True)
      expected = 'admin-unverified'
      result = generated_boolean.status_flags(*args)
      self.assertEqual(result, expected)

   def test_status_flags_9(self):
      args = (True, False, False)
      expected = 'user-unverified'
      result = generated_boolean.status_flags(*args)
      self.assertEqual(result, expected)

   def test_status_flags_10(self):
      args = (False, True, True)
      expected = 'admin-verified'
      result = generated_boolean.status_flags(*args)
      self.assertEqual(result, expected)

   def test_status_flags_11(self):
      args = (False, True, False)
      expected = 'inactive'
      result = generated_boolean.status_flags(*args)
      self.assertEqual(result, expected)

   def test_status_flags_12(self):
      args = (False, False, True)
      expected = 'admin-unverified'
      result = generated_boolean.status_flags(*args)
      self.assertEqual(result, expected)
