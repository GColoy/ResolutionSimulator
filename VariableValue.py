from enum import Enum

class VariableValue(Enum):
  NOT_SET = 0
  TRUE = 1
  FALSE = 2
  BOTH = 3

  def get_variable_str(self, key):
      if self == VariableValue.FALSE:
        return "¬" + key
      if self == VariableValue.BOTH:
        return "¬" + key + ", " + key
      if self == VariableValue.TRUE:
        return key 
      else:
        return ""
      
  def get_variable_LaTeX(self, key):
    if self == VariableValue.FALSE:
      return "\\lnot " + key
    if self == VariableValue.BOTH:
      return "\\lnot " + key + ", " + key
    if self == VariableValue.TRUE:
      return key 
    else:
      return ""
      
  def __str__(self):
    if self == VariableValue.NOT_SET:
        return "NOT_SET"
    elif self == VariableValue.TRUE:
        return "TRUE"
    elif self == VariableValue.FALSE:
        return "FALSE"
    elif self == VariableValue.BOTH:
        return "BOTH"
    else:
        raise Exception("Invalid variable state")

  def __repr__(self):
    return self.__str__()

  def __eq__(self, other):
    if isinstance(other, VariableValue):
      return self.value == other.value
    return False
