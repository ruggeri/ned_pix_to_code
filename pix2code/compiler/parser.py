from typing import List, Tuple

from . import ast
from . import mytoken

# document: commands_block
def consume_document(tokens: List[mytoken.Token]):
  root_command_nodes, token_idx, errors = consume_commands_block(
    tokens, 0
  )

  if errors:
    return None, errors
  elif token_idx != len(tokens):
    return None, [f"Expected end of document, not: {tokens[token_idx]}"]

  return ast.BlockCommandNode(mytoken.Token.parse("body"), root_command_nodes), None

# commands_block: text_commands_block
# commands_block: block_commands_block
def consume_commands_block(tokens: List[mytoken.Token], token_idx: int):
  if token_idx == len(tokens):
    return None, None, [
      "Unexpected end of document", "Failed parsing commands block"
    ]
  elif tokens[token_idx].is_block_command_operator():
    return consume_block_commands_block(tokens, token_idx)
  elif tokens[token_idx].is_text_command_operator():
    return consume_text_commands_block(
      tokens, token_idx
    )
  else:
    return None, token_idx, [
      f"Unexpected token: {tokens[token_idx]}",
      "Failed parsing commands block"
    ]

# text_commands_block: text_command_operator
# text_commands_block: (text_command_operator,)+ text_command_operator
def consume_text_commands_block(tokens: List[mytoken.Token], token_idx):
  text_command_nodes = []

  text_command_node, token_idx, errors = consume_text_command(tokens, token_idx)
  if errors:
    return None, None, errors + ["Failed parsing text commands block"]
  text_command_nodes.append(text_command_node)

  while True:
    if token_idx == len(tokens):
      break
    elif tokens[token_idx].is_block_end_token():
      break
    elif not tokens[token_idx].is_text_command_separator_token():
      return None, None, [
        f"Expected text command separator or end of text commands block, not {tokens[token_idx]}",
        "Failed parsing text commands block"
      ]
    token_idx += 1

    text_command_node, token_idx, errors = consume_text_command(
      tokens, token_idx
    )
    if errors:
      return None, None, errors + ["Failed parsing text commands block"]
    text_command_nodes.append(text_command_node)

  return text_command_nodes, token_idx, None

def consume_text_command(tokens: List[mytoken.Token], token_idx):
  if token_idx >= len(tokens):
    return None, None, ["Expected text command, not end of document"]
  if not tokens[token_idx].is_text_command_operator():
    return None, None, [f"Expected text command, not {tokens[token_idx]}"]

  text_command_node = ast.TextCommandNode(tokens[token_idx])
  token_idx += 1

  return text_command_node, token_idx, None

# block_commands_block: block_command+
def consume_block_commands_block(tokens: List[mytoken.Token], token_idx):
  block_command_nodes = []

  block_command_node, token_idx, errors = consume_block_command(tokens, token_idx)
  if errors:
    return None, None, errors + ["Failed parsing block commands block"]
  block_command_nodes.append(block_command_node)

  while True:
    if token_idx == len(tokens):
      break
    elif tokens[token_idx].is_block_end_token():
      break

    block_command_node, token_idx, errors = consume_block_command(
      tokens, token_idx
    )
    if errors:
      return None, None, errors + ["Failed parsing block commands block"]
    block_command_nodes.append(block_command_node)

  return block_command_nodes, token_idx, None

# block_command: block_command_operator { commands_block }
def consume_block_command(tokens: List[mytoken.Token], token_idx: int):
  if token_idx >= len(tokens):
    return None, None, [
      "Expected block command operator, not end of document",
      "Failed parsing block command",
    ]
  if not tokens[token_idx].is_block_command_operator():
    return None, None, [
      f"Expected block command operator, not {tokens[token_idx]}",
      "Failed parsing block command",
    ]

  block_command_operator_token = tokens[token_idx]
  token_idx += 1

  if token_idx >= len(tokens):
    return None, None, [
      f"Expected block start token, not end of document",
      f"Failed parsing block for {block_command_operator_token}",
    ]
  if not tokens[token_idx].is_block_start_token():
    return None, None, [
      f"Expected block start token, not: {tokens[token_idx]}",
      f"Failed parsing block for {block_command_operator_token}",
    ]
  token_idx += 1

  children, token_idx, errors = consume_commands_block(tokens, token_idx)
  if errors:
    return None, None, errors + [
      f"Failed parsing block for {block_command_operator_token}",
    ]

  if token_idx >= len(tokens):
    return None, None, [
      "Expected block end token, not end of document",
      f"Failed parsing block for {block_command_operator_token}",
    ]
  if not tokens[token_idx].is_block_end_token():
    return None, None, [
      f"Expected block end token, not: {tokens[token_idx]}",
      f"Failed parsing block for {block_command_operator_token}",
    ]
  token_idx += 1

  block_command_node = ast.BlockCommandNode(
    block_command_operator_token, children
  )

  return block_command_node, token_idx, None

if __name__ == "__main__":
  import sys
  import tokenizer

  tokens = tokenizer.tokenize_file(sys.argv[1])
  root_commands, error = consume_document(tokens)
  print(root_commands)
  print(error)

  import pdb
  pdb.set_trace()
