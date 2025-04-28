# Generated from moldo/compiler/Moldo.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\f")
        buf.write("h\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\3\2\3\2\3\2\3\2\3\2")
        buf.write("\3\2\3\2\3\2\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3")
        buf.write("\4\3\4\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\6\3\6\3\6")
        buf.write("\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\7\3\7\7\7A\n\7\f\7\16\7")
        buf.write("D\13\7\3\b\6\bG\n\b\r\b\16\bH\3\t\7\tL\n\t\f\t\16\tO\13")
        buf.write("\t\3\n\6\nR\n\n\r\n\16\nS\3\n\3\n\3\13\3\13\3\13\3\13")
        buf.write("\3\13\3\13\7\13^\n\13\f\13\16\13a\13\13\3\13\3\13\3\13")
        buf.write("\3\13\3\13\3\13\4M_\2\f\3\3\5\4\7\5\t\6\13\7\r\b\17\t")
        buf.write("\21\n\23\13\25\f\3\2\6\5\2C\\aac|\6\2\62;C\\aac|\4\2>")
        buf.write(">@@\5\2\13\f\17\17\"\"\2l\2\3\3\2\2\2\2\5\3\2\2\2\2\7")
        buf.write("\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2")
        buf.write("\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\3\27\3\2\2")
        buf.write("\2\5\37\3\2\2\2\7!\3\2\2\2\t+\3\2\2\2\13\64\3\2\2\2\r")
        buf.write(">\3\2\2\2\17F\3\2\2\2\21M\3\2\2\2\23Q\3\2\2\2\25W\3\2")
        buf.write("\2\2\27\30\7>\2\2\30\31\7o\2\2\31\32\7d\2\2\32\33\7n\2")
        buf.write("\2\33\34\7q\2\2\34\35\7e\2\2\35\36\7m\2\2\36\4\3\2\2\2")
        buf.write("\37 \7@\2\2 \6\3\2\2\2!\"\7>\2\2\"#\7\61\2\2#$\7o\2\2")
        buf.write("$%\7d\2\2%&\7n\2\2&\'\7q\2\2\'(\7e\2\2()\7m\2\2)*\7@\2")
        buf.write("\2*\b\3\2\2\2+,\7>\2\2,-\7r\2\2-.\7{\2\2./\7v\2\2/\60")
        buf.write("\7j\2\2\60\61\7q\2\2\61\62\7p\2\2\62\63\7@\2\2\63\n\3")
        buf.write("\2\2\2\64\65\7>\2\2\65\66\7\61\2\2\66\67\7r\2\2\678\7")
        buf.write("{\2\289\7v\2\29:\7j\2\2:;\7q\2\2;<\7p\2\2<=\7@\2\2=\f")
        buf.write("\3\2\2\2>B\t\2\2\2?A\t\3\2\2@?\3\2\2\2AD\3\2\2\2B@\3\2")
        buf.write("\2\2BC\3\2\2\2C\16\3\2\2\2DB\3\2\2\2EG\n\4\2\2FE\3\2\2")
        buf.write("\2GH\3\2\2\2HF\3\2\2\2HI\3\2\2\2I\20\3\2\2\2JL\13\2\2")
        buf.write("\2KJ\3\2\2\2LO\3\2\2\2MN\3\2\2\2MK\3\2\2\2N\22\3\2\2\2")
        buf.write("OM\3\2\2\2PR\t\5\2\2QP\3\2\2\2RS\3\2\2\2SQ\3\2\2\2ST\3")
        buf.write("\2\2\2TU\3\2\2\2UV\b\n\2\2V\24\3\2\2\2WX\7>\2\2XY\7#\2")
        buf.write("\2YZ\7/\2\2Z[\7/\2\2[_\3\2\2\2\\^\13\2\2\2]\\\3\2\2\2")
        buf.write("^a\3\2\2\2_`\3\2\2\2_]\3\2\2\2`b\3\2\2\2a_\3\2\2\2bc\7")
        buf.write("/\2\2cd\7/\2\2de\7@\2\2ef\3\2\2\2fg\b\13\2\2g\26\3\2\2")
        buf.write("\2\b\2BHMS_\3\b\2\2")
        return buf.getvalue()


class MoldoLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    IDENTIFIER = 6
    TEXT = 7
    PYTHON_CODE = 8
    WS = 9
    COMMENT = 10

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'<mblock'", "'>'", "'</mblock>'", "'<python>'", "'</python>'" ]

    symbolicNames = [ "<INVALID>",
            "IDENTIFIER", "TEXT", "PYTHON_CODE", "WS", "COMMENT" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "IDENTIFIER", 
                  "TEXT", "PYTHON_CODE", "WS", "COMMENT" ]

    grammarFileName = "Moldo.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


