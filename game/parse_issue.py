import sys
import re

body = sys.stdin.read()

if "Reset Game" in body:
    print("reset")
else:
    match = re.search(r'Drop in Column (\d)', body)
    if match:
        print(f"drop|{match.group(1)}")
    else:
        print("invalid")
