from VariableValue import VariableValue
from Klausel import *
from KlauselMenge import *
from logger import *

def test():
  assert setVariable(VariableValue.NOT_SET, VariableValue.TRUE) == VariableValue.TRUE, "Expected NOT_SET + TRUE to be TRUE"
  assert setVariable(VariableValue.TRUE, VariableValue.FALSE) == VariableValue.BOTH, "Expected TRUE + FALSE to be BOTH"
  assert setVariable(VariableValue.TRUE, VariableValue.TRUE) == VariableValue.TRUE, "Expected TRUE + TRUE to be TRUE"
  assert setVariable(VariableValue.FALSE, VariableValue.FALSE) == VariableValue.FALSE, "Expected FALSE + FALSE to be FALSE"
  assert setVariable(VariableValue.BOTH, VariableValue.TRUE) == VariableValue.BOTH, "Expected BOTH + TRUE to be BOTH"

  assert setKeyVariable(VariableValue.BOTH, VariableValue.TRUE) == VariableValue.TRUE, "Expected BOTH + TRUE to be TRUE"
  assert setKeyVariable(VariableValue.BOTH, VariableValue.BOTH) == VariableValue.BOTH, "Expected BOTH + BOTH to be BOTH"
  assert setKeyVariable(VariableValue.TRUE, VariableValue.FALSE) == VariableValue.NOT_SET, "Expected TRUE + FALSE to be NOT_SET"

  assert Klausel({"p": VariableValue.TRUE, "q": VariableValue.FALSE}) == Klausel({"p": VariableValue.TRUE, "q": VariableValue.FALSE}), "Expected equal clauses to be equal"
  assert Klausel({"p": VariableValue.TRUE, "q": VariableValue.FALSE}) != Klausel({"p": VariableValue.TRUE, "q": VariableValue.TRUE}), "Expected different clauses to be not equal"

  assert Klausel({
    "p": VariableValue.TRUE, 
    "q": VariableValue.FALSE}).tryResolventeForKey(
      Klausel(
        {"p": VariableValue.TRUE, 
         "q": VariableValue.TRUE}), "q") == Klausel(
           {"p": VariableValue.TRUE, 
            "q": VariableValue.NOT_SET}), "Expected resolving clauses to produce correct result"

KlauselMenge1 = KlauselMenge("{{¬p, ¬r}, {¬p, r}, {p, ¬r}, {p, r}}")

KlauselMenge1.fullResolution()
log("Final clauses amount after resolution:" + str(KlauselMenge1.klauselAmount()))
log(KlauselMenge1.klauseln)
log(KlauselMenge1.getLaTeX())
logTex(KlauselMenge1.getLaTeX())
log("Removing trivial clauses...")
KlauselMenge1.removeTrivial()
log(KlauselMenge1.klauseln)
