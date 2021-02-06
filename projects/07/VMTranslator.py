import os
import sys


def main():
    src_file_path = sys.argv[1]
    src_file_dir = os.path.dirname(src_file_path)
    src_file_name = os.path.basename(src_file_path)  # xxx.vm
    dest_file_path = os.path.join(src_file_dir, "%s.asm" % src_file_name[:-3])
    with open(src_file_path, "r") as f:
        parser = Parser(f)
        writer = CodeWriter(dest_file_path)
        writer.set_file_name(src_file_name[:-3])
        while parser.has_more_commands():
            parser.advance()
            if parser.command_type() == CommandType.C_ARITHMETIC:
                writer.write_arithmetic(parser.arg1())
            elif parser.command_type() == CommandType.C_PUSH:
                writer.write_push(parser.arg1(), parser.arg2())
            elif parser.command_type() == CommandType.C_POP:
                writer.write_pop(parser.arg1(), parser.arg2())
        writer.close()


class CommandType:
    C_ARITHMETIC = "C_ARITHMETIC"
    C_PUSH = "C_PUSH"
    C_POP = "C_POP"
    C_LABEL = "C_LABEL"
    C_GOTO = "C_GOTO"
    C_IF = "C_IF"
    C_FUNCTION = "C_FUNCTION"
    C_RETURN = "C_RETURN"
    C_CALL = "C_CALL"


class Command:
    ADD = "ADD"
    SUB = "SUB"
    NEG = "NEG"
    EQ = "EQ"
    GT = "GT"
    LT = "LT"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"

    PUSH = "PUSH"
    POP = "POP"

    COMMAND_TYPE_MAPPING = {
        ADD: CommandType.C_ARITHMETIC, 
        SUB: CommandType.C_ARITHMETIC, 
        NEG: CommandType.C_ARITHMETIC, 
        EQ: CommandType.C_ARITHMETIC, 
        GT: CommandType.C_ARITHMETIC, 
        LT: CommandType.C_ARITHMETIC, 
        AND: CommandType.C_ARITHMETIC, 
        OR: CommandType.C_ARITHMETIC, 
        NOT: CommandType.C_ARITHMETIC, 

        PUSH: CommandType.C_PUSH,
        POP: CommandType.C_POP,
    }


class Segment:
    ARGUMENT = "ARGUMENT"
    LOCAL = "LOCAL"
    STATIC = "STATIC"
    CONSTANT = "CONSTANT"
    THIS = "THIS"
    THAT = "THAT"
    POINTER = "POINTER"
    TEMP = "TEMP"

    SEGMENT_MAPPING = {
        ARGUMENT: ARGUMENT,
        LOCAL: LOCAL,
        STATIC: STATIC,
        CONSTANT: CONSTANT,
        THIS: THIS,
        THAT: THAT,
        POINTER: POINTER,
        TEMP: TEMP,
    }


class Parser:

    def __init__(self, src_file):
        self._src_file = src_file

        self._cur_line = ""
        self._cur_command_type = None
        self._cur_arg1 = None
        self._cur_arg2 = None

    def has_more_commands(self):
        if self._cur_line != "":
            return True
        while True:
            line = self._src_file.readline()
            if line == "":
                break
            line = line.strip()
            if line != "" and not line.startswith("//"):
                break
        self._cur_line = line
        return self._cur_line != ""

    def advance(self):
        cur_line = self._cur_line
        self._cur_line = ""

        parts = cur_line.split(" ")
        part0 = parts[0].strip().upper()
        if part0 in Command.COMMAND_TYPE_MAPPING:
            t = Command.COMMAND_TYPE_MAPPING[part0]
            self._cur_command_type = t
            if t == CommandType.C_ARITHMETIC:
                self._cur_arg1 = part0
                self._cur_arg2 = None
            elif t == CommandType.C_PUSH or t == CommandType.C_POP:
                segment = parts[1].strip().upper()
                if segment not in Segment.SEGMENT_MAPPING:
                    raise ValueError("unknown segment: %s" % parts[1])
                index = int(parts[2].strip())
                self._cur_arg1 = Segment.SEGMENT_MAPPING[segment]
                self._cur_arg2 = index
            else:
                raise NotImplementedError("%s is not implemented" % parts[0])
        else:
            raise ValueError("unkown command: %s" % parts[0])

    def command_type(self):
        return self._cur_command_type

    def arg1(self):
        return self._cur_arg1

    def arg2(self):
        return self._cur_arg2


class CodeWriter:
    push_argument_template = """\
@{index}
D=A
@ARG
D=D+M
@addr
M=D
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
"""
    push_local_template = """\
@{index}
D=A
@LCL
D=D+M
@addr
M=D
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
"""
    push_this_template = """\
@{index}
D=A
@THIS
D=D+M
@addr
M=D
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
"""
    push_that_template = """\
@{index}
D=A
@THAT
D=D+M
@addr
M=D
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
"""
    push_static_template = """\
@{file_name}.{index}
D=M
@SP
A=M
M=D
@SP
M=M+1
"""
    push_constant_template = """\
@{index}
D=A
@SP
A=M
M=D
@SP
M=M+1
"""
    push_pointer_template = """\
@{pointer}
D=M
@SP
A=M
M=D
@SP
M=M+1
"""
    push_temp_template = """\
@{index}
D=A
@5
D=D+A
@addr
M=D
@addr
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
"""

    pop_argument_template = """\
@{index}
D=A
@ARG
D=D+M
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
"""
    pop_local_template = """\
@{index}
D=A
@LCL
D=D+M
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
"""
    pop_this_template = """\
@{index}
D=A
@THIS
D=D+M
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
"""
    pop_that_template = """\
@{index}
D=A
@THAT
D=D+M
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
"""
    pop_static_template = """\
@SP
M=M-1
@SP
A=M
D=M
@{file_name}.{index}
M=D
"""
    pop_temp_template = """\
@{index}
D=A
@5
D=D+A
@addr
M=D
@SP
M=M-1
@SP
A=M
D=M
@addr
A=M
M=D
"""
    pop_pointer_template = """\
@SP
M=M-1
@SP
A=M
D=M
@{pointer}
M=D
"""

    add_code = """\
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D+M
@SP
A=M
M=D
@SP
M=M+1
"""
    sub_code = """\
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@SP
A=M
M=D
@SP
M=M+1
"""
    neg_code = """\
@SP
M=M-1
A=M
D=-M
@SP
A=M
M=D
@SP
M=M+1
"""
    eq_code = """\
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@{true_label}
D;JEQ
D=0
@{false_label}
0;JMP
({true_label})
D=-1
({false_label})
@SP
A=M
M=D
@SP
M=M+1
"""
    gt_code = """\
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@{true_label}
D;JGT
D=0
@{false_label}
0;JMP
({true_label})
D=-1
({false_label})
@SP
A=M
M=D
@SP
M=M+1
"""
    lt_code = """\
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@{true_label}
D;JLT
D=0
@{false_label}
0;JMP
({true_label})
D=-1
({false_label})
@SP
A=M
M=D
@SP
M=M+1
"""
    and_code = """\
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D&M
@SP
A=M
M=D
@SP
M=M+1
"""
    or_code = """\
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D|M
@SP
A=M
M=D
@SP
M=M+1
"""
    not_code = """\
@SP
M=M-1
A=M
D=!M
@SP
A=M
M=D
@SP
M=M+1
"""

    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(self.file_path, "w")

        self._compare_count = 0

    def set_file_name(self, file_name):
        self.file_name = file_name

    def _write(self, code):
        self.file.write(code)

    def write_arithmetic(self, command):
        """
        -1(0xffff) represents true and 0(0x0000) represents false
        """
        if command == Command.ADD:
            code = "// ADD\n%s" % self.add_code
        elif command == Command.SUB:
            code = "// SUB\n%s" % self.sub_code
        elif command == Command.NEG:
            code = "// NEG\n%s" % self.neg_code
        elif command == Command.EQ:
            code = "// EQ\n%s" % self.eq_code.format(
                true_label="TRUE_%d" % self._compare_count,
                false_label="FALSE_%d" % self._compare_count
            )
            self._compare_count += 1
        elif command == Command.GT:
            code = "// GT\n%s" % self.gt_code.format(
                true_label="TRUE_%d" % self._compare_count,
                false_label="FALSE_%d" % self._compare_count
            )
            self._compare_count += 1
        elif command == Command.LT:
            code = "// LT\n%s" % self.lt_code.format(
                true_label="TRUE_%d" % self._compare_count,
                false_label="FALSE_%d" % self._compare_count
            )
            self._compare_count += 1
        elif command == Command.AND:
            code = "// AND\n%s" % self.and_code
        elif command == Command.OR:
            code = "// OR\n%s" % self.or_code
        elif command == Command.NOT:
            code = "// NOT\n%s" % self.not_code

        self._write(code)

    def write_push(self, segment, index):
        """
        RAM[0] SP
        RAM[1] LCL
        RAM[2] ARG
        RAM[3] THIS
        RAM[4] THAT
        RAM[5-12] Holds the contents of the temp segment
        RAM[13-15] Can be used by the VM implementation as general purpose registers

        ARGUMENT(LOCAL, THIS, THAT):
        // push argument index
        // addr = ARG + index
        @index
        D=A
        @ARG
        D=D+M
        @addr
        M=D
        // *SP = *addr
        @addr
        A=M
        D=M
        @SP
        A=M
        M=D
        // SP++
        @SP
        M=M+1

        // pop argument index
        // addr = ARG + index
        @index
        D=A
        @ARG
        D=D+M
        @addr
        M=D
        // SP--
        @SP
        M=M-1
        // *addr = *SP
        @SP
        A=M
        D=M
        @addr
        A=M
        M=D

        CONSTANT
        // push constant i
        // *SP = i
        @i
        D=A
        @SP
        A=M
        M=D
        // SP++
        @SP
        M=M+1

        STATIC
        // file_name: test.vm
        // push static i
        @test.i
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1

        // pop static i
        @SP
        M=M-1
        @SP
        A=M
        D=M
        @test.i
        M=D

        TEMP
        // push temp index
        // addr = 5 + index
        @index
        D=A
        @5
        D=D+A
        @addr
        M=D
        // *SP = *addr
        @addr
        A=M
        D=M
        @SP
        A=M
        M=D
        // SP++
        @SP
        M=M+1

        // pop temp index
        // addr = 5 + index
        @index
        D=A
        @5
        D=D+A
        @addr
        M=D
        // SP--
        @SP
        M=M-1
        // *addr = *SP
        @SP
        A=M
        D=M
        @addr
        A=M
        M=D

        POINTER
        // push pointer 0/1 -> *SP = THIS/THAT, SP++
        // pop pointer 0/1 -> SP--, THIS/THAT = *SP

        // push pointer 0
        // *SP = THIS
        @THIS
        D=M
        @SP
        A=M
        M=D
        // SP++
        @SP
        M=M+1

        // push pointer 1
        // *SP = THAT
        @THAT
        D=M
        @SP
        A=M
        M=D
        // SP++
        @SP
        M=M+1

        // pop pointer 0
        // SP--
        @SP
        M=M-1
        // THIS = *SP
        @SP
        A=M
        D=M
        @THIS
        M=D

        // pop pointer 1
        // SP--
        @SP
        M=M-1
        // THAT = *SP
        @SP
        A=M
        D=M
        @THAT
        M=D
        """
        if segment == Segment.ARGUMENT:
            code = self.push_argument_template.format(index=index)
        elif segment == Segment.LOCAL:
            code = self.push_local_template.format(index=index)
        elif segment == Segment.THIS:
            code = self.push_this_template.format(index=index)
        elif segment == Segment.THAT:
            code = self.push_that_template.format(index=index)
        elif segment == Segment.STATIC:
            code = self.push_static_template.format(index=index, file_name=self.file_name)
        elif segment == Segment.CONSTANT:
            code = self.push_constant_template.format(index=index)
        elif segment == Segment.POINTER:
            pointer_mapping = {
                0: "THIS",
                1: "THAT",
            }
            code = self.push_pointer_template.format(pointer=pointer_mapping[index])
        elif segment == Segment.TEMP:
            code = self.push_temp_template.format(index=index)
        code = "// PUSH %s %s\n%s" % (segment, index, code)
        self._write(code)

    def write_pop(self, segment, index):
        if segment == Segment.ARGUMENT:
            code = self.pop_argument_template.format(index=index)
        elif segment == Segment.LOCAL:
            code = self.pop_local_template.format(index=index)
        elif segment == Segment.THIS:
            code = self.pop_this_template.format(index=index)
        elif segment == Segment.THAT:
            code = self.pop_that_template.format(index=index)
        elif segment == Segment.STATIC:
            code = self.pop_static_template.format(index=index, file_name=self.file_name)
        elif segment == Segment.POINTER:
            pointer_mapping = {
                0: "THIS",
                1: "THAT",
            }
            code = self.pop_pointer_template.format(pointer=pointer_mapping[index])
        elif segment == Segment.TEMP:
            code = self.pop_temp_template.format(index=index)
        code = "// POP %s %s\n%s" % (segment, index, code)
        self._write(code)

    def close(self):
        self.file.close()


if __name__ == "__main__":
    main()
