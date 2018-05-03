import os
import os.path
import random
import string
from typing import Dict

from . import ast

TEXT_SYMBOL = "[]"
CHILDREN_SYMBOL = "{}"

TEMPLATES: Dict[str, str] = {}

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), "templates")

def template(name: str) -> str:
  if name in TEMPLATES:
    return TEMPLATES[name]

  path = os.path.join(TEMPLATES_PATH, f"{name}.html")
  with open(path) as f:
    content = f.read()
    TEMPLATES[name] = content

  return content

MAX_TEXT_LENGTH = 20
def random_text():
  text_length = random.randint(1, MAX_TEXT_LENGTH)
  return "".join([random.choice(string.ascii_letters) for _ in range(text_length)])

def render_text_command_node(text_command_node: ast.TextCommandNode):
  text_command = text_command_node.text_command_token.text_command
  _template = template(text_command)

  # Kinda lame because replaces all TEXT_SYMBOL with same random text.
  # But all text commands only have one TEXT_SYMBOL anyway...
  return _template.replace(TEXT_SYMBOL, random_text())

def render_block_command_node(block_command_node: ast.BlockCommandNode):
  inner_content = render(block_command_node.children)

  block_command = block_command_node.block_command_token.block_command
  _template = template(block_command)
  return _template.replace(CHILDREN_SYMBOL, inner_content)

def render(node_or_nodes) -> str:
  if isinstance(node_or_nodes, list):
    content = ""
    for node in node_or_nodes:
      content += render(node)
    return content
  elif isinstance(node_or_nodes, ast.BlockCommandNode):
    return render_block_command_node(node_or_nodes)
  elif isinstance(node_or_nodes, ast.TextCommandNode):
    return render_text_command_node(node_or_nodes)
  else:
    raise Exception("Unexpected node type!")
