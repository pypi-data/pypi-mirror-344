import unittest

import testgen.code_to_test.code_to_fuzz as code_to_fuzz

class TestNone(unittest.TestCase):  

   def test_random_fuzz_code_0(self):
      args = (1927227313, 775789320)
      expected = 1151437993
      result = code_to_fuzz.random_fuzz_code(*args)
      self.assertEqual(result, expected)

   def test_random_fuzz_code_1(self):
      args = (1359311181, 1603562853)
      expected = 2962874034
      result = code_to_fuzz.random_fuzz_code(*args)
      self.assertEqual(result, expected)

   def test_bin_and_2(self):
      args = (False, False)
      expected = False
      result = code_to_fuzz.bin_and(*args)
      self.assertEqual(result, expected)

   def test_bin_and_3(self):
      args = (True, True)
      expected = True
      result = code_to_fuzz.bin_and(*args)
      self.assertEqual(result, expected)

   def test_bin_and_4(self):
      args = (True, False)
      expected = False
      result = code_to_fuzz.bin_and(*args)
      self.assertEqual(result, expected)

   def test_pos_or_neg_5(self):
      args = 1381971091
      expected = 1
      result = code_to_fuzz.pos_or_neg(args)
      self.assertEqual(result, expected)

   def test_pos_or_neg_6(self):
      args = -1792272568
      expected = -1
      result = code_to_fuzz.pos_or_neg(args)
      self.assertEqual(result, expected)

   def test_int_even_7(self):
      args = 612556544
      expected = True
      result = code_to_fuzz.int_even(args)
      self.assertEqual(result, expected)

   def test_int_even_8(self):
      args = 1538337835
      expected = False
      result = code_to_fuzz.int_even(args)
      self.assertEqual(result, expected)

   def test_http_code_9(self):
      args = 1748799535
      expected = 'invalid'
      result = code_to_fuzz.http_code(args)
      self.assertEqual(result, expected)

   def test_add_or_subtract_10(self):
      args = (1167731537, 1136934405)
      expected = 30797132
      result = code_to_fuzz.add_or_subtract(*args)
      self.assertEqual(result, expected)

   def test_add_or_subtract_11(self):
      args = (506636609, 1260222214)
      expected = 1766858823
      result = code_to_fuzz.add_or_subtract(*args)
      self.assertEqual(result, expected)

   def test_bin_and_bad_generated_function_12(self):
      args = (False, False)
      expected = False
      result = code_to_fuzz.bin_and_bad_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_and_bad_generated_function_13(self):
      args = (True, True)
      expected = True
      result = code_to_fuzz.bin_and_bad_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_and_bad_generated_function_14(self):
      args = (False, True)
      expected = True
      result = code_to_fuzz.bin_and_bad_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_nand_generated_function_15(self):
      args = (False, False)
      expected = True
      result = code_to_fuzz.bin_nand_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_nand_generated_function_16(self):
      args = (True, True)
      expected = False
      result = code_to_fuzz.bin_nand_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_nand_generated_function_17(self):
      args = (True, False)
      expected = True
      result = code_to_fuzz.bin_nand_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_nand_generated_function_18(self):
      args = (False, True)
      expected = True
      result = code_to_fuzz.bin_nand_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_nor_generated_function_19(self):
      args = (True, True)
      expected = False
      result = code_to_fuzz.bin_nor_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_nor_generated_function_20(self):
      args = (False, True)
      expected = False
      result = code_to_fuzz.bin_nor_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_nor_generated_function_21(self):
      args = (True, False)
      expected = False
      result = code_to_fuzz.bin_nor_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_or_generated_function_22(self):
      args = (False, True)
      expected = True
      result = code_to_fuzz.bin_or_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_or_generated_function_23(self):
      args = (True, False)
      expected = True
      result = code_to_fuzz.bin_or_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_or_generated_function_24(self):
      args = (True, True)
      expected = True
      result = code_to_fuzz.bin_or_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_or_generated_function_25(self):
      args = (False, False)
      expected = False
      result = code_to_fuzz.bin_or_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_or_bad_generated_function_26(self):
      args = (False, True)
      expected = False
      result = code_to_fuzz.bin_or_bad_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_or_bad_generated_function_27(self):
      args = (True, True)
      expected = False
      result = code_to_fuzz.bin_or_bad_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_or_bad_generated_function_28(self):
      args = (False, False)
      expected = True
      result = code_to_fuzz.bin_or_bad_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_or_bad_generated_function_29(self):
      args = (True, False)
      expected = False
      result = code_to_fuzz.bin_or_bad_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_xor_generated_function_30(self):
      args = (True, True)
      expected = False
      result = code_to_fuzz.bin_xor_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_xor_generated_function_31(self):
      args = (True, False)
      expected = True
      result = code_to_fuzz.bin_xor_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_xor_generated_function_32(self):
      args = (False, True)
      expected = True
      result = code_to_fuzz.bin_xor_generated_function(*args)
      self.assertEqual(result, expected)

   def test_bin_xor_generated_function_33(self):
      args = (False, False)
      expected = False
      result = code_to_fuzz.bin_xor_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_34(self):
      args = (True, False, False, True, False, False)
      expected = True
      result = code_to_fuzz.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_35(self):
      args = (False, True, False, False, True, False)
      expected = True
      result = code_to_fuzz.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_36(self):
      args = (True, False, False, False, True, True)
      expected = False
      result = code_to_fuzz.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_37(self):
      args = (False, True, False, True, False, True)
      expected = False
      result = code_to_fuzz.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_38(self):
      args = (False, False, True, False, True, False)
      expected = False
      result = code_to_fuzz.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_39(self):
      args = (True, False, False, False, False, False)
      expected = False
      result = code_to_fuzz.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_40(self):
      args = (False, True, True, True, True, True)
      expected = True
      result = code_to_fuzz.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_41(self):
      args = (False, False, False, True, False, False)
      expected = False
      result = code_to_fuzz.mux_generated_function(*args)
      self.assertEqual(result, expected)

   def test_mux_generated_function_42(self):
      args = (True, False, True, True, True, False)
      expected = True
      result = code_to_fuzz.mux_generated_function(*args)
      self.assertEqual(result, expected)
