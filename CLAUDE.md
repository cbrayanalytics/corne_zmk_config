# Corne ZMK Config — Dvorak

ZMK firmware configuration for a **Keebmaker Corne 3x5** (36-key wireless split keyboard) using **Nice!Nano v2** microcontrollers. Dvorak is the default layout with a toggleable QWERTY layer.

## Hardware

| Property | Value |
|----------|-------|
| Keyboard | Keebmaker Corne 3x5 (18 keys per half) |
| MCU | Nice!Nano v2 (nRF52840, BLE) |
| Display | OLED (enabled) |
| RGB | **Disabled** (battery life) |
| Matrix | `five_column_transform` (3 rows × 5 cols + 3 thumb keys per side) |

## Building

Firmware builds automatically on push via `.github/workflows/build.yml` (delegates to `zmkfirmware/zmk@v0.3`). No local build required. After pushing, check the Actions tab on GitHub for the `.uf2` artifacts.

To bump the ZMK version: change `revision` in `config/west.yml`.

## Key Files

| File | Purpose |
|------|---------|
| `config/corne.keymap` | All layers and bindings |
| `config/corne.conf` | Kconfig feature flags (RGB off, OLED on) |
| `config/west.yml` | ZMK version pin + module list |
| `config/corne_left.overlay` | Left half device tree (matrix transform) |
| `config/corne_right.overlay` | Right half device tree (matrix transform) |
| `build.yaml` | GitHub Actions build matrix |

## Layer Map

| # | Name | Access |
|---|------|--------|
| 0 | DVORAK | Default |
| 1 | QWERTY | `&tog QWERTY` on ADJUST row 2 col 0 |
| 2 | LOWER | Hold left-thumb middle key |
| 3 | RAISE | Hold right-thumb SPACE |
| 4 | ADJUST | Hold right-thumb BSPC |

### Thumb cluster

```
Left:  [ ESC ]  [ mo(LOWER) ]  [ TAB ]
Right: [ ENT ]  [ lt(RAISE) SPC ]  [ lt(ADJUST) BSPC ]
```

### DVORAK (layer 0)

```
'   ,   .   P   Y     F   G   C   R   L
A   O   E   U   I     D   H   T   N   S
;   Q   J   K   X     B   M   W   V   Z
```

Home-row mods (balanced, tapping-term 250ms, require-prior-idle 150ms):

```
Left pinky→index:  A=LGUI  O=LALT  E=LCTRL  U=LSHIFT
Right index→pinky: H=RSHIFT  T=RCTRL  N=RALT  S=RGUI
```

### QWERTY (layer 1) — toggled fallback

```
Q   W   E   R   T     Y   U   I   O   P
A   S   D   F   G     H   J   K   L   ;
Z   X   C   V   B     N   M   ,   .   /
```

Same home-row mods as DVORAK (ASDF left / JKL; right). Thumb keys are `&trans` — LOWER/RAISE/ADJUST momentary layers from DVORAK still work while QWERTY is active because they have higher layer numbers (2/3/4).

### LOWER (layer 2) — symbols, arrows, F-keys

```
`   [   {   \   -     =   /   }   ]   '
GUI ALT CTL SFT DEL   ←   ↓   ↑   →  RSFT
F1  F2  F3  F4  F5    F6  F7  F8  F9  F10
```

### RAISE (layer 3) — numbers, navigation

```
1   2   3   4   5     6   7   8   9   0
GUI ALT CTL SFT  -     -  SFT CTL ALT GUI
-   HOM PUP PDN END    -   -   -   -   -
                       ENT
```

### ADJUST (layer 4) — Bluetooth, media, system

```
 -    -    -    -    -       -     -     -     -     -
TOG  BT2  BT1  BT0  BTCLR  C_PP  VOLU  VOLD  NEXT  PREV
BOOT RST   -    -   SOFF    -     -     -    RST   BOOT
```

`TOG` = `&tog QWERTY` (toggles layer 1 on/off)

## Making Common Changes

### Remap a key

Edit `config/corne.keymap`. Find the layer, locate the key position in the `bindings = < ... >` block (left-to-right, top-to-bottom, row by row), and replace the binding.

### Add a home-row mod

Replace `&kp KEY` with `&mt MODIFIER KEY`. Available modifiers: `LGUI LALT LCTRL LSHIFT RGUI RALT RCTRL RSHIFT`.

### Change mod-tap timing

Edit the `&mt` or `&lt` block near the top of `corne.keymap`:
- `tapping-term-ms` — hold vs tap threshold (ms)
- `require-prior-idle-ms` — prevents accidental mod activation during fast typing
- `flavor` — `"balanced"` resolves ambiguity on key release; `"tap-preferred"` favors taps

### Re-enable RGB underglow

In `config/corne.conf`:
```
CONFIG_ZMK_RGB_UNDERGLOW=y
CONFIG_WS2812_STRIP=y
```

Then restore the `#include <dt-bindings/zmk/rgb.h>` line and `&rgb_ug` bindings in `corne.keymap`, and add `&led_strip { chain-length = <24>; };` at the end.

### Add a new layer

1. Add a `#define NEWLAYER N` at the top of `corne.keymap`
2. Add the layer block inside `keymap { ... }` with exactly 36 bindings
3. Add a trigger key (`&mo N`, `&lt N KEY`, or `&tog N`) in an existing layer

## Verification

After editing `corne.keymap`, confirm each layer still has exactly 36 bindings:

```sh
python3 -c "
import re
with open('config/corne.keymap') as f:
    content = f.read()
layers = re.findall(r'display-name = \"([^\"]+)\".*?bindings = <(.*?)>;', content, re.DOTALL)
for name, block in layers:
    print(f'{name}: {len(re.findall(chr(38) + r\"\S+\", block))} bindings')
"
```

## ZMK Key Name Reference

| Character | ZMK name |
|-----------|----------|
| `'` | `SQT` |
| `` ` `` | `GRAVE` |
| `,` | `COMMA` |
| `.` | `DOT` |
| `;` | `SEMI` |
| `/` | `FSLH` |
| `\` | `BSLH` |
| `[` | `LBKT` |
| `]` | `RBKT` |
| `{` | `LBRC` |
| `}` | `RBRC` |
| `-` | `MINUS` |
| `=` | `EQUAL` |
| Numbers | `N0`–`N9` |
| F-keys | `F1`–`F24` |
| Page Up/Down | `PG_UP` / `PG_DN` |

Full reference: https://zmk.dev/docs/codes
