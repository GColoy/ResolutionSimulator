from Klausel import *
from KlauselMenge import *
from logger import *
from options import *

KlauselMenge1 = KlauselMenge("{{¬p, ¬r}, {¬p, r}, {p, ¬r}, {p, r}}")

options.verbouseLevel = VerboseLevel.AfterEachRecursionVerbose
options.removeTrivialEachItteration = True
options.stopAtEmptySet = False

KlauselMenge1.fullResolution()
log()
log(VerboseLevel.JustSolution,"Final result:")
log(VerboseLevel.JustSolution, KlauselMenge1.klauseln)
if options.removeTrivialAtEnd:
  log("Removing trivial clauses...")
  KlauselMenge1.removeTrivial()
  log(VerboseLevel.JustSolution ,KlauselMenge1.klauseln)

