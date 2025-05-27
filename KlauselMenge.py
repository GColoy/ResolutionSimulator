from Klausel import Klausel
from logger import *
from VariableValue import VariableValue
import re
from options import options


class KlauselMenge:
  def __init__(self, klauseln: list[Klausel] | str):
    if isinstance(klauseln, list):
      self.klauseln = klauseln
    elif isinstance(klauseln, str):
      self.klauseln = parse_klauselmenge(klauseln)
    else:
      raise TypeError("variables must be a dict or a str")

  def __str__(self):
    if options.logTex:
      return self.getLaTeX(self)
    else:
      return "{" + ", ".join((str(klausel) for klausel in self.klauseln)) + "}"

  def __repr__(self):
    return self.__str__()
  
  def getLaTeX(self):
    return "\\left\\{" + ", ".join((klausel.getLaTeX() for klausel in self.klauseln)) + "\\right\\}"
  
  def copy(self):
    return KlauselMenge([klausel.copy() for klausel in self.klauseln])
  
  def addKlausel(self, klausel: Klausel):
    if not isinstance(klausel, Klausel):
      raise TypeError("klaus must be an instance of Klausel")
    if klausel not in self.klauseln:

      self.klauseln.append(klausel)
  


  def klauselAmount(self):
    return self.klauseln.__len__()

  def fullResolution(self):
    log(VerboseLevel.AfterEachRecursion, "Starting full resolution...")
    steps = 0
    n = self.klauselAmount()
    nprev = -1
    foundEmptySet = False
    while n > nprev:
      steps += 1
      allFoundKlauseln = self.solveStep()
      newKlauseln = []
      for newKlausel in allFoundKlauseln:
        if newKlausel not in self.klauseln:
          newKlauseln.append(newKlausel)
          self.addKlausel(newKlausel)
          if newKlausel.isEmpty() and options.stopAtEmptySet:
            foundEmptySet = True
      newResults = KlauselMenge(newKlauseln)
      nprev = n
      n = self.klauselAmount()
      log()
      log(VerboseLevel.AfterEachRecursion, f"Step {steps}: {n} clauses after resolving {newResults.klauselAmount()} new clauses.")
      log(VerboseLevel.AfterEachRecursion, f"New clauses: {newResults.klauseln}")
      if options.removeTrivialEachItteration:
        log(VerboseLevel.AfterEachRecursionVerbose, f"Total clauses before removing trvial clauses: {self.klauseln}")
        self.removeTrivial()
      log(VerboseLevel.AfterEachRecursion, f"Total clauses: {self.klauseln}")
    if foundEmptySet:
      log(VerboseLevel.AfterEachRecursion, "Found empty set , stopping resolution.")
    else:
      log(VerboseLevel.AfterEachRecursion, "Resolution complete.")
    return self.klauseln

  def solveStep(self) -> list[Klausel]:
    foundKlauseln = []
    for i in range(0, self.klauseln.__len__() - 1):
      firstKlausel = self.klauseln[i]
      log(VerboseLevel.AllNewResolutions, f"  Resolving clause {i}: {firstKlausel}")
      for j in range(i + 1, self.klauseln.__len__()):
        secondKlausel = self.klauseln[j]
        resolution = (firstKlausel.tryResolventeMitKlausel(secondKlausel))
        foundKlauseln.extend(resolution)
        log(VerboseLevel.AllValidResolutions if resolution else VerboseLevel.AllResolutions, f"    With clause {j}: {secondKlausel}")
        for klauseln in resolution:
          if klauseln not in foundKlauseln:
            log(VerboseLevel.AllNewResolutions, f"    New: {klauseln}")
          else:
            log(VerboseLevel.AllValidResolutions, f"    Found: {klauseln}")
    return foundKlauseln
  
  def removeTrivial(self):
    log(VerboseLevel.AfterEachRecursionVerbose ,"Removing trivial clauses...")
    self.klauseln = [klausel for klausel in self.klauseln if not klausel.isTrivial()]
    log(VerboseLevel.AfterEachRecursionVerbose, f"Remaining clauses after removal: {self.klauselAmount()}")

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