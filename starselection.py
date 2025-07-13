from manimlib import *
from math import pow, log
from addict import Dict
# this like dogepro star selection
LEFT_BUTTON = 1
RIGHT_BUTTON = 4

FRAME_RATE = manim_config.camera.fps

star = Dict(
{
	"m": {
		"Xylos": {
			"mass": 0.148,
			"type": 'M5.5V'
		}
	},
	"k": None,
	"g": None,
	"f": {
		"Fertumi": {
			"mass": 1.48,
			"type": 'F2V'
		},
	},
	"a": None,
	"b": None,
	"o": {
		None: {
			"mass": 20.34,
			"type": 'O9V'
		}
	},
}
)

regular_star_type = list(['o', 'b', 'a', 'f', 'g', 'k', 'm'])
brown_dwarf = list(["l", 't', "y"])

def color_temp(lum: float, radius: float):
	temp = 5778*pow(lum/radius**2,1./4)
	temperature_cached = temp / 100
	if temperature_cached >= 67:
		r = 329.698727446046 * (temperature_cached-60)**-0.133204759227737
		g = 288.122169528293 * (temperature_cached-60)**-0.0755148492418579
		b = 255
	# exceed 255 or smaller than 0 will cause error become rgb must range 0 to 255
		r = min(max(0, r), 255)
		g = min(max(0, g), 255)
		b = min(max(0, b), 255)
	else:
		r = 255    
		g = 99.4708025861262 * log(temperature_cached) - 161.119568166068
		g = min(max(0, g), 255)
		if temperature_cached < 20:
			b = 0
		elif 20 <= temperature_cached <= 67:
			b = 138.517761556144 * log(temperature_cached-10) - 305.044792730681
			b = min(max(0, b), 255)
	return '#%02x%02x%02x' % (int(r),int(g),int(b))


class Stars(Group):
	def __init__(self,lum: float = 1,radius: float = 1,glow_radius: float = 2, real_scale: bool = False, realistic_color: bool = False) -> None:
		Group.__init__(self)
		self.lum = lum
		self.radius = radius
		if realistic_color:
			stars = Dot(radius=radius,fill_color=color_temp(lum, radius))
			star_glow = GlowDot(radius=radius*glow_radius).set_color(color_temp(lum, radius))
		else:
			stars = Dot(radius=radius)
			star_glow = GlowDot(radius=radius*glow_radius).set_color(stars.get_color())
		if real_scale:
			stars.scale(0.0046524726)
			star_glow.scale(0.0046524726)
		self.add(stars,star_glow)

class StarDialog(Group):
	def __init__(self,
				 star: str = None,
				 **kwargs
				 ):
		Group.__init__(self, **kwargs)
		self.top = Rectangle(width = FRAME_WIDTH / 2,
					   fill_opacity=0.5,
					   fill_color=GREY_B,
							height=0.4,stroke_width=0)
		self.window = Rectangle(width = FRAME_WIDTH / 2,
								height= FRAME_HEIGHT / 2 - self.top.get_height(),
								stroke_width= 0,
								fill_opacity=0.5,
								color = GREY_A)
		self.top.next_to(self.window,UP,buff=0)
		self.title= Text(f"Select a Star ({star.capitalize()}-Type)",font_size=30).move_to(self.top)
		self.close = Square(side_length=0.4,stroke_width=0,fill_opacity=0,fill_color=RED_D)
		self.close.add_mouse_press_listner(self.closing)
		self.close.move_to(self.top,RIGHT)
		self.close_cross = VGroup(Line(UL,DR,stroke_width=2)
							,Line(DL,UR,stroke_width=2)).scale(0.5*self.close.get_width()*0.5)
		self.close_cross.move_to(self.close)
		self.star_list = Group()
		super().__init__(self.window,self.title,self.top,self.close,self.star_list,self.close_cross, **kwargs)
		#self.fix_in_frame()
		self.add_updater(lambda mob: None)
		self.top.add_mouse_drag_listner(self.drag)
		
		self.check_star(star)
		
	def check_star(self, sel_type: str):
		if sel_type in (regular_star_type + brown_dwarf):
			star_type = star.get(sel_type)
			if star_type:
				self.window.add_mouse_scroll_listner(self.scroll_list_star)
				for star_names, info in star_type.items():
					star_button = Rectangle(width=FRAME_WIDTH / 2,
									height=1,fill_opacity=0.5,fill_color="#5c666b",stroke_width=0)
					star_text_names = Text(f"{'unnamed' if star_names == None else star_names}",font_size=25).move_to([0,0.325,0])
					detail = Group()
					for parameters, value in info.items():
						if parameters in ["mass"]:
							print(f"{parameters}: {value} M☉")
							detail.add(Text(f"{parameters.capitalize()}",fill_color=PURPLE_A,font_size=15).move_to(star_button,DL).shift(0.1*RIGHT+0.1*UP),
									   Text(f"{value} M☉",fill_color=PURPLE_A,font_size=15).move_to(star_button,DR).shift(0.1*LEFT+0.1*UP))
						elif parameters in ["radius"]:
							print(f"{parameters}: {value} R☉")
							detail.add(Text(f"{parameters}: {value} R☉",fill_color=TEAL_B,font_size=15))
						elif parameters in ["age"]:
							print(f"{parameters}: {value} By")
							detail.add(Text(f"{parameters}: {value} By",font_size=15))
						elif parameters in ["type"]:
							print(f"{parameters}: {value}")
							detail.add(Text(f"{parameters.capitalize()}",font_size=15).move_to(star_button,DL).shift(0.1*RIGHT+0.3*UP),
									   Text(f"{value}",font_size=15).move_to(star_button,DR).shift(0.1*LEFT+0.3*UP))
					self.star_list.add(Group(star_button,star_text_names,detail))
				#detail.arrange(DOWN)
			else:
				self.add(Text(f"NO STAR AVAILABLE",font_size=65,fill_opacity=0.2).rotate(20*DEG))
		else:
			raise(Exception)
		self.star_list.arrange(DOWN,center=False,aligned_edge=ORIGIN,buff=0.2)
		self.star_list.move_to(self.window,UP)
		self.fix_in_frame()
	
	def closing(self, mob, event) -> None:
		self.clear()
		self.top.remove_mouse_drag_listner(self.drag)
		self.close.remove_mouse_press_listner(self.closing)
		self.window.remove_mouse_scroll_listner(self.scroll_list_star)
	
	def drag(self, mob, event: dict[str,np.ndarray]) -> bool:
		d_point = event["d_point"]
		self.shift(d_point)
		return False
	
	def scroll_list_star(self, mob, event: dict[str, np.ndarray]) -> bool:
		offset = event["offset"]
		factor = 10 * offset[1]
		self.star_list.set_y(self.star_list.get_y() + factor)
		return False

class StarSelection(Scene):
	def close_window(self):
		if isinstance(self.mobjects, StarDialog):
			self.remove(self.mobjects)
	drag_to_pan = False
	def construct(self):
		background = SVGMobject("background.svg",fill_opacity=0.05).scale(4)
		background.fix_in_frame()
		star_o = Button(Stars(radius=0.9).set_color("#5b7cff"),on_click=lambda _: self.add(StarDialog(star="o")))
		star_o.shift(LEFT*6)
		star_b = Button(Stars(radius=0.81).set_color("#718fff"),on_click=lambda _: self.add(StarDialog(star="b")))
		star_b.shift(LEFT*3.5)
		star_a = Button(Stars(radius=0.74).set_color("#9ab0ff"),on_click=lambda _: self.add(StarDialog(star="a")))
		star_a.shift(LEFT*1.3)
		star_f = Button(Stars(radius=0.64).set_color("#ebe7ff"),on_click=lambda _: self.add(StarDialog(star="f")))
		star_f.shift(RIGHT*0.7)
		star_g = Button(Stars(radius=0.53).set_color("#ffe8d7"),on_click=lambda _: self.add(StarDialog(star="g")))
		star_g.shift(RIGHT*2.6)
		star_k = Button(Stars(radius=0.44).set_color("#ffac6f"),on_click=lambda _: self.add(StarDialog(star="k")))
		star_k.shift(RIGHT*4.2)
		star_m = Button(Stars(radius=0.32).set_color("#ffa448"),on_click=lambda _: self.add(StarDialog(star="m")))
		star_m.shift(RIGHT*5.6)
		star_names = VGroup(Text(names).next_to(star[0][0], DOWN,buff=0.5) for star, names in zip([star_o, star_b, star_a, star_f, star_g, star_k, star_m], ["O", "B", "A", "F", "G", "K", "M"]))
		self.add(background)
		self.add(star_o,star_b,star_a,star_f,star_g,star_k,star_m, star_names)
		#self.embed(show_animation_progress=True)

class ControlsExample(Scene):
	drag_to_pan = False

	def setup(self):
		self.textbox = Textbox()
		self.checkbox = Checkbox()
		self.color_picker = ColorSliders()
		self.panel = ControlPanel(
			Text("Text", font_size=24), self.textbox, Line(),
		)
		self.add(self.panel)

	def construct(self):
		text = Text("text", font_size=96)

		def text_updater(old_text):
			assert(isinstance(old_text, Text))
			new_text = Text(self.textbox.get_value(), font_size=old_text.font_size)
			# new_text.align_data_and_family(old_text)
			new_text.move_to(old_text)
			if self.checkbox.get_value():
				new_text.set_fill(
					color=self.color_picker.get_picked_color(),
					opacity=self.color_picker.get_picked_opacity()
				)
			else:
				new_text.set_opacity(0)
			old_text.become(new_text)

		text.add_updater(text_updater)

		self.add(MotionMobject(text))

		self.textbox.set_value("Manim")

class Scrollable(Scene):
	drag_to_pan = False
	def construct(self):
		screen = Rectangle(width=FRAME_WIDTH,height=FRAME_HEIGHT)
		window = Rectangle(width=FRAME_WIDTH/2,height=FRAME_HEIGHT/2, fill_color=RED, fill_opacity=0.5)
		some_mobject = VGroup(*[Rectangle(height=0.8,width=FRAME_WIDTH/4, fill_color=GREEN, fill_opacity=0.5) for _ in range(5)])
		text = VGroup(Text("Some Text") for i in range(5))
		some_mobject.arrange(UP)
		text.arrange(UP)
		e = Exclusion(screen,window)
		e.set_color(color=BLACK)
		e.set_fill(opacity=0)
		e.set_stroke(width=0)
		self.add(some_mobject,e,window)
		self.embed()