from Klausel import *
from KlauselMenge import *
from logger import *

KlauselMenge1 = KlauselMenge("{{¬p, ¬r}, {¬p, r}, {p, ¬r}, {p, r}}")

KlauselMenge1.fullResolution()
log("Final clauses amount after resolution:" + str(KlauselMenge1.klauselAmount()))
log(KlauselMenge1.klauseln)
log(KlauselMenge1.getLaTeX())
logTex(KlauselMenge1.getLaTeX())
log("Removing trivial clauses...")
KlauselMenge1.removeTrivial()
log(KlauselMenge1.klauseln)
