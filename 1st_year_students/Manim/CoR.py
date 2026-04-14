from manim import *
import math


class Stuiterbal(Scene):
    def construct(self):


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


        Bal = Dot(radius = 0.1).move_to(A)
        sp = VGroup()
        pad1 = Line(start= A, end = B, path_arc= -1)
        pad2 = Line(start = B, end = C, path_arc= -3)
        pad3 = Line(start = C, end = D, path_arc= -3)
        pad4 = Line(start = D, end = E, path_arc= -1)

        # Labels bij de assen toevoegen
        x_label = Tex("\# of paper pages (amount)").scale(0.7)
        x_label.next_to(Assen.x_axis, DOWN, buff = 0.4)

        y_label = Tex("Restitutioncoefficient (ratio)").scale(0.7)
        y_label.next_to(Assen.y_axis, LEFT, buff=0.3)
        y_label.rotate(PI / 2)
        y_label.shift(2 * RIGHT)

        Bal.laatste_pos = Bal.get_center()

        def spoor(mob):
            nieuwe_pos = mob.get_center()
            if np.linalg.norm(nieuwe_pos - mob.laatste_pos) > 0.2:
                stip = Dot(nieuwe_pos, radius=0.05, color=RED)
                sp.add(stip)
                self.add(stip)
                mob.laatste_pos = nieuwe_pos
                print(f"Aantal stippen: {len(sp)}")

    

        
        Bal.add_updater(spoor)
        self.play(Write(VGroup(Assen, x_label, y_label)))
        

        self.play(MoveAlongPath(Bal, pad1), run_time = 1, rate_func = linear)
        Bal.laatste_pos = Bal.get_center()
        self.play(MoveAlongPath(Bal, pad2), run_time = 1, rate_func = linear)
        Bal.laatste_pos = Bal.get_center()
        self.play(MoveAlongPath(Bal, pad3), run_time = 1, rate_func = linear)
        Bal.laatste_pos = Bal.get_center()
        self.play(MoveAlongPath(Bal, pad4), run_time = 1, rate_func = linear)

        self.add(*sp)

        self.wait()
