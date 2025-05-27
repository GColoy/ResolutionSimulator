from VariableValue import VariableValue
from Klausel import *
from KlauselMenge import *
from logger import *

def testAll():
  failures = 0

  try:
     test_setVariable()
     logTestSuccess("test_setVariable passed")
  except Exception as e:
    failures += 1
    logTestError(f"test_setVariable failed: {e}")
  
  try:
    test_setKeyKavriable()
    logTestSuccess("test_setKeyKavriable passed")
  except Exception as e:
    failures += 1
    logTestError(f"test_setKeyKavriable failed: {e}")

  try:
    test_Klausel_eq()
    logTestSuccess("test_Klausel_eq passed")
  except Exception as e:
    failures += 1
    logTestError(f"test_Klausel_eq failed: {e}")

  try:
    test_ResolventeForKey()
    logTestSuccess("test_ResolventeForKey passed")
  except Exception as e:
    failures += 1
    logTestError(f"test_ResolventeForKey failed: {e}")

  return failures

def test_ResolventeForKey():
    assert Klausel({
    "p": VariableValue.TRUE, 
    "q": VariableValue.FALSE}).tryResolventeForKey(
      Klausel(
        {"p": VariableValue.TRUE, 
         "q": VariableValue.TRUE}), "q") == Klausel(
           {"p": VariableValue.TRUE, 
            "q": VariableValue.NOT_SET}), "Expected resolving clauses to produce correct result"

def test_Klausel_eq():
  assert Klausel({"p": VariableValue.TRUE, "q": VariableValue.FALSE}) == Klausel({"p": VariableValue.TRUE, "q": VariableValue.FALSE}), "Expected equal clauses to be equal"
  assert Klausel({"p": VariableValue.TRUE, "q": VariableValue.FALSE}) != Klausel({"p": VariableValue.TRUE, "q": VariableValue.TRUE}), "Expected different clauses to be not equal"

def test_setKeyKavriable():
  assert setKeyVariable(VariableValue.BOTH, VariableValue.TRUE) != VariableValue.TRUE, "Expected BOTH + TRUE to be TRUE"
  assert setKeyVariable(VariableValue.BOTH, VariableValue.BOTH) == VariableValue.BOTH, "Expected BOTH + BOTH to be BOTH"
  assert setKeyVariable(VariableValue.TRUE, VariableValue.FALSE) == VariableValue.NOT_SET, "Expected TRUE + FALSE to be NOT_SET"

def test_setVariable():
  assert setVariable(VariableValue.NOT_SET, VariableValue.TRUE) == VariableValue.TRUE, "Expected NOT_SET + TRUE to be TRUE"
  assert setVariable(VariableValue.TRUE, VariableValue.FALSE) == VariableValue.BOTH, "Expected TRUE + FALSE to be BOTH"
  assert setVariable(VariableValue.TRUE, VariableValue.TRUE) == VariableValue.TRUE, "Expected TRUE + TRUE to be TRUE"
  assert setVariable(VariableValue.FALSE, VariableValue.FALSE) == VariableValue.FALSE, "Expected FALSE + FALSE to be FALSE"
  assert setVariable(VariableValue.BOTH, VariableValue.TRUE) == VariableValue.BOTH, "Expected BOTH + TRUE to be BOTH"

if __name__ == "__main__":
  result = testAll()
  if result == 0:
    logTestSuccess("All tests passed successfully!")
  else:
    logTestError(f"{result} tests failed.")