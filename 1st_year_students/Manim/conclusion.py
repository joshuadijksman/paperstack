from manim import *
import math


class conclusion(Scene):
    def construct(self):
        

        why = Tex('Due to the scope and nature of our experiment, we were not able to figure out exactly why this happens.').scale(0.8)
        list1 = Tex('We thought it could be due to air between the sheets, and tested with a smaller format paper. This did not change the result.').scale(0.8)
        list2 = Tex('Our key finding is that there are three separate regimes in which the CoR behaves unintuitively. Between 0-10 pages, 10-100 pages and 100-350 pages.').scale(0.8)
        list3 = Tex('Further research is required on this topic.').scale(0.8)

        rectangle_yurr = Rectangle(
            height=10,
            width=14,
            color=DARK_BLUE,
            fill_color=BLUE,
            fill_opacity=0.75,
        )

        self.play(Write(VGroup(rectangle_yurr), run_time=3))
        self.play(Write(why.to_edge(UP, buff=0.1)), run_time=3)
        self.wait(2)
        self.play(Write(list1.to_edge(UP, buff=1.1)), run_time=3)
        self.wait(2)
        self.play(Write(list2.to_edge(UP, buff=2.1)), run_time=3)
        self.wait(2)
        self.play(Write(list3.to_edge(UP, buff=4.1)), run_time=3)
        self.wait()
        self.play(FadeOut(why, list1, list2, list3))