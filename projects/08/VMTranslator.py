import os
import sys


def main():
    src_file = sys.argv[1]
    if os.path.isdir(src_file):
        dest_file_name = os.path.basename(src_file) + ".asm"
        dest_file_path = os.path.join(src_file, dest_file_name)
        writer = CodeWriter(dest_file_path)
        writer.write_init()
        for src_file_name in os.listdir(src_file):
            if src_file_name.endswith(".vm"):
                src_file_path = os.path.join(src_file, src_file_name)
                _write_one_file(writer, src_file_path, src_file_name[:-3])
    else:
        src_file_name = os.path.basename(src_file)
        dest_file_name = src_file_name[:-3] + ".asm"
        dest_file_path = os.path.join(os.path.dirname(src_file), dest_file_name)
        writer = CodeWriter(dest_file_path)
        writer.write_init()
        _write_one_file(writer, src_file, src_file_name[:-3])

    writer.close()


def _write_one_file(writer, src_file_path, src_file_name):
    with open(src_file_path, "r") as f:
        parser = Parser(f)
        writer.set_file_name(src_file_name)
        while parser.has_more_commands():
            parser.advance()
            if parser.command_type() == CommandType.C_ARITHMETIC:
                writer.write_arithmetic(parser.arg1())
            elif parser.command_type() == CommandType.C_PUSH:
                writer.write_push(parser.arg1(), parser.arg2())
            elif parser.command_type() == CommandType.C_POP:
                writer.write_pop(parser.arg1(), parser.arg2())
            elif parser.command_type() == CommandType.C_LABEL:
                writer.write_label(parser.arg1())
            elif parser.command_type() == CommandType.C_GOTO:
                writer.write_goto(parser.arg1())
            elif parser.command_type() == CommandType.C_IF:
                writer.write_if(parser.arg1())
            elif parser.command_type() == CommandType.C_FUNCTION:
                writer.write_function(parser.arg1(), parser.arg2())
            elif parser.command_type() == CommandType.C_RETURN:
                writer.write_return()
            elif parser.command_type() == CommandType.C_CALL:
                writer.write_call(parser.arg1(), parser.arg2())
            else:
                raise ValueError("unsupported command type: %s" % parser.command_type())
        

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

    LABEL = "LABEL"
    GOTO = "GOTO"
    IF_GOTO = "IF-GOTO"
    FUNCTION = "FUNCTION"
    RETURN = "RETURN"
    CALL = "CALL"

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

        LABEL: CommandType.C_LABEL,
        GOTO: CommandType.C_GOTO,
        IF_GOTO: CommandType.C_IF,
        FUNCTION: CommandType.C_FUNCTION,
        RETURN: CommandType.C_RETURN,
        CALL: CommandType.C_CALL,
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

        self._function_name = None

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

        i = cur_line.find("//")
        if i > 0:
            cur_line = cur_line[:i]

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
            elif t == CommandType.C_LABEL or t == CommandType.C_GOTO or t == CommandType.C_IF:
                label_name = parts[1].strip()
                if self._function_name is not None:
                    label_name = "%s$%s" % (self._function_name, label_name)
                self._cur_arg1 = label_name
            elif t == CommandType.C_FUNCTION:
                function_name = parts[1].strip()
                num_locals = int(parts[2].strip())
                self._function_name = function_name
                self._cur_arg1 = function_name
                self._cur_arg2 = num_locals
            elif t == CommandType.C_RETURN:
                pass
            elif t == CommandType.C_CALL:
                function_name = parts[1].strip()
                num_args = int(parts[2].strip())
                self._cur_arg1 = function_name
                self._cur_arg2 = num_args
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

        self._return_address_index = 0

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

    def write_init(self):
        """
        SP=256
        call Sys.init
        """
        set_sp = (
            "@256\n"
            "D=A\n"
            "@SP\n"
            "M=D\n"
        )
        self._write(set_sp)
        self.write_call("Sys.init", 0)

    def write_label(self, label):
        code = "({label})\n".format(label=label)
        self._write(code)

    def write_goto(self, label):
        code = (
            "@{label}\n"        
            "0;JMP\n"
        ).format(label=label)
        code = "// GOTO %s\n%s" % (label, code)
        self._write(code)

    def write_if(self, label):
        code = (
            "@SP\n"        
            "M=M-1\n"
            "A=M\n"
            "D=M\n"
            "@{label}\n"
            "D;JNE\n"
        ).format(label=label)
        code = "// IF-GOTO %s\n%s" % (label, code)
        self._write(code)

    def write_call(self, function_name, num_args):
        """
        push return-address
        push LCL
        push ARG
        push THIS
        push THAT
        ARG = SP - num_args - 5
        LCL = SP
        goto function_name
        (return-address)
        """
        def push_d():
            return (
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "@SP\n"
                "M=M+1\n"
            )
        return_address = "%s$return%s" % (function_name, self._return_address_index)
        push_return_address = (
            "@{return_address}\n"            
            "D=A\n"
        ).format(return_address=return_address) + push_d()

        t = "@{name}\nD=M\n" + push_d()
        push_lcl = t.format(name="LCL")
        push_arg = t.format(name="ARG")
        push_this = t.format(name="THIS")
        push_that = t.format(name="THAT")

        arg = (
            "@SP\n"        
            "D=M\n"
            "@{num_args}\n"
            "D=D-A\n"
            "@5\n"
            "D=D-A\n"
            "@ARG\n"
            "M=D\n"
        ).format(num_args=num_args)

        lcl = (
            "@SP\n"        
            "D=M\n"
            "@LCL\n"
            "M=D\n"
        )

        self._write(push_return_address)
        self._write(push_lcl)
        self._write(push_arg)
        self._write(push_this)
        self._write(push_that)
        self._write(arg)
        self._write(lcl)
        self.write_goto(function_name)
        self._write("(%s)\n" % return_address)

        self._return_address_index += 1
        
    def write_return(self):
        """
        FRAME = LCL
        RET = *(FRAME - 5)
        *ARG = pop()
        SP = ARG + 1
        THAT = *(FRAME - 1)
        THIS = *(FRAME - 2)
        ARG = *(FRAME - 3)
        LCL = *(FRAME - 4)
        goto RET
        """
        frame = (
            "@LCL\n"
            "D=M\n"
            "@frame\n"
            "M=D\n"
        )
        ret = (
            "@frame\n"
            "D=M\n"
            "@5\n"
            "D=D-A\n"
            "A=D\n"
            "D=M\n"
            "@ret\n"
            "M=D\n"
        )
        set_return_value = (
            "@SP\n"
            "M=M-1\n"
            "A=M\n"
            "D=M\n"
            "@ARG\n"
            "A=M\n"
            "M=D\n"
        )
        set_sp = (
            "@ARG\n"
            "D=M+1\n"
            "@SP\n"
            "M=D\n"
        )
        that = (
            "@frame\n"
            "D=M\n"
            "@1\n"
            "D=D-A\n"
            "A=D\n"
            "D=M\n"
            "@THAT\n"
            "M=D\n"
        )
        this = (
            "@frame\n"
            "D=M\n"
            "@2\n"
            "D=D-A\n"
            "A=D\n"
            "D=M\n"
            "@THIS\n"
            "M=D\n"
        )
        arg = (
            "@frame\n"
            "D=M\n"
            "@3\n"
            "D=D-A\n"
            "A=D\n"
            "D=M\n"
            "@ARG\n"
            "M=D\n"
        )
        lcl = (
            "@frame\n"
            "D=M\n"
            "@4\n"
            "D=D-A\n"
            "A=D\n"
            "D=M\n"
            "@LCL\n"
            "M=D\n"
        )
        goto_caller = (
            "@ret\n"
            "A=M\n"
            "0;JMP\n"
        )
        code = frame + ret + set_return_value + set_sp + that + this + arg + lcl + goto_caller
        self._write(code)

    def write_function(self, function_name, num_locals):
        self._write("(%s)\n" % function_name)
        for _ in range(num_locals):
            self.write_push(Segment.CONSTANT, 0)

    def close(self):
        self.file.close()


if __name__ == "__main__":
    main()
