from dataclasses import dataclass
from dataclasses import field

@dataclass
class Options:
  logTex: bool = False
  verbouse: bool = False
  logFile: str = "resolution.log"
  stopAtEmptySet: bool = True

options = Options()