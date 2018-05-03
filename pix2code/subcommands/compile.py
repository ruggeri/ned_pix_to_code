import argparse

from ..compiler.compiler import render
from ..compiler.parser import consume_document
from ..compiler.tokenizer import tokenize_file

def configure_parser(compile_parser):
  compile_parser.add_argument("gui_file", help = ".gui file to compile")

def main(args):
  tokens = tokenize_file(args.gui_file)
  root_commands, error = consume_document(tokens)
  rendered_document = render(root_commands)
  print(rendered_document)
