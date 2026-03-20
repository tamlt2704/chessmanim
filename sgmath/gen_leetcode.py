#!/usr/bin/env python3
"""Generate 10 simple LeetCode problem Manim scenes."""
from gen_part1 import *

H_LC = """from manim import *
from common import *
import numpy as np

CELL = 0.7
ARR_COLORS = [TEAL, BLUE, ACCENT, GOLD, ORANGE, PURPLE, GREEN, PINK]

def arr_row(vals, y=0, highlight=None, hl_color=ACCENT):
    cells = VGroup()
    for i, v in enumerate(vals):
        sq = Square(side_length=CELL, color=WHITE_C, fill_opacity=0.05, stroke_width=2)
        t = Text(str(v), font_size=22, color=WHITE_C)
        g = VGroup(sq, t)
        if highlight and i in highlight:
            sq.set_fill(hl_color, opacity=0.35)
            t.set_color(hl_color)
        cells.add(g)
    cells.arrange(RIGHT, buff=0)
    cells.move_to(UP * y)
    return cells

def ptr_arrow(arr, idx, label, color=GOLD, direction=DOWN):
    arrow = Arrow(
        arr[idx].get_edge_center(direction) + direction * 0.5,
        arr[idx].get_edge_center(direction) + direction * 0.05,
        color=color, stroke_width=2, max_tip_length_to_length_ratio=0.3
    )
    lbl = Text(label, font_size=16, color=color).next_to(arrow, direction, buff=0.05)
    return VGroup(arrow, lbl)

"""

print("LeetCode...")

# ── 1. Two Sum ──
w("lc01_two_sum.py", H_LC + """class LC01_TwoSum(Scene):
    def construct(self):
        intro(self, "P5", "LeetCode #1: Two Sum", "Hash Map")
        show_problem(self, "nums=[2,7,11,15], target=9. Find indices.")

        nums = [2, 7, 11, 15]
        arr = arr_row(nums, y=1)
        self.play(LaggedStart(*[FadeIn(c) for c in arr], lag_ratio=0.1), run_time=0.6)

        hmap_title = Text("HashMap", font_size=20, color=TEAL).move_to(LEFT*3 + DOWN*0.5)
        self.play(Write(hmap_title), run_time=0.3)

        entries = VGroup()
        for i, n in enumerate(nums):
            complement = 9 - n
            # highlight current
            self.play(arr[i][0].animate.set_fill(GOLD, opacity=0.3), run_time=0.2)

            if i == 1:  # found match
                found = Text(f"Need {complement}, found at idx 0!", font_size=22, color=ACCENT).move_to(DOWN*1.5)
                self.play(Write(found), run_time=0.4)
                self.play(
                    arr[0][0].animate.set_fill(ACCENT, opacity=0.4),
                    arr[1][0].animate.set_fill(ACCENT, opacity=0.4),
                    run_time=0.5
                )
                break

            entry = Text(f"{n} -> idx {i}", font_size=16, color=TEAL).move_to(LEFT*3 + DOWN*(1 + i*0.4))
            entries.add(entry)
            self.play(Write(entry), run_time=0.25)
            self.play(arr[i][0].animate.set_fill(WHITE_C, opacity=0.05), run_time=0.1)

        show_answer_box(self, "Output: [0, 1]")
""")

# ── 2. Valid Parentheses ──
w("lc02_valid_parentheses.py", H_LC + """class LC02_ValidParentheses(Scene):
    def construct(self):
        intro(self, "P5", "LeetCode #20: Valid Parentheses", "Stack")
        show_problem(self, 's = "({[]})"  — Is it valid?')

        chars = list("({[]})")
        char_mobs = VGroup()
        for i, ch in enumerate(chars):
            t = Text(ch, font_size=36, color=WHITE_C).move_to(LEFT*3 + RIGHT*i*0.8 + UP*1.5)
            char_mobs.add(t)
        self.play(LaggedStart(*[Write(c) for c in char_mobs], lag_ratio=0.08), run_time=0.6)

        stack_label = Text("Stack", font_size=20, color=TEAL).move_to(RIGHT*3 + UP*1.5)
        stack_base = Line(RIGHT*2 + DOWN*1.5, RIGHT*4 + DOWN*1.5, color=WHITE_C, stroke_width=2)
        self.play(Write(stack_label), Create(stack_base), run_time=0.3)

        stack_items = []
        match = {"(": ")", "{": "}", "[": "]"}
        close = set(")]}")
        y_base = -1.3

        for i, ch in enumerate(chars):
            self.play(char_mobs[i].animate.set_color(GOLD), run_time=0.15)
            if ch in match:
                item = Text(ch, font_size=28, color=TEAL).move_to(RIGHT*3 + UP*(y_base + len(stack_items)*0.5))
                stack_items.append(item)
                self.play(FadeIn(item, shift=UP*0.3), run_time=0.2)
            elif ch in close and stack_items:
                top = stack_items.pop()
                self.play(FadeOut(top, shift=UP*0.3), run_time=0.2)
            self.play(char_mobs[i].animate.set_color(TEAL), run_time=0.1)

        result = Text("Stack empty → Valid!", font_size=24, color=ACCENT).move_to(DOWN*0.5)
        self.play(Write(result), run_time=0.4)
        show_answer_box(self, "Output: true")
""")

# ── 3. Merge Two Sorted Lists ──
w("lc03_merge_sorted_lists.py", H_LC + """class LC03_MergeSortedLists(Scene):
    def construct(self):
        intro(self, "P5", "LeetCode #21: Merge Two Sorted Lists", "Two Pointers")
        show_problem(self, "list1=[1,2,4], list2=[1,3,4]. Merge them.")

        l1 = [1, 2, 4]
        l2 = [1, 3, 4]
        a1 = arr_row(l1, y=1.2)
        a2 = arr_row(l2, y=0.4)
        lb1 = Text("L1", font_size=20, color=TEAL).next_to(a1, LEFT, buff=0.3)
        lb2 = Text("L2", font_size=20, color=ACCENT).next_to(a2, LEFT, buff=0.3)
        self.play(FadeIn(a1), Write(lb1), FadeIn(a2), Write(lb2), run_time=0.5)

        merged_label = Text("Merged:", font_size=20, color=GOLD).move_to(LEFT*3.5 + DOWN*1)
        self.play(Write(merged_label), run_time=0.2)

        result = [1, 1, 2, 3, 4, 4]
        merged = VGroup()
        i1, i2 = 0, 0
        for k, val in enumerate(result):
            if i1 < 3 and l1[i1] == val and (i2 >= 3 or l1[i1] <= l2[i2]):
                self.play(a1[i1][0].animate.set_fill(GOLD, opacity=0.3), run_time=0.15)
                i1 += 1
            else:
                self.play(a2[i2][0].animate.set_fill(GOLD, opacity=0.3), run_time=0.15)
                i2 += 1
            sq = Square(side_length=CELL, color=GOLD, fill_opacity=0.15, stroke_width=2)
            t = Text(str(val), font_size=22, color=GOLD)
            g = VGroup(sq, t)
            merged.add(g)
            merged.arrange(RIGHT, buff=0).move_to(DOWN*1 + RIGHT*0.5)
            self.play(FadeIn(g), run_time=0.15)

        show_answer_box(self, "Output: [1,1,2,3,4,4]")
""")

# ── 4. Best Time to Buy and Sell Stock ──
w("lc04_buy_sell_stock.py", H_LC + """class LC04_BuySellStock(Scene):
    def construct(self):
        intro(self, "P5", "LeetCode #121: Best Time to Buy/Sell Stock", "One Pass")
        show_problem(self, "prices=[7,1,5,3,6,4]. Max profit?")

        prices = [7, 1, 5, 3, 6, 4]
        # draw price chart
        axes = Axes(x_range=[0, 6, 1], y_range=[0, 8, 1], x_length=8, y_length=4,
                     axis_config={"color": WHITE_C, "font_size": 16}).move_to(UP*0.3)
        points = [axes.c2p(i, p) for i, p in enumerate(prices)]
        graph = VMobject(color=TEAL, stroke_width=3)
        graph.set_points_as_corners(points)
        dots = VGroup(*[Dot(p, radius=0.08, color=TEAL) for p in points])
        labels = VGroup(*[Text(str(p), font_size=16, color=WHITE_C).next_to(dots[i], UP, buff=0.1) for i, p in enumerate(prices)])
        self.play(Create(axes), run_time=0.5)
        self.play(Create(graph), FadeIn(dots), FadeIn(labels), run_time=0.6)

        # highlight buy at 1, sell at 6
        buy_dot = Dot(points[1], radius=0.15, color=GREEN)
        sell_dot = Dot(points[4], radius=0.15, color=ACCENT)
        buy_lbl = Text("Buy $1", font_size=18, color=GREEN).next_to(buy_dot, DOWN, buff=0.15)
        sell_lbl = Text("Sell $6", font_size=18, color=ACCENT).next_to(sell_dot, UP, buff=0.15)
        arrow = Arrow(points[1], points[4], color=GOLD, stroke_width=2)
        self.play(GrowFromCenter(buy_dot), Write(buy_lbl), run_time=0.3)
        self.play(GrowFromCenter(sell_dot), Write(sell_lbl), Create(arrow), run_time=0.4)

        show_answer_box(self, "Max profit = 6 - 1 = 5")
""")

# ── 5. Valid Palindrome ──
w("lc05_valid_palindrome.py", H_LC + """class LC05_ValidPalindrome(Scene):
    def construct(self):
        intro(self, "P5", "LeetCode #125: Valid Palindrome", "Two Pointers")
        show_problem(self, '"racecar" — Is it a palindrome?')

        word = "racecar"
        cells = arr_row(list(word), y=0.8)
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.06), run_time=0.5)

        left, right = 0, len(word) - 1
        while left < right:
            lp = ptr_arrow(cells, left, "L", color=TEAL, direction=DOWN)
            rp = ptr_arrow(cells, right, "R", color=ACCENT, direction=DOWN)
            self.play(FadeIn(lp), FadeIn(rp), run_time=0.2)
            # match highlight
            self.play(
                cells[left][0].animate.set_fill(TEAL, opacity=0.3),
                cells[right][0].animate.set_fill(TEAL, opacity=0.3),
                run_time=0.25
            )
            match_txt = Text(f"'{word[left]}' == '{word[right]}' ✓", font_size=20, color=TEAL).move_to(DOWN*1.5)
            self.play(Write(match_txt), run_time=0.2)
            self.play(FadeOut(lp), FadeOut(rp), FadeOut(match_txt), run_time=0.15)
            left += 1
            right -= 1

        show_answer_box(self, "Output: true (palindrome)")
""")

# ── 6. Invert Binary Tree ──
w("lc06_invert_binary_tree.py", H_LC + """class LC06_InvertBinaryTree(Scene):
    def construct(self):
        intro(self, "P5", "LeetCode #226: Invert Binary Tree", "Recursion")
        show_problem(self, "Swap left and right children at every node.")

        # original tree: 4 -> (2,7), 2->(1,3), 7->(6,9)
        positions = {4: UP*1.5, 2: LEFT*2+UP*0, 7: RIGHT*2+UP*0,
                     1: LEFT*3+DOWN*1.2, 3: LEFT*1+DOWN*1.2, 6: RIGHT*1+DOWN*1.2, 9: RIGHT*3+DOWN*1.2}
        edges = [(4,2),(4,7),(2,1),(2,3),(7,6),(7,9)]

        nodes = {}
        for val, pos in positions.items():
            c = Circle(radius=0.35, color=TEAL, fill_opacity=0.2).move_to(pos)
            t = Text(str(val), font_size=22, color=WHITE_C).move_to(pos)
            nodes[val] = VGroup(c, t)

        lines = VGroup()
        for a, b in edges:
            lines.add(Line(positions[a], positions[b], color=WHITE_C, stroke_width=1.5))

        tree = VGroup(lines, *nodes.values())
        self.play(FadeIn(tree), run_time=0.6)
        self.wait(0.5)

        # animate swap: move left subtree right and vice versa
        swap_txt = Text("Swap children!", font_size=24, color=GOLD).to_edge(DOWN, buff=1.5)
        self.play(Write(swap_txt), run_time=0.3)

        # inverted positions
        inv = {4: UP*1.5, 7: LEFT*2+UP*0, 2: RIGHT*2+UP*0,
               9: LEFT*3+DOWN*1.2, 6: LEFT*1+DOWN*1.2, 3: RIGHT*1+DOWN*1.2, 1: RIGHT*3+DOWN*1.2}

        anims = []
        for val in positions:
            anims.append(nodes[val].animate.move_to(inv[val]))
        # rebuild edges
        new_lines = VGroup()
        new_edges = [(4,7),(4,2),(7,9),(7,6),(2,3),(2,1)]
        for a, b in new_edges:
            new_lines.add(Line(inv[a], inv[b], color=GOLD, stroke_width=1.5))

        self.play(*anims, FadeOut(lines), run_time=1)
        self.play(FadeIn(new_lines), run_time=0.3)

        show_answer_box(self, "Tree inverted!")
""")

# ── 7. Climbing Stairs ──
w("lc07_climbing_stairs.py", H_LC + """class LC07_ClimbingStairs(Scene):
    def construct(self):
        intro(self, "P5", "LeetCode #70: Climbing Stairs", "Dynamic Programming")
        show_problem(self, "n=5 stairs. 1 or 2 steps at a time. How many ways?")

        # draw staircase
        stairs = VGroup()
        for i in range(5):
            step = Rectangle(width=1, height=0.5, color=TEAL, fill_opacity=0.2, stroke_width=2)
            step.move_to(LEFT*2 + RIGHT*i*0.8 + UP*(-1 + i*0.5))
            num = Text(str(i+1), font_size=16, color=WHITE_C).move_to(step)
            stairs.add(VGroup(step, num))
        self.play(LaggedStart(*[FadeIn(s) for s in stairs], lag_ratio=0.1), run_time=0.6)

        # DP table
        dp_label = Text("dp[i] = dp[i-1] + dp[i-2]", font_size=22, color=GOLD).move_to(RIGHT*2.5 + UP*1.5)
        self.play(Write(dp_label), run_time=0.4)

        dp = [1, 1, 2, 3, 5, 8]
        dp_entries = VGroup()
        for i in range(6):
            entry = Text(f"dp[{i}]={dp[i]}", font_size=18, color=TEAL if i < 2 else ACCENT)
            dp_entries.add(entry)
        dp_entries.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(RIGHT*2.5 + DOWN*0.3)
        self.play(LaggedStart(*[Write(e) for e in dp_entries], lag_ratio=0.15), run_time=1.2)

        show_answer_box(self, "Output: 8 ways")
""")

# ── 8. Maximum Subarray ──
w("lc08_maximum_subarray.py", H_LC + """class LC08_MaximumSubarray(Scene):
    def construct(self):
        intro(self, "P5", "LeetCode #53: Maximum Subarray", "Kadane's Algorithm")
        show_problem(self, "nums=[-2,1,-3,4,-1,2,1,-5,4]. Max subarray sum?")

        nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
        arr = arr_row(nums, y=1)
        self.play(LaggedStart(*[FadeIn(c) for c in arr], lag_ratio=0.06), run_time=0.6)

        cur_label = Text("cur_sum", font_size=18, color=TEAL).move_to(LEFT*4 + DOWN*0.3)
        max_label = Text("max_sum", font_size=18, color=GOLD).move_to(LEFT*4 + DOWN*0.8)
        self.play(Write(cur_label), Write(max_label), run_time=0.3)

        cur_sum, max_sum = 0, nums[0]
        cur_val = Text(f"= {cur_sum}", font_size=18, color=TEAL).next_to(cur_label, RIGHT, buff=0.2)
        max_val = Text(f"= {max_sum}", font_size=18, color=GOLD).next_to(max_label, RIGHT, buff=0.2)
        self.play(Write(cur_val), Write(max_val), run_time=0.2)

        # highlight the winning subarray [4,-1,2,1] = indices 3..6
        best_start, best_end = 3, 6
        for i, n in enumerate(nums):
            cur_sum = max(n, cur_sum + n)
            max_sum = max(max_sum, cur_sum)
            c = TEAL if i >= best_start and i <= best_end else WHITE_C
            self.play(arr[i][0].animate.set_fill(c, opacity=0.3 if c == TEAL else 0.05), run_time=0.12)

        # highlight best subarray
        for i in range(best_start, best_end + 1):
            self.play(arr[i][0].animate.set_fill(GOLD, opacity=0.4), run_time=0.1)

        brace = Brace(VGroup(*[arr[i] for i in range(best_start, best_end+1)]), DOWN, color=GOLD)
        brace_lbl = Text("sum = 6", font_size=20, color=GOLD).next_to(brace, DOWN, buff=0.1)
        self.play(GrowFromCenter(brace), Write(brace_lbl), run_time=0.4)

        show_answer_box(self, "Output: 6  (subarray [4,-1,2,1])")
""")

# ── 9. Contains Duplicate ──
w("lc09_contains_duplicate.py", H_LC + """class LC09_ContainsDuplicate(Scene):
    def construct(self):
        intro(self, "P5", "LeetCode #217: Contains Duplicate", "Hash Set")
        show_problem(self, "nums=[1,2,3,1]. Any duplicates?")

        nums = [1, 2, 3, 1]
        arr = arr_row(nums, y=1.2)
        self.play(LaggedStart(*[FadeIn(c) for c in arr], lag_ratio=0.1), run_time=0.5)

        set_title = Text("Set { }", font_size=20, color=TEAL).move_to(LEFT*2 + DOWN*0.2)
        self.play(Write(set_title), run_time=0.2)

        seen = set()
        set_items = VGroup()
        for i, n in enumerate(nums):
            self.play(arr[i][0].animate.set_fill(GOLD, opacity=0.3), run_time=0.2)

            if n in seen:
                dup = Text(f"{n} already in set! Duplicate!", font_size=22, color=ACCENT).move_to(DOWN*1.5)
                self.play(Write(dup), arr[i][0].animate.set_fill(ACCENT, opacity=0.4), run_time=0.4)
                break

            seen.add(n)
            item = Text(str(n), font_size=18, color=TEAL).move_to(LEFT*2 + RIGHT*len(set_items)*0.6 + DOWN*0.7)
            set_items.add(item)
            self.play(Write(item), run_time=0.2)
            self.play(arr[i][0].animate.set_fill(WHITE_C, opacity=0.05), run_time=0.1)

        show_answer_box(self, "Output: true (has duplicate)")
""")

# ── 10. Reverse Linked List ──
w("lc10_reverse_linked_list.py", H_LC + """class LC10_ReverseLinkedList(Scene):
    def construct(self):
        intro(self, "P5", "LeetCode #206: Reverse Linked List", "Iterative")
        show_problem(self, "head = [1,2,3,4,5]. Reverse it.")

        vals = [1, 2, 3, 4, 5]
        nodes = VGroup()
        arrows = VGroup()
        for i, v in enumerate(vals):
            c = RoundedRectangle(width=0.8, height=0.6, corner_radius=0.1, color=TEAL, fill_opacity=0.2)
            t = Text(str(v), font_size=22, color=WHITE_C)
            g = VGroup(c, t)
            nodes.add(g)
        nodes.arrange(RIGHT, buff=0.6).move_to(UP*1)
        for i in range(len(vals)-1):
            a = Arrow(nodes[i].get_right(), nodes[i+1].get_left(), color=WHITE_C, stroke_width=2,
                      max_tip_length_to_length_ratio=0.3, buff=0.05)
            arrows.add(a)

        self.play(FadeIn(nodes), FadeIn(arrows), run_time=0.5)
        self.wait(0.3)

        # animate reversal
        rev_label = Text("Reverse arrows one by one", font_size=20, color=GOLD).move_to(DOWN*0.3)
        self.play(Write(rev_label), run_time=0.3)

        for i in range(len(arrows)-1, -1, -1):
            new_arrow = Arrow(nodes[i+1].get_left(), nodes[i].get_right(), color=ACCENT, stroke_width=2,
                              max_tip_length_to_length_ratio=0.3, buff=0.05)
            self.play(FadeOut(arrows[i]), FadeIn(new_arrow), run_time=0.25)
            arrows[i] = new_arrow

        # rearrange nodes to show reversed order
        self.play(FadeOut(rev_label), run_time=0.2)
        rev_nodes = VGroup()
        rev_arrows = VGroup()
        for i, v in enumerate(reversed(vals)):
            c = RoundedRectangle(width=0.8, height=0.6, corner_radius=0.1, color=ACCENT, fill_opacity=0.2)
            t = Text(str(v), font_size=22, color=WHITE_C)
            g = VGroup(c, t)
            rev_nodes.add(g)
        rev_nodes.arrange(RIGHT, buff=0.6).move_to(DOWN*1)
        for i in range(len(vals)-1):
            a = Arrow(rev_nodes[i].get_right(), rev_nodes[i+1].get_left(), color=ACCENT, stroke_width=2,
                      max_tip_length_to_length_ratio=0.3, buff=0.05)
            rev_arrows.add(a)

        self.play(FadeIn(rev_nodes), FadeIn(rev_arrows), run_time=0.5)

        show_answer_box(self, "Output: [5,4,3,2,1]")
""")

print(f"  LeetCode done. Created: {created}, Skipped: {skipped}")
