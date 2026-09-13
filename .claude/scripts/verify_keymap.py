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

normalized_adjust_bindings = " ".join(adjust_bindings.split())
expected_layout_row = "&to QWERTY &to DVORAK &to COLEMAK &to COLEMAKDH &bt BT_CLR"
expected_bluetooth_row = "&bt BT_SEL 4 &bt BT_SEL 3 &bt BT_SEL 2 &bt BT_SEL 1 &bt BT_SEL 0"

if expected_layout_row not in normalized_adjust_bindings:
    errors.append("Adjust: layout row must be QWERTY, DVORAK, COLEMAK, COLEMAKDH, BT CLR")

if expected_bluetooth_row not in normalized_adjust_bindings:
    errors.append("Adjust: Bluetooth profiles must run BT4 through BT0")

for name in ("Dvorak", "Colemak", "ColemakDH"):
    bindings = next((re.findall(r'&\S+', block) for layer, block in layers if layer == name), [])
    if bindings[-6:] != ["&trans"] * 6:
        errors.append(f"{name}: thumb bindings must be transparent")

if layers[-1][0] != "Adjust":
    errors.append("Adjust: must be the highest-numbered layer")

adjust_define = re.search(r"^#define\s+ADJUST\s+(\d+)\s*$", content, re.MULTILINE)
if not adjust_define or int(adjust_define.group(1)) != len(layers) - 1:
    errors.append("Adjust: define must equal highest layer number")

if errors:
    print(f"\nKeymap error: {', '.join(errors)}")
    sys.exit(1)
