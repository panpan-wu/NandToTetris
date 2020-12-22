import sys


def main():
    file_path = sys.argv[1]
    hack_assembler = HackAssembler(file_path)
    hack_assembler.assemble()


class HackAssembler:
    VARIABLE_START_ADDRESS = 16
    DEFAULT_SYMBOL_TABLE = {
        "R0": 0, 
        "R1": 1, 
        "R2": 2, 
        "R3": 3, 
        "R4": 4, 
        "R5": 5, 
        "R6": 6, 
        "R7": 7, 
        "R8": 8, 
        "R9": 9, 
        "R10": 10, 
        "R11": 11, 
        "R12": 12, 
        "R13": 13, 
        "R14": 14, 
        "R15": 15, 
        "SCREEN": 16384,
        "KDB": 24576,
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
    }

    def __init__(self, file_path):
        self._file_path = file_path
        self._dest_file_path = self._file_path.split(".")[0] + ".hack"

        self._symbol_table = {}
        self._symbol_table.update(self.DEFAULT_SYMBOL_TABLE)
        self._lines = []
        self._variable_address = self.VARIABLE_START_ADDRESS

    def assemble(self):
        next_line_number = 0
        with open(self._file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line == "":
                    continue
                elif line.startswith("//"):
                    continue
                else:
                    line = line.split("//")[0].strip()
                    if line.startswith("(") and line.endswith(")"):
                        self._symbol_table[line[1:-1]] = next_line_number
                    else:
                        self._lines.append(line)
                        next_line_number += 1

        with open(self._dest_file_path, "w") as f:
            for line in self._lines:
                if line.startswith("@"):
                    symbol = line[1:]
                    if symbol.isdigit():
                        value = int(symbol)
                    else:
                        if symbol not in self._symbol_table:
                            self._symbol_table[symbol] = self._variable_address
                            self._variable_address += 1
                        value = self._symbol_table[symbol]
                    # @value -> 0vvv vvvv vvvv vvvv
                    code = "{0:016b}".format(value)
                else:
                    code = CInstruction(line).code()
                f.write(code + "\n")


class CInstruction:
    """
    dest=comp;jump -> 111a c1c2c3c4 c5c6d1d2 d3j1j2j3 
    """
    code_template = "111{comp}{dest}{jump}"
    comp_table = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "-D": "0001111",
        "-A": "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",

        "M": "1110000",
        "!M": "1110001",
        "-M": "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101",
    }
    dest_table = {
        "null": "000",
        "M": "001",
        "D": "010", 
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111",
    }
    jump_table = {
        "null": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111",
    }

    def __init__(self, instruction):
        self.comp, self.dest, self.jump = self._parse(instruction)

    def _parse(self, instruction):
        comp = None
        dest = "null"
        jump = "null"
        if ";" in instruction:
            left, right = instruction.split(";")
            jump = right
        else:
            left = instruction
        if "=" in left:
            dest, comp = left.split("=")
        else:
            comp = left
        return comp.strip(), dest.strip(), jump.strip()

    def code(self):
        return self.code_template.format(
            comp=self.comp_table[self.comp],       
            dest=self.dest_table[self.dest],
            jump=self.jump_table[self.jump]
        )


if __name__ == "__main__":
    main()
