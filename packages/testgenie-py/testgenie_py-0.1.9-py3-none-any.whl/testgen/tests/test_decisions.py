import pytest

import testgen.code_to_test.decisions as decisions

def test_add_or_subtract_0():
   args = (42, 74)
   expected = 116
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_1():
   args = (11, 67)
   expected = 78
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_2():
   args = (74, 73)
   expected = 1
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_3():
   args = (93, 39)
   expected = 54
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_4():
   args = (61, 77)
   expected = 138
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_5():
   args = (73, 6)
   expected = 67
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_6():
   args = (62, 37)
   expected = 25
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_7():
   args = (42, 52)
   expected = 94
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_8():
   args = (87, 32)
   expected = 55
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_9():
   args = (93, 31)
   expected = 62
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_10():
   args = (53, 42)
   expected = 11
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_11():
   args = (58, 22)
   expected = 36
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_12():
   args = (64, 41)
   expected = 23
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_13():
   args = (76, 13)
   expected = 63
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_14():
   args = (93, 9)
   expected = 84
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_15():
   args = (65, 82)
   expected = 147
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_email_type_16():
   args = 'abc'
   expected = 'invalid'
   result = decisions.email_type(args)
   assert result == expected

def test_http_code_17():
   args = 66
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_18():
   args = 58
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_19():
   args = 26
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_20():
   args = 44
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_21():
   args = 41
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_22():
   args = 13
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_23():
   args = 32
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_24():
   args = 34
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_25():
   args = 12
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_26():
   args = 91
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_27():
   args = 22
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_password_strength_28():
   args = 'abc'
   expected = 'weak'
   result = decisions.password_strength(args)
   assert result == expected
