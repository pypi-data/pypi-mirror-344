# NumRender Library

A simple Python library to convert numbers to their word representations and vice versa.

## Installation

```bash
# Installation instructions will be added here once published
# For now, you can install it locally:
pip install NumRender
```

## Usage

```python
import NumRender

# Convert words to number
number = NumRender.words_to_number("three hundred and twenty five")
print(number)  # Output: 325

number = NumRender.words_to_number("five thousand")
print(number)  # Output: 5000

# Convert number to words
words = NumRender.number_to_words(1234)
print(words) # Output: one thousand two hundred and thirty-four (example, actual output might vary slightly based on implementation)

words = NumRender.number_to_words(5000)
print(words) # Output: five thousand
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details (if added).