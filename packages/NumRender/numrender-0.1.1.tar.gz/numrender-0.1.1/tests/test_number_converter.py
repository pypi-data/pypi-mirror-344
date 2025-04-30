import unittest
from NumRender import words_to_number, number_to_words

class TestNumberConverter(unittest.TestCase):

    def test_words_to_number_simple(self):
        self.assertEqual(words_to_number('one'), 1)
        self.assertEqual(words_to_number('ten'), 10)
        self.assertEqual(words_to_number('nineteen'), 19)
        self.assertEqual(words_to_number('twenty'), 20)
        self.assertEqual(words_to_number('fifty-six'), 56)
        self.assertEqual(words_to_number('ninety-nine'), 99)

    def test_words_to_number_hundreds(self):
        self.assertEqual(words_to_number('one hundred'), 100)
        self.assertEqual(words_to_number('two hundred and fifty'), 250)
        self.assertEqual(words_to_number('three hundred twelve'), 312) # Without 'and'
        self.assertEqual(words_to_number('nine hundred and ninety nine'), 999)

    def test_words_to_number_thousands(self):
        self.assertEqual(words_to_number('one thousand'), 1000)
        self.assertEqual(words_to_number('five thousand'), 5000)
        self.assertEqual(words_to_number('one thousand two hundred'), 1200)
        self.assertEqual(words_to_number('three thousand and fifty six'), 3056)
        self.assertEqual(words_to_number('twenty thousand five hundred and one'), 20501)
        self.assertEqual(words_to_number('one hundred thousand'), 100000)
        self.assertEqual(words_to_number('one hundred and twenty three thousand four hundred and fifty six'), 123456)

    def test_words_to_number_large(self):
        self.assertEqual(words_to_number('one million'), 1000000)
        self.assertEqual(words_to_number('two million five hundred thousand'), 2500000)
        self.assertEqual(words_to_number('one billion'), 1000000000)

    def test_words_to_number_zero(self):
        self.assertEqual(words_to_number('zero'), 0)

    def test_words_to_number_invalid(self):
        with self.assertRaises(ValueError):
            words_to_number('one cat')
        with self.assertRaises(ValueError):
            words_to_number('thousand million') # Invalid order

    # --- Tests for number_to_words ---

    def test_number_to_words_simple(self):
        self.assertEqual(number_to_words(1), 'one')
        self.assertEqual(number_to_words(10), 'ten')
        self.assertEqual(number_to_words(19), 'nineteen')
        self.assertEqual(number_to_words(20), 'twenty')
        self.assertEqual(number_to_words(56), 'fifty-six')
        self.assertEqual(number_to_words(99), 'ninety-nine')

    def test_number_to_words_hundreds(self):
        self.assertEqual(number_to_words(100), 'one hundred')
        self.assertEqual(number_to_words(250), 'two hundred and fifty')
        self.assertEqual(number_to_words(312), 'three hundred and twelve')
        self.assertEqual(number_to_words(999), 'nine hundred and ninety-nine') # Expect hyphenated

    def test_number_to_words_thousands(self):
        self.assertEqual(number_to_words(1000), 'one thousand')
        self.assertEqual(number_to_words(5000), 'five thousand')
        self.assertEqual(number_to_words(1200), 'one thousand two hundred') # No 'and' needed here
        self.assertEqual(number_to_words(3056), 'three thousand and fifty-six')
        self.assertEqual(number_to_words(20501), 'twenty thousand five hundred and one')
        self.assertEqual(number_to_words(100000), 'one hundred thousand')
        self.assertEqual(number_to_words(123456), 'one hundred twenty three thousand four hundred and fifty-six')

    def test_number_to_words_large(self):
        self.assertEqual(number_to_words(1000000), 'one million')
        self.assertEqual(number_to_words(2500000), 'two million five hundred thousand')
        self.assertEqual(number_to_words(1000000000), 'one billion')

    def test_number_to_words_zero(self):
        self.assertEqual(number_to_words(0), 'zero')

    def test_number_to_words_negative(self):
        # Assuming negative numbers aren't handled yet, or add specific handling if they are.
        # self.assertEqual(number_to_words(-5), 'minus five') # Example if implemented
        pass # Update if negative handling is added

    def test_number_to_words_type_error(self):
        with self.assertRaises(TypeError):
            number_to_words('123')
        with self.assertRaises(TypeError):
            number_to_words(123.45)

if __name__ == '__main__':
    unittest.main()