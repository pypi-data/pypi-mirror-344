import unittest

import testgen.code_to_test.code_to_fuzz_lite as code_to_fuzz_lite

class TestNone(unittest.TestCase):  

   def test_random_fuzz_code_0(self):
      args = (-575877166, -506373949)
      expected = -1082251115
      result = code_to_fuzz_lite.random_fuzz_code(*args)
      self.assertEqual(result, expected)

   def test_random_fuzz_code_1(self):
      args = (-804220450, -1215112344)
      expected = 410891894
      result = code_to_fuzz_lite.random_fuzz_code(*args)
      self.assertEqual(result, expected)

   def test_bin_and_2(self):
      args = (True, False)
      expected = False
      result = code_to_fuzz_lite.bin_and(*args)
      self.assertEqual(result, expected)

   def test_bin_and_3(self):
      args = (False, True)
      expected = False
      result = code_to_fuzz_lite.bin_and(*args)
      self.assertEqual(result, expected)

   def test_bin_and_4(self):
      args = (True, True)
      expected = True
      result = code_to_fuzz_lite.bin_and(*args)
      self.assertEqual(result, expected)

   def test_pos_or_neg_5(self):
      args = -44133560
      expected = -1
      result = code_to_fuzz_lite.pos_or_neg(args)
      self.assertEqual(result, expected)

   def test_pos_or_neg_6(self):
      args = 1998904876
      expected = 1
      result = code_to_fuzz_lite.pos_or_neg(args)
      self.assertEqual(result, expected)

   def test_int_even_7(self):
      args = 226913822
      expected = True
      result = code_to_fuzz_lite.int_even(args)
      self.assertEqual(result, expected)

   def test_int_even_8(self):
      args = 343042071
      expected = False
      result = code_to_fuzz_lite.int_even(args)
      self.assertEqual(result, expected)

   def test_bin_and_bad_generated_function_9(self):
      args = (True, True)
      expected = True
      result = code_to_fuzz_lite.bin_and_bad_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_and_bad_generated_function_10(self):
      args = (False, True)
      expected = True
      result = code_to_fuzz_lite.bin_and_bad_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_and_bad_generated_function_11(self):
      args = (False, False)
      expected = False
      result = code_to_fuzz_lite.bin_and_bad_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_and_bad_generated_function_12(self):
      args = (True, False)
      expected = True
      result = code_to_fuzz_lite.bin_and_bad_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_nand_generated_function_13(self):
      args = (False, False)
      expected = True
      result = code_to_fuzz_lite.bin_nand_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_nand_generated_function_14(self):
      args = (True, True)
      expected = False
      result = code_to_fuzz_lite.bin_nand_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_nand_generated_function_15(self):
      args = (True, False)
      expected = True
      result = code_to_fuzz_lite.bin_nand_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_nand_generated_function_16(self):
      args = (False, True)
      expected = True
      result = code_to_fuzz_lite.bin_nand_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_nor_generated_function_17(self):
      args = (False, False)
      expected = True
      result = code_to_fuzz_lite.bin_nor_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_nor_generated_function_18(self):
      args = (False, True)
      expected = False
      result = code_to_fuzz_lite.bin_nor_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_nor_generated_function_19(self):
      args = (True, False)
      expected = False
      result = code_to_fuzz_lite.bin_nor_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_or_generated_function_20(self):
      args = (True, True)
      expected = True
      result = code_to_fuzz_lite.bin_or_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_or_generated_function_21(self):
      args = (True, False)
      expected = True
      result = code_to_fuzz_lite.bin_or_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_or_generated_function_22(self):
      args = (False, True)
      expected = True
      result = code_to_fuzz_lite.bin_or_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_or_bad_generated_function_23(self):
      args = (False, False)
      expected = True
      result = code_to_fuzz_lite.bin_or_bad_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_or_bad_generated_function_24(self):
      args = (False, True)
      expected = False
      result = code_to_fuzz_lite.bin_or_bad_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_or_bad_generated_function_25(self):
      args = (True, True)
      expected = False
      result = code_to_fuzz_lite.bin_or_bad_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_or_bad_generated_function_26(self):
      args = (True, False)
      expected = False
      result = code_to_fuzz_lite.bin_or_bad_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_xor_generated_function_27(self):
      args = (True, False)
      expected = True
      result = code_to_fuzz_lite.bin_xor_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_xor_generated_function_28(self):
      args = (False, True)
      expected = True
      result = code_to_fuzz_lite.bin_xor_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_xor_generated_function_29(self):
      args = (True, True)
      expected = False
      result = code_to_fuzz_lite.bin_xor_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_xor_generated_function_30(self):
      args = (False, False)
      expected = False
      result = code_to_fuzz_lite.bin_xor_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_31(self):
      args = (False, True, True, True, True, True)
      expected = True
      result = code_to_fuzz_lite.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_32(self):
      args = (True, True, True, False, True, False)
      expected = True
      result = code_to_fuzz_lite.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_33(self):
      args = (True, True, False, False, True, True)
      expected = False
      result = code_to_fuzz_lite.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_34(self):
      args = (False, False, True, True, False, False)
      expected = False
      result = code_to_fuzz_lite.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_35(self):
      args = (False, False, False, True, False, False)
      expected = False
      result = code_to_fuzz_lite.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_36(self):
      args = (False, False, True, False, True, True)
      expected = True
      result = code_to_fuzz_lite.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_37(self):
      args = (False, False, True, False, False, True)
      expected = True
      result = code_to_fuzz_lite.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_38(self):
      args = (True, False, False, False, False, True)
      expected = False
      result = code_to_fuzz_lite.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_39(self):
      args = (True, False, False, False, True, True)
      expected = False
      result = code_to_fuzz_lite.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_40(self):
      args = (True, False, True, True, True, False)
      expected = True
      result = code_to_fuzz_lite.mux_generated_function(*args)
      self.assertEqual(result, expected)
