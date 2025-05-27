from VariableValue import VariableValue
from logger import *
from key import keys
from options import options

class Klausel:
  def __init__(self, variables: dict[str, VariableValue] | str, parents: list['Klausel'] = None, depth: int = 0, addedDepth: int = 1):
    if isinstance(variables, dict):
      self.variables = variables
    elif isinstance(variables, str):
      self.variables = variablesFromString(variables)
    self.parents: list[Klausel] = parents
    self.depth = depth
    self.addedDepth = addedDepth

  def __str__(self):
    if options.logTex:
      return self.getLaTeX()
    else:
      return "{" + ", ".join(value.get_variable_str(key) for key, value in self.variables.items() if value.get_variable_str(key).__len__() > 0) + "}"
  
  def getLaTeX(self):
    return "\\left\\{" + ", ".join(value.get_variable_LaTeX(key) for key, value in self.variables.items() if value.get_variable_LaTeX(key).__len__() > 0) + "\\right\\}"
  
  def __repr__(self):
    return self.__str__()
  
  def __eq__(self, other):
    if not isinstance(other, Klausel):
      return False
    for key in keys:
      if self.variables.get(key, VariableValue.NOT_SET) != other.variables.get(key, VariableValue.NOT_SET):
        return False
    return True
  
  def __iter__(self):
    return iter(self.variables)
  
  def __next__(self):
    return next(iter(self.variables.items()))
  
  def copy(self):
    return Klausel(self.variables.copy(), self.parents.copy() if self.parents else None, self.depth, self.addedDepth)
  
  def getAllVariables(self):
    return self.variables.keys()
  
  def isTrivial(self):
    for value in self.variables.values():
      if value == VariableValue.BOTH:
        return True
    return False
  
  def tryResolventeMitKlausel(self, other: 'Klausel'):
    if not isinstance(other, Klausel):
      raise TypeError("other must be an instance of Klausel")
    
    newKlauses = []
    for key in self.variables:
      newKlausel = self.tryResolventeForKey(other, key)
      if newKlausel:
        newKlauses.append(newKlausel)
    return newKlauses
  
  def tryResolventeForKey(self, other: 'Klausel', key: str):
    sV = self.variables.get(key, VariableValue.NOT_SET)
    oV = other.variables.get(key, VariableValue.NOT_SET)
    if sV == VariableValue.NOT_SET or oV == VariableValue.NOT_SET:
      return None
    if sV == oV and sV != VariableValue.BOTH:
      return None
    c = self.copy()
    for k in keys:
      c.variables[k] = setVariable(self.variables.get(k, VariableValue.NOT_SET), other.variables.get(k, VariableValue.NOT_SET))
    c.variables[key] = setKeyVariable(sV, oV)
    c.parents = [self, other]
    c.depth = max(self.depth, other.depth) + 1
    c.addedDepth = self.addedDepth + other.addedDepth
    return c
  
  def isEmpty(self):
    return all(value == VariableValue.NOT_SET for value in self.variables.values())
  
  def logTree(self, depth: int = -1):
    if self.parents is None:
      return
    if depth < 0:
      depth = self.depth
    for parent in self.parents:
      log("     " * depth + str(parent))
      parent.logTree(depth + 1)

def setVariable(a, b):
  if a == VariableValue.NOT_SET:
    return b
  if b == VariableValue.NOT_SET:
    return a
  if a == b:
    return a
  if a == VariableValue.BOTH or b == VariableValue.BOTH:
    return VariableValue.BOTH
  if a != b:
    return VariableValue.BOTH
  
def setKeyVariable(a, b):
  if a != VariableValue.BOTH and b != VariableValue.BOTH:
    return VariableValue.NOT_SET
  if a == VariableValue.BOTH and b == VariableValue.BOTH:
    return VariableValue.BOTH
  if a == VariableValue.BOTH:
    return b
  if b == VariableValue.BOTH:
    return a
  else:
    raise Exception("Invalid variable state")
  
def variablesFromString(k_str: str):
  k_str = k_str.strip('{} ')
  literals = k_str.split(',')
  literal_map = {}
  for literal in literals:
    lit = literal.strip()
    var = lit.strip("¬~ ")
    if not lit:
      continue
    if var in literal_map.keys():
      literal_map[var] = VariableValue.BOTH
    elif lit.startswith('¬') or lit.startswith('~'):
      literal_map[var] = VariableValue.FALSE
    else:
      var = lit
      literal_map[var] = VariableValue.TRUE
  return literal_map