# Karabiner Complex Modifications

Karabiner-Elements complex modification rules for using an **external ANSI (US) keyboard** on a Mac whose built-in keyboard is German and whose macOS input source is set to **German layout**.

## Setup

| Device | Physical layout | macOS sees |
|--------|----------------|------------|
| MacBook built-in keyboard | German | German layout — works as-is |
| External keyboard | ANSI (US) | German layout — keys are wrong without remapping |
| Windows.app (remote Windows session) | — | Windows German layout on the remote side |

Because macOS is configured for German layout, the external ANSI keyboard sends the wrong characters: the ANSI `[` key position is interpreted as `ü`, `/` as `-`, etc. These rules intercept the ANSI key codes and re-emit the correct key+modifier combos that produce the intended characters under the German macOS layout.

The Windows.app scenario adds a further layer: keystrokes sent into Windows.app reach a Windows system also running German layout, so some mappings differ from the native macOS case (e.g. the first commit "Fix ANSI to German Windows mappings for Windows.app").

## Structure

All rule files live in `singles/`, one file per key group. Each file has this shape:

```json
{
    "title": "...",
    "rules": [{
        "description": "...",
        "manipulators": [ ... ]
    }]
}
```

The format is **JSONC** (JSON with `// line comments`), which Karabiner-Elements accepts.

## Universal condition

Every manipulator applies only to **external keyboards**:

```json
"conditions": [{
    "type": "device_if",
    "identifiers": [{ "is_built_in_keyboard": false }]
}]
```

This leaves the built-in German keyboard untouched.

## Files in `singles/`

| File | Maps |
|------|------|
| `ansi_yz_swap.json` | Y↔Z (ANSI Y position → German Z and vice versa) |
| `ansi_angles.json` | `<` `>` `/` `?` |
| `brackets_ansi.json` | `[` `]` `{` `}` (ANSI bracket keys → opt+5/6/8/9 in German layout) |
| `backslash_ansi.json` | `\` → opt+shift+7, `|` → opt+7 |
| `comma_ansi.json` | `;` `:` `'` `"` |
| `ansi_equal.json` | `=` → shift+0, `+` → close_bracket |
| `ansi_grave_tilde.json` | `` ` `` → shift+equal, `~` → opt+n |
| `numbers_shift.json` | shift+number symbols: `@` `#` `^` `&` `*` `(` `)` |
| `ansi_hyphen.json` | `-` → slash, `_` → shift+slash |
| `ansi_plus.json` | CMD+shift+= (zoom in), CMD+- (zoom out) |
| `ansi_commands.json` | CMD+/ (toggle comment) → CMD+shift+7 |
| `ansi_umlaut_cmd.json` | CMD/OPT shortcuts to type ä Ä ö Ö ü Ü ß |
| `ansi_function_keys.json` | Brightness keys → F1/F2; CMD+space → F4; dictation → F5 |
| `ansi_consumer_keys.json` | F1/F2 → brightness decrement/increment (Fn mode, inverse direction) |
| `windows_app_cmd_as_ctrl.json` | **Windows App only:** CMD → CTRL (left+right); bundle ID `com.microsoft.rdc.macos` |

## Key code reference

Karabiner uses its own key code names. Common ones relevant here:

| Karabiner name | ANSI physical key |
|----------------|-------------------|
| `grave_accent_and_tilde` | `` ` `` / `~` |
| `open_bracket` | `[` |
| `close_bracket` | `]` |
| `backslash` | `\` |
| `semicolon` | `;` |
| `quote` | `'` |
| `equal_sign` | `=` |
| `hyphen` | `-` |
| `slash` | `/` |

## Adding a new mapping

1. Identify the key code the ANSI keyboard sends (`from`).
2. Find which key+modifier combo produces the desired character under German macOS layout (`to`).
3. If the mapping only applies inside Windows.app, add a `frontmost_application_if` condition alongside the `device_if` condition.
4. Add a manipulator to the appropriate file in `singles/`, or create a new file following the existing structure.
5. Always include the `device_if` / `is_built_in_keyboard: false` condition.
6. Add a `// comment` above each manipulator indicating the character it produces.
