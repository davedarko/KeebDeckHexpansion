import app
import math
from machine import PWM, Pin
from system.hexpansion.config import HexpansionConfig

class LEDTestApp(app.App):
    def __init__(self):
        
        self.hexpansion_config = HexpansionConfig(4)
        self.pins = {}
        self.step = 0
        self.toggle = 0
        self.pwmval = 0

        # eGPIO pins
        self.pins["ls_1"] = self.hexpansion_config.ls_pin[0]

        # GPIO pins
        self.pins["hs_1"] = self.hexpansion_config.pin[0]
        self.pins["hs_2"] = self.hexpansion_config.pin[1]

        # All pins start in inputs mode. Initialize them as follows:
        self.pins["hs_1"].init(self.pins["hs_1"].OUT)

        # Only LS pins support the PWM function directly.
        self.pins["ls_1"].init(self.pins["ls_1"].PWM)

        self.pwm = PWM(self.pins["hs_2"], freq=120, duty_u16=8192); # Pin(14)

    def update(self, delta):
        self.step = self.step + delta
        if self.step >= 200:
            self.step = 0
            self.pwmval = (self.pwmval+1) * 2 - 1
            if self.pwmval >= 256:
                self.pwmval = 0

            self._toggle_pins()

    def _toggle_pins(self):
        self.pins["ls_1"].duty(self.pwmval)

        if self.pins["hs_1"].value() == 1:
            self.pins["hs_1"].off()
            self.pwm.duty_u16(32768)
            self.toggle = 1
        else:
            self.pins["hs_1"].on()
            self.pwm.duty_u16(8192)
            self.toggle = 0

    def draw(self, ctx):
        ctx.save()
        if self.toggle:
            ctx.rgb(0.9, 0.6, 0.2).rectangle(-120, -120, 240, 240).fill()
        else:
            ctx.rgb(0.2, 0.9, 0.6).rectangle(-120, -120, 240, 240).fill()
        ctx.restore()


__app_export__ = LEDTestApp