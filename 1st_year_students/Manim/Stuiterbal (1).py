from manim import *
import math

class Stuiterbal(Scene):
    def construct(self):
        

        yap_1 = Tex('With this information, we are able to plot the trajectory of the marble.').scale(0.8)
        yap_2 = Tex('The typical trajectory of the marble looks like this:').scale(0.8)


        rectangle_1 = Rectangle(
            height=1, 
            width=13, 
            color=DARK_BLUE, 
            fill_color=BLUE, 
            fill_opacity=0.75
            )

        rectangle_2 = Rectangle(
            height=1, 
            width=10, 
            color=DARK_BLUE, 
            fill_color=BLUE, 
            fill_opacity=0.75
            )

        # Assen aanmaken en assenschaal
        Assen = Axes(
            x_range=[0, 350, 50],
            y_range=[0, 700, 100],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True}
        )
        Assen.scale(0.8)



        A = Assen.c2p(0, 600)
        B = Assen.c2p(130, 0)
        C = Assen.c2p(190, 0)
        D = Assen.c2p(220, 0)
        E = Assen.c2p(250, 0)


        Bal = Dot(radius = 0.1, color=BLUE_D).move_to(A)
        sp = VGroup()
        pad1 = Line(start= A, end = B, path_arc= -1)
        pad2 = Line(start = B, end = C, path_arc= -3)
        pad3 = Line(start = C, end = D, path_arc= -3)
        pad4 = Line(start = D, end = E, path_arc= -1)

        # Labels bij de assen toevoegen
        x_label = Tex('Time ', '(Frames)').scale(0.7)
        x_label.next_to(Assen.x_axis, DOWN, buff = 0.4)
        x_label[1].color=BLUE

        y_label = Tex('Height ', '(Pixels)').scale(0.7)
        y_label[1].color=RED
        y_label.next_to(Assen.y_axis, LEFT, buff=0.3)
        y_label.rotate(PI / 2)
        y_label.shift(1 * RIGHT)

        Bal.laatste_pos = Bal.get_center()

        def spoor(mob):
            nieuwe_pos = mob.get_center()
            if np.linalg.norm(nieuwe_pos - mob.laatste_pos) > 0.2:
                stip = Dot(nieuwe_pos, radius=0.05, color=BLUE_B)
                sp.add(stip)
                self.add(stip)
                mob.laatste_pos = nieuwe_pos
                print(f"Aantal stippen: {len(sp)}")

        self.play(Write(VGroup(rectangle_1)))
        self.play(Write(yap_1), run_time=3)
        self.wait()
        self.play(RemoveTextLetterByLetter(yap_1), run_time=3)
        self.remove(rectangle_1)
        self.wait()
        self.play(Write(VGroup(rectangle_2).to_edge(UP, buff=0.3)))
        self.play(Write(yap_2.to_edge(UP, buff=0.6)))
        self.wait()

        Bal.add_updater(spoor)
        self.play(Write(VGroup(Assen, x_label, y_label), run_time=3))
        

        self.play(MoveAlongPath(Bal, pad1), run_time = 1, rate_func = linear)
        Bal.laatste_pos = Bal.get_center()
        self.play(MoveAlongPath(Bal, pad2), run_time = 1, rate_func = linear)
        Bal.laatste_pos = Bal.get_center()
        self.play(MoveAlongPath(Bal, pad3), run_time = 1, rate_func = linear)
        Bal.laatste_pos = Bal.get_center()
        self.play(MoveAlongPath(Bal, pad4), run_time = 1, rate_func = linear)

        self.add(*sp)

        self.wait(3)
        self.play(FadeOut(rectangle_2, yap_2, Assen, x_label, y_label,  Bal, pad1, pad2, pad3, pad4, sp))