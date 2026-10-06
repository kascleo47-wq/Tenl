#from __future__ import braces

import os, sys
if len(sys.argv) != 2:
    print("need one .tnl file")
    exit(1)
var = {}
mem = [0] * 3000

def split_if(s, sep, ifch, ifch2):
    vec = []
    s2 = ""
    c = None
    dospl = True
    for part in s:
        if part == ifch:
            if dospl:
                dospl = False
                c = 1
            else:
                c += 1
        elif part == ifch2:
            c -= 1
            if c == 0:
                dospl = True
        elif part == sep:
            if dospl:
                vec.append(s2)
                s2 = ""
                continue
        s2 += part
    vec.append(s2)
    return vec


def run_block(s):
    global var, mem
    s = s.strip()
    if len(s) == 3 and s[0] == "*" and s[2] == "*":
        return ord(s[1])
    elif s.isdigit() or (len(s) >= 2 and s[0] == "-" and s[1:].isdigit()):
        return int(s)
    elif var.get(s) != None:
        return var[s]
    if len(s) < 2 or s[0] != "(" or s[-1] != ")":
        raise SyntaxError("needed braces or invalid syntax: " + s)
    s = split_if(s[1:][:-1].strip(), ",", "(", ")")
    if len(s) != 3:
        raise AttributeError("block must have 3 args (<com>, <val1>, <val2>): " + ",\n".join(s))
    match s[0].strip():
        case "set":
            var[s[1].strip()] = run_block(s[2])
            return 0
        case "printn":
            print(run_block(s[1]), run_block(s[2]))
            return 0
        case "printc":
            print(chr(run_block(s[1])) + chr(run_block(s[2])))
            return 0
        case "for":
            run = 0
            while True:
                if not run_block(s[1]):
                    return run
                run = run_block(s[2])
        case "if":
            if run_block(s[1]):
                return run_block(s[2])
            else:
                return 0
        case "do":
            run_block(s[1])
            run_block(s[2])
        case "inputc":
            return ord((input(chr(run_block(s[1])) + chr(run_block(s[2]))) + " ")[0])
        case "+":
            return run_block(s[1]) + run_block(s[2])
        case "-":
            return run_block(s[1]) - run_block(s[2])
        case "/":
            return int(run_block(s[1]) / run_block(s[2]))
        case "*":
            return run_block(s[1]) * run_block(s[2])
        case "%":
            return int(run_block(s[1]) % run_block(s[2]))
        case "<":
            return int(run_block(s[1]) < run_block(s[2]))
        case ">":
            return int(run_block(s[1]) > run_block(s[2]))
        case "==":
            return int(run_block(s[1]) == run_block(s[2]))
        case "!=":
            return int(run_block(s[1]) != run_block(s[2]))
        case "<=":
            return int(run_block(s[1]) <= run_block(s[2]))
        case ">=":
            return int(run_block(s[1]) >= run_block(s[2]))
        case _:
            raise NameError("keyword or Op not defined: " + s[0])
with open(sys.argv[1], "r") as f:
    scode = f.read()

scode = scode.strip()
code = ""
for part in scode.split("\n"):
    code += part.strip()
try:
    exi = run_block(code)
except Exception as err:
    print("<error>: " + str(err.args))
    exi = 1
exit(exi)