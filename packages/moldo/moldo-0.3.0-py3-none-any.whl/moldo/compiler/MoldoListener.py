# Generated from moldo/compiler/Moldo.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MoldoParser import MoldoParser
else:
    from MoldoParser import MoldoParser

# This class defines a complete listener for a parse tree produced by MoldoParser.
class MoldoListener(ParseTreeListener):

    # Enter a parse tree produced by MoldoParser#program.
    def enterProgram(self, ctx:MoldoParser.ProgramContext):
        pass

    # Exit a parse tree produced by MoldoParser#program.
    def exitProgram(self, ctx:MoldoParser.ProgramContext):
        pass


    # Enter a parse tree produced by MoldoParser#block.
    def enterBlock(self, ctx:MoldoParser.BlockContext):
        pass

    # Exit a parse tree produced by MoldoParser#block.
    def exitBlock(self, ctx:MoldoParser.BlockContext):
        pass


    # Enter a parse tree produced by MoldoParser#mblock.
    def enterMblock(self, ctx:MoldoParser.MblockContext):
        pass

    # Exit a parse tree produced by MoldoParser#mblock.
    def exitMblock(self, ctx:MoldoParser.MblockContext):
        pass


    # Enter a parse tree produced by MoldoParser#block_type.
    def enterBlock_type(self, ctx:MoldoParser.Block_typeContext):
        pass

    # Exit a parse tree produced by MoldoParser#block_type.
    def exitBlock_type(self, ctx:MoldoParser.Block_typeContext):
        pass


    # Enter a parse tree produced by MoldoParser#block_content.
    def enterBlock_content(self, ctx:MoldoParser.Block_contentContext):
        pass

    # Exit a parse tree produced by MoldoParser#block_content.
    def exitBlock_content(self, ctx:MoldoParser.Block_contentContext):
        pass


    # Enter a parse tree produced by MoldoParser#python_block.
    def enterPython_block(self, ctx:MoldoParser.Python_blockContext):
        pass

    # Exit a parse tree produced by MoldoParser#python_block.
    def exitPython_block(self, ctx:MoldoParser.Python_blockContext):
        pass



del MoldoParser