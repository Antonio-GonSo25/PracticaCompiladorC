"""Pruebas del analizador léxico de Mini C (proyecto 1)."""

import pytest

from minic.diagnostics.diagnostic import Diagnostic
from minic.lexer.lexer import Lexer
from minic.lexer.token import Token
from minic.lexer.token_type import TokenType
from minic.output.diagnostic_printer import format_diagnostic
from minic.output.token_printer import format_token


def test_section_7_valid_source() -> None:
    source = "int2 = 12abc;\nwhilex == -5"
    tokens, diagnostics = Lexer(source).scan()

    assert diagnostics == []

    expected_output = [
        "IDENTIFIER 'int2' 1 1",
        "ASSIGN '=' 1 6",
        "INTEGER_LITERAL '12' 1 8",
        "IDENTIFIER 'abc' 1 10",
        "SEMICOLON ';' 1 13",
        "IDENTIFIER 'whilex' 2 1",
        "EQUAL_EQUAL '==' 2 8",
        "MINUS '-' 2 11",
        "INTEGER_LITERAL '5' 2 12",
        "EOF '' 2 13",
    ]

    actual_output = [format_token(t) for t in tokens]
    assert actual_output == expected_output

    assert tokens[2].literal == 12
    assert tokens[8].literal == 5


def test_section_7_error_source() -> None:
    source = "int x = @;\nx ! = 0; // fin"
    tokens, diagnostics = Lexer(source).scan()

    expected_tokens = [
        "KW_INT 'int' 1 1",
        "IDENTIFIER 'x' 1 5",
        "ASSIGN '=' 1 7",
        "SEMICOLON ';' 1 10",
        "IDENTIFIER 'x' 2 1",
        "ASSIGN '=' 2 5",
        "INTEGER_LITERAL '0' 2 7",
        "SEMICOLON ';' 2 8",
        "IDENTIFIER 'fin' 2 13",
        "EOF '' 2 16",
    ]

    expected_diagnostics = [
        "LEX001 error 1:9 Carácter no reconocido: '@'",
        "LEX001 error 2:3 Carácter no reconocido: '!'",
        "LEX001 error 2:10 Carácter no reconocido: '/'",
        "LEX001 error 2:11 Carácter no reconocido: '/'",
    ]

    actual_tokens = [format_token(t) for t in tokens]
    actual_diagnostics = [format_diagnostic(d) for d in diagnostics]

    assert actual_tokens == expected_tokens
    assert actual_diagnostics == expected_diagnostics


def test_all_15_token_types() -> None:
    source = "int while x 123 = + - == != ( ) { } ;"
    tokens, diagnostics = Lexer(source).scan()

    assert diagnostics == []
    assert len(tokens) == 15  # 14 input tokens + 1 EOF

    expected_types = [
        TokenType.KW_INT,
        TokenType.KW_WHILE,
        TokenType.IDENTIFIER,
        TokenType.INTEGER_LITERAL,
        TokenType.ASSIGN,
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.EQUAL_EQUAL,
        TokenType.NOT_EQUAL,
        TokenType.LPAREN,
        TokenType.RPAREN,
        TokenType.LBRACE,
        TokenType.RBRACE,
        TokenType.SEMICOLON,
        TokenType.EOF,
    ]

    actual_types = [t.type for t in tokens]
    assert actual_types == expected_types


def test_integer_literal_values() -> None:
    source = "0 007 42"
    tokens, _ = Lexer(source).scan()

    assert tokens[0].literal == 0
    assert tokens[1].literal == 7
    assert tokens[2].literal == 42


def test_empty_source_emits_single_eof() -> None:
    tokens, diagnostics = Lexer("").scan()

    assert diagnostics == []
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF
    assert tokens[0].lexeme == ""
    assert tokens[0].line == 1
    assert tokens[0].column == 1


def test_positions_and_whitespace() -> None:
    source = "\t  \r\n  x"
    tokens, diagnostics = Lexer(source).scan()

    assert diagnostics == []
    assert len(tokens) == 2  # x and EOF
    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].lexeme == "x"
    assert tokens[0].line == 2
    assert tokens[0].column == 3


def test_example_valid() -> None:
    source = "int x = 10; while (x != 0) { x = x - 1; }"
    tokens, diagnostics = Lexer(source).scan()

    assert diagnostics == []
    assert tokens[-1].type == TokenType.EOF
