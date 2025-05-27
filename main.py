from Klausel import *
from KlauselMenge import *
from logger import *
from options import *

KlauselMenge1 = KlauselMenge("{{¬p,¬t,s},{p},{¬p,¬q,r},{t},{¬p,¬s,q},{¬s,¬r,t},{¬p,¬u,r},{¬u},{¬q}}")

options.verbouseLevel = VerboseLevel.AfterEachRecursionVerbose
options.removeTrivialEachItteration = True
options.stopAtEmptySet = False
options.optimiseTree = False
options.stopAfterStep = 4

KlauselMenge1.fullResolution()
log()
log(VerboseLevel.JustSolution,"Final result:")
log(VerboseLevel.JustSolution, KlauselMenge1.klauseln)
if options.removeTrivialAtEnd:
  log("Removing trivial clauses...")
  KlauselMenge1.removeTrivial()
  log(VerboseLevel.JustSolution, KlauselMenge1.klauseln)

KlauselMenge1.traceKlausel(Klausel("{}"))

