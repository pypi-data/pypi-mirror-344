# Generated from moldo/compiler/Moldo.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MoldoParser import MoldoParser
else:
    from MoldoParser import MoldoParser

# This class defines a complete generic visitor for a parse tree produced by MoldoParser.

class MoldoVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MoldoParser#program.
    def visitProgram(self, ctx:MoldoParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MoldoParser#block.
    def visitBlock(self, ctx:MoldoParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MoldoParser#mblock.
    def visitMblock(self, ctx:MoldoParser.MblockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MoldoParser#block_type.
    def visitBlock_type(self, ctx:MoldoParser.Block_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MoldoParser#block_content.
    def visitBlock_content(self, ctx:MoldoParser.Block_contentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MoldoParser#python_block.
    def visitPython_block(self, ctx:MoldoParser.Python_blockContext):
        return self.visitChildren(ctx)



del MoldoParser