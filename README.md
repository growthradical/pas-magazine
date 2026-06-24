# ПАС — Macedonian Football Monthly

Brand system and print-ready artwork for **ПАС**, a Macedonian football magazine.
Aesthetic: minimalist, socialist, Yugoslav-Macedonian — Cyrillic display type, a
three-ink palette (socialist red, star gold, newsprint cream, warm ink), heavy
rules and framed devices.

## Edition 01
- **Main coverline:** Времето на ЛИСЕЦОТ (Vasil Ringov, retro feature)
- Secondary: Македонија на Светско · Вардар, Шкендија и Силекс во еврокуповите
- Bottom: Копачки за Џеко (designer) · Европски биланс (results)

## Contents
| Path | What |
|------|------|
| `brandkit.html` / `out/PAS_brandkit.pdf` | Brand-book sheet (logo, palette, type, elements) |
| `cover.html` / `out/PAS_01_cover.pdf` | Cover #01, print-ready |
| `brand.css` | Design tokens + components |
| `fonts.css` | Base64-embedded fonts (self-contained render) |
| `grade.py` | 80s-magazine duotone/halftone photo grade |
| `img/` | Source + graded featured photo |
| `fonts/` | Oswald, PT Sans / Narrow / Serif (OFL) |

## Design specs
- **Trim:** A4 portrait (210×297 mm) + **3 mm bleed** → 216×303 mm page box
- **Photo:** embedded at 300 dpi
- **Palette:** Хартија `#ECE4D4` · Мастило `#1A1512` · Црвена `#B3122B` · Злато `#D29A32`
- **Type:** Oswald (display) · PT Sans family (text/labels/quotes) — all Cyrillic

## Rebuild
```bash
python grade.py            # regenerate graded photo
# render with headless Chrome:
chrome --headless=new --no-pdf-header-footer \
  --print-to-pdf=out/PAS_01_cover.pdf cover.html
```

## Notes
- Source featured photo is low-res (770×513); the grain/halftone grade makes the
  upscale read as intentional vintage. Swap in a higher-res scan when available.
- The two bottom tiles use on-brand line illustrations as placeholders — swap for
  real photos for the Џеко-boots and euro-results stories.

Fonts are licensed under the SIL Open Font License.
