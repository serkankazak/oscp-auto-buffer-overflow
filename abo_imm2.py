#!/usr/bin/env python

import immlib, os, struct, socket, time, sys, binascii
from operator import itemgetter
from string import ascii_uppercase, ascii_lowercase, digits

def pattern_search(needle):
    haystack = ""
    for upper in ascii_uppercase:
        for lower in ascii_lowercase:
            for digit in digits:
                haystack += upper + lower + digit
                found_at = haystack.find(needle)
                if found_at > -1:
                    return found_at

def bform(inn):
    i = str("%02x" % inn)
    return str("\\x%s\\x%s\\x%s\\x%s" % (i[6:8], i[4:6], i[2:4], i[0:2]))
 
def main(args):
    
    imm = immlib.Debugger()
    imm.ignoreSingleStep()

    if (args[0] == "3"):            
        all = ""
        for i in digits + "abcdef":
            for j in digits + "abcdef":
                c = "%s%s" % (i, j)
                if c != "0a" and c != "0d" and c != "00" and c != "ff":
                    all += c
        sta = binascii.hexlify(imm.readMemory(imm.getRegs()["ESP"], len(all)))            
        diff = ""
        for i in xrange(0, len(all), 2):
            if all[i:i + 2] != sta[i: i + 2]:
                diff += "\\x" + all[i:i + 2]
        return diff

    if (args[0] == "2"):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((args[2], 9999))
        s.sendall(binascii.hexlify(imm.readMemory(imm.getRegs()["ESP"], int(args[1]))))
        return "ok"

    if (args[0] == "1"):

        esp = pattern_search(imm.readMemory(imm.getRegs()["ESP"], 4))
        eip = pattern_search(hex(imm.getRegs()["EIP"])[2:-1].decode("hex")[::-1])
        
        jesps = sorted(imm.search(imm.assemble("jmp esp")))
        
        mods1 = []
        mods2 = []
        
        for mod in imm.getAllModules():
            
            mzbase = mod.getBaseAddress()

            safeseh_offset = 0x5f
            if imm.getOsVersion() in ["6", "7", "8", "vista", "win7", "2008server", "win8", "win8.1", "win10"]:
                safeseh_offset = 0x5e

            if (struct.unpack('<H', imm.readMemory(mzbase + struct.unpack('<L', imm.readMemory(mzbase + 0x3c, 4))[0] + safeseh_offset, 2))[0] & 0x0040) == 0:
                mods1.append([mod.getSize(), mod.getBase()])
            else:
                mods2.append([mod.getSize(), mod.getBase()])        
        
        for m in sorted(mods1, key = itemgetter(0)):
            for j in jesps:
                if j >= m[1] and j <= m[1] + m[0]:
                    return str("%d, %s, %d" % (eip, bform(j), esp - eip - 4))
                    
        for m in sorted(mods2, key = itemgetter(0)):
            for j in jesps:
                if j >= m[1] and j <= m[1] + m[0]:
                    return str("%d, %s, %d" % (eip, bform(j), esp - eip - 4))

    return ""
