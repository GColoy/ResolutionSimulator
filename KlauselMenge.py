from Klausel import Klausel
from logger import *
from VariableValue import VariableValue
import re


class KlauselMenge:
  def __init__(self, klauseln: list[Klausel] | str):
    if isinstance(klauseln, list):
      self.klauseln = klauseln
    elif isinstance(klauseln, str):
      self.klauseln = parse_klauselmenge(klauseln)
    else:
      raise TypeError("variables must be a dict or a str")

  def __str__(self):
    return "{" + ", ".join((str(klausel) for klausel in self.klauseln)) + "}"

  def __repr__(self):
    return self.__str__()
  
  def getLaTeX(self):
    return "\\left\\{" + ", ".join((klausel.getLaTeX() for klausel in self.klauseln)) + "\\right\\}"
  
  def copy(self):
    return KlauselMenge([klausel.copy() for klausel in self.klauseln])
  
  def addKlausel(self, klaus: Klausel):
    if not isinstance(klaus, Klausel):
      raise TypeError("klaus must be an instance of Klausel")
    if klaus not in self.klauseln:
      self.klauseln.append(klaus)
      log(f"Added clause: {klaus}")
    else:
      log(f"Clause {klaus} already exists, skipping")

  def klauselAmount(self):
    return self.klauseln.__len__()

  def fullResolution(self):
    log("Starting full resolution...")
    steps = 0
    n = self.klauselAmount()
    nprev = -1
    logTex(f"\\text{{Res}}^{{0}}= {self.getLaTeX()}")
    while n > nprev:
      steps += 1
      log(f"Current number of clauses: {n}")
      log("Resolving clauses...")
      resultList = self.solveStep()
      newREsultList = []
      for newKlausel in resultList:
        new_var = newKlausel not in self.klauseln
        if new_var:
          newREsultList.append(newKlausel)
          self.addKlausel(newKlausel)
          if newKlausel.isEmpty():
            log("Empty clause found, stopping resolution.")
            return self.klauseln
      newResults = KlauselMenge(newREsultList)
      logTex(f"\\text{{Res}}^{{{steps}}}=\\text{{Res}}^{{{steps-1}}} \cup {newResults.getLaTeX()}")
      # logTex(f"\\text{{Res}}^{{{steps}}}= {self.getLaTeX()}")
      nprev = n
      n = self.klauselAmount()
      log("\n\n")
    log("Full resolution completed in " + str(steps) + " steps.")
    return self.klauseln
  
  def solveStep(self):
    resultList = []
    for i in range(0, self.klauseln.__len__()):
      firstKlausel = self.klauseln[i]
      log(f"  Resolving clause {i}: {firstKlausel}")
      for j in range(i, self.klauseln.__len__()):
        if i == j:
          continue
        secondKlausel = self.klauseln[j]
        log(f"    with clause {j}: {secondKlausel}")
        newKlauses = firstKlausel.tryResolventeMitKlausel(secondKlausel)
        for newKlausel in newKlauses:
          if newKlausel not in self.klauseln:
            log(f"      New: {newKlausel}")
            resultList.append(newKlausel)
          # else:
            # log(f"      Already exists: {newKlausel}")
    return resultList
  
  def removeTrivial(self):
    log("Removing trivial clauses...")
    self.klauseln = [klausel for klausel in self.klauseln if not klausel.isTrivial()]
    log(f"Remaining clauses after removal: {self.klauselAmount()}")

def parse_klauselmenge(input_str):
  # Entferne äußere Klammern und Leerzeichen
  input_str = input_str.strip()[1:-1].strip()
  
  # Finde alle Klauseln als Strings mit geschweiften Klammern
  klausel_strings = re.findall(r'\{[^{}]*\}', input_str)
  
  klauseln = []
  for k_str in klausel_strings:
      k_str = k_str.strip('{} ')
      literals = k_str.split(',')
      literal_map = {}
      for literal in literals:
          lit = literal.strip()
          if not lit:
              continue
          if lit.startswith('¬') or lit.startswith('~'):
              var = lit[1:].strip()
              literal_map[var] = VariableValue.FALSE
          else:
              var = lit
              literal_map[var] = VariableValue.TRUE
      klauseln.append(Klausel(literal_map))
  
  return klauseln