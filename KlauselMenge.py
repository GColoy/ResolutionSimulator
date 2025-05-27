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
    foundTargetKlausel = False
    while n > nprev and not foundEmptySet and options.stopAfterStep != steps and not foundTargetKlausel:
      steps += 1
      allFoundKlauseln = self.solveStep()
      newKlauseln = []
      for newKlausel in allFoundKlauseln:
        if newKlausel in self.klauseln:
          if not options.optimiseTree:
            continue
          existingKlausel = self.klauseln[self.klauseln.index(newKlausel)]
          if existingKlausel.addedDepth <= newKlausel.addedDepth:
            continue
          else:
            self.klauseln.remove(existingKlausel)
        newKlauseln.append(newKlausel)
        self.addKlausel(newKlausel)
        if options.stopAtEmptySet and newKlausel.isEmpty():
          foundEmptySet = True
        if options.stopWhenFoundKlausel and newKlausel == options.stopWhenFoundKlausel:
          foundTargetKlausel = True
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
    elif foundTargetKlausel:
      log(VerboseLevel.AfterEachRecursion, f"Found target clause {options.stopWhenFoundKlausel}, stopping resolution.")
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

  def traceKlausel(self, klausel: Klausel):
    if not isinstance(klausel, Klausel):
      raise TypeError("klausel must be an instance of Klausel")
    if klausel in self.klauseln:
      logTree(self.klauseln[self.klauseln.index(klausel)])
    else:
      return None

def parse_klauselmenge(input_str):
  # Entferne äußere Klammern und Leerzeichen
  input_str = input_str.strip()[1:-1].strip()
  
  # Finde alle Klauseln als Strings mit geschweiften Klammern
  klausel_strings: str = re.findall(r'\{[^{}]*\}', input_str)
  
  klauseln = []
  for k_str in klausel_strings:  
    klauseln.append(Klausel(k_str.strip()))
  
  return klauseln

def logTree(klausel: Klausel, depth: int = 0):
    log(input="     " * depth + str(klausel))
    if klausel.parents is None:
        return
    for parent in klausel.parents:
        logTree(parent, depth + 1)