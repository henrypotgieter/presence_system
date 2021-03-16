# Punchclock controller code
#
# By: Henry Potgieter
#
# Purpose of this script is to provide a control interface for the RPi
# punchclock box, allows for easy time tracking and setting of a presence
# device via a simple web API to notify family members of current status/
# availability
#
# Written for Python v2

import RPi.GPIO as GPIO
import requests
from time import sleep

# Define static input and output assignments
IN_BUSY = 15
IN_RED = 2
IN_GREEN = 3
IN_BLUE = 22
IN_YELLOW = 14
OUT_RED = 4
OUT_GREEN = 17
OUT_BLUE = 27
OUT_YELLOW = 18
OUT_RGB_RED = 13
OUT_RGB_GREEN = 12
OUT_RGB_BLUE = 19

# Define IP of notifier/presence host and default http timeout
NOTIFIER_IP = "0.0.0.0"
WEB_TIMEOUT = 3

# Define file names to use for state tracking
LED_STATE = "/var/punchclock.led.state"
DND_STATE = "/var/punchclock.dnd.state"

# Setup various GPIO interfaces
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(OUT_RED, GPIO.OUT)
GPIO.setup(OUT_GREEN, GPIO.OUT)
GPIO.setup(OUT_BLUE, GPIO.OUT)
GPIO.setup(OUT_YELLOW, GPIO.OUT)
GPIO.setup(IN_RED, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IN_GREEN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IN_BLUE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IN_YELLOW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IN_BUSY, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(OUT_RGB_RED, GPIO.OUT)
GPIO.setup(OUT_RGB_GREEN, GPIO.OUT)
GPIO.setup(OUT_RGB_BLUE, GPIO.OUT)

# Define RGB LED PWM settings
pwm_red = GPIO.PWM(OUT_RGB_RED, 100)
pwm_green = GPIO.PWM(OUT_RGB_GREEN, 100)
pwm_blue = GPIO.PWM(OUT_RGB_BLUE, 100)
pwm_red.start(0)
pwm_green.start(0)
pwm_blue.start(0)


class fileops:
    """ File operations class """

    def read_state(self):
        s = ""
        with open(LED_STATE) as f:
            s = f.read()
        f.close()
        return s

    def read_dnd(self):
        s = ""
        with open(DND_STATE) as f:
            s = f.read()
        f.close()
        return s

    def write_state(self, state):
        with open(LED_STATE, "w") as f:
            f.write(state)
        f.close()

    def write_dnd(self, state):
        with open(DND_STATE, "w") as f:
            f.write(state)
        f.close()


class output_led:
    """ LED Output Class """

    def __init__(self, busy_light):
        self.file = fileops()
        self.busy_light = busy_light

    def web_set(self, colour):
        """ Update the notifier via simple web API if required """
        # Check existing LCD colour to not set unnecessarily
        if self.busy_light.busy_light_colour != colour:
            # Try/except for settings appropriate notifier status
            try:
                response = requests.get(
                    "http://" + NOTIFIER_IP + "?" + colour + "=1", timeout=WEB_TIMEOUT
                )
            except:
                print "Unable to communicate with webseriver at " + NOTIFIER_IP + " when setting " + colour + " status."

    def red(self, is_busy):
        """ Set the red punch status """
        GPIO.output(OUT_RED, 1)
        GPIO.output(OUT_GREEN, 0)
        GPIO.output(OUT_BLUE, 0)
        GPIO.output(OUT_YELLOW, 0)
        self.file.write_state("red")
        if is_busy:
            self.web_set("red")
        else:
            self.web_set("yellow")

    def green(self, is_busy):
        """ Set the red punch status """
        GPIO.output(OUT_RED, 0)
        GPIO.output(OUT_GREEN, 1)
        GPIO.output(OUT_BLUE, 0)
        GPIO.output(OUT_YELLOW, 0)
        self.file.write_state("green")
        if is_busy:
            self.web_set("red")
        else:
            self.web_set("green")

    def blue(self, is_busy):
        """ Set the blue punch status """
        GPIO.output(OUT_RED, 0)
        GPIO.output(OUT_GREEN, 0)
        GPIO.output(OUT_BLUE, 1)
        GPIO.output(OUT_YELLOW, 0)
        self.file.write_state("blue")
        if is_busy:
            self.web_set("red")
        else:
            self.web_set("yellow")

    def yellow(self, is_busy):
        """ Set the yellow punch status """
        GPIO.output(OUT_RED, 0)
        GPIO.output(OUT_GREEN, 0)
        GPIO.output(OUT_BLUE, 0)
        GPIO.output(OUT_YELLOW, 1)
        self.file.write_state("yellow")
        if is_busy:
            self.web_set("red")
        else:
            self.web_set("yellow")


class busy_led:
    """ Class for interacting with the busy light RGB LED """

    busy_light_colour = ""
    dnd_set = False
    service_active = True

    def __init__(self):
        self.file = fileops()

    def set_busy(self):
        """ Set the busy led status to true """
        self.rgb_red()
        self.dnd_set = True
        try:
            response = requests.get(
                "http://" + NOTIFIER_IP + "?red=1", timeout=WEB_TIMEOUT
            )
            self.service_active = True
        except:
            print "Unable to communicate with webseriver at " + NOTIFIER_IP + " when setting DND to true"
            self.service_active = False

    def busy_toggle(self):
        """ Toggle the busy led light status """
        sleep(0.1)
        if self.dnd_set == True:
            try:
                response = requests.get(
                    "http://" + NOTIFIER_IP + "?yellow=1", timeout=WEB_TIMEOUT
                )
                self.rgb_yellow()
                self.dnd_set = False
                self.file.write_dnd("no")
                self.service_active = True
            except:
                print "Unable to communicate with webseriver at " + NOTIFIER_IP + " when setting DND to false"
                self.service_active = False
        else:
            try:
                response = requests.get(
                    "http://" + NOTIFIER_IP + "?red=1", timeout=WEB_TIMEOUT
                )
                self.rgb_red()
                self.dnd_set = True
                self.file.write_dnd("yes")
                self.service_active = True
            except:
                print "Unable to communicate with webseriver at " + NOTIFIER_IP + " when setting DND to true"
                self.service_active = False

    def rgb_red(self):
        """ Set rgb led to red """
        pwm_red.ChangeDutyCycle(20)
        pwm_green.ChangeDutyCycle(0)
        pwm_blue.ChangeDutyCycle(0)
        self.busy_light_colour = "red"

    def rgb_green(self):
        """ Set rgb led to green """
        pwm_red.ChangeDutyCycle(0)
        pwm_green.ChangeDutyCycle(15)
        pwm_blue.ChangeDutyCycle(0)
        self.busy_light_colour = "green"

    def rgb_yellow(self):
        """ Set rgb led to yellow """
        pwm_red.ChangeDutyCycle(20)
        pwm_green.ChangeDutyCycle(15)
        pwm_blue.ChangeDutyCycle(0)
        self.busy_light_colour = "yellow"

    def rgb_blue(self):
        """ Set rgb led to blue """
        pwm_red.ChangeDutyCycle(0)
        pwm_green.ChangeDutyCycle(0)
        pwm_blue.ChangeDutyCycle(20)

    def rgb_purlpe(self):
        """ Set rgb led to purple """
        pwm_red.ChangeDutyCycle(30)
        pwm_green.ChangeDutyCycle(5)
        pwm_blue.ChangeDutyCycle(2)

    def check_status(self):
        """ Check the status of the notifier presence light and update vars """
        # Record currently known dnd set value
        current_dnd_set = self.dnd_set
        try:
            response2 = requests.get("http://" + NOTIFIER_IP, timeout=WEB_TIMEOUT)
            self.service_active = True
            if 'class="status-dnd"' in response2.text:
                self.rgb_red()
                self.dnd_set = True
                if current_dnd_set != self.dnd_set:
                    self.file.write_dnd("yes")
                self.busy_light_colour = "red"
            elif 'class="status-busy"' in response2.text:
                self.rgb_yellow()
                self.dnd_set = False
                if current_dnd_set != self.dnd_set:
                    self.file.write_dnd("no")
                self.busy_light_colour = "yellow"
            elif 'class="status-free"' in response2.text:
                self.rgb_green()
                self.dnd_set = False
                if current_dnd_set != self.dnd_set:
                    self.file.write_dnd("no")
                self.busy_light_colour = "green"
        except:
            print "Unable get data from webseriver at " + NOTIFIER_IP
            self.service_active = False


def main():
    """ Main! """
    # Instantiate the fileops class
    file = fileops()

    # Read state of DND state file and set dnd_set boolean
    # based on retults of file_read_dnd()
    local_dnd_set = False
    if "yes" in file.read_dnd():
        local_dnd_set = True

    # Instantiate other classes
    busy_light = busy_led()
    # Pass the busy_light class into output_led class
    output_light = output_led(busy_light)
    # Set dnd status based on the previous if statement
    busy_light.dnd_set = local_dnd_set

    # Perform initial status check (prevents us from rewriting same state to
    # the notifier device needlessly)
    busy_light.check_status()

    # On startup check the current state and set work type LED
    # If DND is enabled also set DND according to boolean
    # In each case we pass the DND status to the output_light methods
    # being called to ensure that the correct representation of 'busy' or not
    # is set on the remote presence indicator/notifier host
    # We also ensure that if DND is set that we pass this to the busy_led
    # class so the local RGB LED on the controller box indicates correctly
    current_state = file.read_state()
    if current_state == "red":
        output_light.red(busy_light.dnd_set)
        if busy_light.dnd_set:
            busy_light.set_busy
        else:
            busy_light.busy_light_colour = "yellow"
    elif current_state == "green":
        output_light.green(busy_light.dnd_set)
        if busy_light.dnd_set:
            busy_light.set_busy
        else:
            busy_light.busy_light_colour = "green"
    elif current_state == "blue":
        output_light.blue(busy_light.dnd_set)
        if busy_light.dnd_set:
            busy_light.set_busy
        else:
            busy_light.busy_light_colour = "yellow"
    elif current_state == "yellow":
        output_light.yellow(busy_light.dnd_set)
        if busy_light.dnd_set:
            busy_light.set_busy
        else:
            busy_light.busy_light_colour = "yellow"

    # Initialize main loop, start the loop counter at 39 so the
    # initial status check happens fast
    loop_counter = 19
    while True:
        loop_counter += 1
        # If we're at the 20th iteration reset and check the status
        # from the notifier for busy indicator (in case another control
        # device/system changed it)
        if loop_counter == 20:
            loop_counter = 0
            busy_light.check_status()

        # Check for input on one of the 5 control buttons
        if not GPIO.input(IN_RED):
            output_light.red(busy_light.dnd_set)
            busy_light.check_status()
        if not GPIO.input(IN_GREEN):
            busy_light.dnd_set = False
            output_light.green(busy_light.dnd_set)
            busy_light.check_status()
        if not GPIO.input(IN_BLUE):
            output_light.blue(busy_light.dnd_set)
            busy_light.check_status()
        if not GPIO.input(IN_YELLOW):
            output_light.yellow(busy_light.dnd_set)
            busy_light.check_status()
        if not GPIO.input(IN_BUSY):
            busy_light.busy_toggle()

        # Impart a 100ms delay between loop iterations
        sleep(0.1)

        # Put some cycling on the rgb led to flash between blue and the current
        # rgb busy light status color
        if loop_counter % 2 == 0 and loop_counter < 16:
            if busy_light.service_active == False:
                busy_light.rgb_purlpe()
            else:
                busy_light.rgb_blue()
        if loop_counter % 4 == 0:
            if busy_light.busy_light_colour == "red":
                busy_light.rgb_red()
            elif busy_light.busy_light_colour == "yellow":
                busy_light.rgb_yellow()
            elif busy_light.busy_light_colour == "green":
                busy_light.rgb_green()


if __name__ == "__main__":
    main()
