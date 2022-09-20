from manim import *
from main import p_read, TBP_calculate

# Calculate array
TBP = TBP_calculate()

r1 = TBP[0]
r2 = TBP[1]
r3 = TBP[2]

# Provide paramters
sun_speed = p_read('sun_speed', int)
fade_length = p_read('fade_length', int)
framerate = p_read('framerate', int)
run_time = p_read('run_time', int)

rays = p_read('rays', bool)
tail = p_read('tail', bool)


#################### MANIM ANIMATIONS ####################

# starting animation
class TBP_starting_scene(Scene):
    def construct(self):
        timeline = ValueTracker(0)

        # Kreieren der 3 Sonnen
        sun1 = VGroup(Circle(color = WHITE, radius = 0.1, fill_color = WHITE, fill_opacity = 0.5)).shift(r1[:,0])
        sun2 = VGroup(Circle(color = RED, radius = 0.1, fill_color = RED, fill_opacity = 0.5)).shift(r2[:,0])
        sun3 = VGroup(Circle(color = YELLOW, radius = 0.1, fill_color = YELLOW, fill_opacity = 0.5)).shift(r3[:,0])

        # Überschrift
        head = Text('Numerical Solution of the Three-Body-Problem', color = WHITE).to_edge(UP).scale(0.8)
        foot = Text('animated in manim using center-of-mass coordinates.', color = BLUE).to_edge(DOWN).scale(0.6)
        self.play(Write(head), run_time = 1.5)
        self.play(Write(foot), run_time = 1.5)
        self.wait(0.5)
        self.play(ReplacementTransform(VGroup(foot), VGroup(sun1, sun2, sun3)), Unwrite(head, reverse = False), run_time = 2)
        self.wait(0.5)

        # Hizufügen der Strahlen (optional)
        if rays:
            for i in range(16):
                sb1e = Line().rotate(2*PI/16*i).scale(0.15).shift(r1[:,0]).get_end()
                s1e = Line().rotate(2*PI/16*i).scale(np.random.uniform(0.3, 0.6)).shift(r1[:,0]).get_end()
                sun1_ray = DashedLine(sb1e, s1e, color = WHITE, dash_length=0.005)
                sun1.add(sun1_ray)
                self.add(sun1_ray)

                sb2e = Line().rotate(2*PI/16*i).scale(0.15).shift(r2[:,0]).get_end()
                s2e = Line().rotate(2*PI/16*i).scale(np.random.uniform(0.3, 0.6)).shift(r2[:,0]).get_end()
                sun2_ray = DashedLine(sb2e, s2e, color = RED, dash_length=0.005)
                sun2.add(sun2_ray)
                self.add(sun2_ray)

                sb3e = Line().rotate(2*PI/16*i).scale(0.15).shift(r3[:,0]).get_end()
                s3e = Line().rotate(2*PI/16*i).scale(np.random.uniform(0.3, 0.6)).shift(r3[:,0]).get_end()
                sun3_ray = DashedLine(sb3e, s3e, color = YELLOW, dash_length=0.005)
                sun3.add(sun3_ray) 
                self.add(sun3_ray)
                self.wait(0.075)
        self.wait(1)


# main animation
class TBP_main_scene(Scene):
    def construct(self):
        timeline = ValueTracker(0)

        # Kreieren der 3 Sonnen
        sun1 = VGroup(Circle(color = WHITE, radius = 0.1, fill_color = WHITE, fill_opacity = 0.5))
        sun2 = VGroup(Circle(color = RED, radius = 0.1, fill_color = RED, fill_opacity = 0.5))
        sun3 = VGroup(Circle(color = YELLOW, radius = 0.1, fill_color = YELLOW, fill_opacity = 0.5))

        # Positionsiteratoren der 3 Sonnen
        sun1.iter = iter(r1.T[::sun_speed,])
        sun2.iter = iter(r2.T[::sun_speed,])
        sun3.iter = iter(r3.T[::sun_speed,])

        # Updater der Sonnenpositionen
        def sun_updater(sun):
            sun.move_to(next(sun.iter))

        # Schweif-Updater
        def dot1_fadeout_updater(dot1):
            if dot1.counter != fade_length and dot1.counter != 1:
                dot1.fill_opacity -= 1/fade_length
                dot1.set_opacity(dot1.fill_opacity)
                dot1.counter -= 1                
            elif dot1.counter == fade_length:
                dot1.move_to(sun1.get_center())
                dot1.fill_opacity = 1
                dot1.set_opacity(dot1.fill_opacity)
                dot1.counter -= 1
            else:
                dot1.counter = fade_length
                dot1.fill_opacity = 1

        def dot2_fadeout_updater(dot2):
            if dot2.counter != fade_length and dot2.counter != 1:
                dot2.fill_opacity -= 1/fade_length
                dot2.set_opacity(dot2.fill_opacity)
                dot2.counter -= 1                
            elif dot2.counter == fade_length:
                dot2.move_to(sun2.get_center())
                dot2.fill_opacity = 1
                dot2.set_opacity(dot2.fill_opacity)
                dot2.counter -= 1
            else:
                dot2.counter = fade_length
                dot2.fill_opacity = 1           

        def dot3_fadeout_updater(dot3):
            if dot3.counter != fade_length and dot3.counter != 1:
                dot3.fill_opacity -= 1/fade_length
                dot3.set_opacity(dot3.fill_opacity)
                dot3.counter -= 1
            elif dot3.counter == fade_length:
                dot3.move_to(sun3.get_center())
                dot3.fill_opacity = 1
                dot3.set_opacity(dot3.fill_opacity)
                dot3.counter -= 1
            else:
                dot3.counter = fade_length
                dot3.fill_opacity = 1

        # Hinzufügen der Schweife
        if tail:
            for i in range(fade_length):
                dot1 = Dot(radius = 0.05, fill_color = WHITE, fill_opacity = 0.5)
                dot1.counter = fade_length + i
                dot1.fill_opacity = 0
                dot1.set_opacity(dot1.fill_opacity)
                self.add(dot1)
                dot1.add_updater(dot1_fadeout_updater)

                dot2 = Dot(radius = 0.05, fill_color = RED, fill_opacity = 0.5)
                dot2.counter = fade_length + i
                dot2.fill_opacity = 0
                dot2.set_opacity(dot2.fill_opacity)
                self.add(dot2)
                dot2.add_updater(dot2_fadeout_updater)

                dot3 = Dot(radius = 0.05, fill_color = YELLOW, fill_opacity = 0.5)
                dot3.counter = fade_length + i
                dot3.fill_opacity = 0
                dot3.set_opacity(dot3.fill_opacity)
                self.add(dot3)
                dot3.add_updater(dot3_fadeout_updater)

        # Hizufügen der Strahlen (optional)
        if rays:
            for i in range(16):
                se = Line(color = RED).rotate(2*PI/16*i).scale(0.15).get_end()
                s1e = Line().rotate(2*PI/16*i).scale(np.random.uniform(0.3, 0.6)).get_end()
                s2e = Line().rotate(2*PI/16*i).scale(np.random.uniform(0.3, 0.6)).get_end()
                s3e = Line().rotate(2*PI/16*i).scale(np.random.uniform(0.3, 0.6)).get_end()
                sun1_ray = DashedLine(se, s1e, color = WHITE, dash_length=0.005)
                sun2_ray = DashedLine(se, s2e, color = RED, dash_length=0.005)
                sun3_ray = DashedLine(se, s3e, color = YELLOW, dash_length=0.005)
                sun1.add(sun1_ray)
                sun2.add(sun2_ray)
                sun3.add(sun3_ray)

        # Hinzufügen der Sonnen
        self.add(sun1, sun2, sun3)

        sun1.move_to(r1[:,0])
        sun2.move_to(r2[:,0])
        sun3.move_to(r3[:,0])
        
        # Hinzufügen der Updater
        sun1.add_updater(sun_updater)
        sun2.add_updater(sun_updater)
        sun3.add_updater(sun_updater)

        # Timeline als ValueTracker
        self.play(timeline.animate.set_value(5), rate_func= linear, run_time = run_time)


# 3D-animation
class TBP_main_3D(ThreeDScene):
    def construct(self):
        timeline = ValueTracker(0)
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        axes = ThreeDAxes()

        # Kreieren der 3 Sonnen
        sun1 = VGroup(Sphere(radius = 0.15, resolution = (16, 16)).set_color(WHITE))
        sun2 = VGroup(Sphere(radius = 0.15, resolution = (16, 16)).set_color(RED))
        sun3 = VGroup(Sphere(radius = 0.15, resolution = (16, 16)).set_color(YELLOW))

        # Positionsiteratoren der 3 Sonnen
        sun1.iter = iter(r1.T[::sun_speed,])
        sun2.iter = iter(r2.T[::sun_speed,])
        sun3.iter = iter(r3.T[::sun_speed,])

        # Updater der Sonnenpositionen
        def sun_updater(sun):
            sun.move_to(next(sun.iter))

        # Schweif-Updater
        def dot1_fadeout_updater(dot1):
            if dot1.counter != fade_length and dot1.counter != 1:
                dot1.fill_opacity -= 1/fade_length
                dot1.set_opacity(dot1.fill_opacity)
                dot1.counter -= 1                
            elif dot1.counter == fade_length:
                dot1.move_to(sun1.get_center())
                dot1.fill_opacity = 1
                dot1.set_opacity(dot1.fill_opacity)
                dot1.counter -= 1
            else:
                dot1.counter = fade_length
                dot1.fill_opacity = 1

        def dot2_fadeout_updater(dot2):
            if dot2.counter != fade_length and dot2.counter != 1:
                dot2.fill_opacity -= 1/fade_length
                dot2.set_opacity(dot2.fill_opacity)
                dot2.counter -= 1                
            elif dot2.counter == fade_length:
                dot2.move_to(sun2.get_center())
                dot2.fill_opacity = 1
                dot2.set_opacity(dot2.fill_opacity)
                dot2.counter -= 1
            else:
                dot2.counter = fade_length
                dot2.fill_opacity = 1           

        def dot3_fadeout_updater(dot3):
            if dot3.counter != fade_length and dot3.counter != 1:
                dot3.fill_opacity -= 1/fade_length
                dot3.set_opacity(dot3.fill_opacity)
                dot3.counter -= 1
            elif dot3.counter == fade_length:
                dot3.move_to(sun3.get_center())
                dot3.fill_opacity = 1
                dot3.set_opacity(dot3.fill_opacity)
                dot3.counter -= 1
            else:
                dot3.counter = fade_length
                dot3.fill_opacity = 1

        # Hinzufügen der Schweife
        if tail:
            for i in range(fade_length):
                dot1 = Dot3D(radius = 0.05).set_color(WHITE)
                dot1.counter = fade_length + i
                dot1.fill_opacity = 0
                dot1.set_opacity(dot1.fill_opacity)
                self.add(dot1)
                dot1.add_updater(dot1_fadeout_updater)

                dot2 = Dot3D(radius = 0.05).set_color(RED)
                dot2.counter = fade_length + i
                dot2.fill_opacity = 0
                dot2.set_opacity(dot2.fill_opacity)
                self.add(dot2)
                dot2.add_updater(dot2_fadeout_updater)

                dot3 = Dot3D(radius = 0.05).set_color(YELLOW)
                dot3.counter = fade_length + i
                dot3.fill_opacity = 0
                dot3.set_opacity(dot3.fill_opacity)
                self.add(dot3)
                dot3.add_updater(dot3_fadeout_updater)
        
        # Hinzufügen der Sonnen
        self.add(axes, sun1, sun2, sun3)

        sun1.move_to(r1[:,0])
        sun2.move_to(r2[:,0])
        sun3.move_to(r3[:,0])
        
        self.begin_ambient_camera_rotation(rate=0.15)

        # Hinzufügen der Updater
        sun1.add_updater(sun_updater)
        sun2.add_updater(sun_updater)
        sun3.add_updater(sun_updater)

        # Timeline als ValueTracker
        self.play(timeline.animate.set_value(5), rate_func= linear, run_time = run_time)