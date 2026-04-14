from manim import *

class Animation(Scene):
    def construct(self):
        # tekst
        textboven = Text("Restitution Coefficient")
        textboven.move_to(UP * 0.5)
        textonder = Text("of a falling marble on a stack of paper")
        textonder.move_to(DOWN * 0.5)

        self.play(Write(textboven))
        self.play(Write(textonder))
        self.wait(2)
        self.play(FadeOut(textboven),FadeOut(textonder))
        

        # knikker en papier maken en benoemen     
        circle = Circle(radius = 0.5) 
        circle.set_fill(BLUE,opacity=0.7)      
        rectangular = Rectangle(width=4, height = 1)
        rectangular.set_fill(WHITE, opacity=0.7)     
        rectangular.to_edge(DOWN)
        self.play(Create(rectangular))
        
        textpapier = Text("Stack of paper with x number of layers")
        textpapier.move_to(UP * 0.5)
        self.play(Write(textpapier))
        arrow = Arrow (ORIGIN, [0,-2,0], buff = 0 )
        self.play(Create(arrow))
        self.play(FadeOut(arrow), FadeOut(textpapier))
        circle.to_edge(UP)
        self.play(Create(circle))
        textknikker = Text("marble")
        textknikker.move_to(DOWN * 0.5)
        self.play(Write(textknikker))
        arrow = Arrow(ORIGIN, [0,2,0], buff = 0)
        self.play(Create(arrow))
        self.play(FadeOut(arrow), FadeOut(textknikker))

        # laten stuiteren van de knikker
        self.play(circle.animate.shift(DOWN * 5), run_time = 1)
        self.play(circle.animate.shift(UP * 4), run_time = 0.75)
        self.play(circle.animate.shift(DOWN * 4), run_time = 0.75)
        texthoogte = Text("The marble drops lower with each bounce")
        texthoogte.move_to(UP * 3)
        self.play(Write(texthoogte), circle.animate.shift(UP * 3), run_time = 0.5)
        self.play(circle.animate.shift(DOWN * 3), run_time = 0.5)
        self.play(circle.animate.shift(UP * 2), run_time = 0.25)
        self.play(circle.animate.shift(DOWN * 2), run_time = 0.25)
        self.play(circle.animate.shift(UP * 1), run_time = 0.125)
        self.play(circle.animate.shift(DOWN * 1), run_time = 0.125)
        self.play(circle.animate.shift(UP * 0.5), run_time = 0.06)
        self.play(circle.animate.shift(DOWN * 0.5), run_time = 0.06)
        self.play(circle.animate.shift(UP * 0.25), run_time = 0.03)
        self.play(circle.animate.shift(DOWN * 0.25), run_time = 0.03)
        self.play(FadeOut(texthoogte), FadeOut(circle), FadeOut(rectangular))
    
        # Uitleg CoR
        textuitlegcordeel1 = Text("The ratio of")
        textuitlegcordeel3 = Text("the height after and before a bounce")
        textuitlegcordeel2 = Text("is equal to the restitution coefficient:")
        textuitlegcordeel1.move_to(UP * 1)
        textuitlegcordeel2.move_to(DOWN * 1)
        self.play(FadeIn(textuitlegcordeel1), FadeIn(textuitlegcordeel2), FadeIn(textuitlegcordeel3))
        self.wait(3)
        self.play(FadeOut(textuitlegcordeel1), FadeOut(textuitlegcordeel2), FadeOut(textuitlegcordeel3))

        # laten zien van CoR
        circle = Circle(radius = 0.5) 
        circle.set_fill(BLUE,opacity=0.7)      
        rectangular = Rectangle(width=4, height = 1)
        rectangular.set_fill(WHITE, opacity=0.7)     
        rectangular.to_edge(DOWN)
        self.play(Create(rectangular)) 
        circle.to_edge(UP)
        self.play(Create(circle))
        texthoogte1 = Text("The height of the marble before the bounce.")
        texth1 = Text("Height 1")
        texth1.move_to(DOWN * 1)
        lineh1 = Line([-0.5,2.5,0], [0.5,2.5,0]).set_color(WHITE)
        self.play(Create(lineh1))
        self.play(Write(texthoogte1))
        self.play(Write(texth1))
        self.play(FadeOut(texthoogte1), FadeOut(lineh1))
        self.play(texth1.animate.shift(RIGHT * 4))
        #self.play(texth1.animate.shift(DOWN * 1))
        self.play(circle.animate.shift(DOWN*5))
        self.play(circle.animate.shift(UP*3))
        texthoogte2 = Text("The height of the marble after the bounce.")
        texth2 = Text("Height 2")
        texth2.move_to(DOWN*1)
        lineh2 = Line([-0.5,0.5,0], [0.5, 0.5, 0]).set_color(WHITE)
        self.play(Create(lineh2))
        self.play(Write(texthoogte2))
        self.play(Write(texth2))
        self.play(FadeOut(texthoogte2), FadeOut(lineh2))
        self.play(texth2.animate.shift(UP * 1.5))
        self.play(texth2.animate.shift(RIGHT * 4))
        #self.play(texth2.animate.shift(UP*1.5))
        self.play(FadeOut(circle), FadeOut(rectangular))
        self.play(texth1.animate.shift(LEFT*4), texth2.animate.shift(LEFT*4))
        linebreuk1 = Line([1,0,0], [-1,0,0]).set_color(WHITE)
        self.play(Create(linebreuk1), texth1.animate.shift(UP*0.5))
        self.play(texth1.animate.shift(LEFT * 3.5), texth2.animate.shift(LEFT * 3.5), linebreuk1.animate.shift(LEFT * 3.5))
        lineis1 = Line([-1.7,0.15,0], [-0.7,0.15,0]).set_color(WHITE)
        lineis2 = Line([-1.7,-0.2,0], [-0.7,-0.2,0]).set_color(WHITE)
        self.play(Create(lineis1), Create(lineis2))

        textboven.move_to(RIGHT*2.5)
        self.play(Write(textboven))
        self.play(FadeOut(textboven), FadeOut(texth1), FadeOut(texth2), FadeOut(lineis1), FadeOut(lineis2))

    # grafiek maken
        # ax = Axes(
        #     x_range=[0,500, 50], y_range=[0,1,0.1], x_axis_config= {"numbers_to_include":[]}, y_axis_config = {"numbers_to_include":[]})
        # #labels = ax.get_axis_labels(x_label ="aantal vellen papier", y_label = "Resitutie Coëfficient (CoR)")
        # self.add(ax)

        #labels = assen.get_axis_labels(x_label="x", y_label="f(x)")

        #functie = assen.plot(lambda x: x**2, color=YELLOW) Hier nog eigenfunctie toepassen

        #functielabel = assen.get_graph_label(functie, label="x^2") Hier nog eigen label toepassen

        #self.play(Create(assen))
        #self.play(Create(functie))

        # arrowdal = Arrow([], [0,2,0], buff = 0) #plek nog toevoegen
        # arrowpiek = Arrow([], [0,2,0], buff = 0) #plek nog toevoegen
        # textdal = Text("The coefficient of restitution is lowest for x sheets")
        # textdal.move_to( UP*3)

        # textpiek = Text("The coefficient of restitution is highest for x sheets")
        # textpiek.move_to(UP*3)

        # self.play(Create(arrowdal), Create(textdal))
        # self.wait(2)
        # self.play(FadeOut(arrowdal), FadeOut(textdal))
        # self.play(Create(arrowpiek), Create(textpiek))
        # self.wait(FadeOut(arrowpiek), FadeOut(textpiek))

        #self.play(FadeOut(assen), FadeOut(functie))

    # Hier nu de 2 filmpjes naast elkaar voegen die we ook gebruiken bij het tracken van de aantal papiertjes met de hoogste CoR en laagste CoR

        #textreden = Text("The reason for this is probably ....")
        # self.play(Write(textreden))
        # self.wait(5)
        # self.play(FadeOut(textreden))



        



