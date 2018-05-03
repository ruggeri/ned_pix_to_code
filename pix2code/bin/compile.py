from pix2code.compiler.compiler import render
from pix2code.compiler.parser import consume_document
from pix2code.compiler.tokenizer import tokenize_file
import sys

tokens = tokenize_file(sys.argv[1])
root_commands, error = consume_document(tokens)
rendered_document = render(root_commands)
print(rendered_document)
