"""
Render all 50 Primary 1 Singapore Math videos.
Usage:
    python render_p1.py              # 720p
    python render_p1.py --hd         # 1080p for YouTube
    python render_p1.py --preview    # 480p fast preview
    python render_p1.py --scene 5    # Render only scene 5
"""
import subprocess, sys, os, re, time

SCENES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes")

def discover_p1_scenes():
    """Find all p1_XX_*.py files and extract scene class names."""
    scenes = []
    for fn in sorted(os.listdir(SCENES_DIR)):
        m = re.match(r"p1_(\d+)_(.+)\.py$", fn)
        if not m:
            continue
        num = int(m.group(1))
        filepath = os.path.join(SCENES_DIR, fn)
        # Extract class name from file
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        cls_match = re.search(r"class\s+(P1_\w+)\s*\(", content)
        if cls_match:
            scenes.append((num, fn, cls_match.group(1), filepath))
    return scenes

def main():
    quality = "-qh"
    if "--hd" in sys.argv:
        quality = "-qh"
    elif "--preview" in sys.argv:
        quality = "-ql"
    elif "--4k" in sys.argv:
        quality = "-qk"

    single = None
    if "--scene" in sys.argv:
        idx = sys.argv.index("--scene")
        if idx + 1 < len(sys.argv):
            single = int(sys.argv[idx + 1])

    scenes = discover_p1_scenes()
    if not scenes:
        print("No P1 scenes found in scenes/ directory.")
        print("Run gen_part1.py first to generate scene files.")
        return

    if single:
        scenes = [s for s in scenes if s[0] == single]
        if not scenes:
            print(f"Scene p1_{single:02d} not found.")
            return

    print(f"\n{'='*60}")
    print(f"  Singapore Math P1 - Rendering {len(scenes)} videos")
    print(f"  Quality: {quality}")
    print(f"{'='*60}\n")

    ok, fail = 0, 0
    start = time.time()

    for num, fn, cls, filepath in scenes:
        print(f"  [{num:02d}/{scenes[-1][0]:02d}] {cls} ...", end=" ", flush=True)
        cmd = ["manim", quality, filepath, cls]
        result = subprocess.run(cmd, capture_output=True, cwd=SCENES_DIR)
        if result.returncode == 0:
            print("✓")
            ok += 1
        else:
            print("✗ ERROR")
            fail += 1
            stderr = result.stderr.decode("utf-8", errors="replace")
            for line in stderr.strip().split("\n")[-3:]:
                print(f"        {line}")

    elapsed = time.time() - start
    print(f"\n{'='*60}")
    print(f"  Done: {ok} rendered, {fail} failed ({elapsed:.0f}s)")
    print(f"  Output: media/videos/")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
