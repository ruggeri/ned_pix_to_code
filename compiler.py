import os
import os.path

TEXT_SYMBOL = "[]"
CHILDREN_SYMBOL = "{}"

class OperatorToken:
  OPERATOR_TOKENS_MAP = {}

  @classmethod
  def get(clazz, token_name) -> OperatorToken:
    return clazz.OPERATOR_TOKENS_MAP[token_name]

  @classmethod
  def load_all(clazz):
      for fname in os.listdir("./templates"):
        path_name = os.path.join("./templates", fname)
        if not os.path.isfile(path_name): continue
        token_name = fname.rstrip(".html")
        with open(path_name) as f:
          content = f.read()
          clazz.OPERATOR_TOKENS_MAP[token_name] = OperatorToken(token_name, content)

  def __init__(self, token_name: str, content: str):
    self.name = token_name

    if not content.find(TEXT_SYMBOL) == -1:
      self.left, self.right = content.split(TEXT_SYMBOL)
      self._node_type = "TEXT"
      return
    if not content.find(CHILDREN_SYMBOL) == -1:
      self.left, self.right = content.split(CHILDREN_SYMBOL)
      self._node_type = "CHILDREN"
      return

    raise Exception("Neither text or children operator???")

  @property
  def is_text_node(self):
    return self._node_type == "TEXT"

  @property
  def is_children_node(self):
    return self._node_type == "CHILDREN"


class ASTNode:
  def __init__(self, token: OperatorToken):
    self.token = token
    if self.token.is_children_node:
      self.children = []
    else:
      self.children = None

  def generate(self):
    result = self.token.left
    if self.children:
      result += ",".join([child.generate() for child in self.children])
    result += self.token.right
    return result

OperatorToken.load_all()
