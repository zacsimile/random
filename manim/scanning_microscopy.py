import manim as mn
import numpy as np

from psf import gauss1D, gauss2D, donut1D, donut2D, lorentzian1D, colorize

mn.config.media_width = "75%"
mn.config.verbosity = "WARNING"
mn.config.background_color = mn.BLACK

SCALE = 4
OPACITY = 1
EX_COLOR = mn.YELLOW  # excitation
STED_COLOR = mn.MAROON  # STED beam
FL_COLOR = mn.RED  # fluorophore

class Gaussian(mn.Scene):
    def construct(self):
        
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        gauss = gauss2D(x, y)

        gaussim = mn.ImageMobject(colorize(gauss, c=EX_COLOR)).scale(5)
        self.add(gaussim)

class Donut(mn.Scene):
    def construct(self):
        
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        donut = donut2D(x, y)

        donutim = mn.ImageMobject(colorize(donut, c=EX_COLOR)).scale(5)
        self.add(donutim)
        
class MoveGaussian(mn.Scene):
    def construct(self):
        
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        gauss = gauss2D(x, y)

        line = mn.Line([0, 0, 0], [5, 0, 0])

        gaussim = mn.ImageMobject(colorize(gauss, c=EX_COLOR)).scale(5)
        self.add(gaussim)
        self.play(mn.MoveAlongPath(gaussim, line), run_time=2, rate_func=mn.linear)
        self.wait()

# class ScanSingleFlConfocal(mn.Scene):
#     def construct(self):

#         line = mn.Line([-5, 0, 0], [-1, 0, 0])

#         fl = mn.Dot([-3, 0, 0], color=FL_COLOR)
#         x = np.linspace(-3, 3, 100)
#         y = np.linspace(-3, 3, 100)

#         flgauss = gauss2D(x, y)
#         flgaussim = mn.ImageMobject(colorize(flgauss, c=FL_COLOR)).scale(3)
#         flgaussim.set_x(3)
#         flgaussim.set_opacity(OPACITY)

#         gauss = gauss2D(x, y)
#         gaussim = mn.ImageMobject(colorize(gauss, c=EX_COLOR)).scale(3)
#         gaussim.set_opacity(OPACITY)

#         self.add(fl)
#         self.play(mn.LaggedStart(mn.MoveAlongPath(gaussim, line), 
#                                  mn.Succession(mn.GrowFromCenter(flgaussim, run_time=0.1), 
#                                                mn.ShrinkToCenter(flgaussim, run_time=0.1)),
#                                                lag_ratio=0.4), 
#                   run_time=4, rate_func=mn.linear)

#         self.wait()

class ScanSingleFlConfocal(mn.Scene):
    def construct(self):

        p = mn.ValueTracker(-5)

        flpos = [-3, 0, 0]

        fl = mn.Dot(flpos, color=FL_COLOR)

        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        flgauss = gauss2D(x, y)
        flgaussim = mn.ImageMobject(colorize(flgauss, c=FL_COLOR)).scale(SCALE)
        flgaussim.set_x(np.abs(flpos[0]))
        flgaussim.set_opacity(0)

        gauss = gauss2D(x, y)
        gaussim = mn.ImageMobject(colorize(gauss, c=EX_COLOR)).scale(SCALE)
        gaussim.set_opacity(OPACITY)
        gaussim.set_x(-5)

        gaussim.add_updater(lambda z: z.set_x(p.get_value()))
        flgaussim.add_updater(lambda z: z.set_opacity(OPACITY*np.exp(-8*(p.get_value()-flpos[0])**2)))
        
        psf_text = mn.MathTex("\\sim 200 \\text{ nm}", font_size=40)
        psf_text.next_to(flgaussim, mn.UP)
        d1 = mn.DoubleArrow([np.abs(flpos[0])-1, 0,0], [np.abs(flpos[0])+1, 0, 0], buff=0)

        self.add(gaussim, flgaussim, fl)

        self.play(p.animate.set_value(-1), run_time=2, rate_func=mn.linear)
        self.play(p.animate.set_value(-5), run_time=2, rate_func=mn.linear)
        self.play(p.animate.set_value(-3), run_time=1, rate_func=mn.linear)
        self.play(mn.Write(psf_text), mn.Write(d1))
        self.wait()

class ScanTwoFlFarConfocal(mn.Scene):
    def construct(self):

        p = mn.ValueTracker(-5)

        flpos0 = [-3.5, 0, 0]
        flpos1 = [-2.5, 0, 0]

        fl0 = mn.Dot(flpos0, color=FL_COLOR)
        fl1 = mn.Dot(flpos1, color=FL_COLOR)

        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        flgauss0 = gauss2D(x, y)
        flgaussim0 = mn.ImageMobject(colorize(flgauss0, c=FL_COLOR)).scale(SCALE)
        flgaussim0.set_x(np.abs(flpos1[0]))
        flgaussim0.set_opacity(0)

        flgauss1 = gauss2D(x, y)
        flgaussim1 = mn.ImageMobject(colorize(flgauss1, c=FL_COLOR)).scale(SCALE)
        flgaussim1.set_x(np.abs(flpos0[0]))
        flgaussim1.set_opacity(0)

        gauss = gauss2D(x, y)
        gaussim = mn.ImageMobject(colorize(gauss, c=EX_COLOR)).scale(SCALE)
        gaussim.set_opacity(OPACITY)
        gaussim.set_x(-5)

        gaussim.add_updater(lambda z: z.set_x(p.get_value()))
        flgaussim0.add_updater(lambda z: z.set_opacity(OPACITY*np.exp(-8*(p.get_value()-flpos0[0])**2)))
        flgaussim1.add_updater(lambda z: z.set_opacity(OPACITY*np.exp(-8*(p.get_value()-flpos1[0])**2)))
        
        self.add(gaussim, flgaussim0, flgaussim1, fl0, fl1)

        self.play(p.animate.set_value(-1), run_time=3, rate_func=mn.linear)
        self.play(p.animate.set_value(-5), run_time=3, rate_func=mn.linear)
        self.wait()

class ScanTwoFlCloseConfocal(mn.Scene):
    def construct(self):

        p = mn.ValueTracker(-5)

        flpos0 = [-3.1, 0, 0]
        flpos1 = [-2.9, 0, 0]

        fl0 = mn.Dot(flpos0, color=FL_COLOR)
        fl1 = mn.Dot(flpos1, color=FL_COLOR)

        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        flgauss0 = gauss2D(x, y)
        flgaussim0 = mn.ImageMobject(colorize(flgauss0, c=FL_COLOR)).scale(SCALE)
        flgaussim0.set_x(np.abs(flpos1[0]))
        flgaussim0.set_opacity(0)

        flgauss1 = gauss2D(x, y)
        flgaussim1 = mn.ImageMobject(colorize(flgauss1, c=FL_COLOR)).scale(SCALE)
        flgaussim1.set_x(np.abs(flpos0[0]))
        flgaussim1.set_opacity(0)

        gauss = gauss2D(x, y)
        gaussim = mn.ImageMobject(colorize(gauss, c=EX_COLOR)).scale(SCALE)
        gaussim.set_opacity(OPACITY)
        gaussim.set_x(-5)

        gaussim.add_updater(lambda z: z.set_x(p.get_value()))
        flgaussim0.add_updater(lambda z: z.set_opacity(OPACITY*np.exp(-8*(p.get_value()-flpos0[0])**2)))
        flgaussim1.add_updater(lambda z: z.set_opacity(OPACITY*np.exp(-8*(p.get_value()-flpos1[0])**2)))
        
        self.add(gaussim, flgaussim0, flgaussim1, fl0, fl1)

        self.play(p.animate.set_value(-1), run_time=3, rate_func=mn.linear)
        self.play(p.animate.set_value(-5), run_time=3, rate_func=mn.linear)
        self.wait()

class ScanTwoFlCloseConfocalSMLM(mn.Scene):
    def construct(self):

        p = mn.ValueTracker(-5)
        op0 = mn.ValueTracker(0)
        op1 = mn.ValueTracker(0)

        flpos0 = [-3.1, 0, 0]
        flpos1 = [-2.9, 0, 0]

        fl0 = mn.Dot(flpos0, color=FL_COLOR)
        fl1 = mn.Dot(flpos1, color=FL_COLOR)

        FL_ACTIVE_COLOR = mn.PINK

        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        flgauss0 = gauss2D(x, y)
        flgaussim0 = mn.ImageMobject(colorize(flgauss0, c=FL_COLOR)).scale(SCALE)
        flgaussim0.set_x(np.abs(flpos1[0]))
        flgaussim0.set_opacity(op0.get_value())

        flgauss1 = gauss2D(x, y)
        flgaussim1 = mn.ImageMobject(colorize(flgauss1, c=FL_COLOR)).scale(SCALE)
        flgaussim1.set_x(np.abs(flpos0[0]))
        flgaussim1.set_opacity(op1.get_value())

        gauss = gauss2D(x, y)
        gaussim = mn.ImageMobject(colorize(gauss, c=EX_COLOR)).scale(SCALE)
        gaussim.set_opacity(OPACITY)
        gaussim.set_x(-5)

        gaussim.add_updater(lambda z: z.set_x(p.get_value()))
        flgaussim0.add_updater(lambda z: z.set_opacity(op0.get_value()))
        flgaussim1.add_updater(lambda z: z.set_opacity(op1.get_value()))
        # flgaussim0.add_updater(lambda z: z.set_opacity(OPACITY*np.exp(-8*(p.get_value()-flpos0[0])**2)))
        # flgaussim1.add_updater(lambda z: z.set_opacity(OPACITY*np.exp(-8*(p.get_value()-flpos1[0])**2)))
        
        self.add(gaussim, flgaussim0, flgaussim1, fl0, fl1)

        self.play(p.animate.set_value(-3), run_time=2, rate_func=mn.linear)
        self.play(op0.animate.set_value(1), fl0.animate.set_color(FL_ACTIVE_COLOR), run_time=1, rate_func=mn.linear)
        self.play(op0.animate.set_value(0), fl0.animate.set_color(FL_COLOR), run_time=1, rate_func=mn.linear)
        self.play(op1.animate.set_value(1), fl1.animate.set_color(FL_ACTIVE_COLOR), run_time=1, rate_func=mn.linear)
        self.play(op1.animate.set_value(0), fl1.animate.set_color(FL_COLOR), run_time=1, rate_func=mn.linear)
        self.play(op0.animate.set_value(1), fl0.animate.set_color(FL_ACTIVE_COLOR), run_time=1, rate_func=mn.linear)
        self.play(op0.animate.set_value(0), fl0.animate.set_color(FL_COLOR), run_time=1, rate_func=mn.linear)
        self.play(op0.animate.set_value(1), fl0.animate.set_color(FL_ACTIVE_COLOR), run_time=0.5, rate_func=mn.linear)
        self.play(op0.animate.set_value(0), fl0.animate.set_color(FL_COLOR), run_time=0.5, rate_func=mn.linear)
        self.play(op1.animate.set_value(1), fl1.animate.set_color(FL_ACTIVE_COLOR), run_time=1, rate_func=mn.linear)
        self.play(op1.animate.set_value(0), fl1.animate.set_color(FL_COLOR), run_time=1, rate_func=mn.linear)
        self.play(op1.animate.set_value(1), fl1.animate.set_color(FL_ACTIVE_COLOR), run_time=1, rate_func=mn.linear)
        self.play(op1.animate.set_value(0), fl1.animate.set_color(FL_COLOR), run_time=1, rate_func=mn.linear)
        self.play(op1.animate.set_value(1), fl1.animate.set_color(FL_ACTIVE_COLOR), run_time=0.5, rate_func=mn.linear)
        self.play(op1.animate.set_value(0), fl1.animate.set_color(FL_COLOR), run_time=1, rate_func=mn.linear)
        self.play(op0.animate.set_value(0), fl0.animate.set_color(FL_COLOR), run_time=1, rate_func=mn.linear)
        self.play(op0.animate.set_value(1), fl0.animate.set_color(FL_ACTIVE_COLOR), run_time=0.5, rate_func=mn.linear)
        self.play(op0.animate.set_value(0), fl0.animate.set_color(FL_COLOR), run_time=1, rate_func=mn.linear)
        self.wait()

class ScanSingleFlSTED(mn.Scene):
    def construct(self):

        p = mn.ValueTracker(-5)

        flpos = [-3, 0, 0]

        fl = mn.Dot(flpos, color=FL_COLOR)

        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        
        gauss = gauss2D(x, y)
        flgaussim = mn.ImageMobject(colorize(gauss, c=FL_COLOR)).scale(SCALE)
        flgaussim.set_x(np.abs(flpos[0]))
        flgaussim.set_opacity(0)

        flstedim = mn.ImageMobject(colorize(gauss, c=FL_COLOR)).scale(SCALE/3)
        flstedim.set_x(np.abs(flpos[0]))
        flstedim.set_opacity(0)

        gaussim = mn.ImageMobject(colorize(gauss, c=EX_COLOR)).scale(SCALE)
        gaussim.set_opacity(OPACITY)
        gaussim.set_x(-5)

        donut = donut2D(x, y)
        gauss05 = gauss2D(x, y, sig=0.5)
        donutim = mn.ImageMobject(np.maximum(colorize(gauss05, c=EX_COLOR), colorize(donut, c=STED_COLOR))).scale(SCALE)
        donutim.set_opacity(0)

        gaussim.add_updater(lambda z: z.set_x(p.get_value()))
        donutim.add_updater(lambda z: z.set_x(p.get_value()))
        flgaussim.add_updater(lambda z: z.set_opacity(OPACITY*np.exp(-8*(p.get_value()-flpos[0])**2)))

        # lorentzian
        gamma = OPACITY
        flstedim.add_updater(lambda z: z.set_opacity(OPACITY/(np.pi*gamma*(1+((p.get_value()-flpos[0])/gamma)**2))))
        
        psf_text = mn.MathTex("30 \\sim 50 \\text{ nm}", font_size=40)
        psf_text.next_to(flgaussim, mn.UP)
        d1 = mn.DoubleArrow([np.abs(flpos[0])-0.25, 0,0], [np.abs(flpos[0])+0.25, 0, 0], buff=0)

        self.add(gaussim, flgaussim, donutim, fl)

        self.play(p.animate.set_value(flpos[0]), run_time=2, rate_func=mn.linear)
        self.play(donutim.animate.set_opacity(OPACITY), flgaussim.animate.scale(0.5))
        self.play(p.animate.set_value(-1), run_time=2, rate_func=mn.linear)
        self.play(p.animate.set_value(-5), run_time=2, rate_func=mn.linear)
        self.play(p.animate.set_value(-3), run_time=1, rate_func=mn.linear)
        self.play(mn.Write(psf_text), mn.Write(d1))
        self.wait()


# class ScanTwoFlCloseSTED(mn.Scene):
#     def construct(self):

#         p = mn.ValueTracker(-5)

#         flpos0 = [-3.1, 0, 0]
#         flpos1 = [-2.9, 0, 0]

#         fl0 = mn.Dot(flpos0, color=FL_COLOR)
#         fl1 = mn.Dot(flpos1, color=FL_COLOR)

#         x = np.linspace(-3, 3, 100)
#         y = np.linspace(-3, 3, 100)
#         flgauss0 = gauss2D(x, y)
#         flgaussim0 = mn.ImageMobject(colorize(flgauss0, c=FL_COLOR)).scale(1.5)
#         flgaussim0.set_x(np.abs(flpos1[0]))
#         flgaussim0.set_opacity(0)

#         flgauss1 = gauss2D(x, y)
#         flgaussim1 = mn.ImageMobject(colorize(flgauss1, c=FL_COLOR)).scale(1.5)
#         flgaussim1.set_x(np.abs(flpos0[0]))
#         flgaussim1.set_opacity(0)

#         donut = donut2D(x, y)
#         gauss05 = gauss2D(x, y, sig=OPACITY)
#         donutim = mn.ImageMobject(np.maximum(colorize(gauss05, c=EX_COLOR), colorize(donut, c=STED_COLOR))).scale(3)
#         donutim.set_opacity(OPACITY)
#         donutim.set_x(-5)

#         donutim.add_updater(lambda z: z.set_x(p.get_value()))
#         gamma = 0.02
#         flgaussim0.add_updater(lambda z: z.set_opacity(np.minimum(OPACITY/(np.pi*gamma*(1+((p.get_value()-flpos0[0])/gamma)**2)),OPACITY)))
#         flgaussim1.add_updater(lambda z: z.set_opacity(np.minimum(OPACITY/(np.pi*gamma*(1+((p.get_value()-flpos1[0])/gamma)**2)),OPACITY)))
        
#         self.add(donutim, flgaussim0, flgaussim1, fl0, fl1)

#         self.play(p.animate.set_value(-1), run_time=3, rate_func=mn.linear)
#         self.play(p.animate.set_value(-5), run_time=3, rate_func=mn.linear)
#         self.wait()

class ScanTwoFlCloseSTED(mn.Scene):
    def construct(self):

        leftscan, rightscan = -4, -2

        p = mn.ValueTracker(leftscan)

        flpos0 = [-3.1, 0, 0]
        flpos1 = [-2.9, 0, 0]

        fl0 = mn.Dot(flpos0, color=FL_COLOR)
        fl1 = mn.Dot(flpos1, color=FL_COLOR)

        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        gauss = gauss2D(x, y)

        flgaussim0 = mn.ImageMobject(colorize(gauss, c=FL_COLOR)).scale(SCALE)
        flgaussim0.set_x(np.abs(flpos1[0]))
        flgaussim0.set_opacity(0)

        flgaussim1 = mn.ImageMobject(colorize(gauss, c=FL_COLOR)).scale(SCALE)
        flgaussim1.set_x(np.abs(flpos0[0]))
        flgaussim1.set_opacity(0)

        gaussim = mn.ImageMobject(colorize(gauss, c=EX_COLOR)).scale(SCALE)
        gaussim.set_opacity(OPACITY)
        gaussim.set_x(leftscan)

        donut = np.minimum(donut2D(x, y, a=1), 1)
        gauss05 = gauss2D(x, y, sig=0.3)
        donutim = mn.ImageMobject(np.maximum(colorize(gauss05, c=EX_COLOR), colorize(donut, c=STED_COLOR))).scale(SCALE)
        donutim.set_opacity(0)
        donutim.set_x(leftscan)

        gaussim.add_updater(lambda z: z.set_x(p.get_value()))
        donutim.add_updater(lambda z: z.set_x(p.get_value()))
        flgaussim0.add_updater(lambda z: z.set_opacity(OPACITY*np.exp(-8*(p.get_value()-flpos0[0])**2)))
        flgaussim1.add_updater(lambda z: z.set_opacity(OPACITY*np.exp(-8*(p.get_value()-flpos1[0])**2)))
        
        self.add(gaussim, flgaussim0, flgaussim1, fl0, fl1)

        self.play(p.animate.set_value(flpos0[0]), run_time=1, rate_func=mn.linear)
        flgaussim0.clear_updaters()
        flgaussim1.clear_updaters()
        self.play(donutim.animate.set_opacity(OPACITY), 
                  flgaussim1.animate.set_opacity(0), 
                  flgaussim0.animate.scale(0.3), 
                  run_time=3, rate_func=mn.linear)
        self.wait(OPACITY)
        flgaussim1.scale(0.3)
        gamma = 0.02
        flgaussim0.add_updater(lambda z: z.set_opacity(np.minimum(OPACITY/(np.pi*gamma*(1+((p.get_value()-flpos0[0])/gamma)**2)),OPACITY)))
        flgaussim1.add_updater(lambda z: z.set_opacity(np.minimum(OPACITY/(np.pi*gamma*(1+((p.get_value()-flpos1[0])/gamma)**2)),OPACITY)))
        self.play(p.animate.set_value(rightscan), run_time=3, rate_func=mn.linear)
        self.play(p.animate.set_value(leftscan), run_time=3, rate_func=mn.linear)
        self.play(p.animate.set_value(flpos1[0]), run_time=3, rate_func=mn.linear)

        psf_text = mn.MathTex("30 \\sim 50 \\text{ nm}", font_size=40)
        psf_text.next_to(flgaussim1, mn.UP)
        d1 = mn.DoubleArrow([np.abs(flpos0[0])-0.2, 0,0], [np.abs(flpos0[0])+0.2, 0, 0], buff=0)
        self.play(mn.Write(psf_text), mn.Write(d1))
        self.wait()

class SaturateTwoFlCloseSTED(mn.Scene):
    def construct(self):

        p = mn.ValueTracker(-2.9)

        flpos0 = [-3.1, 0, 0]
        flpos1 = [-2.9, 0, 0]

        fl0 = mn.Dot(flpos0, color=FL_COLOR)
        fl1 = mn.Dot(flpos1, color=FL_COLOR)

        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        gauss = gauss2D(x, y)

        flgaussim0 = mn.ImageMobject(colorize(gauss, c=FL_COLOR)).scale(SCALE/3)
        flgaussim0.set_x(np.abs(flpos1[0]))
        flgaussim0.set_opacity(0)

        flgaussim1 = mn.ImageMobject(colorize(gauss, c=FL_COLOR)).scale(SCALE/3)
        flgaussim1.set_x(np.abs(flpos0[0]))
        flgaussim1.set_opacity(0)

        donut = donut2D(x, y)
        gauss05 = gauss2D(x, y, sig=0.5)
        donutim05 = mn.ImageMobject(np.maximum(colorize(gauss05, c=EX_COLOR), colorize(donut, c=STED_COLOR))).scale(SCALE)
        donutim05.set_opacity(OPACITY)
        donutim05.set_x(-5)

        donut02 = np.minimum(donut2D(x, y, a=1, b=0.1), 1)
        gauss02 = gauss2D(x, y, sig=0.3)
        donutim07 = mn.ImageMobject(np.maximum(colorize(gauss02, c=EX_COLOR), colorize(donut02, c=STED_COLOR))).scale(SCALE)
        donutim07.set_opacity(0)
        donutim07.set_x(-5)

        donut022 = np.minimum(donut2D(x, y, a=2, b=0.1), 1)
        gauss022 = gauss2D(x, y, sig=0.2)
        donutim072 = mn.ImageMobject(np.maximum(colorize(gauss022, c=EX_COLOR), colorize(donut022, c=STED_COLOR))).scale(SCALE)
        donutim072.set_opacity(0)
        donutim072.set_x(-5)

        donut0222 = np.minimum(donut2D(x, y, a=4, b=0.1), 1)
        gauss0222 = gauss2D(x, y, sig=0.1)
        donutim0722 = mn.ImageMobject(np.maximum(colorize(gauss0222, c=EX_COLOR), colorize(donut0222, c=STED_COLOR))).scale(SCALE)
        donutim0722.set_opacity(0)
        donutim0722.set_x(-5)

        donutim05.add_updater(lambda z: z.set_x(p.get_value()))
        donutim07.add_updater(lambda z: z.set_x(p.get_value()))
        donutim072.add_updater(lambda z: z.set_x(p.get_value()))
        donutim0722.add_updater(lambda z: z.set_x(p.get_value()))
        flgaussim0.add_updater(lambda z: z.set_opacity(OPACITY*np.exp(-8*(p.get_value()-flpos0[0])**2)))
        flgaussim1.add_updater(lambda z: z.set_opacity(OPACITY*np.exp(-8*(p.get_value()-flpos1[0])**2)))
        
        self.add(donutim05, flgaussim0, flgaussim1, fl0, fl1)

        gamma = 0.02
        flgaussim0.add_updater(lambda z: z.set_opacity(np.minimum(OPACITY/(np.pi*gamma*(1+((p.get_value()-flpos0[0])/gamma)**2)),OPACITY)))
        flgaussim1.add_updater(lambda z: z.set_opacity(np.minimum(OPACITY/(np.pi*gamma*(1+((p.get_value()-flpos1[0])/gamma)**2)),OPACITY)))
        self.play(donutim05.animate.set_opacity(0),
                  donutim07.animate.set_opacity(OPACITY), 
                  flgaussim1.animate.scale(0.75),
                  run_time=1, rate_func=mn.linear)
        self.wait(1)
        self.play(donutim07.animate.set_opacity(0),
                  donutim072.animate.set_opacity(OPACITY), 
                  flgaussim1.animate.scale(0.75),
                  run_time=1, rate_func=mn.linear)
        self.wait(1)
        flgaussim1.clear_updaters()
        self.play(donutim072.animate.set_opacity(0),
                  donutim0722.animate.set_opacity(OPACITY), 
                  flgaussim1.animate.set_opacity(0),
                  run_time=1, rate_func=mn.linear)
        self.wait()

class PlotDonut(mn.Scene):
    def construct(self):
        ax = mn.Axes(
            x_range=[-3,3], y_range=[0, 3, OPACITY], axis_config={"include_tip": False},
            x_length=3, y_length=3,
        )
        ax.set_x(3)
        labels = ax.get_axis_labels(x_label="x (nm)", y_label="amplitude")

        a = mn.ValueTracker(0)

        graph = mn.always_redraw(lambda: ax.plot(lambda x: donut1D(x, a=a.get_value()), color=STED_COLOR))

        self.add(ax, labels, graph)
        self.play(a.animate.set_value(2))
        self.wait()

class PlotDonutSTED(mn.Scene):
    def construct(self):

        p = mn.ValueTracker(-2.9)

        flpos0 = [-3.1, 0, 0]
        flpos1 = [-2.9, 0, 0]

        fl0 = mn.Dot(flpos0, color=FL_COLOR)
        fl1 = mn.Dot(flpos1, color=FL_COLOR)

        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)

        b = mn.ValueTracker(0.1)
        a = mn.ValueTracker(0)
        a2 = mn.ValueTracker(3*np.pi/2)
        g = mn.ValueTracker(1)

        gauss = np.minimum(gauss2D(x, y, b=b.get_value()), 1)

        gaussim = mn.ImageMobject(colorize(gauss, c=EX_COLOR)).scale(SCALE)
        gaussim.set_opacity(OPACITY)
        gaussim.set_x(p.get_value())

        donut02 = np.minimum(donut2D(x, y, a=1, b=0.1), 1)
        gauss02 = gauss2D(x, y, sig=0.3)
        donutim07 = mn.ImageMobject(np.maximum(colorize(gauss02, c=EX_COLOR), colorize(donut02, c=STED_COLOR))).scale(SCALE)
        donutim07.set_opacity(0)
        donutim07.set_x(p.get_value())

        donut022 = np.minimum(donut2D(x, y, a=2, b=0.1), 1)
        gauss022 = gauss2D(x, y, sig=0.2)
        donutim072 = mn.ImageMobject(np.maximum(colorize(gauss022, c=EX_COLOR), colorize(donut022, c=STED_COLOR))).scale(SCALE)
        donutim072.set_opacity(0)
        donutim072.set_x(p.get_value())

        donut0222 = np.minimum(donut2D(x, y, a=4, b=0.1), 1)
        gauss0222 = gauss2D(x, y, sig=0.1)
        donutim0722 = mn.ImageMobject(np.maximum(colorize(gauss0222, c=EX_COLOR), colorize(donut0222, c=STED_COLOR))).scale(SCALE)
        donutim0722.set_opacity(0)
        donutim0722.set_x(p.get_value())

        donut02222 = np.minimum(donut2D(x, y, a=4, b=0), 1)
        donutim07222 = mn.ImageMobject(np.maximum(colorize(gauss0222, c=EX_COLOR), colorize(donut02222, c=STED_COLOR))).scale(SCALE)
        donutim07222.set_opacity(0)
        donutim07222.set_x(p.get_value())

        donutim07.add_updater(lambda z: z.set_x(p.get_value()))
        donutim072.add_updater(lambda z: z.set_x(p.get_value()))
        donutim0722.add_updater(lambda z: z.set_x(p.get_value()))
        donutim07222.add_updater(lambda z: z.set_x(p.get_value()))
        
        ax = mn.Axes(
            x_range=[-4,4], y_range=[0, 5], axis_config={"include_tip": False},
            x_length=6, y_length=4,
        )
        ax.set_x(3)
        axloc = ax.get_center()
        labels = ax.get_axis_labels(x_label="x (nm)", y_label="amplitude").scale(0.75)

        graph_gauss = mn.always_redraw(lambda: ax.plot(lambda x: gauss1D(x, a=4, b=b.get_value()), color=EX_COLOR))
        graph_gauss_em = ax.plot(lambda x: 4/2*(gauss1D(x, mu=0, b=b.get_value()) + gauss1D(x, mu=-0.4, b=b.get_value())), color=mn.GREEN)
        graph = mn.always_redraw(lambda: ax.plot(lambda x: donut1D(x, a=a.get_value(), b=b.get_value()), color=STED_COLOR))
        graph_lorentzian = mn.always_redraw(lambda: ax.plot(lambda x: lorentzian1D(x, a=a2.get_value(), b=0, gamma=g.get_value()), color=mn.GREEN))

        fl0graph = mn.Dot(ax.coords_to_point(0, 0.4), color=FL_COLOR)
        fl1graph = mn.Dot(ax.coords_to_point(-0.4, 0.4), color=FL_COLOR)

        line = mn.DashedLine([p.get_value()-1.5,0,0], [p.get_value()+1.5,0,0]).set_color(mn.PINK)

        top = mn.DashedLine([axloc[0]-3.25,axloc[1]+3,0], [axloc[0]+3.5,axloc[1]+3,0]).set_color(mn.PINK)
        right = mn.DashedLine([axloc[0]+3.5,axloc[1]-2.5,0], [axloc[0]+3.5,axloc[1]+3,0]).set_color(mn.PINK)
        bottom = mn.DashedLine([axloc[0]-3.25,axloc[1]-2.5,0], [axloc[0]+3.5,axloc[1]-2.5,0]).set_color(mn.PINK)
        left = mn.DashedLine([axloc[0]-3.25,axloc[1]+3,0], [axloc[0]-3.25,axloc[1]-2.5,0]).set_color(mn.PINK)
        
        self.add(gaussim, fl0, fl1)#, ax, labels, graph_gauss, graph)
        self.play(mn.Create(labels), mn.FadeIn(top, right, bottom, left, graph, graph_gauss, graph_gauss_em, ax, fl0graph, fl1graph, line))
        line.set_z_index(1000)
        self.wait(2)
        self.play(gaussim.animate.set_opacity(0),
                  donutim07.animate.set_opacity(OPACITY),
                  a.animate.set_value(1),
                  mn.Transform(graph_gauss_em, graph_lorentzian, replace_mobject_with_target_in_scene=True),
                  run_time=1, rate_func=mn.linear)
        self.wait(2)
        self.play(donutim07.animate.set_opacity(0),
                  donutim072.animate.set_opacity(OPACITY), 
                  a.animate.set_value(2),
                  a2.animate.set_value(2*np.pi/2),
                  run_time=1, rate_func=mn.linear)
        self.wait(2)
        self.play(donutim072.animate.set_opacity(0),
                  donutim0722.animate.set_opacity(OPACITY), 
                  a.animate.set_value(4),
                  a2.animate.set_value(0),
                  run_time=1, rate_func=mn.linear)
        self.wait(2)
        self.play(donutim07222.animate.set_opacity(OPACITY),
                  donutim0722.animate.set_opacity(0), 
                  b.animate.set_value(0),
                  a2.animate.set_value(4*np.pi/2),
                  run_time=1, rate_func=mn.linear)
        self.wait(2)
        self.play(donutim07222.animate.set_opacity(0),
                  donutim07.animate.set_opacity(OPACITY),
                  a.animate.set_value(1),
                  a2.animate.set_value(2*4*np.pi/2),
                  g.animate.set_value(2),
                  run_time=1, rate_func=mn.linear)
        self.wait(2)
        self.play(donutim07222.animate.set_opacity(OPACITY),
                  donutim07.animate.set_opacity(0), 
                  a.animate.set_value(4),
                  a2.animate.set_value(4*np.pi/2),
                  g.animate.set_value(1),
                  run_time=1, rate_func=mn.linear)
        self.wait(2)
        self.wait()