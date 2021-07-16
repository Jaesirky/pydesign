"""This is a mini text caculator interpreter

Here is the grammar:
    expression ::= func | value | group | `(` expression `)`
    func ::= sin(expression)|cos(expression)|tan(expression)|cos(expression)|
    value ::= 1.0 | nan

Author: Jaesirky
Email: jaesirky@163.com
License: MIT
Version: 0.0.1
"""

import re
import math
from typing import *


class Expression:
    pattern: re.Pattern = None

    def interpret(self, text: str) -> float:
        match = self.pattern.match(text)
        if not match:
            raise Exception('unkown error')
        data = match.groupdict()
        print(self.__class__.__name__, '|', data, "|", match.group())
        return data


class UnTerminalExpression(Expression):
    operators = {
        '+': lambda a, b: a+b,
        '-': lambda a, b: a-b,
        '*': lambda a, b: a*b,
        '%': lambda a, b: a % b,
        '/': lambda a, b: a/b,
        '//': lambda a, b: a//b,
        '**': lambda a, b: a**b,
    }

    def interpret(self, text):
        data = super().interpret(text)
        exp1 = interpret(data['exp1'])
        exp2 = interpret(data['exp2'])
        op = data['op']
        func = self.operators[op]
        return func(exp1, exp2)


class Value(Expression):
    pattern: re.Pattern = re.compile(r'^(?P<value>[+-]?[0-9]+\.?[0-9]*)$')

    def interpret(self, text: str):
        data = super().interpret(text)
        return float(data['value'])


class Func(Expression):
    pattern: re.Pattern = re.compile(
        r'^(?P<func_name>(\w+))\((?P<exp>.+)\)$')
    funcs = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan
    }

    def interpret(self, text):
        data = super().interpret(text)
        val = interpret(data['exp'])
        return self.funcs[data['func_name']](val)


class Brackets(Expression):
    pattern = re.compile(r'^\( *(?P<exp>.+) *\)$')

    def interpret(self, text):
        data = super().interpret(text)
        return interpret(data['exp'])


class FloorExpression(UnTerminalExpression):
    pattern = re.compile(r'^(?P<exp1>.*?) *(?P<op>//) *(?P<exp2>.*)$')


class ModExpression(UnTerminalExpression):
    pattern = re.compile(r'^(?P<exp1>.*?) *(?P<op>%) *(?P<exp2>.*)$')


class PowerExpression(UnTerminalExpression):
    pattern = re.compile(r'^(?P<exp1>.*?) *(?P<op>\*\*) *(?P<exp2>.*)$')


class MultiExpression(UnTerminalExpression):
    pattern = re.compile(r'^(?P<exp1>.*?) *(?P<op>\*) *(?P<exp2>.*)$')


class DivideByExpression(UnTerminalExpression):
    pattern = re.compile(r'^(?P<exp1>.*?) *(?P<op>/) *(?P<exp2>.*)$')


class PlusExpression(UnTerminalExpression):
    pattern = re.compile(r'^(?P<exp1>.*?) *(?P<op>\+) *(?P<exp2>.*)$')


class LessExpression(UnTerminalExpression):
    pattern = re.compile(r'^(?P<exp1>.*?) *(?P<op>-) *(?P<exp2>.*)$')


def interpret(text):
    import inspect
    for kls in globals().values():
        if inspect.isclass(kls) and kls not in [Expression, UnTerminalExpression] and kls and issubclass(kls, Expression):
            if kls.pattern.match(text):
                return kls().interpret(text)
    raise NotImplementedError(text)


assert interpret('1+2') == 3
assert interpret('1-2') == -1
assert interpret('1*2') == 2
assert interpret('1/2') == 0.5
assert interpret('1%2') == 1
assert interpret('2**3') == 8
assert interpret('2//3') == 0
assert interpret('2//3') == 0
assert interpret('2//3') == 0
assert interpret('2+1*5') == 15
assert interpret('2+1*5**2') == 225
assert interpret('(2+1)*3') == 9
assert interpret('sin(0)') == 0
assert interpret('cos(0)') == 1
