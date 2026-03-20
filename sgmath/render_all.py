"""
Render all Singapore Math videos by level.
Usage:
    python render_all.py              # 720p all videos
    python render_all.py --hd         # 1080p for YouTube
    python render_all.py --preview    # 480p fast preview
    python render_all.py --level p3   # Only render P3 videos
"""
import subprocess
import sys
import os

SCENES = {
    "P1": [
        ("scenes/p1_01_number_bonds.py", "P1_NumberBonds"),
        ("scenes/p1_02_comparing_numbers.py", "P1_ComparingNumbers"),
        ("scenes/p1_03_addition_within_20.py", "P1_AdditionWithin20"),
    ],
    "P2": [
        ("scenes/p2_01_bar_model_addition.py", "P2_BarModelAddition"),
        ("scenes/p2_02_multiplication_groups.py", "P2_MultiplicationGroups"),
        ("scenes/p2_03_subtraction_regrouping.py", "P2_SubtractionRegrouping"),
    ],
    "P3": [
        ("scenes/p3_01_fractions.py", "P3_Fractions"),
        ("scenes/p3_02_area_perimeter.py", "P3_AreaPerimeter"),
        ("scenes/p3_03_time_duration.py", "P3_TimeDuration"),
    ],
    "P4": [
        ("scenes/p4_01_equivalent_fractions.py", "P4_EquivalentFractions"),
        ("scenes/p4_02_angles.py", "P4_Angles"),
        ("scenes/p4_03_bar_model_comparison.py", "P4_BarModelComparison"),
    ],
    "P5": [
        ("scenes/p5_01_percentage.py", "P5_Percentage"),
        ("scenes/p5_02_volume.py", "P5_Volume"),
        ("scenes/p5_03_ratio.py", "P5_Ratio"),
    ],
    "P6": [
        ("scenes/p6_01_algebra.py", "P6_Algebra"),
        ("scenes/p6_02_speed_distance_time.py", "P6_SpeedDistanceTime"),
        ("scenes/p6_03_pie_chart.py", "P6_PieChart"),
    ],
}

def main():
    quality = "-qm"
    if "--hd" in sys.argv:
        quality = "-qh"
    elif "--preview" in sys.argv:
        quality = "-ql"

    # Filter by level
    level_filter = None
    for arg in sys.argv:
        if arg.startswith("--level"):
            idx = sys.argv.index(arg)
            if idx + 1 < len(sys.argv):
                level_filter = sys.argv[idx + 1].upper()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    total = 0
    errors = 0

    for level, scenes in SCENES.items():
        if level_filter and level != level_filter:
            continue

        print(f"\n{'#'*60}")
        print(f"  {level} - Singapore Math Series")
        print(f"{'#'*60}")

        for filepath, scene_name in scenes:
            total += 1
            full_path = os.path.join(script_dir, filepath)
            print(f"\n  Rendering: {scene_name}")
            cmd = ["manim", quality, full_path, scene_name]
            result = subprocess.run(cmd, cwd=script_dir)
            if result.returncode != 0:
                print(f"  ERROR: {scene_name}")
                errors += 1
            else:
                print(f"  Done: {scene_name}")

    print(f"\n{'='*60}")
    print(f"  Rendered {total - errors}/{total} videos successfully.")
    if errors:
        print(f"  {errors} video(s) had errors.")
    print(f"  Output: media/videos/")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
