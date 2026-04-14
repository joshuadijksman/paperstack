from manim import *
import math


A4_AND_A5_COR_H = 'C:/Users/salad/manimations/Manim/media/images/results/A4_AND_A5_COR_H_AVG_SIGMA.png'
A4_AND_A5_COR_V = 'C:/Users/salad/manimations/Manim/media/images/results/A4_AND_A5_COR_V_AVG_SIGMA.png'
A5_COR_H_LOW = 'C:/Users/salad/manimations/Manim/media/images/results/A5_COR_H_LOW_AVG_SIGMA.png'
A5_COR_V_LOW = 'C:/Users/salad/manimations/Manim/media/images/results/A5_COR_V_LOW_AVG_SIGMA.png'

class results(Scene):
    def construct(self):
        

        im1 = ImageMobject(A4_AND_A5_COR_H)
        im2 = ImageMobject(A4_AND_A5_COR_V)
        im3 = ImageMobject(A5_COR_H_LOW)
        im4 = ImageMobject(A5_COR_V_LOW)

        yap_3 = Tex('With the trajectory, we are able to calculate the CoR.').scale(0.8)
        yap_4 = Tex('Here we can see the CoR plotted against the amount of paper sheets, for A4-format and A5-format. On the left calculated with height ratio, and the right velocity ratio.').scale(0.8)
        eq_1 = MathTex(r'\sqrt{\frac{h_1}{h_0}}')
        eq_2 = MathTex(r'\frac{v_1}{v_0}')
        yap_5 = Tex('Weird trend, huh? But why does it happen?')


        rectangle_1 = Rectangle(
            height=1, 
            width=10, 
            color=DARK_BLUE,
            fill_color=BLUE,
            fill_opacity=0.75
            )

        rectangle_2 = Rectangle(
            height=2, 
            width=14, 
            color=DARK_BLUE,
            fill_color=BLUE,
            fill_opacity=0.75,
            )
        
        self.play(Write(VGroup(rectangle_1)))
        self.play(Write(yap_3))
        self.wait(3)
        self.play(RemoveTextLetterByLetter(yap_3))
        self.remove(rectangle_1)
        self.wait()
        self.play(Write(VGroup(rectangle_2.to_edge(UP, buff=0.3))))
        self.play(Write(yap_4.to_edge(UP, buff=0.6), run_time=7))
        self.play(Write(eq_1.to_edge(LEFT, buff=0.1)))
        self.play(FadeIn(im1.to_edge(LEFT, buff=0.5).scale(0.8)))
        self.play(FadeIn(im2.to_edge(RIGHT, buff=0.5).scale(0.8)))
        self.play(Write(eq_2.to_edge(RIGHT, buff=0.5)))
        self.wait(3)
        self.play(Write(yap_5.to_edge(DOWN, buff=1.5)))
        self.wait(5)
        self.play(FadeOut(rectangle_2, yap_4, eq_1, im1, im2,  eq_2, yap_5))