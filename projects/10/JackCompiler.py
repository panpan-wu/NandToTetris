"""
Whitespace and comments:
    Space characters, newline characters and comments are ignored.
    The following comment formats are supported:
    // Comment to end of line
    /* Comment until closing */
    /** API documentation comment */
Lexical elements:
    keyword:
        'class' | 'constructor' | 'function' | 'method' | 'field' | 'static' |
        'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' | 'false' |
        'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 'while' | 'return'
    symbol:
        '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | '-' |
        '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~'
    integer constant:
        A decimal number in the range 0..32767
    string constant:
        '"' A sequence of Unicode characters not including double quote or new line '"'
    identifier:
        A sequence of letters, digits, and underscore('_') not starting with a digit.
Program structure:
    class: 'class' className '{' classVarDec* subroutineDec* '}'
    classVarDec: ('static' | 'field') type varName(',' varName)* ';'
    type: 'int' | 'char' | 'boolean' | className
    subroutineDec: ('constructor' | 'function' | 'method')
                   ('void' | type) subroutineName '(' parameterList ')'
                   subroutineBody
    parameterList: ((type varName)(',' type varName)*)?
    subroutineBody: '{' varDec* statements '}'
    varDec: 'var' type varName (',' varName)* ';'
    className: identifier
    subroutineName: identifier
    varName: identifier

    statements: statement*
    statement: letStatement | ifStatement | whileStatement | doStatement | returnStatement
    letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    ifStatement: 'if' '(' expression ')' '{' statements '}'
                 ('else' '{' statements '}')?
    whileStatement: 'while' '(' expression ')' '{' statements '}'
    doStatement: 'do' subroutineCall ';'
    returnStatement: 'return' expression? ';'

    expression: term (op term)*
    term: integerConstant | stringConstant | keywordConstant | varName |
          varName'[' expression ']' | subroutineCall | '(' expression ')' |
          unaryOp term
    subroutineCall: subroutineName '(' expressionList ')' |
                    (className | varName) '.' subroutineName '(' expressionList ')'
    expressionList: (expression (',' expression)*)?
    op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    unaryOp: '~' | '-'
    keywordConstant: 'true' | 'false' | 'null' | 'this'
"""

import os
import sys
import string


def main():
    src_file = sys.argv[1]
    if os.path.isdir(src_file):
        for src_file_name in os.listdir(src_file):
            if src_file_name.endswith(".jack"):
                src_file_path = os.path.join(src_file, src_file_name)
                token_file_path = os.path.join(src_file, src_file_name[:-5] + "Token.xml")
                compilation_result_file_path = os.path.join(src_file, src_file_name[:-5] + "Compilation.xml")
                _compile(src_file_path, token_file_path, compilation_result_file_path)
    elif os.path.isfile(src_file) and src_file.endswith(".jack"):
        token_file_path = src_file[:-5] + "Token.xml"
        compilation_result_file_path = src_file[:-5] + "Compilation.xml"
        _compile(src_file, token_file_path, compilation_result_file_path)
    else:
        raise ValueError("only support file and directory")


def test():
    class Writer:
        def write(self, s):
            print(s, end="")

    src_file = "Square/Square.jack"
    with open(src_file, "r") as f:
        tokenizer = JackTokenizer(f)
        _write_token(tokenizer, Writer())

    with open(src_file, "r") as f:
        tokenizer = JackTokenizer(f)
        compilation_engine = CompilationEngine(tokenizer, Writer())
        compilation_engine.compile_class()
            

def _compile(src_file, token_file, compilation_result_file):
    with open(src_file, "r") as src, open(token_file, "w") as dest:
        tokenizer = JackTokenizer(src)
        _write_token(tokenizer, dest)
    with  open(src_file, "r") as src, open(compilation_result_file, "w") as dest:
        tokenizer = JackTokenizer(src)
        compilation_engine = CompilationEngine(tokenizer, dest)
        compilation_engine.compile_class()


def _write_token(tokenizer, writer):
    writer.write("<tokens>\n")
    while tokenizer.has_more_tokens():
        tokenizer.advance()
        t = tokenizer.token_type()
        if t == TokenType.KEYWORD:
            v = tokenizer.keyword()
            writer.write("<keyword> %s </keyword>\n" % v.lower())
        elif t == TokenType.IDENTIFIER:
            v = tokenizer.identifier()
            writer.write("<identifier> %s </identifier>\n" % v)
        elif t == TokenType.SYMBOL:
            v = tokenizer.symbol()
            writer.write("<symbol> %s </symbol>\n" % _escape(v))
        elif t == TokenType.INT_CONST:
            v = tokenizer.int_val()
            writer.write("<integerConstant> %s </integerConstant>\n" % v)
        elif t == TokenType.STRING_CONST:
            v = tokenizer.string_val()
            writer.write("<stringConstant> %s </stringConstant>\n" % v)
        else:
            raise ValueError("unsupported token type: %s" % t)
    writer.write("</tokens>\n")


def _escape(c):
    if c == "<":
        return "&lt;"
    elif c == ">":
        return "&gt;"
    elif c == "&":
        return "&amp;"
    return c


class JackAnalyzer:
    pass


class TokenType:
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    IDENTIFIER = "IDENTIFIER"
    INT_CONST = "INT_CONST"
    STRING_CONST = "STRING_CONST"


class Keyword:
    CLASS = "CLASS"
    CONSTRUCTOR = "CONSTRUCTOR"
    FUNCTION = "FUNCTION"
    METHOD = "METHOD"
    FIELD = "FIELD"
    STATIC = "STATIC"
    VAR = "VAR"
    INT = "INT"
    CHAR = "CHAR"
    BOOLEAN = "BOOLEAN"
    VOID = "VOID"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NULL = "NULL"
    THIS = "THIS"
    LET = "LET"
    DO = "DO"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    RETURN = "RETURN"


class JackTokenizer:
    keywords = (
        "class", "constructor", "function", "method", "field", "static",
        "var", "int", "char", "boolean", "void", "true", "false",
        "null", "this", "let", "do", "if", "else", "while", "return",
    )
    symbols = (
        "{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-",
        "*", "/", "&", "|", "<", ">", "=", "~",
    )
    digits = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    letters = string.ascii_letters

    def __init__(self, file_obj):
        self.f = file_obj

        self._token_type = ""

        self._chars = ""
        self._char_index = 0
        self._leader_char = ""

        self._token_type = ""
        self._keyword = ""
        self._int_val = 0
        self._string_val = ""
        self._symbol = ""
        self._identifier = ""

        self._next_token_type = ""
        self._next_keyword = ""
        self._next_int_val = 0
        self._next_string_val = ""
        self._next_symbol = ""
        self._next_identifier = ""

    def _has_more_chars(self):
        if self._char_index == len(self._chars):
            self._chars = self.f.read(1024)
            self._char_index = 0
        if not self._chars:
            return False
        return True

    def _next_char(self):
        c = self._chars[self._char_index]
        self._char_index += 1
        return c

    def _look_up_next_char(self):
        return self._chars[self._char_index]

    def _parse_next_token(self):
        if self._leader_char == "":
            if self._has_more_chars():
                self._leader_char = self._next_char()
        if self._leader_char == "":
            return

        c = self._leader_char
        if c in self.digits:
            self._parse_integer()
        elif c == '"':
            self._parse_string()
        elif (c in self.letters) or (c == "_"):
            self._parse_identifier()
        elif c in (" ", "\t", "\n"):
            self._leader_char = ""
            self._parse_next_token()
        elif c == "/":
            if self._has_more_chars():
                next_char = self._look_up_next_char()
                if next_char == "/":
                    self._leader_char = self._next_char()
                    self._parse_one_line_comment()
                    self._parse_next_token()
                elif next_char == "*":
                    self._leader_char = self._next_char()
                    self._parse_multi_line_comment()
                    self._parse_next_token()
                else:
                    self._parse_symbol()
            else:
                self._parse_symbol()
        elif c in self.symbols:
            self._parse_symbol()
        else:
            raise ValueError("unsupported char: %s" % c)

    def _parse_integer(self):
        """
        A decimal number in the range 0..32767
        """
        token = self._leader_char
        self._leader_char = ""
        while self._has_more_chars():
            c = self._next_char()
            if c in self.digits:
                token += c
            else:
                self._leader_char = c
                break

        d = int(token)
        if d > 32767:
            raise ValueError("the number: %s is too big" % token)

        self._next_token_type = TokenType.INT_CONST
        self._next_int_val = d

    def _parse_string(self):
        """
        '"' A sequence of Unicode characters not including double quote or new line '"'
        """
        token = ""
        self._leader_char = ""
        while self._has_more_chars():
            c = self._next_char()
            if c == "\n":
                raise ValueError("string can't include new line")
            elif c == '"':
                break
            else:
                token += c

        self._next_token_type = TokenType.STRING_CONST
        self._next_string_val = token

    def _parse_identifier(self):
        """
        A sequence of letters, digits, and underscore('_') not starting with a digit.
        """
        token = self._leader_char
        self._leader_char = ""
        while self._has_more_chars():
            c = self._next_char()
            if c in self.letters or c in self.digits or c == "_":
                token += c
            else:
                self._leader_char = c
                break
        if token in self.keywords:
            self._next_token_type = TokenType.KEYWORD
            self._next_keyword = token.upper()
        else:
            self._next_token_type = TokenType.IDENTIFIER
            self._next_identifier = token

    def _parse_symbol(self):
        token = self._leader_char
        self._leader_char = ""

        self._next_token_type = TokenType.SYMBOL
        self._next_symbol = token

    def _parse_one_line_comment(self):
        self._leader_char = ""
        while self._has_more_chars():
            c = self._next_char()
            if c == "\n":
                break

    def _parse_multi_line_comment(self):
        self._leader_char = ""
        end_comment = False
        while self._has_more_chars():
            c1 = self._next_char()
            if c1 == "*":
                if self._has_more_chars():
                    c2 = self._look_up_next_char()
                    if c2 == "/":
                        self._next_char()
                        end_comment = True
                        break

        if not end_comment:
            raise ValueError("the format of multi line comment is wrong")

    def has_more_tokens(self):
        if self._next_token_type:
            return True

        self._next_token_type = ""
        self._next_keyword = ""
        self._next_int_val = 0
        self._next_string_val = ""
        self._next_symbol = ""
        self._next_identifier = ""

        self._parse_next_token()
        if self._next_token_type:
            return True
        return False

    def advance(self):
        if self._next_token_type:
            self._token_type = self._next_token_type
            self._keyword = self._next_keyword
            self._int_val = self._next_int_val
            self._string_val = self._next_string_val
            self._symbol = self._next_symbol
            self._identifier = self._next_identifier

            self._next_token_type = ""

    def look_up_next_token(self):
        if self._next_token_type:
            self._token_type = self._next_token_type
            self._keyword = self._next_keyword
            self._int_val = self._next_int_val
            self._string_val = self._next_string_val
            self._symbol = self._next_symbol
            self._identifier = self._next_identifier

    def token_type(self):
        return self._token_type

    def keyword(self):
        return self._keyword

    def symbol(self):
        return self._symbol

    def identifier(self):
        return self._identifier

    def int_val(self):
        return self._int_val

    def string_val(self):
        return self._string_val


class CompilationEngine:

    def __init__(self, parser, writer):
        self.parser = parser
        self.writer = writer

        self._space_number = 0
        self._indent = 2

    def _write(self, s):
        s += "\n"
        self.writer.write(s)

    def _write_keyword(self, keyword):
        self._write(self._space_number * " " + "<keyword> %s </keyword>" % keyword.lower())

    def _write_identifier(self, identifier):
        self._write(self._space_number * " " + "<identifier> %s </identifier>" % identifier)

    def _write_symbol(self, symbol):
        self._write(self._space_number * " " + "<symbol> %s </symbol>" % _escape(symbol))

    def compile_class(self):
        """
        class: 'class' className '{' classVarDec* subroutineDec* '}'
        """
        self._write(self._space_number * " " + "<class>")
        self._space_number += self._indent

        self._consume_keyword(Keyword.CLASS)
        self._consume_identifier()
        self._consume_symbol("{")
        # classVarDec*
        while self._the_next_token_is_keyword(Keyword.STATIC, Keyword.FIELD):
            self.compile_class_var_dec()
        # subroutineDec*
        while self._the_next_token_is_keyword(Keyword.CONSTRUCTOR, Keyword.FUNCTION, Keyword.METHOD):
            self.compile_subroutine_dec()
        self._consume_symbol("}")

        self._space_number -= 2
        self._write(self._space_number * " " + "</class>")

    def compile_class_var_dec(self):
        """
        classVarDec: ('static' | 'field') type varName(',' varName)* ';'
        type: 'int' | 'char' | 'boolean' | className
        """
        self._write(self._space_number * " " + "<classVarDec>")
        self._space_number += self._indent

        self._consume_keyword(Keyword.STATIC, Keyword.FIELD)
        self._consume_type()
        self._consume_identifier()
        # (',' varName)*
        while self._the_next_token_is_symbol(","):
            self._consume_symbol(",")
            self._consume_identifier()
        self._consume_symbol(";")

        self._space_number -= 2
        self._write(self._space_number * " " + "</classVarDec>")

    def compile_subroutine_dec(self):
        """
        subroutineDec: ('constructor' | 'function' | 'method')
                       ('void' | type) subroutineName '(' parameterList ')'
                       subroutineBody
        type: 'int' | 'char' | 'boolean' | className
        subroutineBody: '{' varDec* statements '}'
        """
        self._write(self._space_number * " " + "<subroutineDec>")
        self._space_number += self._indent

        self._consume_keyword(Keyword.CONSTRUCTOR, Keyword.FUNCTION, Keyword.METHOD)
        self._consume_void_or_type()
        self._consume_identifier()
        self._consume_symbol("(")
        self.compile_parameter_list()
        self._consume_symbol(")")

        self._write(self._space_number * " " + "<subroutineBody>")
        self._space_number += self._indent

        self._consume_symbol("{")
        # varDec*
        while self._the_next_token_is_keyword(Keyword.VAR):
            self.compile_var_dec()
        self.compile_statements()
        self._consume_symbol("}")

        self._space_number -= 2
        self._write(self._space_number * " " + "</subroutineBody>")

        self._space_number -= 2
        self._write(self._space_number * " " + "</subroutineDec>")

    def compile_parameter_list(self):
        """
        parameterList: ((type varName)(',' type varName)*)?
        type: 'int' | 'char' | 'boolean' | className
        """
        self._write(self._space_number * " " + "<parameterList>")
        self._space_number += self._indent

        if self._the_next_token_is_type():
            self._consume_type()
            self._consume_identifier()
            while self._the_next_token_is_symbol(","):
                self._consume_symbol(",")
                self._consume_type()
                self._consume_identifier()

        self._space_number -= 2
        self._write(self._space_number * " " + "</parameterList>")

    def compile_var_dec(self):
        """
        varDec: 'var' type varName (',' varName)* ';'
        type: 'int' | 'char' | 'boolean' | className
        """
        self._write(self._space_number * " " + "<varDec>")
        self._space_number += self._indent

        self._consume_keyword(Keyword.VAR)
        self._consume_type()
        self._consume_identifier()
        # (',' varName)*
        while self._the_next_token_is_symbol(","):
            self._consume_symbol(",")
            self._consume_identifier()
        self._consume_symbol(";")

        self._space_number -= 2
        self._write(self._space_number * " " + "</varDec>")

    def compile_statements(self):
        """
        statements: statement*
        statement: letStatement | ifStatement | whileStatement | doStatement | returnStatement
        """
        self._write(self._space_number * " " + "<statements>")
        self._space_number += self._indent

        while self.parser.has_more_tokens():
            self.parser.look_up_next_token()
            t = self.parser.token_type()
            if t == TokenType.KEYWORD:
                v = self.parser.keyword()
                if v == Keyword.LET:
                    self.compile_let()
                elif v == Keyword.IF:
                    self.compile_if()
                elif v == Keyword.WHILE:
                    self.compile_while()
                elif v == Keyword.DO:
                    self.compile_do()
                elif v == Keyword.RETURN:
                    self.compile_return()
                else:
                    break
            else:
                break

        self._space_number -= 2
        self._write(self._space_number * " " + "</statements>")

    def compile_do(self):
        """
        doStatement: 'do' subroutineCall ';'
        subroutineCall: subroutineName '(' expressionList ')' |
                        (className | varName) '.' subroutineName '(' expressionList ')'
        """
        self._write(self._space_number * " " + "<doStatement>")
        self._space_number += self._indent

        self._consume_keyword(Keyword.DO)

        # subroutineCall
        self._consume_identifier()
        if self._the_next_token_is_symbol("."):
            self._consume_symbol(".")
            self._consume_identifier()
        self._consume_symbol("(")
        self.compile_expression_list()
        self._consume_symbol(")")

        self._consume_symbol(";")

        self._space_number -= 2
        self._write(self._space_number * " " + "</doStatement>")

    def compile_let(self):
        """
        letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
        """
        self._write(self._space_number * " " + "<letStatement>")
        self._space_number += self._indent

        self._consume_keyword(Keyword.LET)
        self._consume_identifier()
        if self._the_next_token_is_symbol("["):
            self._consume_symbol("[")
            self.compile_expression()
            self._consume_symbol("]")
        self._consume_symbol("=")
        self.compile_expression()
        self._consume_symbol(";")

        self._space_number -= 2
        self._write(self._space_number * " " + "</letStatement>")

    def compile_while(self):
        """
        whileStatement: 'while' '(' expression ')' '{' statements '}'
        """
        self._write(self._space_number * " " + "<whileStatement>")
        self._space_number += self._indent

        self._consume_keyword(Keyword.WHILE)
        self._consume_symbol("(")
        self.compile_expression()
        self._consume_symbol(")")
        self._consume_symbol("{")
        self.compile_statements()
        self._consume_symbol("}")

        self._space_number -= 2
        self._write(self._space_number * " " + "</whileStatement>")

    def compile_return(self):
        """
        returnStatement: 'return' expression? ';'
        """
        self._write(self._space_number * " " + "<returnStatement>")
        self._space_number += self._indent

        self._consume_keyword(Keyword.RETURN)
        if not self._the_next_token_is_symbol(";"):
            self.compile_expression()
        self._consume_symbol(";")

        self._space_number -= 2
        self._write(self._space_number * " " + "</returnStatement>")

    def compile_if(self):
        """
        ifStatement: 'if' '(' expression ')' '{' statements '}'
                     ('else' '{' statements '}')?
        """
        self._write(self._space_number * " " + "<ifStatement>")
        self._space_number += self._indent

        self._consume_keyword(Keyword.IF)
        self._consume_symbol("(")
        self.compile_expression()
        self._consume_symbol(")")
        self._consume_symbol("{")
        self.compile_statements()
        self._consume_symbol("}")
        if self._the_next_token_is_keyword(Keyword.ELSE):
            self._consume_keyword(Keyword.ELSE)
            self._consume_symbol("{")
            self.compile_statements()
            self._consume_symbol("}")

        self._space_number -= 2
        self._write(self._space_number * " " + "</ifStatement>")

    def compile_expression(self):
        """
        expression: term (op term)*
        op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
        """
        self._write(self._space_number * " " + "<expression>")
        self._space_number += self._indent

        self.compile_term()
        op = ("+", "-", "*", "/", "&", "|", "<", ">", "=")
        while self._the_next_token_is_symbol(*op):
            self._consume_symbol(*op)
            self.compile_term()

        self._space_number -= 2
        self._write(self._space_number * " " + "</expression>")

    def compile_term(self):
        """
        term: integerConstant | stringConstant | keywordConstant | varName |
              varName'[' expression ']' | subroutineCall | '(' expression ')' |
              unaryOp term
        keywordConstant: 'true' | 'false' | 'null' | 'this'
        unaryOp: '~' | '-'
        subroutineCall: subroutineName '(' expressionList ')' |
                        (className | varName) '.' subroutineName '(' expressionList ')'
        """
        self._write(self._space_number * " " + "<term>")
        self._space_number += self._indent

        legal = False
        if self.parser.has_more_tokens():
            self.parser.advance()
            t = self.parser.token_type()
            if t == TokenType.INT_CONST:
                v = self.parser.int_val()
                self._write(self._space_number * " " + "<integerConstant> %s </integerConstant>" % v)
                legal = True
            elif t == TokenType.STRING_CONST:
                v = self.parser.string_val()
                self._write(self._space_number * " " + "<stringConstant> %s </stringConstant>" % v)
                legal = True
            elif t == TokenType.KEYWORD:
                v = self.parser.keyword()
                if v in (Keyword.TRUE, Keyword.FALSE, Keyword.NULL, Keyword.THIS):
                    self._write_keyword(v)
                    legal = True
            elif t == TokenType.IDENTIFIER:
                v = self.parser.identifier()
                self._write_identifier(v)
                if self._the_next_token_is_symbol("["):
                    self._consume_symbol("[")
                    self.compile_expression()
                    self._consume_symbol("]")
                elif self._the_next_token_is_symbol("("):
                    self._consume_symbol("(")
                    self.compile_expression_list()
                    self._consume_symbol(")")
                elif self._the_next_token_is_symbol("."):
                    self._consume_symbol(".")
                    self._consume_identifier()
                    self._consume_symbol("(")
                    self.compile_expression_list()
                    self._consume_symbol(")")
                legal = True
            elif t == TokenType.SYMBOL:
                v = self.parser.symbol()
                self._write_symbol(v)
                if v in "~-":
                    self.compile_term()
                    legal = True
                elif v == "(":
                    self.compile_expression()
                    self._consume_symbol(")")
                    legal = True

        if not legal:
            raise ValueError("syntax error")

        self._space_number -= 2
        self._write(self._space_number * " " + "</term>")

    def compile_expression_list(self):
        """
        expressionList: (expression (',' expression)*)?
        expression: term (op term)*
        op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
        term: integerConstant | stringConstant | keywordConstant | varName |
              varName'[' expression ']' | subroutineCall | '(' expression ')' |
              unaryOp term
        """
        self._write(self._space_number * " " + "<expressionList>")
        self._space_number += self._indent

        meet_expression = False
        if self.parser.has_more_tokens():
            self.parser.look_up_next_token()
            t = self.parser.token_type()
            if t == TokenType.INT_CONST:
                meet_expression = True
            elif t == TokenType.STRING_CONST:
                meet_expression = True
            elif t == TokenType.KEYWORD:
                v = self.parser.keyword()
                if v in (Keyword.TRUE, Keyword.FALSE, Keyword.NULL, Keyword.THIS):
                    meet_expression = True
            elif t == TokenType.IDENTIFIER:
                meet_expression = True
            elif t == TokenType.SYMBOL:
                v = self.parser.symbol()
                if v in "~-(":
                    meet_expression = True

        if meet_expression:
            self.compile_expression()
            while self._the_next_token_is_symbol(","):
                self._consume_symbol(",")
                self.compile_expression()

        self._space_number -= 2
        self._write(self._space_number * " " + "</expressionList>")

    def _consume_identifier(self):
        legal = False
        if self.parser.has_more_tokens():
            self.parser.advance()
            t = self.parser.token_type()
            if t == TokenType.IDENTIFIER:
                v = self.parser.identifier()
                self._write_identifier(v)
                legal = True
        if not legal:
            raise ValueError("syntax error")

    def _consume_keyword(self, *args):
        legal = False
        if self.parser.has_more_tokens():
            self.parser.advance()
            t = self.parser.token_type()
            if t == TokenType.KEYWORD:
                v = self.parser.keyword()
                if (not args) or (v in args):
                    self._write_keyword(v)
                    legal = True
        if not legal:
            raise ValueError("syntax error")

    def _consume_symbol(self, *args):
        legal = False
        if self.parser.has_more_tokens():
            self.parser.advance()
            t = self.parser.token_type()
            if t == TokenType.SYMBOL:
                v = self.parser.symbol()
                if (not args) or (v in args):
                    self._write_symbol(v)
                    legal = True
        if not legal:
            raise ValueError("syntax error")

    def _consume_type(self):
        legal = False
        if self.parser.has_more_tokens():
            self.parser.advance()
            t = self.parser.token_type()
            if t == TokenType.KEYWORD:
                v = self.parser.keyword()
                if v == Keyword.INT or v == Keyword.CHAR or v == Keyword.BOOLEAN:
                    self._write_keyword(v)
                    legal = True
            elif t == TokenType.IDENTIFIER:
                v = self.parser.identifier()
                self._write_identifier(v)
                legal = True
        if not legal:
            raise ValueError("syntax error")

    def _consume_void_or_type(self):
        legal = False
        if self.parser.has_more_tokens():
            self.parser.advance()
            t = self.parser.token_type()
            if t == TokenType.KEYWORD:
                v = self.parser.keyword()
                if v == Keyword.VOID or v == Keyword.INT or v == Keyword.CHAR or v == Keyword.BOOLEAN:
                    self._write_keyword(v)
                    legal = True
            elif t == TokenType.IDENTIFIER:
                v = self.parser.identifier()
                self._write_identifier(v)
                legal = True
        if not legal:
            raise ValueError("syntax error")

    def _the_next_token_is_type(self):
        if self.parser.has_more_tokens():
            self.parser.look_up_next_token()
            t = self.parser.token_type()
            if t == TokenType.KEYWORD:
                v = self.parser.keyword()
                if v == Keyword.INT or v == Keyword.CHAR or v == Keyword.BOOLEAN:
                    return True
            elif t == TokenType.IDENTIFIER:
                return True
        return False

    def _the_next_token_is_symbol(self, *args):
        if self.parser.has_more_tokens():
            self.parser.look_up_next_token()
            t = self.parser.token_type()
            if t == TokenType.SYMBOL:
                v = self.parser.symbol()
                if (not args) or (v in args):
                    return True
        return False

    def _the_next_token_is_keyword(self, *args):
        if self.parser.has_more_tokens():
            self.parser.look_up_next_token()
            t = self.parser.token_type()
            if t == TokenType.KEYWORD:
                v = self.parser.keyword()
                if (not args) or (v in args):
                    return True
        return False


if __name__ == "__main__":
    main()
