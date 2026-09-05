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

> **Layer ordering rule:** ADJUST must always be the highest layer number. Toggleable layout layers (QWERTY, COLEMAK, COLEMAKDH) have higher ZMK priority than any lower-numbered layer. If ADJUST is not the top layer, its toggle keys become unreachable while an alternate layout is active. Current order: DVORAK=0, QWERTY=1, LOWER=2, RAISE=3, COLEMAK=4, COLEMAKDH=5, ADJUST=6.

| # | Name | Access |
|---|------|--------|
| 0 | DVORAK | Default |
| 1 | QWERTY | `&tog QWERTY` on ADJUST row 2 col 0 |
| 2 | LOWER | Hold left-thumb middle key |
| 3 | RAISE | Hold right-thumb SPACE |
| 4 | COLEMAK | `&tog COLEMAK` on ADJUST row 1 col 0 |
| 5 | COLEMAKDH | `&tog COLEMAKDH` on ADJUST row 1 col 1 |
| 6 | ADJUST | Hold right-thumb BSPC |

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

Home-row mods (`&mt`: balanced, tapping-term 200ms, require-prior-idle 250ms, quick-tap 175ms):

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

Same home-row mods as DVORAK (ASDF left / JKL; right). Thumb keys are `&trans` — LOWER/RAISE/ADJUST momentary layers from DVORAK still work while QWERTY is active because they have higher layer numbers (2/3/6).

### COLEMAK (layer 4) — toggled alternative

```
Q   W   F   P   G     J   L   U   Y   ;
A   R   S   T   D     H   N   E   I   O
Z   X   C   V   B     K   M   ,   .   /
```

Same home-row mod positions as DVORAK: A R S T left / N E I O right. Thumb keys are `&trans`.

### COLEMAK-DH (layer 5) — toggled alternative

```
Q   W   F   P   B     J   L   U   Y   ;
A   R   S   T   G     M   N   E   I   O
Z   X   C   D   V     K   H   ,   .   /
```

Mod-DH variant: B/G swap on rows 1–2, D/H move to row 3. Same HRM positions as Colemak. Thumb keys are `&trans`.

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

### ADJUST (layer 6) — Bluetooth, media, system

```
CMK  CDH   -    -    -       -     -     -     -     -
TOG  BT2  BT1  BT0  BTCLR  C_PP  VOLU  VOLD  NEXT  PREV
BOOT RST   -    -   SOFF    -     -     -    RST   BOOT
```

`TOG` = `&tog QWERTY`, `CMK` = `&tog COLEMAK`, `CDH` = `&tog COLEMAKDH`

Only one alternative layout should be active at a time — higher layer number wins if multiple are toggled on.

## Making Common Changes

### Remap a key

Edit `config/corne.keymap`. Find the layer, locate the key position in the `bindings = < ... >` block (left-to-right, top-to-bottom, row by row), and replace the binding.

### Add a home-row mod

Replace `&kp KEY` with `&mt MODIFIER KEY`. Available modifiers: `LGUI LALT LCTRL LSHIFT RGUI RALT RCTRL RSHIFT`.

### Change mod-tap timing

`&mt` and `&lt` are tuned **separately and must stay that way** — they solve opposite
problems. `&mt` drives home-row mods, where the risk is a fast letter tap misfiring as a
modifier. `&lt` drives the thumb layer keys (`&lt RAISE SPACE`, `&lt ADJUST BSPC`), where
the risk is losing a space. Do not copy settings between the two blocks.

Current values in `corne.keymap`:

| Property | `&mt` (home row) | `&lt` (thumbs) |
|----------|------------------|----------------|
| `tapping-term-ms` | 200 | 200 |
| `flavor` | `balanced` | `tap-preferred` |
| `require-prior-idle-ms` | 250 | *(none — see warning)* |
| `quick-tap-ms` | 175 | 175 |

Parameters:
- `tapping-term-ms` — hold vs tap threshold (ms)
- `require-prior-idle-ms` — if the key is pressed within this window of the *previous*
  keypress, it resolves as a **tap immediately** and the hold is never considered
- `quick-tap-ms` — re-pressing within this window after a tap always taps (enables key repeat)
- `flavor` — `"balanced"` resolves a hold if another key is pressed *and released* during
  the hold; `"tap-preferred"` only holds once the tapping term expires, so rollover can
  never steal the tap

> **Never set `require-prior-idle-ms` on `&lt`.** During normal typing the previous
> keypress is almost always under the threshold, so every thumb press force-taps and the
> layer becomes **completely unreachable**. This silently broke RAISE and ADJUST until
> commit `28447b6`. The setting is correct on `&mt` (home-row keys are surrounded by fast
> typing) and wrong on thumb keys.
>
> If you remove it from `&lt`, `flavor` **must** be `tap-preferred`. Under `balanced`,
> `require-prior-idle-ms` was the only thing protecting the space tap during rollover —
> dropping it while leaving `balanced` in place makes spaces vanish constantly.

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

## Git Workflow

Commit after each completed logical task — do not batch unrelated changes. Each commit should:

1. Cover one change (one layer edit, one config flag, one refactor)
2. Pass the 36-binding verification before committing
3. Use the `.gitmessage` template format: imperative title + one-line why

Note: `/build` pushes commits but does **not** auto-commit — stage and commit changes first or the push will be a no-op.

## Verification

After editing `corne.keymap`, confirm each layer still has exactly 36 bindings:

```sh
python3 .claude/scripts/verify_keymap.py
```

This script is also run automatically by a hook after every `Edit` or `Write` to `corne.keymap`.

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/verify` | Run binding count check — flags any layer not at exactly 36 |
| `/layers` | Print a human-readable summary of every layer |
| `/build` | Push current branch and report GitHub Actions CI status |
| `/timing` | Show current HRM timing values and tuning guidance |

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
