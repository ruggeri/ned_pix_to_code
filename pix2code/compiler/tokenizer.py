import pix2code.compiler.mytoken as mytoken
import re

WHITESPACE_REGEXP = re.compile(r"\w+")

def tokenize(body: str):
  body = body.replace(",", " , ")
  token_strs = body.split()

  tokens = []
  for token_str in token_strs:
    t = mytoken.Token.parse(token_str)
    tokens.append(t)

  return tokens

def tokenize_file(filename: str):
  with open(filename) as f:
    body = f.read()
  return tokenize(body)
