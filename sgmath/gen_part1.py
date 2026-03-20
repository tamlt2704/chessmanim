#!/usr/bin/env python3
"""Part 1: Core generator functions and P1 scenes."""
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes")
os.makedirs(D, exist_ok=True)
H = "from manim import *\nfrom common import *\n\n"
created = 0
skipped = 0

def w(fn, code):
    global created, skipped
    p = os.path.join(D, fn)
    if os.path.exists(p):
        skipped += 1
        return
    with open(p, "w", encoding="utf-8") as f:
        f.write(code)
    created += 1


# Template generators
def T(cls, level, title, sub, body):
    """Generic scene template."""
    return H + f"class {cls}(Scene):\n    def construct(self):\n        intro(self, \"{level}\", \"{title}\", \"{sub}\")\n" + body

def T3D(cls, level, title, body):
    """3D scene template."""
    return H + f"class {cls}(ThreeDScene):\n    def construct(self):\n        self.camera.background_color = BG\n        t=Text(\"{title}\",font_size=44,color=GOLD)\n        self.add_fixed_in_frame_mobjects(t)\n        self.play(Write(t),run_time=0.8)\n        self.wait(0.5)\n        self.play(FadeOut(t),run_time=0.3)\n" + body

def prob(text):
    return f"        show_problem(self, \"{text}\")\n"

def ans(text, y=None):
    if y:
        return f"        show_answer_box(self, \"{text}\", y={y})\n"
    return f"        show_answer_box(self, \"{text}\")\n"

def steps(items):
    code = ""
    for i, s in enumerate(items):
        y = round(0.5 + i * 0.55, 2)
        code += f"        s{i}=Text(\"{s}\",font_size=26,color=TEAL if {i}%2==0 else GOLD).move_to(DOWN*{y})\n        self.play(Write(s{i}),run_time=0.4)\n"
    return code

def dots_add(a, b, total):
    return f"""        left=VGroup(*[Dot(radius=0.15,color=TEAL) for _ in range({a})]).arrange_in_grid(rows=max(1,{a}//5),buff=0.2).move_to(LEFT*2.5+UP*0.3)
        right=VGroup(*[Dot(radius=0.15,color=ACCENT) for _ in range({b})]).arrange_in_grid(rows=max(1,{b}//5),buff=0.2).move_to(RIGHT*1+UP*0.3)
        plus=Text("+",font_size=36,color=GOLD).move_to(LEFT*0.7+UP*0.3)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in left],lag_ratio=0.04),run_time=0.6)
        self.play(Write(plus),run_time=0.15)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in right],lag_ratio=0.04),run_time=0.5)
        self.wait(0.3)
"""

def dots_sub(a, b, result):
    return f"""        dots=VGroup(*[Dot(radius=0.15,color=TEAL) for _ in range({a})]).arrange_in_grid(rows=2,buff=0.2).move_to(UP*0.5)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots],lag_ratio=0.03),run_time=0.6)
        crosses=VGroup(*[Cross(dots[{a}-1-i],color=ACCENT,stroke_width=3) for i in range({b})])
        self.play(LaggedStart(*[Create(c) for c in crosses],lag_ratio=0.08),run_time=0.5)
        self.wait(0.3)
"""

def mult_groups(groups, per_group):
    total = groups * per_group
    return f"""        gs=VGroup()
        for g in range({groups}):
            box=RoundedRectangle(width=1+{per_group}*0.25,height=0.7,corner_radius=0.1,color=TEAL,fill_opacity=0.15)
            ds=VGroup(*[Dot(radius=0.08,color=ORANGE) for _ in range({per_group})]).arrange(RIGHT,buff=0.12).move_to(box)
            gs.add(VGroup(box,ds))
        gs.arrange_in_grid(rows=min({groups},5),buff=0.25).move_to(UP*0.2)
        for grp in gs:
            self.play(Create(grp[0]),LaggedStart(*[GrowFromCenter(d) for d in grp[1]],lag_ratio=0.04),run_time=0.25)
        self.wait(0.3)
"""

def div_groups(total, divisor):
    each = total // divisor
    return f"""        colors=[TEAL,ACCENT,BLUE,PURPLE,ORANGE,GREEN,PINK,GOLD]
        gs=VGroup()
        for g in range({divisor}):
            box=RoundedRectangle(width=1.2+{each}*0.2,height=0.6,corner_radius=0.1,color=colors[g%8],fill_opacity=0.2)
            ds=VGroup(*[Dot(radius=0.08,color=colors[g%8]) for _ in range({each})]).arrange(RIGHT,buff=0.1).move_to(box)
            lbl=Text(str({each}),font_size=18,color=colors[g%8]).next_to(box,DOWN,buff=0.08)
            gs.add(VGroup(box,ds,lbl))
        gs.arrange_in_grid(rows=min({divisor},4),buff=0.25).move_to(DOWN*0.2)
        self.play(LaggedStart(*[FadeIn(g) for g in gs],lag_ratio=0.1),run_time=1)
        self.wait(0.3)
"""

def bar_model(name1, v1, name2, v2, total):
    w1 = round(v1/total*8, 1)
    w2 = round(v2/total*8, 1)
    return f"""        b1=Rectangle(width={w1},height=0.7,color=BLUE,fill_opacity=0.4).move_to(LEFT*0.5+UP*0.3)
        l1=Text("{name1}: {v1}",font_size=24,color=BLUE).move_to(b1)
        b2=Rectangle(width={w2},height=0.7,color=ACCENT,fill_opacity=0.4)
        b2.next_to(b1,DOWN,buff=0.3,aligned_edge=LEFT)
        l2=Text("{name2}: {v2}",font_size=24,color=ACCENT).move_to(b2)
        self.play(Create(b1),Write(l1),run_time=0.5)
        self.play(Create(b2),Write(l2),run_time=0.5)
        br=Brace(VGroup(b1,b2),RIGHT,color=GOLD)
        bl=Text("?",font_size=32,color=GOLD).next_to(br,RIGHT,buff=0.2)
        self.play(GrowFromCenter(br),Write(bl),run_time=0.5)
        self.wait(0.3)
"""

def frac_bar(num, den):
    return f"""        bar=VGroup()
        pw=6.0/{den}
        for i in range({den}):
            cell=Rectangle(width=pw,height=0.8,color=TEAL if i<{num} else WHITE_C,fill_opacity=0.4 if i<{num} else 0.05,stroke_width=2,stroke_color=WHITE_C)
            bar.add(cell)
        bar.arrange(RIGHT,buff=0).move_to(UP*0.3)
        self.play(LaggedStart(*[Create(c) for c in bar],lag_ratio=0.04),run_time=0.7)
        self.wait(0.3)
"""

def ratio_bars(n1, n2, r1, r2, total):
    unit = total // (r1 + r2)
    v1, v2 = r1*unit, r2*unit
    return f"""        uw=0.75
        b1=VGroup(*[Rectangle(width=uw,height=0.6,color=BLUE,fill_opacity=0.4,stroke_width=2) for _ in range({r1})]).arrange(RIGHT,buff=0)
        b1.move_to(LEFT*1+UP*0.5)
        l1=Text("{n1}",font_size=22,color=BLUE).next_to(b1,LEFT,buff=0.3)
        b2=VGroup(*[Rectangle(width=uw,height=0.6,color=ACCENT,fill_opacity=0.4,stroke_width=2) for _ in range({r2})]).arrange(RIGHT,buff=0)
        b2.next_to(b1,DOWN,buff=0.3,aligned_edge=LEFT)
        l2=Text("{n2}",font_size=22,color=ACCENT).next_to(b2,LEFT,buff=0.3)
        self.play(LaggedStart(*[Create(b) for b in b1],lag_ratio=0.08),Write(l1),run_time=0.5)
        self.play(LaggedStart(*[Create(b) for b in b2],lag_ratio=0.08),Write(l2),run_time=0.5)
        br=Brace(VGroup(b1,b2),RIGHT,color=GOLD)
        bl=Text("{total}",font_size=28,color=GOLD).next_to(br,RIGHT,buff=0.2)
        self.play(GrowFromCenter(br),Write(bl),run_time=0.4)
        self.wait(0.3)
"""


# ===== P1 (16-50) =====
print("P1...")
w("p1_16_before_after.py", T("P1_BeforeAfter","P1","Before and After","What number comes next?", prob("What comes before and after 12?") + "        boxes=VGroup()\n        for i,(n,c) in enumerate([(11,TEAL),(12,GOLD),(13,ACCENT)]):\n            sq=Square(side_length=1.2,color=c,fill_opacity=0.2)\n            t=Text(str(n),font_size=40,color=c)\n            g=VGroup(sq,t).move_to(LEFT*2.5+RIGHT*i*2.5+UP*0.3)\n            boxes.add(g)\n            self.play(FadeIn(g),run_time=0.3)\n" + ans("11 before 12, 13 after 12")))
w("p1_17_addition_story.py", T("P1_AdditionStory","P1","Addition Story","Word problem", prob("Sam has 5 apples. Lily gives 3 more.") + bar_model("Sam",5,"Lily",3,8) + ans("5 + 3 = 8 apples")))
w("p1_18_subtraction_story.py", T("P1_SubtractionStory","P1","Subtraction Story","Taking away", prob("8 birds. 3 fly away. How many left?") + dots_sub(8,3,5) + ans("8 - 3 = 5 birds")))
w("p1_19_zero.py", T("P1_Zero","P1","The Number Zero","Nothing left", prob("5 - 5 = ?") + "        dots=VGroup(*[Dot(radius=0.2,color=TEAL) for _ in range(5)]).arrange(RIGHT,buff=0.3).move_to(UP*0.5)\n        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots],lag_ratio=0.1),run_time=0.6)\n        self.play(LaggedStart(*[FadeOut(d,shift=DOWN) for d in dots],lag_ratio=0.15),run_time=0.8)\n" + ans("5 - 5 = 0")))
w("p1_20_length.py", T("P1_Length","P1","Comparing Length","Longer and shorter", prob("Which is longer?") + "        p1=Rectangle(width=5,height=0.3,color=TEAL,fill_opacity=0.5).move_to(UP*0.5)\n        p2=Rectangle(width=3,height=0.3,color=ACCENT,fill_opacity=0.5).move_to(DOWN*0.5)\n        self.play(Create(p1),Create(p2),run_time=0.5)\n        self.play(Write(Text('A',font_size=22,color=TEAL).next_to(p1,LEFT)),Write(Text('B',font_size=22,color=ACCENT).next_to(p2,LEFT)),run_time=0.3)\n" + ans("A is longer than B")))
w("p1_21_weight.py", T("P1_Weight","P1","Comparing Weight","Heavier and lighter", prob("Which is heavier?") + "        beam=Line(LEFT*3,RIGHT*3,color=WHITE_C,stroke_width=3)\n        pivot=Triangle(color=WHITE_C,fill_opacity=0.3).scale(0.3).next_to(beam,DOWN,buff=0)\n        self.play(Create(beam),Create(pivot),run_time=0.4)\n        h=Circle(radius=0.5,color=ACCENT,fill_opacity=0.5).move_to(LEFT*2+UP*0.8)\n        l=Circle(radius=0.3,color=TEAL,fill_opacity=0.5).move_to(RIGHT*2+UP*0.8)\n        self.play(FadeIn(h),FadeIn(l),run_time=0.4)\n        self.play(beam.animate.rotate(-0.15,about_point=pivot.get_top()),run_time=0.6)\n" + ans("The bigger one is heavier!")))
w("p1_22_add_3nums.py", T("P1_Add3Nums","P1","Adding 3 Numbers","2+3+4", prob("2 + 3 + 4 = ?") + steps(["2 + 3 = 5","5 + 4 = 9"]) + ans("2 + 3 + 4 = 9")))
w("p1_23_bonds_8.py", T("P1_Bonds8","P1","Number Bonds of 8","Ways to make 8", prob("Find pairs that make 8") + "        pairs=[(1,7),(2,6),(3,5),(4,4)]\n        for i,(a,b) in enumerate(pairs):\n            y=UP*0.8+DOWN*i*0.7\n            eq=Text(f'{a}+{b}=8',font_size=26,color=GOLD).move_to(y)\n            self.play(Write(eq),run_time=0.3)\n" + ans("1+7, 2+6, 3+5, 4+4 all make 8")))
w("p1_24_odd_even.py", T("P1_OddEven","P1","Odd and Even","Pair them up", prob("Which are odd? Which are even?") + "        for i in range(1,11):\n            c=TEAL if i%2==0 else ACCENT\n            x=-4.5+(i-1)*1\n            t=Text(str(i),font_size=24,color=c).move_to(RIGHT*x+UP*0.5)\n            lbl=Text('E' if i%2==0 else 'O',font_size=16,color=c).next_to(t,DOWN,buff=0.1)\n            self.play(Write(t),Write(lbl),run_time=0.15)\n" + ans("Even: 2,4,6,8,10. Odd: 1,3,5,7,9")))
w("p1_25_money.py", T("P1_Money","P1","Counting Coins","Adding up money", prob("10c + 10c + 5c + 1c + 1c = ?") + "        vals=[10,10,5,1,1]\n        total=0\n        for i,v in enumerate(vals):\n            c=Circle(radius=0.3,color=GOLD,fill_opacity=0.3).move_to(LEFT*3.5+RIGHT*i*1.5+UP*0.5)\n            l=Text(f'{v}c',font_size=18,color=GOLD).move_to(c)\n            total+=v\n            self.play(FadeIn(c),Write(l),run_time=0.2)\n" + ans("Total = 27 cents")))
w("p1_26_days.py", T("P1_Days","P1","Days of the Week","7 days", prob("How many days in a week?") + "        days=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']\n        for i,d in enumerate(days):\n            t=Text(d,font_size=24,color=[TEAL,BLUE,PURPLE,ORANGE,ACCENT,GOLD,GREEN][i]).move_to(LEFT*4.5+RIGHT*i*1.5+UP*0.5)\n            self.play(Write(t),run_time=0.2)\n" + ans("7 days in a week!")))
w("p1_27_time_hour.py", T("P1_TimeHour","P1","Telling Time","O'clock", prob("What time is shown?") + "        import numpy as np\n        clock=Circle(radius=1.8,color=WHITE_C,stroke_width=2).move_to(UP*0.2)\n        self.play(Create(clock),run_time=0.4)\n        for h in range(12):\n            a=PI/2-h*PI/6\n            p=UP*0.2+1.5*np.array([np.cos(a),np.sin(a),0])\n            self.play(Write(Text(str(h if h else 12),font_size=16,color=WHITE_C).move_to(p)),run_time=0.06)\n        hh=Line(UP*0.2,UP*0.2+RIGHT*1,color=GOLD,stroke_width=4)\n        mh=Line(UP*0.2,UP*0.2+UP*1.3,color=TEAL,stroke_width=2)\n        self.play(Create(hh),Create(mh),run_time=0.4)\n" + ans("It is 3 o'clock!")))
w("p1_28_time_half.py", T("P1_TimeHalf","P1","Half Past","30 minutes", prob("What is half past 6?") + steps(["The minute hand points to 6","The hour hand is between 6 and 7","It is 6:30"]) + ans("Half past 6 = 6:30")))
w("p1_29_equal_groups.py", T("P1_EqualGroups","P1","Equal Groups","Same in each group", prob("3 groups of 4 = ?") + mult_groups(3,4) + ans("3 groups of 4 = 12")))
w("p1_30_sharing.py", T("P1_Sharing","P1","Sharing Equally","Fair shares", prob("Share 12 sweets among 3 children") + div_groups(12,3) + ans("12 / 3 = 4 each")))
w("p1_31_bonds_5.py", T("P1_Bonds5","P1","Number Bonds of 5","Ways to make 5", prob("Find all ways to make 5") + "        for i,(a,b) in enumerate([(0,5),(1,4),(2,3),(3,2),(4,1),(5,0)]):\n            eq=Text(f'{a}+{b}=5',font_size=24,color=GOLD).move_to(UP*1.2+DOWN*i*0.5)\n            self.play(Write(eq),run_time=0.2)\n" + ans("6 ways to make 5!")))
w("p1_32_position.py", T("P1_Position","P1","Position Words","Above, below, beside", prob("Where is the star?") + "        box=Square(side_length=1.5,color=BLUE,fill_opacity=0.3)\n        self.play(Create(box),run_time=0.3)\n        for w2,p,c in [('above',UP*1.5,TEAL),('below',DOWN*1.5,ACCENT),('left',LEFT*2.5,GOLD),('right',RIGHT*2.5,PURPLE)]:\n            d=Dot(radius=0.15,color=c).move_to(p)\n            l=Text(w2,font_size=20,color=c).next_to(d,DOWN,buff=0.1)\n            self.play(GrowFromCenter(d),Write(l),run_time=0.3)\n" + ans("Above, below, left, right!")))
w("p1_33_doubles_plus1.py", T("P1_DoublesPlus1","P1","Doubles Plus 1","Near doubles", prob("6 + 7 = ?") + steps(["6+6 = 12 (double)","12+1 = 13 (plus 1)"]) + ans("6 + 7 = 13")))
w("p1_34_count_back.py", T("P1_CountBack","P1","Counting Backwards","20 to 0", prob("Count back from 20 by 2s") + "        nl=NumberLine(x_range=[0,20,2],length=10,include_numbers=True,font_size=16,color=WHITE_C).move_to(UP*0.5)\n        self.play(Create(nl),run_time=0.6)\n        for n in range(20,-1,-2):\n            self.play(GrowFromCenter(Dot(nl.n2p(n),radius=0.1,color=ACCENT)),run_time=0.12)\n" + ans("20,18,16,14,12,10,8,6,4,2,0")))


w("p1_35_more_less.py", T("P1_MoreLess","P1","More and Less","Comparing amounts", prob("8 vs 5: which is more?") + "        l=VGroup(*[Dot(radius=0.15,color=BLUE) for _ in range(8)]).arrange_in_grid(rows=2,buff=0.15).move_to(LEFT*2.5+UP*0.3)\n        r=VGroup(*[Dot(radius=0.15,color=ACCENT) for _ in range(5)]).arrange_in_grid(rows=2,buff=0.15).move_to(RIGHT*2.5+UP*0.3)\n        self.play(FadeIn(l),FadeIn(r),run_time=0.5)\n        self.play(Write(Text('8',font_size=32,color=BLUE).next_to(l,DOWN,buff=0.2)),Write(Text('5',font_size=32,color=ACCENT).next_to(r,DOWN,buff=0.2)),run_time=0.3)\n" + ans("8 is more than 5")))
w("p1_36_add_10plus.py", T("P1_Add10Plus","P1","10 + Something","Quick addition", prob("10 + 6 = ?") + dots_add(10,6,16) + ans("10 + 6 = 16")))
w("p1_37_sub_from10.py", T("P1_SubFrom10","P1","Subtract from 10","Taking from 10", prob("10 - 4 = ?") + dots_sub(10,4,6) + ans("10 - 4 = 6")))
w("p1_38_capacity.py", T("P1_Capacity","P1","Capacity","Full, half, empty", prob("How full is each glass?") + "        for i,(lbl,fill,c) in enumerate([('Full',1.8,TEAL),('Half',0.9,GOLD),('Empty',0.0,ACCENT)]):\n            x=-3+i*3\n            glass=Rectangle(width=1.2,height=2,color=WHITE_C,stroke_width=2).move_to(RIGHT*x+UP*0.2)\n            water=Rectangle(width=1.1,height=fill,color=c,fill_opacity=0.5,stroke_width=0).move_to(glass.get_bottom()+UP*fill/2+UP*0.05)\n            self.play(Create(glass),FadeIn(water),Write(Text(lbl,font_size=22,color=c).next_to(glass,DOWN,buff=0.15)),run_time=0.4)\n" + ans("Full, half full, and empty!")))
w("p1_39_sorting.py", T("P1_Sorting","P1","Sorting Shapes","Group by type", prob("Sort: circles, squares, triangles") + "        shapes=[(Circle(radius=0.2,color=TEAL,fill_opacity=0.5),'circle'),(Square(side_length=0.35,color=ACCENT,fill_opacity=0.5),'square'),(Triangle(color=GOLD,fill_opacity=0.5).scale(0.25),'triangle')]*3\n        mixed=VGroup(*[s[0].copy().move_to(LEFT*4+RIGHT*i*0.9+UP*1.2) for i,s in enumerate(shapes)])\n        self.play(LaggedStart(*[FadeIn(s) for s in mixed],lag_ratio=0.04),run_time=0.6)\n" + ans("3 groups: circles, squares, triangles")))
w("p1_40_nl_add.py", T("P1_NLAdd","P1","Number Line Addition","Jump forward", prob("3 + 4 on a number line") + "        nl=NumberLine(x_range=[0,10,1],length=10,include_numbers=True,font_size=18,color=WHITE_C).move_to(UP*0.5)\n        self.play(Create(nl),run_time=0.5)\n        self.play(GrowFromCenter(Dot(nl.n2p(3),radius=0.12,color=TEAL)),run_time=0.3)\n        for j in range(4):\n            arc=ArcBetweenPoints(nl.n2p(3+j)+UP*0.2,nl.n2p(4+j)+UP*0.2,angle=-PI/3,color=GOLD)\n            self.play(Create(arc),run_time=0.2)\n        self.play(GrowFromCenter(Dot(nl.n2p(7),radius=0.12,color=ACCENT)),run_time=0.3)\n" + ans("3 + 4 = 7")))
w("p1_41_nl_sub.py", T("P1_NLSub","P1","Number Line Subtraction","Jump backward", prob("9 - 3 on a number line") + "        nl=NumberLine(x_range=[0,10,1],length=10,include_numbers=True,font_size=18,color=WHITE_C).move_to(UP*0.5)\n        self.play(Create(nl),run_time=0.5)\n        self.play(GrowFromCenter(Dot(nl.n2p(9),radius=0.12,color=TEAL)),run_time=0.3)\n        for j in range(3):\n            arc=ArcBetweenPoints(nl.n2p(9-j)+UP*0.2,nl.n2p(8-j)+UP*0.2,angle=PI/3,color=ACCENT)\n            self.play(Create(arc),run_time=0.2)\n        self.play(GrowFromCenter(Dot(nl.n2p(6),radius=0.12,color=GOLD)),run_time=0.3)\n" + ans("9 - 3 = 6")))
w("p1_42_fact_family.py", T("P1_FactFamily","P1","Fact Families","Related facts", prob("Fact family: 3, 5, 8") + "        facts=['3+5=8','5+3=8','8-3=5','8-5=3']\n        for i,f in enumerate(facts):\n            t=Text(f,font_size=30,color=[TEAL,BLUE,ACCENT,GOLD][i]).move_to(UP*0.8+DOWN*i*0.7)\n            self.play(Write(t),run_time=0.4)\n" + ans("4 facts in one family!")))
w("p1_43_missing_num.py", T("P1_MissingNum","P1","Missing Number","Find the blank", prob("_ + 4 = 9") + steps(["Think: 9 - 4 = ?","9 - 4 = 5"]) + ans("5 + 4 = 9")))
w("p1_44_picture_graph.py", T("P1_PictureGraph","P1","Picture Graphs","Reading data", prob("Favourite fruits") + "        for i,(name,count,c) in enumerate([('Apple',5,ACCENT),('Banana',3,GOLD),('Orange',4,ORANGE)]):\n            y=UP*0.5+DOWN*i*1\n            lbl=Text(name,font_size=22,color=c).move_to(LEFT*4+y)\n            icons=VGroup(*[Dot(radius=0.12,color=c) for _ in range(count)]).arrange(RIGHT,buff=0.25).move_to(LEFT*1+y)\n            self.play(Write(lbl),LaggedStart(*[GrowFromCenter(d) for d in icons],lag_ratio=0.08),run_time=0.4)\n" + ans("Apple is most popular (5)!")))
w("p1_45_make10_pairs.py", T("P1_Make10Pairs","P1","Pairs that Make 10","Number pairs", prob("Which pairs make 10?") + "        for i,(a,b) in enumerate([(1,9),(2,8),(3,7),(4,6),(5,5)]):\n            t=Text(f'{a}+{b}=10',font_size=26,color=GOLD).move_to(UP*1+DOWN*i*0.55)\n            self.play(Write(t),run_time=0.25)\n" + ans("5 pairs that make 10!")))
w("p1_46_sub_objects.py", T("P1_SubObjects","P1","Subtraction with Objects","Cross them out", prob("7 - 2 = ?") + dots_sub(7,2,5) + ans("7 - 2 = 5")))
w("p1_47_count_on.py", T("P1_CountOn","P1","Count On Strategy","Start from bigger", prob("9 + 3: start at 9, count on 3") + steps(["Start at 9","10... 11... 12!","9 + 3 = 12"]) + ans("9 + 3 = 12")))
w("p1_48_part_whole.py", T("P1_PartWhole","P1","Part-Whole Model","Parts make a whole", prob("6 red + 4 blue = ?") + "        whole=Rectangle(width=6,height=0.7,color=GOLD,fill_opacity=0.15,stroke_width=2).move_to(UP*1)\n        wl=Text('Whole: ?',font_size=22,color=GOLD).move_to(whole)\n        p1=Rectangle(width=3,height=0.7,color=TEAL,fill_opacity=0.3).move_to(LEFT*1.5+DOWN*0.3)\n        p2=Rectangle(width=3,height=0.7,color=ACCENT,fill_opacity=0.3).move_to(RIGHT*1.5+DOWN*0.3)\n        self.play(Create(whole),Write(wl),run_time=0.4)\n        self.play(Create(p1),Write(Text('6',font_size=28,color=TEAL).move_to(p1)),Create(p2),Write(Text('4',font_size=28,color=ACCENT).move_to(p2)),run_time=0.5)\n" + ans("6 + 4 = 10")))
w("p1_49_calendar.py", T("P1_Calendar","P1","Calendar","12 months", prob("How many months in a year?") + "        months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']\n        cs=[TEAL,BLUE,GREEN,GOLD,ORANGE,ACCENT,PURPLE,PINK,TEAL,BLUE,GOLD,ACCENT]\n        for i,(m,c) in enumerate(zip(months,cs)):\n            r,col=divmod(i,4)\n            t=Text(m,font_size=20,color=c).move_to(LEFT*3+RIGHT*col*2+UP*0.8+DOWN*r*0.8)\n            self.play(Write(t),run_time=0.1)\n" + ans("12 months in a year!")))
w("p1_50_review.py", T("P1_Review","P1","P1 Review Quiz","Test yourself!", prob("Quick quiz!") + "        qs=[('7+5=?','12'),('10-3=?','7'),('Double 4=?','8')]\n        for i,(q,a) in enumerate(qs):\n            y=UP*0.5+DOWN*i*0.8\n            self.play(Write(Text(q,font_size=28,color=WHITE_C).move_to(LEFT*2+y)),run_time=0.3)\n            self.wait(0.3)\n            self.play(Write(Text(a,font_size=28,color=GOLD).move_to(RIGHT*2+y)),run_time=0.3)\n" + ans("Great job! P1 complete!")))

print(f"  P1 done")


# ===== P2 (04-50) =====
print("P2...")
w("p2_04_mult2.py", T("P2_Mult2","P2","2 Times Table","Multiply by 2", prob("2 times table") + mult_groups(2,7) + ans("2 x 7 = 14")))
w("p2_05_mult3.py", T("P2_Mult3","P2","3 Times Table","Multiply by 3", prob("3 x 6 = ?") + mult_groups(3,6) + ans("3 x 6 = 18")))
w("p2_06_mult4.py", T("P2_Mult4","P2","4 Times Table","Multiply by 4", prob("4 x 5 = ?") + mult_groups(4,5) + ans("4 x 5 = 20")))
w("p2_07_mult5.py", T("P2_Mult5","P2","5 Times Table","Multiply by 5", prob("5 x 8 = ?") + mult_groups(5,8) + ans("5 x 8 = 40")))
w("p2_08_mult10.py", T("P2_Mult10","P2","10 Times Table","Multiply by 10", prob("10 x 6 = ?") + steps(["10 x 6: just add a zero","6 becomes 60"]) + ans("10 x 6 = 60")))
w("p2_09_div_share.py", T("P2_DivShare","P2","Division as Sharing","Share equally", prob("Share 20 among 4 children") + div_groups(20,4) + ans("20 / 4 = 5 each")))
w("p2_10_div_group.py", T("P2_DivGroup","P2","Division as Grouping","Make equal groups", prob("15 into groups of 5") + div_groups(15,3) + ans("15 / 5 = 3 groups")))
w("p2_11_add_3digit.py", T("P2_Add3Digit","P2","3-Digit Addition","Column addition", prob("245 + 138 = ?") + steps(["Ones: 5+8=13, write 3 carry 1","Tens: 4+3+1=8","Hundreds: 2+1=3"]) + ans("245 + 138 = 383")))
w("p2_12_sub_3digit.py", T("P2_Sub3Digit","P2","3-Digit Subtraction","Column subtraction", prob("452 - 178 = ?") + steps(["Ones: 12-8=4 (borrow)","Tens: 14-7=7 (borrow)","Hundreds: 3-1=2"]) + ans("452 - 178 = 274")))
w("p2_13_money_add.py", T("P2_MoneyAdd","P2","Adding Money","Dollars and cents", prob("$3.50 + $1.20 = ?") + steps(["Add cents: 50+20=70c","Add dollars: 3+1=$4","Total: $4.70"]) + ans("$3.50 + $1.20 = $4.70")))
w("p2_14_money_change.py", T("P2_MoneyChange","P2","Giving Change","How much change?", prob("Pay $5 for $3.20 toy. Change?") + steps(["$5.00 - $3.00 = $2.00","$2.00 - $0.20 = $1.80"]) + ans("Change = $1.80")))
w("p2_15_length_cm.py", T("P2_LengthCm","P2","Measuring in cm","Using a ruler", prob("How long is the pencil?") + "        ruler=Rectangle(width=8,height=0.3,color=WHITE_C,fill_opacity=0.1).move_to(DOWN*0.5)\n        pencil=Rectangle(width=6,height=0.2,color=GOLD,fill_opacity=0.6).move_to(UP*0.2+LEFT*1)\n        self.play(Create(ruler),FadeIn(pencil),run_time=0.5)\n        for i in range(9):\n            t=Line(DOWN*0.5+UP*0.15+RIGHT*(i-4),DOWN*0.5+RIGHT*(i-4),color=WHITE_C,stroke_width=1)\n            self.play(Create(t),run_time=0.06)\n" + ans("The pencil is 6 cm")))
w("p2_16_length_m.py", T("P2_LengthM","P2","Metres and cm","Converting units", prob("1 m = ? cm") + steps(["1 metre = 100 centimetres","2 m = 200 cm","1 m 50 cm = 150 cm"]) + ans("1 m = 100 cm")))
w("p2_17_mass_kg.py", T("P2_MassKg","P2","Mass in kg and g","Weighing things", prob("1 kg = ? g") + steps(["1 kilogram = 1000 grams","2 kg = 2000 g","500 g = half a kg"]) + ans("1 kg = 1000 g")))
w("p2_18_volume_l.py", T("P2_VolumeL","P2","Volume in Litres","Measuring liquid", prob("1 litre = ? ml") + steps(["1 litre = 1000 ml","500 ml = half a litre","2 litres = 2000 ml"]) + ans("1 litre = 1000 ml")))
w("p2_19_bar_sub.py", T("P2_BarSub","P2","Bar Model Subtraction","Finding difference", prob("Ali:45, Ben:28. How many more?") + "        b1=Rectangle(width=6,height=0.7,color=BLUE,fill_opacity=0.4).move_to(UP*0.3)\n        l1=Text('Ali: 45',font_size=24,color=BLUE).move_to(b1)\n        b2=Rectangle(width=3.7,height=0.7,color=ACCENT,fill_opacity=0.4)\n        b2.next_to(b1,DOWN,buff=0.3,aligned_edge=LEFT)\n        l2=Text('Ben: 28',font_size=24,color=ACCENT).move_to(b2)\n        self.play(Create(b1),Write(l1),Create(b2),Write(l2),run_time=0.6)\n        diff=Rectangle(width=2.3,height=0.7,color=GOLD,fill_opacity=0.3)\n        diff.next_to(b2,RIGHT,buff=0)\n        dl=Text('?',font_size=28,color=GOLD).move_to(diff)\n        self.play(Create(diff),Write(dl),run_time=0.4)\n" + ans("45 - 28 = 17 more")))
w("p2_20_time_minutes.py", T("P2_TimeMinutes","P2","Time in Minutes","Reading minutes", prob("What time: hour hand at 4, minute at 3?") + steps(["Hour hand at 4 = 4 o'clock hour","Minute hand at 3 = 15 minutes","Time = 4:15"]) + ans("The time is 4:15")))
w("p2_21_time_duration.py", T("P2_TimeDuration","P2","Time Duration","How long?", prob("Start 9:00, end 10:30. How long?") + steps(["From 9:00 to 10:00 = 1 hour","From 10:00 to 10:30 = 30 min","Total = 1 hour 30 minutes"]) + ans("Duration = 1 h 30 min")))


w("p2_22_shapes_3d.py", T("P2_Shapes3D","P2","3D Shapes","Cube, Sphere, Cylinder", prob("Name these 3D shapes") + "        shapes=[('Cube',Square(side_length=1,color=TEAL,fill_opacity=0.3),'6 faces'),('Sphere',Circle(radius=0.6,color=ACCENT,fill_opacity=0.3),'0 edges'),('Cylinder',Rectangle(width=1,height=1.4,color=GOLD,fill_opacity=0.3),'2 circles')]\n        for i,(name,s,desc) in enumerate(shapes):\n            s.move_to(LEFT*3.5+RIGHT*i*3.5+UP*0.3)\n            n=Text(name,font_size=22,color=s.get_color()).next_to(s,UP,buff=0.15)\n            d=Text(desc,font_size=16,color=WHITE_C).next_to(s,DOWN,buff=0.15)\n            self.play(Create(s),Write(n),Write(d),run_time=0.5)\n" + ans("Cube, Sphere, Cylinder!")))
w("p2_23_patterns_shape.py", T("P2_PatternsShape","P2","Shape Patterns","What comes next?", prob("Circle, Square, Circle, Square, ?") + "        shapes=[Circle(radius=0.3,color=TEAL,fill_opacity=0.5),Square(side_length=0.5,color=ACCENT,fill_opacity=0.5)]*2+[Text('?',font_size=36,color=GOLD)]\n        for i,s in enumerate(shapes):\n            s.move_to(LEFT*3.5+RIGHT*i*1.8+UP*0.5)\n            self.play(FadeIn(s),run_time=0.3)\n" + ans("Next is Circle!")))
w("p2_24_number_patterns.py", T("P2_NumberPatterns","P2","Number Patterns","Find the rule", prob("3, 6, 9, 12, ?") + "        for i,n in enumerate([3,6,9,12]):\n            t=Text(str(n),font_size=36,color=TEAL).move_to(LEFT*3+RIGHT*i*2+UP*0.5)\n            self.play(Write(t),run_time=0.25)\n            if i>0:\n                a=Text('+3',font_size=18,color=GOLD).move_to(LEFT*3+RIGHT*(i-0.5)*2+UP*1)\n                self.play(Write(a),run_time=0.15)\n        q=Text('?',font_size=36,color=GOLD).move_to(LEFT*3+RIGHT*4*2+UP*0.5)\n        self.play(Write(q),run_time=0.2)\n" + ans("Pattern: +3. Next is 15!")))
w("p2_25_fractions_half.py", T("P2_FractionsHalf","P2","Halves and Quarters","1/2 and 1/4", prob("What is 1/2 and 1/4?") + frac_bar(1,2) + "        bar2=VGroup()\n        for i in range(4):\n            cell=Rectangle(width=1.5,height=0.8,color=ACCENT if i<1 else WHITE_C,fill_opacity=0.4 if i<1 else 0.05,stroke_width=2,stroke_color=WHITE_C)\n            bar2.add(cell)\n        bar2.arrange(RIGHT,buff=0).move_to(DOWN*1.5)\n        self.play(LaggedStart(*[Create(c) for c in bar2],lag_ratio=0.05),run_time=0.5)\n" + ans("1/2 = 2 parts, 1/4 = 4 parts")))
w("p2_26_equal_fractions.py", T("P2_EqualFractions","P2","Equal Parts","Fractions need equal parts", prob("Are these halves?") + "        good=Rectangle(width=4,height=0.8,color=TEAL,fill_opacity=0.2).move_to(UP*0.5)\n        gl=Line(good.get_center()+UP*0.4,good.get_center()+DOWN*0.4,color=TEAL)\n        gt=Text('Equal halves ✓',font_size=22,color=TEAL).next_to(good,RIGHT,buff=0.3)\n        self.play(Create(good),Create(gl),Write(gt),run_time=0.5)\n        bad=Rectangle(width=4,height=0.8,color=ACCENT,fill_opacity=0.2).move_to(DOWN*0.8)\n        bl=Line(bad.get_left()+RIGHT*1+UP*0.4,bad.get_left()+RIGHT*1+DOWN*0.4,color=ACCENT)\n        bt=Text('Not equal ✗',font_size=22,color=ACCENT).next_to(bad,RIGHT,buff=0.3)\n        self.play(Create(bad),Create(bl),Write(bt),run_time=0.5)\n" + ans("Fractions must be equal parts!")))
w("p2_27_multiplication_word.py", T("P2_MultWord","P2","Multiplication Word Problem","Groups of items", prob("5 bags, 6 oranges each. Total?") + mult_groups(5,6) + ans("5 x 6 = 30 oranges")))
w("p2_28_division_word.py", T("P2_DivWord","P2","Division Word Problem","Sharing equally", prob("24 cookies shared among 6 children") + div_groups(24,6) + ans("24 / 6 = 4 cookies each")))
w("p2_29_odd_even_100.py", T("P2_OddEven100","P2","Odd and Even to 100","Bigger numbers", prob("Is 47 odd or even? Is 82?") + steps(["47: ones digit is 7 (odd) -> ODD","82: ones digit is 2 (even) -> EVEN","Look at the ones digit!"]) + ans("47=odd, 82=even")))
w("p2_30_place_value_100s.py", T("P2_PlaceValue100s","P2","Place Value to 1000","Hundreds, tens, ones", prob("What is 365?") + "        for i,(lbl,val,c) in enumerate([('Hundreds',3,TEAL),('Tens',6,BLUE),('Ones',5,ACCENT)]):\n            box=Rectangle(width=2.5,height=0.8,color=c,fill_opacity=0.2).move_to(LEFT*3+RIGHT*i*3+UP*0.5)\n            t=Text(f'{lbl}: {val}',font_size=24,color=c).move_to(box)\n            self.play(Create(box),Write(t),run_time=0.4)\n" + ans("365 = 3 hundreds + 6 tens + 5 ones")))
w("p2_31_rounding_10.py", T("P2_Rounding10","P2","Rounding to 10","Nearest ten", prob("Round 37 to nearest 10") + "        nl=NumberLine(x_range=[30,40,1],length=10,include_numbers=True,font_size=18,color=WHITE_C).move_to(UP*0.5)\n        self.play(Create(nl),run_time=0.5)\n        d=Dot(nl.n2p(37),radius=0.12,color=ACCENT)\n        self.play(GrowFromCenter(d),run_time=0.3)\n        arr=Arrow(nl.n2p(37)+UP*0.5,nl.n2p(40)+UP*0.5,color=GOLD,stroke_width=2)\n        self.play(Create(arr),run_time=0.4)\n" + ans("37 rounds to 40")))
w("p2_32_estimation.py", T("P2_Estimation","P2","Estimation","Guess then check", prob("Estimate 48 + 33") + steps(["48 is about 50","33 is about 30","Estimate: 50+30=80","Actual: 48+33=81"]) + ans("Estimate 80, actual 81. Close!")))
w("p2_33_bar_graph.py", T("P2_BarGraph","P2","Bar Graphs","Reading bar charts", prob("Favourite sports") + "        sports=[('Soccer',8,TEAL),('Swimming',5,BLUE),('Running',6,ACCENT)]\n        for i,(name,val,c) in enumerate(sports):\n            bar=Rectangle(width=0.8,height=val*0.3,color=c,fill_opacity=0.5)\n            bar.move_to(LEFT*2.5+RIGHT*i*2+DOWN*0.5+UP*val*0.15)\n            lbl=Text(name,font_size=18,color=c).next_to(bar,DOWN,buff=0.1)\n            vt=Text(str(val),font_size=20,color=c).next_to(bar,UP,buff=0.1)\n            self.play(GrowFromEdge(bar,DOWN),Write(lbl),Write(vt),run_time=0.5)\n" + ans("Soccer is most popular (8)!")))
w("p2_34_line_symmetry.py", T("P2_LineSymmetry","P2","Line Symmetry","Mirror image", prob("Which shapes have symmetry?") + "        sq=Square(side_length=1.5,color=TEAL,fill_opacity=0.2).move_to(LEFT*3+UP*0.3)\n        sl=DashedLine(sq.get_top(),sq.get_bottom(),color=GOLD,dash_length=0.1)\n        self.play(Create(sq),Create(sl),Write(Text('Yes ✓',font_size=20,color=TEAL).next_to(sq,DOWN,buff=0.2)),run_time=0.5)\n        tri=Triangle(color=ACCENT,fill_opacity=0.2).scale(0.8).move_to(RIGHT*0+UP*0.3)\n        tl=DashedLine(tri.get_top(),tri.get_bottom()+DOWN*0.1,color=GOLD,dash_length=0.1)\n        self.play(Create(tri),Create(tl),Write(Text('Yes ✓',font_size=20,color=ACCENT).next_to(tri,DOWN,buff=0.2)),run_time=0.5)\n" + ans("Symmetric = same on both sides!")))
w("p2_35_mental_add.py", T("P2_MentalAdd","P2","Mental Addition","Quick tricks", prob("67 + 28 = ? (mentally)") + steps(["67 + 30 = 97 (add 30)","97 - 2 = 95 (subtract 2)","Because 28 = 30 - 2"]) + ans("67 + 28 = 95")))
w("p2_36_mental_sub.py", T("P2_MentalSub","P2","Mental Subtraction","Quick tricks", prob("83 - 29 = ? (mentally)") + steps(["83 - 30 = 53 (subtract 30)","53 + 1 = 54 (add back 1)","Because 29 = 30 - 1"]) + ans("83 - 29 = 54")))


w("p2_37_mult_word2.py", T("P2_MultWord2","P2","Multiplication Story 2","Rows and columns", prob("3 rows of 7 chairs. How many?") + mult_groups(3,7) + ans("3 x 7 = 21 chairs")))
w("p2_38_div_remainder.py", T("P2_DivRemainder","P2","Division with Remainder","Leftovers", prob("13 / 4 = ?") + steps(["4 x 3 = 12 (fits 3 times)","13 - 12 = 1 (remainder)","13 / 4 = 3 remainder 1"]) + ans("13 / 4 = 3 R 1")))
w("p2_39_number_bonds_20.py", T("P2_NumberBonds20","P2","Number Bonds of 20","Pairs to 20", prob("Find pairs that make 20") + "        for i,(a,b) in enumerate([(2,18),(5,15),(8,12),(10,10),(13,7)]):\n            t=Text(f'{a}+{b}=20',font_size=24,color=GOLD).move_to(UP*1+DOWN*i*0.55)\n            self.play(Write(t),run_time=0.2)\n" + ans("Many pairs make 20!")))
w("p2_40_doubles_20.py", T("P2_Doubles20","P2","Doubles to 20","Double it!", prob("Doubles: 6+6, 7+7, 8+8, 9+9, 10+10") + "        for i,(n,t2) in enumerate([(6,12),(7,14),(8,16),(9,18),(10,20)]):\n            t=Text(f'{n}+{n}={t2}',font_size=26,color=TEAL).move_to(UP*1+DOWN*i*0.55)\n            self.play(Write(t),run_time=0.25)\n" + ans("Doubles are easy to remember!")))
w("p2_41_comparison_word.py", T("P2_ComparisonWord","P2","Comparison Word Problem","How many more?", prob("Ali:35 stickers, Ben:22. Difference?") + "        b1=Rectangle(width=5.5,height=0.7,color=BLUE,fill_opacity=0.4).move_to(UP*0.3)\n        l1=Text('Ali: 35',font_size=24,color=BLUE).move_to(b1)\n        b2=Rectangle(width=3.5,height=0.7,color=ACCENT,fill_opacity=0.4)\n        b2.next_to(b1,DOWN,buff=0.3,aligned_edge=LEFT)\n        l2=Text('Ben: 22',font_size=24,color=ACCENT).move_to(b2)\n        self.play(Create(b1),Write(l1),Create(b2),Write(l2),run_time=0.6)\n" + ans("35 - 22 = 13 more")))
w("p2_42_2step_word.py", T("P2_2StepWord","P2","2-Step Word Problem","Two operations", prob("Sam has 15. Gets 8 more. Gives 6 away.") + steps(["Step 1: 15 + 8 = 23","Step 2: 23 - 6 = 17"]) + ans("Sam has 17 left")))
w("p2_43_tables_data.py", T("P2_TablesData","P2","Reading Tables","Data in tables", prob("Read the table") + "        header=VGroup(Text('Fruit',font_size=20,color=GOLD),Text('Count',font_size=20,color=GOLD)).arrange(RIGHT,buff=2).move_to(UP*1.2)\n        self.play(Write(header),run_time=0.3)\n        for i,(f,c) in enumerate([('Apple',12),('Banana',8),('Orange',15)]):\n            row=VGroup(Text(f,font_size=20,color=WHITE_C),Text(str(c),font_size=20,color=TEAL)).arrange(RIGHT,buff=2.3).move_to(UP*0.5+DOWN*i*0.6)\n            self.play(Write(row),run_time=0.3)\n" + ans("Orange has the most (15)!")))
w("p2_44_ordinal_20.py", T("P2_Ordinal20","P2","Ordinal Numbers to 20","Position in line", prob("What is the 15th letter?") + "        for i in range(20):\n            c=GOLD if i==14 else WHITE_C\n            t=Text(str(i+1),font_size=16,color=c).move_to(LEFT*5+RIGHT*(i%10)*1+UP*0.5+DOWN*(i//10)*0.6)\n            self.play(Write(t),run_time=0.06)\n" + ans("15th position highlighted!")))
w("p2_45_money_notes.py", T("P2_MoneyNotes","P2","Money Notes","$2, $5, $10", prob("$10 + $5 + $2 = ?") + "        for i,(val,c) in enumerate([('$10',TEAL),('$5',BLUE),('$2',ACCENT)]):\n            note=RoundedRectangle(width=2,height=1,corner_radius=0.1,color=c,fill_opacity=0.3).move_to(LEFT*3+RIGHT*i*2.5+UP*0.5)\n            t=Text(val,font_size=24,color=c).move_to(note)\n            self.play(Create(note),Write(t),run_time=0.3)\n" + ans("$10 + $5 + $2 = $17")))
w("p2_46_capacity_ml.py", T("P2_CapacityMl","P2","Capacity in ml","Measuring cups", prob("250 ml + 250 ml = ?") + steps(["250 ml + 250 ml","= 500 ml","= half a litre"]) + ans("250 + 250 = 500 ml")))
w("p2_47_perimeter_intro.py", T("P2_PerimeterIntro","P2","Perimeter Introduction","Distance around", prob("Walk around the rectangle") + "        rect=Rectangle(width=4,height=2,color=BLUE,fill_opacity=0.15,stroke_width=3).move_to(UP*0.3)\n        self.play(Create(rect),run_time=0.5)\n        corners=[rect.get_corner(UL),rect.get_corner(UR),rect.get_corner(DR),rect.get_corner(DL),rect.get_corner(UL)]\n        trace=VMobject(color=GOLD,stroke_width=4)\n        trace.set_points_as_corners(corners)\n        self.play(Create(trace),run_time=1.5)\n" + ans("Perimeter = distance around!")))
w("p2_48_equal_sign.py", T("P2_EqualSign","P2","Equal Sign Meaning","Balance both sides", prob("Is 3+4 = 5+2 true?") + steps(["Left side: 3+4 = 7","Right side: 5+2 = 7","7 = 7 ✓ TRUE!"]) + ans("3+4 = 5+2 (both equal 7)")))
w("p2_49_inverse_ops.py", T("P2_InverseOps","P2","Inverse Operations","Undo with opposite", prob("Addition undoes subtraction") + steps(["8 + 5 = 13","13 - 5 = 8 (back to start!)","+ and - are inverse operations"]) + ans("Addition and subtraction are inverses")))
w("p2_50_review.py", T("P2_Review","P2","P2 Review Quiz","Test yourself!", prob("Quick quiz!") + "        qs=[('3x5=?','15'),('20/4=?','5'),('245+138=?','383')]\n        for i,(q,a) in enumerate(qs):\n            y=UP*0.5+DOWN*i*0.8\n            self.play(Write(Text(q,font_size=28,color=WHITE_C).move_to(LEFT*2+y)),run_time=0.3)\n            self.wait(0.3)\n            self.play(Write(Text(a,font_size=28,color=GOLD).move_to(RIGHT*2+y)),run_time=0.3)\n" + ans("Great job! P2 complete!")))

print(f"  P2 done")

