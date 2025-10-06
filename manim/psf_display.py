import manim as mn
import numpy as np

from psf import gauss1D, gauss2D, donut2D, colorize

mn.config.media_width = "75%"
mn.config.verbosity = "WARNING"
mn.config.background_color = mn.BLACK

FL_COLOR = mn.RED  # fluorophore

class PsfGallery(mn.Scene):
    def construct(self):
        
        # opposite of mn.BLUE
        # bc = mn.ManimColor("#A73B22")

        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)

        gauss = gauss2D(x, y)
        donut = donut2D(x, y)

        gaussim = mn.ImageMobject(colorize(gauss, c=mn.YELLOW)).scale(5)
        donutim = mn.ImageMobject(colorize(donut, c=mn.YELLOW)).scale(5)

        # STED excitation + depletion
        gaussim2 = mn.ImageMobject(np.maximum(colorize(gauss, c=mn.YELLOW), colorize(donut, c=mn.MAROON))).scale(5)
        # donutim2 = mn.ImageMobject(colorize(donut, c=mn.BLUE), invert=True).scale(5)

        gaussim.set_x(4)
        donutim.set_x(-4)

        gaussim2.set_x(0)
        # donutim2.set_x(0)

        # op = 0.8
        gaussim.set_opacity(1)
        donutim.set_opacity(1)
        gaussim2.set_opacity(1)
        # donutim2.set_opacity(0.7)
        
        self.add(gaussim, donutim, gaussim2) #, donutim2)

class PsfFit(mn.Scene):
    def construct(self):
        
        # opposite of mn.BLUE
        # bc = mn.ManimColor("#A73B22")

        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)

        p = -2.9

        gauss = gauss2D(x, y)

        gaussim = mn.ImageMobject(colorize(gauss, c=FL_COLOR)).scale(5)

        flpos = [p, 0, 0]

        fl0 = mn.Dot(flpos, color=FL_COLOR)

        line = mn.DashedLine([p-1.5,0,0], [p+1.5,0,0]).set_color(mn.PINK)

        ax = mn.Axes(
            x_range=[-4,4], y_range=[0, 5], axis_config={"include_tip": False},
            x_length=6, y_length=4,
        )
        ax.set_x(3)
        axloc = ax.get_center()
        labels = ax.get_axis_labels(x_label="x (nm)", y_label="amplitude").scale(0.75)

        graph_gauss = mn.always_redraw(lambda: ax.plot(lambda x: gauss1D(x, a=4, b=0), color=FL_COLOR))
        fl0graph = mn.Dot(ax.coords_to_point(0, 0.4), color=FL_COLOR)

        top = mn.DashedLine([axloc[0]-3.25,axloc[1]+3,0], [axloc[0]+3.5,axloc[1]+3,0]).set_color(mn.PINK)
        right = mn.DashedLine([axloc[0]+3.5,axloc[1]-2.5,0], [axloc[0]+3.5,axloc[1]+3,0]).set_color(mn.PINK)
        bottom = mn.DashedLine([axloc[0]-3.25,axloc[1]-2.5,0], [axloc[0]+3.5,axloc[1]-2.5,0]).set_color(mn.PINK)
        left = mn.DashedLine([axloc[0]-3.25,axloc[1]+3,0], [axloc[0]-3.25,axloc[1]-2.5,0]).set_color(mn.PINK)

        d1 = mn.DoubleArrow(ax.coords_to_point(-1.1, 2), ax.coords_to_point(1.1, 2), buff=0)
        psf_text = mn.MathTex("R \\sim 200 \\text{ nm}", font_size=30)
        psf_text.next_to(d1, mn.LEFT)

        d2 = mn.DoubleArrow(ax.coords_to_point(0, 3), ax.coords_to_point(-0.7, 3), buff=0)
        loc_text = mn.MathTex("\\sigma_{PSF} \\sim 75 \\text{ nm}", font_size=30)
        loc_text.next_to(d2, mn.LEFT)

        gaussim.set_x(p)

        gaussim.set_opacity(1)
        
        self.add(gaussim, fl0)
        self.play(mn.FadeIn(line, graph_gauss, fl0graph, ax, labels, top, right, bottom, left), run_time=0.1, rate_func=mn.linear)
        self.play(mn.FadeIn(d1, psf_text), run_time=0.1, rate_func=mn.linear)
        self.play(mn.FadeIn(d2, loc_text), run_time=0.1, rate_func=mn.linear)


