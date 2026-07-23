from pathlib import Path

TITLES = {1:"ROT13 Substitution Cipher",2:"Caesar Cipher (Unknown Shift)",3:"Frequency Analysis",4:"Vigenere Cipher (Known Key Length)",5:"Vigenere Cipher (Kasiski Test)",6:"Stream Cipher / LFSR"}
POLICY=("Authorized CEI Labs training only. Misuse of this system is prohibited.","Do not use AI or external tools/services to cheat or obtain answers.","Stay within your assigned challenge environment only.")
def render(level):
    if set(TITLES)!=set(range(1,7)): raise ValueError("Krypton coverage")
    lines=["  .-.-."," ( lock ) CEI Labs Krypton %d: %s"%(level,TITLES[level]),"  `-'-'","Logged in as krypton%d"%level, "Final level: submit your result; there is no next account." if level==6 else "Submit this level, then use CTFd launch panel for krypton%d."%(level+1),*POLICY]
    if any(any(ord(c)>127 for c in line) or len(line)>80 for line in lines): raise ValueError("unsafe banner")
    return "\n".join(lines)+"\n"
def generate(root):
    root=Path(root)
    for level in range(1,7): (root/("krypton%d"%level)).write_text(render(level),encoding="ascii")
if __name__=="__main__":
    import sys; generate(sys.argv[1])
