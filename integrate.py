import time
import digitalio
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import pygame
from adafruit_rgb_display import ili9341, color565

# Setup SPI and the display
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs_pin = digitalio.DigitalInOut(board.CE0)  # Chip select
dc_pin = digitalio.DigitalInOut(board.D24)  # Data/Command
rst_pin = digitalio.DigitalInOut(board.D25)  # Reset

# Create Display Object
display = ili9341.ILI9341(spi, cs=cs_pin, dc=dc_pin, rst=rst_pin, baudrate=10000000, width=320, height=240)

# Pygame Initialization
pygame.init()

# Create a Pygame screen for display (Virtual Screen)
screen = pygame.display.set_mode((display.width, display.height))

# Define button properties
button_width = 140
button_height = 50
button_radius = 5  # Corner radius
button_color = (169,169,169)  # Initial grey color for the button
button_pressed_color = (0,255,0)  # Color when pressed (green)
text_color = (255, 255, 255)  # Text color (white)
text = "CLICK ME"

# Function to draw a button
def draw_button(color):
    button_x = (display.width - button_width) // 2  # Center Horizontally
    button_y = (display.height - button_height) // 2  # Center Vertically
    
    # Clear screen and fill it with a background color
    screen.fill((0, 0, 0))  # Fill with black background

    # Draw the button as a rectangle with rounded corners
    pygame.draw.rect(screen, color, (button_x, button_y, button_width, button_height), border_radius=button_radius)
    
    # Load font and calculate text position
    font = pygame.font.Font(None, 36)  # Using default font
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(button_x + button_width//2, button_y + button_height//2))

    # Draw the text on top of the button
    screen.blit(text_surface, text_rect)

# Event loop to handle touch and interaction
running = True
button_color = button_color
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print(f"Touch detected at X: {mouse_x}, Y: {mouse_y}")

            # Check if the touch is within the button's area
            if (display.width // 2 - button_width // 2 <= mouse_x <= display.width // 2 + button_width // 2 and
                display.height // 2 - button_height // 2 <= mouse_y <= display.height // 2 + button_height // 2):
                print("Button pressed!")
                button_color = button_pressed_color
            else:
                button_color = (169,169,169)  # Reset button color
        elif event.type == pygame.MOUSEBUTTONUP:
            button_color = (169,169,169)  # Reset button color when touch is released

    # Redraw the button
    draw_button(button_color)

    # Update the display (copy screen to the hardware)
    display.image(screen)

    # Small delay to control refresh rate
    pygame.time.delay(10)

# Quit pygame when done
pygame.quit()

