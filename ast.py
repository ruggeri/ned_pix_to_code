import mytoken

class BlockCommandNode:
  def __init__(self, block_command_token: mytoken.BlockCommandOperatorToken, children):
    if not block_command_token.is_block_command_operator():
      raise Exception(f"Expected a block command operator: {block_command_token}")

    self.block_command_token = block_command_token
    self.children = children

  def __repr__(self):
    return f"<node: {self.block_command_token.block_command}>"

class TextCommandNode:
  def __init__(self, text_command_token: mytoken.TextCommandOperatorToken):
    if not text_command_token.is_text_command_operator():
      raise Exception(f"Expected a text command operator: {text_command_token}")
    self.text_command_token = text_command_token

  def __repr__(self):
    return f"<node: {self.text_command_token.text_command}>"
