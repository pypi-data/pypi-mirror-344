# Core functions for number-word conversion will go here

_UNIT_MAP = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
    'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16,
    'seventeen': 17, 'eighteen': 18, 'nineteen': 19
}

_TENS_MAP = {
    'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90
}

_SCALE_MAP = {
    'hundred': 100,
    'thousand': 1000,
    'million': 1000000,
    'billion': 1000000000,
    # Add more scales as needed (e.g., trillion)
}

def words_to_number(word_string):
    """Converts a number written in words (e.g., 'five thousand', 'three hundred and twenty five') to an integer."""
    words = word_string.lower().replace('-', ' ').split()
    current_number = 0
    total_number = 0
    last_scale_value = float('inf') # Track the scale to ensure descending order

    # Remove 'and' if present, as it doesn't affect the value
    words = [word for word in words if word != 'and']

    for word in words:
        if word in _UNIT_MAP:
            current_number += _UNIT_MAP[word]
        elif word in _TENS_MAP:
            current_number += _TENS_MAP[word]
        elif word in _SCALE_MAP:
            scale_value = _SCALE_MAP[word]
            # Check for invalid scale order (e.g., "thousand million")
            if scale_value >= last_scale_value:
                 raise ValueError(f"Invalid scale order: '{word}' cannot follow a scale of {last_scale_value} or larger.")

            if word == 'hundred':
                # Multiply the last part by 100
                current_number = max(1, current_number) * scale_value
            else:
                # Apply scale and reset current number for the next scale
                total_number += max(1, current_number) * scale_value
                last_scale_value = scale_value # Update the last scale seen
                current_number = 0
        else:
            raise ValueError(f"Unknown word: {word}")

    # Ensure the final current_number isn't larger than the last scale allows
    if current_number >= last_scale_value:
        raise ValueError(f"Invalid number structure near end: {current_number} cannot follow scale {last_scale_value}")

    total_number += current_number
    return total_number

_WORDS_UNIT_MAP = {
    0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine',
    10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen',
    17: 'seventeen', 18: 'eighteen', 19: 'nineteen'
}

_WORDS_TENS_MAP = {
    2: 'twenty', 3: 'thirty', 4: 'forty', 5: 'fifty', 6: 'sixty', 7: 'seventy', 8: 'eighty', 9: 'ninety'
}

_WORDS_SCALE_MAP = [
    (1000000000, 'billion'),
    (1000000, 'million'),
    (1000, 'thousand'),
    (100, 'hundred')
    # Add more scales as needed (e.g., trillion)
]

def _number_to_words_less_than_1000(number, is_part_of_larger_scale=False):
    """Helper function to convert numbers less than 1000 to words.

    Args:
        number (int): The number to convert (0-999).
        is_part_of_larger_scale (bool): If True, avoids adding 'and' after 'hundred'
                                        when this number is part of a larger scale
                                        (e.g., the '123' in '123 thousand').
    """
    if number < 20:
        return _WORDS_UNIT_MAP[number]
    elif number < 100:
        tens, units = divmod(number, 10)
        if units == 0:
            return _WORDS_TENS_MAP[tens]
        else:
            # Use hyphen only if not part of a larger scale (e.g., 'twenty-three', but 'one hundred twenty three thousand')
            separator = '-' if not is_part_of_larger_scale else ' '
            return f"{_WORDS_TENS_MAP[tens]}{separator}{_WORDS_UNIT_MAP[units]}"
    else: # 100 to 999
        hundreds, remainder = divmod(number, 100)
        parts = [_WORDS_UNIT_MAP[hundreds], 'hundred']
        if remainder > 0:
            # Only add 'and' if this is the final part (not followed by a larger scale like thousand/million)
            if not is_part_of_larger_scale:
                 parts.append('and')
            # Pass the flag down. Hyphenation is handled correctly in the recursive call based on the flag.
            # The recursive call needs the flag to determine hyphenation vs. space for tens/units.
            parts.append(_number_to_words_less_than_1000(remainder, is_part_of_larger_scale))
        return ' '.join(parts)

def number_to_words(number):
    """Converts an integer (e.g., 5000, 325) to its word representation."""
    if not isinstance(number, int):
        raise TypeError("Input must be an integer.")

    if number == 0:
        return _WORDS_UNIT_MAP[0]

    if number < 0:
        return f"minus {_number_to_words_less_than_1000(abs(number))}"

    parts = []
    remaining_number = number

    for scale_value, scale_name in _WORDS_SCALE_MAP:
        if remaining_number >= scale_value:
            count, remaining_number = divmod(remaining_number, scale_value)
            # Pass True for is_part_of_larger_scale here
            parts.append(_number_to_words_less_than_1000(count, is_part_of_larger_scale=True))
            parts.append(scale_name)

    if remaining_number > 0:
        # Append the final part (less than 1000)
        # Add 'and' if a larger scale part precedes this final remainder AND the remainder is < 100.
        # Example: 1056 -> one thousand *and* fifty-six. But 1200 -> one thousand two hundred.
        if parts and remaining_number < 100:
             # Check if the last part added was a scale word (excluding hundred)
             # This check might be redundant if 'and' after hundred is handled correctly in the helper
             # Let's keep it simple for now: add 'and' if scale parts exist and remainder < 100
             parts.append('and')

        # Pass False for is_part_of_larger_scale for the final remainder
        parts.append(_number_to_words_less_than_1000(remaining_number, is_part_of_larger_scale=False))

    # Join parts and clean up potential extra spaces
    result = ' '.join(parts)
    result = ' '.join(result.split()) # Consolidate multiple spaces
    return result