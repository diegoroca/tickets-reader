import evdev
from evdev import ecodes

# Replace with the correct touchscreen device
device = evdev.InputDevice('/dev/input/event2')

print(f"Listening for touch events on {device}")

for event in device.read_loop():
    if event.type == ecodes.EV_ABS:
        if event.code == ecodes.ABS_X:
            x = event.value
            print(f"X: {x}")
        elif event.code == ecodes.ABS_Y:
            y = event.value
            print(f"Y: {y}")

    if event.type == ecodes.EV_KEY:
        if event.code == ecodes.BTN_TOUCH:
            if event.value == 1:
                print("Touch detected!")
            elif event.value == 0:
                print("Touch released!")

