#!/usr/bin/env python3

import logging
import os
import sys

import re




# Regular expressions matching each assembly command
RE_COMMANDS = (
    ( 'RE_INST_A', re.compile(r"^@(\d+|[a-zA-Z_.$:][\w.$:]*)$") ),
    ( 'RE_INST_C', re.compile(r"^([A?M?D?]+=)?[+\-!&|01AMD]+(;J[A-Z]{2})?$") ),
    ( 'RE_LABEL', re.compile(r"^\([a-zA-Z_.$:][\w.$:]*\)$") ),
    ( 'RE_COMMENT', re.compile(r"^//") ),
)




def match_regex(s):
    # Please make sure there's no whitespace in s.
    for cmd_type, pattern in RE_COMMANDS:
        if pattern.match(s):
            return cmd_type
    return None

def is_decimal(s):
    if s[0] in ('-', '+'):
        return s[1:].isdecimal()
    return s.isdecimal()

def set_indent(lst):
    res = ''
    for elem in lst:
        curr = ('    ' if elem[0] != '(' else '') + "{}\n".format(elem)
        res += curr
    return res

def error_line():
    logging.error("Some instruction has a syntactic error...")




def main():
    logging.basicConfig(level=logging.DEBUG)

    # Initializations.
    try:
        lines = list(filter(None, [line.strip() for line in open(sys.argv[1])]))
        logging.info("Start translating <{}>.".format(sys.argv[1]))
        filename_vm = (sys.argv[1])[:-3]
        f_asm = open("{}.asm".format(filename_vm), 'w')
        cond_cnt = 0
    except IndexError:
        logging.error("Please properly enter the name of vm file as an argument.")
        return
    except FileNotFoundError:
        logging.error("Could not read input: <{}>.".format(sys.argv[1]))
        return

    for line in lines:
	# Parse current line.
        tokens = re.split(r"//", line)[0].split()
        logging.debug("tokens: <{}>".format(tokens))
        if len(''.join(tokens)) < 1:
            continue
        # Decode instruction.
        if tokens[0] == 'push':
            operand = int(tokens[2])
            if tokens[1] == 'constant':
                code = [ '@{}'.format(operand), 'D=A' ]
            elif tokens[1] == 'local':
                code = [ '@{}'.format(operand), 'D=A', '@LCL', 'A=D+M', 'D=M' ]
            elif tokens[1] == 'argument':
                code = [ '@{}'.format(operand), 'D=A', '@ARG', 'A=D+M', 'D=M' ]
            elif tokens[1] == 'this':
                code = [ '@{}'.format(operand), 'D=A', '@THIS', 'A=D+M', 'D=M' ]
            elif tokens[1] == 'that':
                code = [ '@{}'.format(operand), 'D=A', '@THAT', 'A=D+M', 'D=M' ]
            elif tokens[1] == 'temp':
                code = [ '@{}'.format(operand), 'D=A', '@R5', 'A=D+A', 'D=M' ]
            elif tokens[1] == 'pointer':
                code = [ ('@THIS' if int(tokens[2]) == 0 else '@THAT'), 'D=M' ]
            elif tokens[1] == 'static':
                pass
            code.extend([ '@SP', 'AM=M+1', 'A=A-1', 'M=D' ])
        elif tokens[0] == 'pop':
            operand = int(tokens[2])
            if tokens[1] == 'local':
                code = [ '@{}'.format(operand), 'D=A', '@LCL', 'D=D+M', '@R13', 'M=D', '@SP', 'AM=M-1', 'D=M', '@R13', 'A=M', 'M=D']
            elif tokens[1] == 'argument':
                code = [ '@{}'.format(operand), 'D=A', '@ARG', 'D=D+M', '@R13', 'M=D', '@SP', 'AM=M-1', 'D=M', '@R13', 'A=M', 'M=D']
            elif tokens[1] == 'this':
                code = [ '@{}'.format(operand), 'D=A', '@THIS', 'D=D+M', '@R13', 'M=D', '@SP', 'AM=M-1', 'D=M', '@R13', 'A=M', 'M=D']
            elif tokens[1] == 'that':
                code = [ '@{}'.format(operand), 'D=A', '@THAT', 'D=D+M', '@R13', 'M=D', '@SP', 'AM=M-1', 'D=M', '@R13', 'A=M', 'M=D']
            elif tokens[1] == 'temp':
                code = [ '@{}'.format(operand), 'D=A', '@R5', 'D=D+A', '@R13', 'M=D', '@SP', 'AM=M-1', 'D=M', '@R13', 'A=M', 'M=D']
            elif tokens[1] == 'pointer':
                code = [ '@SP', 'AM=M-1', 'D=M', ('@THIS' if int(tokens[2]) == 0 else '@THAT'), 'M=D' ]
            elif tokens[1] == 'static':
                pass
        elif tokens[0] == 'add':
            code = [ '@SP', 'AM=M-1', 'D=M', 'A=A-1', 'M=D+M' ]
        elif tokens[0] == 'sub':
            code = [ '@SP', 'AM=M-1', 'D=M', 'A=A-1', 'M=M-D' ]
        elif tokens[0] == 'neg':
            code = [ '@SP', 'A=M-1', 'M=-M' ]
        elif tokens[0] == 'eq':
            label_in, label_out = 'EQ{}_IN'.format(cond_cnt), 'EQ{}_OUT'.format(cond_cnt)
            code = [ '@SP', 'AM=M-1', 'D=M', 'A=A-1', 'D=D-M', '@{}'.format(label_in), 'D;JEQ', 'D=0', '@{}'.format(label_out), '0;JMP', '({})'.format(label_in), 'D=-1', '({})'.format(label_out), '@SP', 'A=M-1', 'M=D' ]
            cond_cnt = cond_cnt + 1
        elif tokens[0] == 'gt':
            label_in, label_out = 'GT{}_IN'.format(cond_cnt), 'GT{}_OUT'.format(cond_cnt)
            code = [ '@SP', 'AM=M-1', 'D=M', 'A=A-1', 'D=D-M', '@{}'.format(label_in), 'D;JLT', 'D=0', '@{}'.format(label_out), '0;JMP', '({})'.format(label_in), 'D=-1', '({})'.format(label_out), '@SP', 'A=M-1', 'M=D' ]
            cond_cnt = cond_cnt + 1
        elif tokens[0] == 'lt':
            label_in, label_out = 'GT{}_IN'.format(cond_cnt), 'GT{}_OUT'.format(cond_cnt)
            code = [ '@SP', 'AM=M-1', 'D=M', 'A=A-1', 'D=D-M', '@{}'.format(label_in), 'D;JGT', 'D=0', '@{}'.format(label_out), '0;JMP', '({})'.format(label_in), 'D=-1', '({})'.format(label_out), '@SP', 'A=M-1', 'M=D' ]
            cond_cnt = cond_cnt + 1
        elif tokens[0] == 'and':
            code = [ '@SP', 'AM=M-1', 'D=M', 'A=A-1', 'M=D&M' ]
        elif tokens[0] == 'or':
            code = [ '@SP', 'AM=M-1', 'D=M', 'A=A-1', 'M=D|M' ]
        elif tokens[0] == 'not':
            code = [ '@SP', 'A=M-1', 'M=!M' ]
        else:
            pass
        # Write code.
        f_asm.write(set_indent(code))

    # Clean up.
    f_asm.close() 
    logging.info("Done.")

if __name__ == '__main__':
    main()
