from kivy.properties import NumericProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout

class Runner(BoxLayout):
    value = NumericProperty(0)
    finished = BooleanProperty(False)
    def __init__(self,
                total = 10, steptime = 1, aoutorepeat= True,
                bcolor = (0.93,0.515,0.7,0.4),
                btext_inprogress='squat',
                **kwargs):
        super().__init__(**kwargs)

        self.total = total
        self.aoutorepeat = aoutorepeat
        self.btext_inprogress = btext_inprogress
        self.animation =(Animation(pos_hint={'top':0.1},duration=steptime/2)
                        + Animation(pos_hint={'top': 1.0}, duration=steptime/2))
        self.animation.on_progress = self.next
        self.btn = Button(size_hint=(1,0.1), pos_hint={'top': 1.0},background_color = bcolor)
        self.add_widget(self.btn)

    def start(self):
        self.value = 0
        self.finished = False
        self.btn.text = self.btext_inprogress
        if self.aoutorepeat:
            self.animation.repeat = True
        self.animation.start(self.btn)

    def next(self, widget, step):
        if step == 1.0:
            self.value += 1
            if self.value >= self.total:
                self.animation.repeat = True
                self.finished = True


