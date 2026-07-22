from pathlib import Path
from html import escape
T={0:"View Source",1:"Right-Click Block",2:"Directory Traversal (Files)",3:"Web Crawlers (Robots.txt)",4:"Referer Spoofing",5:"Cookie Manipulation",6:"Hidden Inclusion Files",7:"Local File Inclusion (LFI)",8:"Reversing Crypto Schemes",9:"Command Injection I",10:"Command Injection II (Sanitization Bypass)",11:"XOR Encryption Bypass",12:"Arbitrary File Upload (Web Shell)",13:"File Upload Bypass (Magic Bytes)",14:"SQL Injection (SQLi)"}
def main(root):
 root=Path(root)
 for n,title in T.items():
  text="CEI Labs Natas %d: %s\nAccount: natas%d\nAuthorized CEI Labs training only. Misuse of this system is prohibited.\nDo not use AI or external tools/services to cheat or obtain answers.\n"%(n,title,n)
  (root/("natas%d.html"%n)).write_text('<pre class="cei-login-banner">'+escape(text)+'</pre>',"ascii")
if __name__=="__main__":
 import sys; main(sys.argv[1])
