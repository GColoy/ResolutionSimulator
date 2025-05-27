import logging
from options import *

first = True

def logTestError(input):
  baseLog("ERROR: " + input)
  print("ERROR: " + input)

def logTestSuccess(input):
  baseLog("SUCCESS: " + input)
  print("SUCCESS: " + input)

def logTest(input):
  baseLog(input)
  print(input)

def baseLog(input):
  global first
  if first:
      logging.basicConfig(level=logging.INFO, format='%(message)s', filename=options.logFile, filemode='w')
      first = False
  logging.info(input)
  if not options.testLogMode:
    print(input)
  return

def log(level: VerboseLevel = VerboseLevel.JustSolution, input = ""):
  if options.verbouseLevel.value <= level.value:
    baseLog(input)
  return

def logTex(input):
  log(input)
  return
