import time
import digitalio
import board
import busio
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import ili9341, color565

# Setup SPI
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Define control pins
cs_pin = digitalio.DigitalInOut(board.CE0)  # Chip select
dc_pin = digitalio.DigitalInOut(board.D24)  # Data/Command
rst_pin = digitalio.DigitalInOut(board.D25)  # Reset

# Create Display Object
display = ili9341.ILI9341(
    spi, cs=cs_pin, dc=dc_pin, rst=rst_pin,
    baudrate=10000000, width=320, height=240
)

# Rotate screen if needed
display.rotation = 0  # Try 0, 90, 180, or 270

# Create a blank black image
image = Image.new("RGB", (display.width, display.height), "black")
draw = ImageDraw.Draw(image)

# Define button properties
button_width = 140
button_height = 50
button_x = (display.width - button_width) // 2  # Center Horizontally
button_y = (display.height - button_height) // 2  # Center Vertically
button_radius = 5  # Corner radius
button_color = (10,10,10)
text_color = "white"
text = "CLICK ME"

# Draw rounded rectangle (button)
draw.rounded_rectangle(
    (button_x, button_y, button_x + button_width, button_y + button_height),
    radius=button_radius, fill=button_color
)

# Load font
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except:
    font = ImageFont.load_default()

# Calculate text position
text_size = draw.textbbox((0, 0), text, font=font)
text_x = button_x + (button_width - (text_size[2] - text_size[0])) // 2
text_y = button_y + (button_height - (text_size[3] - text_size[1])) // 2

# Draw text on button
draw.text((text_x, text_y), text, font=font, fill=text_color)

# Show image on display
display.image(image)
print("Button drawn!")

