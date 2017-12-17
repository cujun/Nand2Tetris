#!/usr/bin/env python3

import logging
import os
import sys

import re




# Regular expressions matching each assembly command
RE_COMMANDS = (
    ( 'RE_COMMENT', re.compile(r"^//") ),
)

# Base RAM address for each segment
BASE_ADDRESS = {
    'static': 16,
    'stack': 256,
    'heap': 2048,
    'mmapio': 16384,
    'unused': 24575,
}




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

    ## Initializations.
    try:
        filenames_vm, outputname = [], ''
        if (sys.argv[1])[-3:] != '.vm':
            for fn in os.listdir(sys.argv[1]):
                fullpath = os.path.join(sys.argv[1], fn)
                if os.path.isfile(fullpath) and fullpath[-3:] == '.vm':
                    filenames_vm.append(fullpath)
            outputname = sys.argv[1] if sys.argv[1][-1] != '/' else sys.argv[1][:-1]
            outputname += '/' + outputname.split('/')[-1]
        else:
            filenames_vm.append(sys.argv[1])
            outputname = (sys.argv[1])[:-3]
        f_asm = open("{}.asm".format(outputname), 'w')
        cond_cnt = 0
    except IndexError:
        logging.error("Please properly enter the name of vm file or directory as an argument.")
        return
    except FileNotFoundError:
        logging.error("Could not read input: <{}>.".format(sys.argv[1]))
        return

    logging.info("Start translating <{}>.".format(sys.argv[1]))

    ## Bootstrap code.
    bootstrap_code = [ '@256', 'D=A', '@SP', 'M=D' ] # SP = 256
    bootstrap_code.extend([ '@RET{}_Sys.init'.format(cond_cnt), 'D=A', '@SP', 'AM=M+1', 'A=A-1', 'M=D' ]) # call Sys.init
    bootstrap_code.extend([ '@LCL', 'D=M', '@SP', 'AM=M+1', 'A=A-1', 'M=D' ])
    bootstrap_code.extend([ '@ARG', 'D=M', '@SP', 'AM=M+1', 'A=A-1', 'M=D' ])
    bootstrap_code.extend([ '@THIS', 'D=M', '@SP', 'AM=M+1', 'A=A-1', 'M=D' ])
    bootstrap_code.extend([ '@THAT', 'D=M', '@SP', 'AM=M+1', 'A=A-1', 'M=D' ])
    bootstrap_code.extend([ '@SP', 'D=M', '@LCL', 'M=D', '@5', 'D=D-A', '@ARG', 'M=D' ])
    bootstrap_code.extend([ '@Sys.init', '0;JMP', '(RET{}_Sys.init)'.format(cond_cnt) ])
    cond_cnt = cond_cnt + 1
    f_asm.write(set_indent(bootstrap_code))
    ## Actual code.
    for filename_vm in filenames_vm:
        logging.debug("vm file: <{}>".format(filename_vm))
        lines = list(filter(None, [line.strip() for line in open(filename_vm)]))
        curr_funcname = ''
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
                    code = [ '@{}'.format(BASE_ADDRESS['static'] + operand), 'D=M' ]
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
                    code = [ '@SP', 'AM=M-1', 'D=M', '@{}'.format(BASE_ADDRESS['static'] + operand), 'M=D' ]
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
            elif tokens[0] == 'label':
                labelname = tokens[1]
                code = [ '({}${})'.format(curr_funcname, labelname) ]
            elif tokens[0] == 'goto':
                labelname = tokens[1]
                code = [ '@{}${}'.format(curr_funcname, labelname), '0;JMP' ]
            elif tokens[0] == 'if-goto':
                labelname = tokens[1]
                code = [ '@SP', 'AM=M-1', 'D=M', '@{}${}'.format(curr_funcname, labelname), 'D;JNE' ]
            elif tokens[0] == 'function':
                funcname, cnt_localvar = tokens[1], int(tokens[2])
                curr_funcname = funcname
                code = [ '({})'.format(funcname), '@SP', 'A=M' ]
                for _ in range(cnt_localvar):
                    code.extend([ 'M=0', 'A=A+1' ])
                code.extend([ 'D=A', '@SP', 'M=D' ])
            elif tokens[0] == 'return':
                code = [ '@LCL', 'D=M', '@R13','M=D', '@5', 'A=D-A', 'D=M', '@R14', 'M=D', '@SP', 'A=M-1', 'D=M', '@ARG', 'A=M', 'M=D', 'D=A+1', '@SP', 'M=D' ]
                # Restore THAT, THIS, ARG, LCL
                code.extend([ '@R13', 'D=M-1', '@R15', 'AM=D', 'D=M', '@THAT', 'M=D' ])
                code.extend([ '@R15', 'AM=M-1', 'D=M', '@THIS', 'M=D' ])
                code.extend([ '@R15', 'AM=M-1', 'D=M', '@ARG', 'M=D' ])
                code.extend([ '@R15', 'AM=M-1', 'D=M', '@LCL', 'M=D' ])
                # goto return-address
                code.extend([ '@R14', 'A=M', '0;JMP' ])
            elif tokens[0] == 'call':
                funcname, cnt_arg = tokens[1], int(tokens[2])
                # Store RET, LCL, ARG, THIS, THAT
                code = [ '@RET{}_{}'.format(cond_cnt, funcname), 'D=A', '@SP', 'AM=M+1', 'A=A-1', 'M=D' ]
                code.extend([ '@LCL', 'D=M', '@SP', 'AM=M+1', 'A=A-1', 'M=D' ])
                code.extend([ '@ARG', 'D=M', '@SP', 'AM=M+1', 'A=A-1', 'M=D' ])
                code.extend([ '@THIS', 'D=M', '@SP', 'AM=M+1', 'A=A-1', 'M=D' ])
                code.extend([ '@THAT', 'D=M', '@SP', 'AM=M+1', 'A=A-1', 'M=D' ])
                # Set new ARG, LCL
                code.extend([ '@SP', 'D=M', '@LCL', 'M=D', '@{}'.format(cnt_arg), 'D=D-A', '@5', 'D=D-A', '@ARG', 'M=D' ])
                # goto function and label return
                code.extend([ '@{}'.format(funcname), '0;JMP', '(RET{}_{})'.format(cond_cnt, funcname) ])
                cond_cnt = cond_cnt + 1
            else:
                logging.error("Unexpected insturction... :(")
                return
            # Write code.
            f_asm.write(set_indent(code))
    ## Clean up.
    f_asm.close()

    logging.info("Done.")

if __name__ == '__main__':
    main()
