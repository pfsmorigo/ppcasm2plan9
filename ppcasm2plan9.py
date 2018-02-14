#!/usr/bin/env python
# coding=utf-8

import sys
import re
import pprint
import os.path
import pprint

instruction_list = {}
translation_list = {}

def ins_format(instruction):
    return re.sub('\s+', ' ', \
            instruction.split("#", 1)[0].replace('(', ' ').replace(',', ' ').replace(')', '')).strip().split()

def load_instruction_list():
    with open("list", "rtU") as f:
        for line in f:
            if line.strip().startswith("#"):
                continue
            line = line.strip().split('|')
            if len(line) is 2:
                original = ins_format(line[0])
                plan9 = line[1].strip()
                instruction_list[original[0] + ' ' + str(len(original) - 1)] = [ original, plan9 ]

def load_translation_list():
    if len(sys.argv) > 2 and os.path.isfile(sys.argv[2]):
        with open(sys.argv[2], "rtU") as f:
            for line in f:
                if line.strip().startswith("#"):
                    continue
                line = line.strip().split('|')
                if len(line) is 2:
                    translation_list[line[0].strip()] = line[1].strip()

def pre_translate(entry):
    for item in translation_list:
        entry = entry.replace(item, translation_list[item])
    return entry

def translate(ppcasm_entry):
    ppcasm_entry_formatted = ins_format(pre_translate(ppcasm_entry))
    if ppcasm_entry_formatted:
        list_entry = instruction_list.get(ppcasm_entry_formatted[0] + \
                ' ' + str(len(ppcasm_entry_formatted) - 1), '')
        if list_entry:
            ppcasm_formatted = list_entry[0]
            plan9 = list_entry[1].split(' ', 1)

            for num in range(1, len(ppcasm_formatted)):
                prefix = ""
                # if using variables, doesn't add the R prefix
                if not is_number(ppcasm_entry_formatted[num]):
                    prefix = "R"

                plan9[1] = plan9[1].replace(prefix+ppcasm_formatted[num], \
                        ppcasm_entry_formatted[num])

            if len(plan9) > 1:
                return plan9[0] + " " + plan9[1]
            else:
                return plan9[0]

    return ""

def is_number(text):
    try:
        int(text)
        return True
    except ValueError:
        return False


load_instruction_list()
load_translation_list()

with open(sys.argv[1], "rtU") as f:
    global_func = ""
    for line in f:
        matchObj = re.match('^\s+', line, re.M|re.I)
        indentation = matchObj.group() if matchObj else ''

        exclude_list = [ ".align", ".machine",
                         ".abiversion", ".text", "#include" ]
        ppcasm_entry = line.strip()
        if any(word in ppcasm_entry for word in exclude_list):
            continue
        elif ppcasm_entry.startswith("__"):
            continue
        elif ppcasm_entry.startswith("_GLOBAL"):
            global_func = ppcasm_entry.replace("_GLOBAL(", "").strip(")")
            print("TEXT ·%s(SB),NOSPLIT|NOFRAME,$0" % global_func)
        elif ppcasm_entry.endswith(":"):
            func_name = "%s" % ppcasm_entry.strip(".: \t")
            if func_name != global_func:
                print("\n%s:" % func_name.lower())
        elif ppcasm_entry:
            print("%s%-30s // %s" % (indentation, translate(ppcasm_entry), ppcasm_entry))
        else:
            print ''
