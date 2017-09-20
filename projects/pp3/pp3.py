import os
import sys
import logging

import re


# Regular expression matching optional whitespace followed by a token
# (if group 1 matches) or an error (if group 2 matches).
# TOKEN_RE = re.compile(r'\s*(?:([A-Za-z01()~+*]|->)|(\S))')
TOKEN_RE = re.compile(r'(?:([a-zA-Z0-9]+|[()~+*]|->)|(\S))')

# Special token indicating the end of the input string.
TOKEN_END = '<end of input>'

# File name of input
INPUT_FILE_NAME = 'input.txt'


def tokenize(s):
    """Generate tokens from the string s, followed by TOKEN_END."""
    for m in TOKEN_RE.finditer(s):
        if m.group(1):
            yield m.group(1)
        else:
            raise SyntaxError("Unexpected character {!r}".format(m.group(2)))
    yield TOKEN_END


if __name__ == '__main__':
    try:
        lines = (line.rstrip('\n') for line in open(INPUT_FILE_NAME))
        for line in lines:
            line_tokenized = [l.strip() for l in line.split('=')]
            if len(line_tokenized) != 2:
                logging.warning("Unexpected input line exists...")
                continue
            name = line_tokenized[0]; formula = line_tokenized[1]
            formula_tokenized = tokenize(formula);
    except IOError:
        logging.error("Could not read file: {}".format(INPUT_FILE_NAME))
