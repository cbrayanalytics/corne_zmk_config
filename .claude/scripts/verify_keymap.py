import re, sys

KEYMAP = "config/corne.keymap"
EXPECTED = 36

try:
    with open(KEYMAP) as f:
        content = f.read()
except FileNotFoundError:
    print(f"Keymap error — {KEYMAP} not found (run from the repo root)")
    sys.exit(1)

layers = re.findall(r'display-name = "([^"]+)".*?bindings = <(.*?)>;', content, re.DOTALL)

if not layers:
    print(f"Keymap error — no layers found in {KEYMAP}")
    sys.exit(1)

errors = []

for name, block in layers:
    count = len(re.findall(r'&\S+', block))
    status = "✓" if count == EXPECTED else "✗"
    if count != EXPECTED:
        errors.append(f"{name}: {count} (expected {EXPECTED})")
    print(f"  {status} {name}: {count}/{EXPECTED} bindings")

if errors:
    print(f"\nKeymap error — wrong binding count: {', '.join(errors)}")
    sys.exit(1)
