import pytest

import testgen.code_to_test.decisions as decisions

def test_add_or_subtract_0():
   args = (12, 71)
   expected = 83
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_1():
   args = (7, 81)
   expected = 88
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_2():
   args = (97, 75)
   expected = 22
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_3():
   args = (38, 40)
   expected = 78
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_4():
   args = (66, 3)
   expected = 63
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_5():
   args = (84, 10)
   expected = 74
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_6():
   args = (95, 89)
   expected = 6
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_7():
   args = (57, 12)
   expected = 45
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_8():
   args = (64, 98)
   expected = 162
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_9():
   args = (94, 80)
   expected = 14
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_10():
   args = (26, 3)
   expected = 23
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_11():
   args = (91, 39)
   expected = 52
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_12():
   args = (53, 42)
   expected = 11
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_13():
   args = (15, 42)
   expected = 57
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_14():
   args = (13, 67)
   expected = 80
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_15():
   args = (62, 92)
   expected = 154
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_add_or_subtract_16():
   args = (91, 2)
   expected = 89
   result = decisions.add_or_subtract(*args)
   assert result == expected

def test_email_type_17():
   args = 'abc'
   expected = 'invalid'
   result = decisions.email_type(args)
   assert result == expected

def test_http_code_18():
   args = 81
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_19():
   args = 60
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_20():
   args = 29
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_21():
   args = 11
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_22():
   args = 79
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_23():
   args = 70
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_24():
   args = 52
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_25():
   args = 41
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_26():
   args = 6
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_27():
   args = 63
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_28():
   args = 47
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_29():
   args = 58
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_http_code_30():
   args = 87
   expected = 'invalid'
   result = decisions.http_code(args)
   assert result == expected

def test_password_strength_31():
   args = 'abc'
   expected = 'weak'
   result = decisions.password_strength(args)
   assert result == expected
