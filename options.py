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
  removeTrivialAtEnd: bool = False
  removeTrivialEachItteration: bool = False

options = Options()