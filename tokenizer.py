import re
import token

WHITESPACE_REGEXP = re.compile(r"\w+")

def tokenize(body: str):
  body = body.replace(",", " , ")
  token_strs = body.split()

  tokens = []
  for token_str in token_strs:
    t = token.Token.parse(token_str)
    tokens.append(t)

  return tokens

def tokenize_file(filename: str):
  with open(filename) as f:
    body = f.read()
  return tokenize(body)

tokens = tokenize_file("data/FEF248A4-868E-4A6C-94D6-9B38A67974F0.gui")
print(tokens)
