import logging

first = True

def logTestError(input):
   print("ERROR: " + input)
   log(input)

def logTestSuccess(input):
  print("SUCCESS: " + input)
  log(input)

def log(input):
  global first
  if first:
      logging.basicConfig(level=logging.INFO, format='%(message)s', filename='resolution.log', filemode='w')
      first = False
  logging.info(input)
  print(input)
  return

def flush():
  logging.basicConfig(level=logging.INFO, format='%(message)s')
  logging.getLogger().handlers[0].flush()

def logTex(input):
  # global first
  # if first:
  #     logging.basicConfig(level=logging.INFO, format='%(message)s', filename='tex.log', filemode='w')
  #     first = False
  # logging.info(" & " + input + "  \\\\")
  # print(input)
  return