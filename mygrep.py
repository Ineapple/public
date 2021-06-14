#!/usr/bin/python3
import sys
import os
import re
file= 'none'
a = 2
exit_code = 0
rx = {0:"",1:"",2:""}
textBefore = ''
textAfter = ''
b1 = True
b2 = False
block =''
b = False
printMatched = True
def p(var):
  global rx
  rx[0] = var
  return 2
def p2(var):
  global rx
  rx[1] = var
  return 2
def r(var):
  global rx
  rx[2] = var
  return 2
def nm(var):
  global printMatched
  printMatched = False
  return 1
options = { "-p": p,
            "-p2": p2,
            "-r": r,
            "--": nm
}
if len(sys.argv) > 1:
    filename = sys.argv[1]
    if (sys.argv[1] == "?"):
        print("-p: regex begin\n-p2: regex end\n--: print not matched\n++: print matched\n-r: replaced matched with string")
        exit(0)
    while a < len(sys.argv):
      if len(sys.argv) > a+1:
          inc = options[sys.argv[a]](sys.argv[a+1])
      else:
          inc = options[sys.argv[a]]("")
      a +=inc

    with open(os.path.join(os.getcwd(), sys.argv[1]), 'r') as f: # open in readonly mode
      file = f.read().split("\n")

    for line in file:
      if b:
        block += line+"\n"
        if rx[1] != "" and re.search(rx[1],line) is not None:
          b2 = True
          b = False
      if b2:
        textAfter += line+"\n"
      if rx[0] != "" and re.search(rx[0],line) is not None and b1:
        block += line+"\n"
        b1 = False
        if rx[1]!= "":
            b = True
        else:
            b2 = True
      if b1:
        textBefore += line+"\n"
if rx[2] != "":
    print(textBefore + rx[2] + "\n" + textAfter, end = '')
elif printMatched:

    if(block == ""):
        exit_code = 1
    else:
        print(block, end = '')
else:
    if textAfter == "" and textBefore == "":
        exit_code = 1
    else:
        print(textBefore +  textAfter, end = '')
sys.exit(exit_code)
