# Singapore Math Visualization Videos

Animated math problem videos for children using Manim, based on the Singapore Math curriculum.

## Problems Covered
1. **Number Bonds** (P1) - Breaking numbers into parts
2. **Bar Model - Addition** (P2) - Visual addition with bar models
3. **Multiplication as Groups** (P2-P3) - Understanding multiplication
4. **Fractions** (P3) - Understanding fractions visually
5. **Area & Perimeter** (P3-P4) - Rectangle area and perimeter

## How to Render

Render all videos:
```bash
python render_all.py
```

Render a single scene:
```bash
manim -pql scenes/01_number_bonds.py NumberBonds
```

## Quality Options
- `-ql` = 480p (fast preview)
- `-qm` = 720p
- `-qh` = 1080p (YouTube ready)
- `-qk` = 4K
