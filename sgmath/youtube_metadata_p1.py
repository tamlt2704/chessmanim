"""
YouTube metadata for 50 Primary 1 Singapore Math videos.
Optimized for YouTube SEO targeting parents & kids searching for P1 math help.

Usage:
    python youtube_metadata_p1.py              # Print all metadata
    python youtube_metadata_p1.py --csv        # Export as CSV
    python youtube_metadata_p1.py --json       # Export as JSON
"""
import json, csv, sys, io

CHANNEL = "Singapore Math for Kids"
PLAYLIST = "Singapore Math Primary 1 - Complete Course (50 Lessons)"

COMMON_TAGS = [
    "singapore math", "primary 1 math", "P1 math", "math for kids",
    "math animation", "learn math", "singapore curriculum", "manim",
    "kindergarten math", "grade 1 math", "year 1 maths",
]

VIDEOS = [
    {
        "ep": 1, "scene": "P1_NumberBonds", "file": "p1_01_number_bonds.py",
        "title": "Number Bonds - Breaking 10 Into Parts | Singapore Math P1 Ep1",
        "desc": "Learn how to split 10 into two parts using number bond diagrams and dot visualizations. A fun way to understand addition!",
        "tags": ["number bonds", "breaking 10", "addition basics"],
    },
    {
        "ep": 2, "scene": "P1_ComparingNumbers", "file": "p1_02_comparing_numbers.py",
        "title": "Comparing Numbers - Which is Greater? | Singapore Math P1 Ep2",
        "desc": "Use block towers to compare numbers visually. Learn the greater than (>) and less than (<) symbols.",
        "tags": ["comparing numbers", "greater than", "less than"],
    },
    {
        "ep": 3, "scene": "P1_AdditionWithin20", "file": "p1_03_addition_within_20.py",
        "title": "Addition Within 20 - Make 10 Strategy | Singapore Math P1 Ep3",
        "desc": "Solve 8 + 5 using the Make 10 strategy! Fill the ten frame first, then count what's left. A powerful mental math trick.",
        "tags": ["addition", "make 10", "ten frame", "mental math"],
    },
    {
        "ep": 4, "scene": "P1_SubtractionWithin10", "file": "p1_04_subtraction_within_10.py",
        "title": "Subtraction Within 10 - Taking Away | Singapore Math P1 Ep4",
        "desc": "Learn subtraction by crossing out dots! Watch 9 - 4 come alive with colorful animations.",
        "tags": ["subtraction", "taking away", "within 10"],
    },
    {
        "ep": 5, "scene": "P1_CountingTo20", "file": "p1_05_counting_to_20.py",
        "title": "Counting to 20 - Number Line Fun | Singapore Math P1 Ep5",
        "desc": "Count from 1 to 20 on a number line with bouncing dots. Perfect for young learners!",
        "tags": ["counting", "numbers to 20", "number line"],
    },
    {
        "ep": 6, "scene": "P1_OrdinalNumbers", "file": "p1_06_ordinal_numbers.py",
        "title": "Ordinal Numbers - 1st, 2nd, 3rd | Singapore Math P1 Ep6",
        "desc": "Who is 1st, 2nd, 3rd in the race? Learn ordinal numbers with a fun animal race animation!",
        "tags": ["ordinal numbers", "1st 2nd 3rd", "position"],
    },
    {
        "ep": 7, "scene": "P1_Shapes2D", "file": "p1_07_shapes_2d.py",
        "title": "2D Shapes - Circle, Square, Triangle | Singapore Math P1 Ep7",
        "desc": "Meet the basic 2D shapes! Count their sides and corners with colorful animations.",
        "tags": ["2D shapes", "circle", "square", "triangle", "geometry"],
    },
    {
        "ep": 8, "scene": "P1_Patterns", "file": "p1_08_patterns.py",
        "title": "Patterns - What Comes Next? | Singapore Math P1 Ep8",
        "desc": "Red, blue, red, blue... what comes next? Learn to spot and continue patterns!",
        "tags": ["patterns", "repeating patterns", "what comes next"],
    },
    {
        "ep": 9, "scene": "P1_CountingBy2s", "file": "p1_09_counting_by_2s.py",
        "title": "Skip Counting by 2s | Singapore Math P1 Ep9",
        "desc": "2, 4, 6, 8, 10! Learn to skip count by 2s with a number line and jumping dots.",
        "tags": ["skip counting", "counting by 2s", "even numbers"],
    },
    {
        "ep": 10, "scene": "P1_CountingBy5s", "file": "p1_10_counting_by_5s.py",
        "title": "Skip Counting by 5s | Singapore Math P1 Ep10",
        "desc": "5, 10, 15, 20! Skip count by 5s - great for telling time and counting money later.",
        "tags": ["skip counting", "counting by 5s"],
    },
    {
        "ep": 11, "scene": "P1_CountingBy10s", "file": "p1_11_counting_by_10s.py",
        "title": "Skip Counting by 10s | Singapore Math P1 Ep11",
        "desc": "10, 20, 30... all the way to 100! Skip counting by 10s made easy with animations.",
        "tags": ["skip counting", "counting by 10s", "tens"],
    },
    {
        "ep": 12, "scene": "P1_NumberOrder", "file": "p1_12_number_order.py",
        "title": "Number Order - Smallest to Biggest | Singapore Math P1 Ep12",
        "desc": "Put numbers in order from smallest to biggest. Watch them sort themselves on a number line!",
        "tags": ["number order", "ascending", "ordering numbers"],
    },
    {
        "ep": 13, "scene": "P1_PlaceValueTensOnes", "file": "p1_13_place_value_tens_ones.py",
        "title": "Place Value - Tens and Ones | Singapore Math P1 Ep13",
        "desc": "What does the 1 in 14 mean? Learn tens and ones with place value blocks!",
        "tags": ["place value", "tens and ones", "base 10"],
    },
    {
        "ep": 14, "scene": "P1_Doubles", "file": "p1_14_doubles.py",
        "title": "Doubles - Adding Same Numbers | Singapore Math P1 Ep14",
        "desc": "3 + 3 = 6, 4 + 4 = 8! Learn doubles facts with mirror dot animations.",
        "tags": ["doubles", "doubles facts", "addition strategy"],
    },
    {
        "ep": 15, "scene": "P1_Halves", "file": "p1_15_halves.py",
        "title": "Halves - Splitting in Two | Singapore Math P1 Ep15",
        "desc": "Cut a shape in half! Learn what 1/2 means by splitting shapes into two equal parts.",
        "tags": ["halves", "half", "fractions intro", "equal parts"],
    },
    {
        "ep": 16, "scene": "P1_BeforeAfter", "file": "p1_16_before_after.py",
        "title": "Before and After Numbers | Singapore Math P1 Ep16",
        "desc": "What comes before 12? What comes after? Learn number neighbours with animated boxes!",
        "tags": ["before and after", "number neighbours", "number sequence"],
    },
    {
        "ep": 17, "scene": "P1_AdditionStory", "file": "p1_17_addition_story.py",
        "title": "Addition Word Problem - Apple Story | Singapore Math P1 Ep17",
        "desc": "Sam has 5 apples, Lily gives 3 more. How many altogether? Solve with a bar model!",
        "tags": ["word problem", "addition story", "bar model"],
    },
    {
        "ep": 18, "scene": "P1_SubtractionStory", "file": "p1_18_subtraction_story.py",
        "title": "Subtraction Word Problem - Birds Fly Away | Singapore Math P1 Ep18",
        "desc": "8 birds on a tree, 3 fly away. How many left? Watch the dots disappear!",
        "tags": ["word problem", "subtraction story", "taking away"],
    },
    {
        "ep": 19, "scene": "P1_Zero", "file": "p1_19_zero.py",
        "title": "The Number Zero - Nothing Left! | Singapore Math P1 Ep19",
        "desc": "5 - 5 = 0! What happens when you take everything away? Meet the number zero.",
        "tags": ["zero", "nothing", "subtraction to zero"],
    },
    {
        "ep": 20, "scene": "P1_Length", "file": "p1_20_length.py",
        "title": "Comparing Length - Longer and Shorter | Singapore Math P1 Ep20",
        "desc": "Which pencil is longer? Compare lengths visually with colorful bars side by side.",
        "tags": ["length", "longer shorter", "comparing", "measurement"],
    },
    {
        "ep": 21, "scene": "P1_Weight", "file": "p1_21_weight.py",
        "title": "Comparing Weight - Heavier and Lighter | Singapore Math P1 Ep21",
        "desc": "Which is heavier? Watch the balance beam tilt to find out! Fun intro to weight.",
        "tags": ["weight", "heavier lighter", "balance", "measurement"],
    },
    {
        "ep": 22, "scene": "P1_Add3Nums", "file": "p1_22_add_3nums.py",
        "title": "Adding 3 Numbers Together | Singapore Math P1 Ep22",
        "desc": "2 + 3 + 4 = ? Learn to add three numbers step by step. Add the first two, then the third!",
        "tags": ["adding 3 numbers", "three addends", "addition"],
    },
    {
        "ep": 23, "scene": "P1_Bonds8", "file": "p1_23_bonds_8.py",
        "title": "Number Bonds of 8 | Singapore Math P1 Ep23",
        "desc": "How many ways can you make 8? Discover all the number bond pairs: 1+7, 2+6, 3+5, 4+4!",
        "tags": ["number bonds", "bonds of 8", "addition pairs"],
    },
    {
        "ep": 24, "scene": "P1_OddEven", "file": "p1_24_odd_even.py",
        "title": "Odd and Even Numbers | Singapore Math P1 Ep24",
        "desc": "Is 7 odd or even? Learn to tell odd from even numbers 1-10 with pair-up animations!",
        "tags": ["odd even", "odd numbers", "even numbers"],
    },
    {
        "ep": 25, "scene": "P1_Money", "file": "p1_25_money.py",
        "title": "Counting Coins - Adding Up Money | Singapore Math P1 Ep25",
        "desc": "10c + 10c + 5c + 1c + 1c = ? Count coins one by one to find the total!",
        "tags": ["money", "counting coins", "cents", "singapore coins"],
    },
    {
        "ep": 26, "scene": "P1_Days", "file": "p1_26_days.py",
        "title": "Days of the Week - 7 Days | Singapore Math P1 Ep26",
        "desc": "Monday, Tuesday... how many days in a week? Learn all 7 days with colorful text!",
        "tags": ["days of the week", "7 days", "calendar"],
    },
    {
        "ep": 27, "scene": "P1_TimeHour", "file": "p1_27_time_hour.py",
        "title": "Telling Time - O'Clock | Singapore Math P1 Ep27",
        "desc": "What time is it? Learn to read the clock when the minute hand points to 12. It's 3 o'clock!",
        "tags": ["telling time", "o'clock", "clock", "hour hand"],
    },
    {
        "ep": 28, "scene": "P1_TimeHalf", "file": "p1_28_time_half.py",
        "title": "Half Past - 30 Minutes | Singapore Math P1 Ep28",
        "desc": "What is half past 6? The minute hand points to 6, making it 6:30. Learn half past times!",
        "tags": ["half past", "30 minutes", "telling time"],
    },
    {
        "ep": 29, "scene": "P1_EqualGroups", "file": "p1_29_equal_groups.py",
        "title": "Equal Groups - Intro to Multiplication | Singapore Math P1 Ep29",
        "desc": "3 groups of 4 = 12! See equal groups form with dots in boxes. Early multiplication concept!",
        "tags": ["equal groups", "multiplication intro", "groups of"],
    },
    {
        "ep": 30, "scene": "P1_Sharing", "file": "p1_30_sharing.py",
        "title": "Sharing Equally - Intro to Division | Singapore Math P1 Ep30",
        "desc": "Share 12 sweets among 3 children. Each gets 4! Watch items split into equal groups.",
        "tags": ["sharing equally", "division intro", "fair shares"],
    },
    {
        "ep": 31, "scene": "P1_Bonds5", "file": "p1_31_bonds_5.py",
        "title": "Number Bonds of 5 | Singapore Math P1 Ep31",
        "desc": "Find all the ways to make 5! 0+5, 1+4, 2+3... six different number bond pairs.",
        "tags": ["number bonds", "bonds of 5", "making 5"],
    },
    {
        "ep": 32, "scene": "P1_Position", "file": "p1_32_position.py",
        "title": "Position Words - Above, Below, Beside | Singapore Math P1 Ep32",
        "desc": "Where is the star? Above, below, left, or right of the box? Learn position words!",
        "tags": ["position words", "above below", "left right", "spatial"],
    },
    {
        "ep": 33, "scene": "P1_DoublesPlus1", "file": "p1_33_doubles_plus1.py",
        "title": "Doubles Plus 1 - Near Doubles Strategy | Singapore Math P1 Ep33",
        "desc": "6 + 7 is tricky? Use doubles! 6+6=12, then add 1 more = 13. A clever mental math trick!",
        "tags": ["doubles plus 1", "near doubles", "mental math strategy"],
    },
    {
        "ep": 34, "scene": "P1_CountBack", "file": "p1_34_count_back.py",
        "title": "Counting Backwards by 2s | Singapore Math P1 Ep34",
        "desc": "20, 18, 16, 14... count backwards from 20 by 2s on a number line with jumping dots!",
        "tags": ["counting backwards", "count back", "skip counting"],
    },
    {
        "ep": 35, "scene": "P1_MoreLess", "file": "p1_35_more_less.py",
        "title": "More and Less - Comparing Amounts | Singapore Math P1 Ep35",
        "desc": "8 vs 5: which group has more? Compare dot groups side by side to find out!",
        "tags": ["more less", "comparing amounts", "which is more"],
    },
    {
        "ep": 36, "scene": "P1_Add10Plus", "file": "p1_36_add_10plus.py",
        "title": "10 + Something - Quick Addition | Singapore Math P1 Ep36",
        "desc": "10 + 6 = 16! Adding to 10 is easy - just put the number after the 1. See it with dots!",
        "tags": ["adding 10", "10 plus", "teen numbers"],
    },
    {
        "ep": 37, "scene": "P1_SubFrom10", "file": "p1_37_sub_from10.py",
        "title": "Subtract from 10 | Singapore Math P1 Ep37",
        "desc": "10 - 4 = ? Start with 10 dots, cross out 4, count what's left. Subtraction made visual!",
        "tags": ["subtract from 10", "taking from 10"],
    },
    {
        "ep": 38, "scene": "P1_Capacity", "file": "p1_38_capacity.py",
        "title": "Capacity - Full, Half, Empty | Singapore Math P1 Ep38",
        "desc": "Is the glass full, half full, or empty? Learn about capacity with animated water levels!",
        "tags": ["capacity", "full half empty", "measurement", "volume"],
    },
    {
        "ep": 39, "scene": "P1_Sorting", "file": "p1_39_sorting.py",
        "title": "Sorting Shapes - Group by Type | Singapore Math P1 Ep39",
        "desc": "Sort circles, squares, and triangles into groups! Learn to classify shapes by their type.",
        "tags": ["sorting", "classifying shapes", "grouping"],
    },
    {
        "ep": 40, "scene": "P1_NLAdd", "file": "p1_40_nl_add.py",
        "title": "Number Line Addition - Jump Forward | Singapore Math P1 Ep40",
        "desc": "3 + 4 on a number line: start at 3, jump forward 4 times to land on 7! Visual addition.",
        "tags": ["number line", "addition", "jump forward"],
    },
    {
        "ep": 41, "scene": "P1_NLSub", "file": "p1_41_nl_sub.py",
        "title": "Number Line Subtraction - Jump Backward | Singapore Math P1 Ep41",
        "desc": "9 - 3 on a number line: start at 9, jump back 3 times to land on 6! Visual subtraction.",
        "tags": ["number line", "subtraction", "jump backward"],
    },
    {
        "ep": 42, "scene": "P1_FactFamily", "file": "p1_42_fact_family.py",
        "title": "Fact Families - 4 Related Facts | Singapore Math P1 Ep42",
        "desc": "3, 5, 8 make a fact family: 3+5=8, 5+3=8, 8-3=5, 8-5=3. Four facts from three numbers!",
        "tags": ["fact families", "related facts", "addition subtraction"],
    },
    {
        "ep": 43, "scene": "P1_MissingNum", "file": "p1_43_missing_num.py",
        "title": "Missing Number - Find the Blank | Singapore Math P1 Ep43",
        "desc": "_ + 4 = 9. What's the missing number? Think backwards: 9 - 4 = 5!",
        "tags": ["missing number", "find the blank", "unknown"],
    },
    {
        "ep": 44, "scene": "P1_PictureGraph", "file": "p1_44_picture_graph.py",
        "title": "Picture Graphs - Reading Data | Singapore Math P1 Ep44",
        "desc": "Which fruit is most popular? Read a picture graph to find out! Apples win with 5 votes.",
        "tags": ["picture graph", "data", "reading graphs", "statistics"],
    },
    {
        "ep": 45, "scene": "P1_Make10Pairs", "file": "p1_45_make10_pairs.py",
        "title": "Pairs That Make 10 | Singapore Math P1 Ep45",
        "desc": "1+9, 2+8, 3+7, 4+6, 5+5 - five special pairs that always add up to 10!",
        "tags": ["make 10", "pairs to 10", "number bonds 10"],
    },
    {
        "ep": 46, "scene": "P1_SubObjects", "file": "p1_46_sub_objects.py",
        "title": "Subtraction with Objects - Cross Them Out | Singapore Math P1 Ep46",
        "desc": "7 - 2 = ? Draw 7 dots, cross out 2, count what's left. Hands-on subtraction!",
        "tags": ["subtraction", "cross out", "concrete subtraction"],
    },
    {
        "ep": 47, "scene": "P1_CountOn", "file": "p1_47_count_on.py",
        "title": "Count On Strategy - Start from Bigger | Singapore Math P1 Ep47",
        "desc": "9 + 3: start at 9 and count on... 10, 11, 12! A fast addition strategy for kids.",
        "tags": ["count on", "counting on", "addition strategy"],
    },
    {
        "ep": 48, "scene": "P1_PartWhole", "file": "p1_48_part_whole.py",
        "title": "Part-Whole Model | Singapore Math P1 Ep48",
        "desc": "6 red + 4 blue = ? The part-whole model shows how parts combine to make a whole. Classic Singapore Math!",
        "tags": ["part whole", "part whole model", "bar model intro"],
    },
    {
        "ep": 49, "scene": "P1_Calendar", "file": "p1_49_calendar.py",
        "title": "Calendar - 12 Months of the Year | Singapore Math P1 Ep49",
        "desc": "January, February, March... learn all 12 months of the year with colorful animations!",
        "tags": ["calendar", "months", "12 months", "year"],
    },
    {
        "ep": 50, "scene": "P1_Review", "file": "p1_50_review.py",
        "title": "P1 Review Quiz - Test Yourself! | Singapore Math P1 Ep50",
        "desc": "Can you answer all the questions? A fun review quiz covering everything in Primary 1 Math!",
        "tags": ["review", "quiz", "test yourself", "P1 revision"],
    },
]

def full_description(v):
    return (
        f"{v['desc']}\n\n"
        f"Singapore Math Primary 1 Series - Episode {v['ep']} of 50\n\n"
        f"This video is part of the \"{PLAYLIST}\" series.\n"
        f"Perfect for Primary 1 / Grade 1 / Year 1 students (ages 6-7).\n\n"
        f"📚 Topics covered in this series:\n"
        f"• Counting & Number Sense (1-20)\n"
        f"• Addition & Subtraction\n"
        f"• Number Bonds & Fact Families\n"
        f"• Shapes, Patterns & Position\n"
        f"• Measurement (Length, Weight, Capacity)\n"
        f"• Time & Money\n"
        f"• Picture Graphs & Data\n\n"
        f"#SingaporeMath #Primary1 #MathForKids #P1Math #Grade1Math"
    )

def all_tags(v):
    return COMMON_TAGS + v["tags"] + [f"episode {v['ep']}"]


if __name__ == "__main__":
    if "--json" in sys.argv:
        out = []
        for v in VIDEOS:
            out.append({
                "episode": v["ep"],
                "scene": v["scene"],
                "file": v["file"],
                "title": v["title"],
                "description": full_description(v),
                "tags": all_tags(v),
                "playlist": PLAYLIST,
            })
        print(json.dumps(out, indent=2))

    elif "--csv" in sys.argv:
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["Episode", "Title", "Description", "Tags", "File"])
        for v in VIDEOS:
            writer.writerow([
                v["ep"], v["title"], full_description(v),
                "|".join(all_tags(v)), v["file"]
            ])
        print(buf.getvalue())

    else:
        print(f"\n{'='*60}")
        print(f"  {PLAYLIST}")
        print(f"{'='*60}\n")
        for v in VIDEOS:
            print(f"  Ep{v['ep']:02d}: {v['title']}")
            print(f"        Scene: {v['scene']}  |  File: {v['file']}")
        print(f"\n  Total: {len(VIDEOS)} videos")
        print(f"\n  Export options:")
        print(f"    python youtube_metadata_p1.py --json")
        print(f"    python youtube_metadata_p1.py --csv")
        print(f"{'='*60}")
