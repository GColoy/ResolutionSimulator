from dataclasses import dataclass
from dataclasses import field
from enum import Enum

class VerboseLevel(Enum):
  AllResolutions = 0
  AllValidResolutions = 1
  AllNewResolutions = 2
  AfterEachRecursionVerbose = 3
  AfterEachRecursion = 4
  JustSolution = 5

@dataclass
class Options:
  logTex: bool = False
  verbouseLevel: VerboseLevel = VerboseLevel.AllResolutions
  logFile: str = "resolution.log"
  testLogMode: bool = False
  stopAtEmptySet: bool = True
  stopWhenFoundKlausel = None # Needs klausel as type; NOT WORKING YET
  stopAfterStep: int = -1  # -1 means no limit
  removeTrivialAtEnd: bool = False
  removeTrivialEachItteration: bool = False
  optimiseTree: bool = True

options = Options()