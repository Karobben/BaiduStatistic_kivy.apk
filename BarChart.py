'''
This script was originally contributed by @CSHF from *Kivy* QQ group in 2020/01/02.
I was simplifed it and added more parameters
'''

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle


class ColorBox(Widget):
    def __init__(self,bg_color, **kw):
        self.bg_color = bg_color
        super().__init__(**kw)
        if self.bg_color != None:
            self.canvas.before.clear()
            with self.canvas.before:
                Color(rgba=self.bg_color)
                Rectangle(pos=self.pos, size=self.size)

    def on_size(self, *args):
        if self.bg_color != None:
            self.canvas.before.clear()
            with self.canvas.before:
                Color(rgba=self.bg_color)
                Rectangle(pos=self.pos, size=self.size)

class MyBoxColor(BoxLayout):
    def __init__(self, **kw):
        if "bg_color" in kw:
            self.bg_color = kw["bg_color"]
            kw.pop("bg_color")
        else:
            self.bg_color = None
        super().__init__(**kw)
        if self.bg_color != None:
            self.canvas.before.clear()
            with self.canvas.before:
                Color(rgba=self.bg_color)
                Rectangle(pos=self.pos, size=self.size)

    def on_size(self, *args):
        if self.bg_color != None:
            self.canvas.before.clear()
            with self.canvas.before:
                Color(rgba=self.bg_color)
                Rectangle(pos=self.pos, size=self.size)

class BarChart(BoxLayout):
	spacing = 10
	List = [1,2,2,3,4,5]
	bg_color = (0,0,0,.3)
	bar_color = (.0, 1, 1, .6)

	def __init__(self, **kw):
	    super().__init__(**kw)
	    self.orientation = "vertical"
	    self.bind(size=self.update)
	    self.bind(pos=self.update)

	def update(self, *args):
	    if self.height == 100 or self.width == 100:
	        return
	    self.clear_widgets()

	    b3 = MyBoxColor(size_hint = (1, 1), bg_color = self.bg_color)

	    b3.spacing = 1
	    Num = 20
	    test = [b3.add_widget(ColorBox(self.bar_color,size_hint = (0.2, (_+.00000001)/max(self.List) )))  for _ in self.List]
	    self.add_widget(b3)
