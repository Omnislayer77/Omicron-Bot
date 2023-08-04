from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QPushButton, 
    QLabel, 
    QSlider, 
    QSpinBox, 
    QDoubleSpinBox,
    QGridLayout
)
from PyQt5.QtCore import (
    Qt, 
    QThread, 
    QTimer,
    pyqtSignal
)    
import pynput  
import opensimplex

import time
import random
import math
import os
import sys
import signal


class Bot(QWidget):
    def __init__(self):
        super().__init__()

        opensimplex.seed(random.randint(0,100000))
        self.mouse = pynput.mouse.Controller()
        self.keyboard = pynput.keyboard.Controller()

        key_listener = pynput.keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        key_listener.start()

        mouse_listener = pynput.mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        mouse_listener.start()

        # user variables
        self.line_width = 20
        self.width_variation = 0.05
        self.width_variation_constant = 2
        self.line_offset = 2            
        self.hole_percent = 0.02    
        self.zoom = 1
        
        self.speed = 20
        self.speed_variation = 3
       

        self.time_noise_counter = 0
        self.width_noise_counter = 0
        self.paused = True



        self.initUI()

        self.wall_timer = QTimer(self)
        self.wall_timer.interval = 10 # 10ms
        self.wall_timer.timeout.connect(self.wall)

        self.wall_timer.start()


    def on_release(self, key):
        pass

    def on_press(self, key):
        try:
            if(key.char == 'x'):
                self.paused = not self.paused
        except AttributeError:
            pass
    
    def on_move(self, x, y):
        pass

    def on_click(self, x, y, button, pressed):
        pass

    def on_scroll(self, x, y, dx, dy):
        pass


    def place_pixel(self, origin, x, y):
        self.mouse.position = [
            origin[0] + x * self.zoom,
            origin[1] + y * self.zoom
        ]
        self.mouse.press(pynput.mouse.Button.left)
        time.sleep(1.0 / (self.speed + self.speed_variation * opensimplex.noise2(self.time_noise_counter/3, 0)))
        self.mouse.release(pynput.mouse.Button.left)

    def wall(self):
        if self.paused: # bot is paused, nothing to do
            return
        print("Now walling")
        

        # save where the mouse originally was
        mouseStart = list(self.mouse.position) 

        y = 0 # current line number

        while True:
            self.width_noise_counter += 1
            time.sleep(0.05)
         
            # for varying the width of lines to make the bot look more human-like
            extra_width = int(
                self.line_width * self.width_variation * opensimplex.noise2(self.width_noise_counter/7.0, 0.0) + 
                opensimplex.noise2(self.width_noise_counter/7.0, 0.0) * self.width_variation_constant
            )
            # moves the line left or right relative to the others, to make it more human-like
            line_offset = int(self.line_offset * random.random());
            
            # so that the bot goes back and forth instead of just right
            x_values = range(self.line_width + 2 * extra_width)
            if y % 2:
                x_values = x_values[::-1] # flip the x-values so the bot does the line backwards
            
            for x in x_values:
                if self.paused: # Stop placing pixels, user paused the bot
                    return

                self.time_noise_counter += 1 # increment a noise counter 

                if(random.random() < self.hole_percent): # small chance to skip pixels since humans do that
                    continue
                
                self.place_pixel(mouseStart, x - extra_width + line_offset, y) # place the pixel
            
            y += 1 # move to next line
                
    def initUI(self):
        self.setGeometry(200, 200, 400, 500)
        
        self.setWindowTitle("SovietStalin's Omicron Bot v1.0")

        # Create a label to display the current slider value
        self.top_label = QLabel(
            'How to use: Go to PixelPlace, and press X to start and stop the bot.\n'
            'NOTE: You are responsible for any misuse of this bot on MVP, etc.\n'
            '\n'
            'Line Width - base width of the lines\n'
            'Width Variation Factor - percent the width of lines will vary by\n'
            'Width Variation Constant - variation of line not proportional to Line Width\n'
            'Line Offset - how much lines can be offset from each other\n'
            'Hole Percentage - percent of pixels to skip while drawing\n'
            'Zoom - set this to the zoom on PixelPlace, must be a whole number\n'
            'Speed - speed of the bot in px/s\n'
            'Speed Variation - how much to vary the speed by over time\n'
            '\n'
            "It's best to experiment with these settings on a private canvas or 7 to get a feel\n"
            'for how the bot works\n', 
            self
        )
        
        self.line_width_label = QLabel('Line Width (px)', self)

        self.line_width_slider = QSlider()
        self.line_width_slider.setOrientation(1)  # Vertical orientation
        self.line_width_slider.setRange(0, 100)
        self.line_width_slider.valueChanged.connect(self.onLineWidthSliderChange)
        self.line_width_slider.setValue(self.line_width)

        self.line_width_spin_box = QSpinBox()
        self.line_width_spin_box.setRange(0, 100)
        self.line_width_spin_box.valueChanged.connect(self.onLineWidthSpinBoxChange)
        self.line_width_spin_box.setValue(self.line_width)


        self.width_variation_label = QLabel('Line Width Variation Factor (%)', self)

        self.width_variation_slider = QSlider()
        self.width_variation_slider.setOrientation(1)  # Vertical orientation
        self.width_variation_slider.setRange(0, 100)
        self.width_variation_slider.valueChanged.connect(self.onWidthVariationSliderChange)
        self.width_variation_slider.setValue(int(self.width_variation * 100))

        self.width_variation_spin_box = QSpinBox()
        self.width_variation_spin_box.setRange(0, 100)
        self.width_variation_spin_box.valueChanged.connect(self.onWidthVariationSpinBoxChange)
        self.width_variation_spin_box.setValue(int(self.width_variation * 100))


        self.width_variation_constant_label = QLabel('Line Width Variation Constant (px)', self)

        self.width_variation_constant_slider = QSlider()
        self.width_variation_constant_slider.setOrientation(1)  # Vertical orientation
        self.width_variation_constant_slider.setRange(0, 10)
        self.width_variation_constant_slider.valueChanged.connect(self.onWidthVariationConstantSliderChange)
        self.width_variation_constant_slider.setValue(self.width_variation_constant)

        self.width_variation_constant_spin_box = QSpinBox()
        self.width_variation_constant_spin_box.setRange(0, 10)
        self.width_variation_constant_spin_box.valueChanged.connect(self.onWidthVariationConstantSpinBoxChange)
        self.width_variation_constant_spin_box.setValue(self.width_variation_constant)


        self.line_offset_label = QLabel('Line Offset (px)', self)

        self.line_offset_slider = QSlider()
        self.line_offset_slider.setOrientation(1)  # Vertical orientation
        self.line_offset_slider.setRange(0, 10)
        self.line_offset_slider.valueChanged.connect(self.onLineOffsetSliderChange)
        self.line_offset_slider.setValue(self.line_offset)

        self.line_offset_spin_box = QSpinBox()
        self.line_offset_spin_box.setRange(0, 10)
        self.line_offset_spin_box.valueChanged.connect(self.onLineOffsetSpinBoxChange)
        self.line_offset_spin_box.setValue(self.line_offset)


        self.hole_percent_label = QLabel('Hole Percentage (%)', self)

        self.hole_percent_slider = QSlider()
        self.hole_percent_slider.setOrientation(1)  # Vertical orientation
        self.hole_percent_slider.setRange(0, 100)
        self.hole_percent_slider.valueChanged.connect(self.onHolePercentSliderChange)
        self.hole_percent_slider.setValue(int(100 * self.hole_percent))

        self.hole_percent_spin_box = QSpinBox()
        self.hole_percent_spin_box.setRange(0, 100)
        self.hole_percent_spin_box.valueChanged.connect(self.onHolePercentSpinBoxChange)
        self.hole_percent_spin_box.setValue(int(100 * self.hole_percent))


        self.zoom_label = QLabel('Zoom', self)

        self.zoom_slider = QSlider()
        self.zoom_slider.setOrientation(1)  # Vertical orientation
        self.zoom_slider.setRange(1, 20)
        self.zoom_slider.valueChanged.connect(self.onZoomSliderChange)
        self.zoom_slider.setValue(self.zoom)

        self.zoom_spin_box = QSpinBox()
        self.zoom_spin_box.setRange(1, 20)
        self.zoom_spin_box.valueChanged.connect(self.onZoomSpinBoxChange)
        self.zoom_spin_box.setValue(self.zoom)


        self.speed_label = QLabel('Placement Speed (px/s)', self)

        self.speed_slider = QSlider()
        self.speed_slider.setOrientation(1)  # Vertical orientation
        self.speed_slider.setRange(1, 45)
        self.speed_slider.valueChanged.connect(self.onSpeedSliderChange)
        self.speed_slider.setValue(self.speed)

        self.speed_spin_box = QSpinBox()
        self.speed_spin_box.setRange(1, 45)
        self.speed_spin_box.valueChanged.connect(self.onSpeedSpinBoxChange)
        self.speed_spin_box.setValue(self.speed)


        self.speed_variation_label = QLabel('Placement Speed variation (px/s)', self)

        self.speed_variation_slider = QSlider()
        self.speed_variation_slider.setOrientation(1)  # Vertical orientation
        self.speed_variation_slider.setRange(0, 15)
        self.speed_variation_slider.valueChanged.connect(self.onSpeedVariationSliderChange)
        self.speed_variation_slider.setValue(self.speed_variation)

        self.speed_variation_spin_box = QSpinBox()
        self.speed_variation_spin_box.setRange(0, 15)
        self.speed_variation_spin_box.valueChanged.connect(self.onSpeedVariationSpinBoxChange)
        self.speed_variation_spin_box.setValue(self.speed_variation)

 

        # Layout
        vbox = QGridLayout()
        vbox.addWidget(self.top_label, 0, 0, 1, 3)
        
        vbox.addWidget(self.line_width_label, 1, 0)
        vbox.addWidget(self.line_width_spin_box, 1, 1)
        vbox.addWidget(self.line_width_slider, 1, 2)
        
        vbox.addWidget(self.width_variation_label, 2, 0)
        vbox.addWidget(self.width_variation_spin_box, 2, 1)
        vbox.addWidget(self.width_variation_slider, 2, 2)

        vbox.addWidget(self.width_variation_constant_label, 3, 0)
        vbox.addWidget(self.width_variation_constant_spin_box, 3, 1)
        vbox.addWidget(self.width_variation_constant_slider, 3, 2)

        vbox.addWidget(self.line_offset_label, 4, 0)
        vbox.addWidget(self.line_offset_spin_box, 4, 1)
        vbox.addWidget(self.line_offset_slider, 4, 2)

        vbox.addWidget(self.hole_percent_label, 5, 0)
        vbox.addWidget(self.hole_percent_spin_box, 5, 1)
        vbox.addWidget(self.hole_percent_slider, 5, 2)

        vbox.addWidget(self.zoom_label, 6, 0)
        vbox.addWidget(self.zoom_spin_box, 6, 1)
        vbox.addWidget(self.zoom_slider, 6, 2)

        vbox.addWidget(self.speed_label, 7, 0)
        vbox.addWidget(self.speed_spin_box, 7, 1)
        vbox.addWidget(self.speed_slider, 7, 2)

        vbox.addWidget(self.speed_variation_label, 8, 0)
        vbox.addWidget(self.speed_variation_spin_box, 8, 1)
        vbox.addWidget(self.speed_variation_slider, 8, 2)


        self.setLayout(vbox)
        self.show()


    def onLineWidthSliderChange(self, value):
        self.line_width = value
        if self.line_width_slider.hasFocus():
            self.line_width_spin_box.setValue(value)

    def onLineWidthSpinBoxChange(self, value):
        self.line_width = value
        if self.line_width_spin_box.hasFocus():
            self.line_width_slider.setValue(value)
    
    def onWidthVariationSliderChange(self, value):
        self.width_variation = value / 100.0
        if self.width_variation_slider.hasFocus():
            self.width_variation_spin_box.setValue(value)

    def onWidthVariationSpinBoxChange(self, value):
        self.width_variation = value / 100.0
        if self.width_variation_spin_box.hasFocus():
            self.width_variation_slider.setValue(value)

    def onWidthVariationConstantSliderChange(self, value):
        self.width_variation_constant = value
        if self.width_variation_constant_slider.hasFocus():
            self.width_variation_constant_spin_box.setValue(value)

    def onWidthVariationConstantSpinBoxChange(self, value):
        self.width_variation_constant = value
        if self.width_variation_constant_spin_box.hasFocus():
            self.width_variation_constant_slider.setValue(value)

    def onLineOffsetSliderChange(self, value):
        self.line_offset = value
        if self.line_offset_slider.hasFocus():
            self.line_offset_spin_box.setValue(value)

    def onLineOffsetSpinBoxChange(self, value):
        self.line_offset = value
        if self.line_offset_spin_box.hasFocus():
            self.line_offset_slider.setValue(value)

    def onHolePercentSliderChange(self, value):
        self.hole_percent = value / 100.0
        if self.hole_percent_slider.hasFocus():
            self.hole_percent_spin_box.setValue(value)

    def onHolePercentSpinBoxChange(self, value):
        self.hole_percent = value / 100.0
        if self.hole_percent_spin_box.hasFocus():
            self.hole_percent_slider.setValue(value)

    def onZoomSliderChange(self, value):
        self.zoom = value
        if self.zoom_slider.hasFocus():
            self.zoom_spin_box.setValue(value)

    def onZoomSpinBoxChange(self, value):
        self.zoom = value
        if self.zoom_spin_box.hasFocus():
            self.zoom_slider.setValue(value)

    def onSpeedSliderChange(self, value):
        self.speed = value
        if self.speed_slider.hasFocus():
            self.speed_spin_box.setValue(value)

    def onSpeedSpinBoxChange(self, value):
        self.speed = value
        if self.speed_spin_box.hasFocus():
            self.speed_slider.setValue(value)

    def onSpeedVariationSliderChange(self, value):
        self.speed_variation = value
        if self.speed_variation_slider.hasFocus():
            self.speed_variation_spin_box.setValue(value)

    def onSpeedVariationSpinBoxChange(self, value):
        self.speed_variation= value
        if self.speed_variation_spin_box.hasFocus():
            self.speed_variation_slider.setValue(value)


    def start():
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
        
    bot = Bot()


    sys.exit(app.exec_())
    
