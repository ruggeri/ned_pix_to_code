from ast import BlockCommandNode, TextCommandNode
import os
import os.path
from typing import Dict

TEXT_SYMBOL = "[]"
CHILDREN_SYMBOL = "{}"

TEMPLATES: Dict[str, str] = {}

def template(name: str) -> str:
  if name in TEMPLATES:
    return TEMPLATES[name]

  path = os.path.join("./templates", f"{name}.html")
  with open(path) as f:
    content = f.read()
    TEMPLATES[name] = content

  return content

def random_text():
  return "ASDF"

def render_text_command_node(text_command_node: TextCommandNode):
  text_command = text_command_node.text_command_token.text_command
  _template = template(text_command)

  # Kinda lame because replaces all TEXT_SYMBOL with same random text.
  # But all text commands only have one TEXT_SYMBOL anyway...
  return _template.replace(TEXT_SYMBOL, random_text())

def render_block_command_node(block_command_node: BlockCommandNode):
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
  elif isinstance(node_or_nodes, BlockCommandNode):
    return render_block_command_node(node_or_nodes)
  elif isinstance(node_or_nodes, TextCommandNode):
    return render_text_command_node(node_or_nodes)
  else:
    raise Exception("Unexpected node type!")

if __name__ == "__main__":
  import sys
  import parser
  import tokenizer

  tokens = tokenizer.tokenize_file(sys.argv[1])
  root_commands, error = parser.consume_document(tokens)
  rendered_document = render(root_commands)
  print(rendered_document)
