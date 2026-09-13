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

adjust_bindings = next((block for name, block in layers if name == "Adjust"), "")
required_layout_selections = (
    "&to QWERTY",
    "&to DVORAK",
    "&to COLEMAK",
    "&to COLEMAKDH",
)
missing_selections = [binding for binding in required_layout_selections if binding not in adjust_bindings]

if missing_selections:
    errors.append(f"Adjust: missing exclusive layout selections: {', '.join(missing_selections)}")

if "&tog " in adjust_bindings:
    errors.append("Adjust: layout selection must use &to, not &tog")

if errors:
    print(f"\nKeymap error: {', '.join(errors)}")
    sys.exit(1)
