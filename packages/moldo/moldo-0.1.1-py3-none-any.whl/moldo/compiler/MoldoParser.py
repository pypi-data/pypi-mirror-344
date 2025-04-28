# Generated from moldo/compiler/Moldo.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\f")
        buf.write(".\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\3\2")
        buf.write("\7\2\20\n\2\f\2\16\2\23\13\2\3\2\3\2\3\3\3\3\5\3\31\n")
        buf.write("\3\3\4\3\4\3\4\3\4\3\4\3\4\3\5\3\5\3\6\3\6\7\6%\n\6\f")
        buf.write("\6\16\6(\13\6\3\7\3\7\3\7\3\7\3\7\2\2\b\2\4\6\b\n\f\2")
        buf.write("\2\2+\2\21\3\2\2\2\4\30\3\2\2\2\6\32\3\2\2\2\b \3\2\2")
        buf.write("\2\n&\3\2\2\2\f)\3\2\2\2\16\20\5\4\3\2\17\16\3\2\2\2\20")
        buf.write("\23\3\2\2\2\21\17\3\2\2\2\21\22\3\2\2\2\22\24\3\2\2\2")
        buf.write("\23\21\3\2\2\2\24\25\7\2\2\3\25\3\3\2\2\2\26\31\5\6\4")
        buf.write("\2\27\31\5\f\7\2\30\26\3\2\2\2\30\27\3\2\2\2\31\5\3\2")
        buf.write("\2\2\32\33\7\3\2\2\33\34\5\b\5\2\34\35\7\4\2\2\35\36\5")
        buf.write("\n\6\2\36\37\7\5\2\2\37\7\3\2\2\2 !\7\b\2\2!\t\3\2\2\2")
        buf.write("\"%\5\4\3\2#%\7\t\2\2$\"\3\2\2\2$#\3\2\2\2%(\3\2\2\2&")
        buf.write("$\3\2\2\2&\'\3\2\2\2\'\13\3\2\2\2(&\3\2\2\2)*\7\6\2\2")
        buf.write("*+\7\n\2\2+,\7\7\2\2,\r\3\2\2\2\6\21\30$&")
        return buf.getvalue()


class MoldoParser ( Parser ):

    grammarFileName = "Moldo.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'<mblock'", "'>'", "'</mblock>'", "'<python>'", 
                     "'</python>'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "IDENTIFIER", "TEXT", "PYTHON_CODE", 
                      "WS", "COMMENT" ]

    RULE_program = 0
    RULE_block = 1
    RULE_mblock = 2
    RULE_block_type = 3
    RULE_block_content = 4
    RULE_python_block = 5

    ruleNames =  [ "program", "block", "mblock", "block_type", "block_content", 
                   "python_block" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    IDENTIFIER=6
    TEXT=7
    PYTHON_CODE=8
    WS=9
    COMMENT=10

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(MoldoParser.EOF, 0)

        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MoldoParser.BlockContext)
            else:
                return self.getTypedRuleContext(MoldoParser.BlockContext,i)


        def getRuleIndex(self):
            return MoldoParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = MoldoParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 15
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==MoldoParser.T__0 or _la==MoldoParser.T__3:
                self.state = 12
                self.block()
                self.state = 17
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 18
            self.match(MoldoParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def mblock(self):
            return self.getTypedRuleContext(MoldoParser.MblockContext,0)


        def python_block(self):
            return self.getTypedRuleContext(MoldoParser.Python_blockContext,0)


        def getRuleIndex(self):
            return MoldoParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = MoldoParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_block)
        try:
            self.state = 22
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [MoldoParser.T__0]:
                self.enterOuterAlt(localctx, 1)
                self.state = 20
                self.mblock()
                pass
            elif token in [MoldoParser.T__3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 21
                self.python_block()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class MblockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def block_type(self):
            return self.getTypedRuleContext(MoldoParser.Block_typeContext,0)


        def block_content(self):
            return self.getTypedRuleContext(MoldoParser.Block_contentContext,0)


        def getRuleIndex(self):
            return MoldoParser.RULE_mblock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMblock" ):
                listener.enterMblock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMblock" ):
                listener.exitMblock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMblock" ):
                return visitor.visitMblock(self)
            else:
                return visitor.visitChildren(self)




    def mblock(self):

        localctx = MoldoParser.MblockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_mblock)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self.match(MoldoParser.T__0)
            self.state = 25
            self.block_type()
            self.state = 26
            self.match(MoldoParser.T__1)
            self.state = 27
            self.block_content()
            self.state = 28
            self.match(MoldoParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Block_typeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(MoldoParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return MoldoParser.RULE_block_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock_type" ):
                listener.enterBlock_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock_type" ):
                listener.exitBlock_type(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock_type" ):
                return visitor.visitBlock_type(self)
            else:
                return visitor.visitChildren(self)




    def block_type(self):

        localctx = MoldoParser.Block_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_block_type)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.match(MoldoParser.IDENTIFIER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Block_contentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MoldoParser.BlockContext)
            else:
                return self.getTypedRuleContext(MoldoParser.BlockContext,i)


        def TEXT(self, i:int=None):
            if i is None:
                return self.getTokens(MoldoParser.TEXT)
            else:
                return self.getToken(MoldoParser.TEXT, i)

        def getRuleIndex(self):
            return MoldoParser.RULE_block_content

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock_content" ):
                listener.enterBlock_content(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock_content" ):
                listener.exitBlock_content(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock_content" ):
                return visitor.visitBlock_content(self)
            else:
                return visitor.visitChildren(self)




    def block_content(self):

        localctx = MoldoParser.Block_contentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_block_content)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << MoldoParser.T__0) | (1 << MoldoParser.T__3) | (1 << MoldoParser.TEXT))) != 0):
                self.state = 34
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [MoldoParser.T__0, MoldoParser.T__3]:
                    self.state = 32
                    self.block()
                    pass
                elif token in [MoldoParser.TEXT]:
                    self.state = 33
                    self.match(MoldoParser.TEXT)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 38
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class Python_blockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PYTHON_CODE(self):
            return self.getToken(MoldoParser.PYTHON_CODE, 0)

        def getRuleIndex(self):
            return MoldoParser.RULE_python_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPython_block" ):
                listener.enterPython_block(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPython_block" ):
                listener.exitPython_block(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPython_block" ):
                return visitor.visitPython_block(self)
            else:
                return visitor.visitChildren(self)




    def python_block(self):

        localctx = MoldoParser.Python_blockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_python_block)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            self.match(MoldoParser.T__3)
            self.state = 40
            self.match(MoldoParser.PYTHON_CODE)
            self.state = 41
            self.match(MoldoParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





