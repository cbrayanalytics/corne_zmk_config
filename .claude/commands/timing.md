Show the current HRM (home-row mod) timing configuration and explain each parameter.

Steps:
1. Run `grep -A4 '&mt {' config/corne.keymap` to extract the current mt timing block
2. Run `grep -A4 '&lt {' config/corne.keymap` to extract the current lt timing block
3. Report the values in a table and explain what each one does:
   - `tapping-term-ms` — max duration of a keypress before it's treated as a hold (mod); shorter = faster mod activation threshold
   - `require-prior-idle-ms` — how long the keyboard must be idle before a hold can activate; higher = safer during fast typing bursts
   - `flavor` — `"balanced"` resolves tap-vs-hold on key release; `"tap-preferred"` always favors the tap unless clearly held past tapping-term
4. Suggest typical tuning directions:
   - Accidental mods during fast typing → raise `require-prior-idle-ms`
   - Mods slow to activate → lower `tapping-term-ms`
   - Still getting wrong keys → try `flavor = "tap-preferred"`
