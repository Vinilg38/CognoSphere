import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageDraw, ImageFont
from tkinter import ttk
from ttkthemes import ThemedTk

def generate_handwriting():
    # Create a blank white image
    width, height = 800, 400
    background_color = (255, 255, 255)  # White
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Load the "bb.otf" handwriting-style font
    font_size = 30
    font = ImageFont.truetype("bb.otf", font_size)

    # Text to be converted to handwriting
    text = input_text.get()

    # Position and color
    text_position = (50, 100)
    text_color = (0, 0, 0)  # Black

    # Write the text on the image
    draw.text(text_position, text, fill=text_color, font=font)

    # Save the image
    image.save("handwritten.png")

    # Display the image
    photo = PhotoImage(file="handwritten.png")
    image_label.config(image=photo)
    image_label.image = photo

app = ThemedTk(theme="arc")  # Use the "arc" theme from ttkthemes
app.title("Handwritten Text")
app.geometry("600x400")
frame = ttk.Frame(app)
frame.pack(padx=20, pady=20)
# Create an input field for the text
input_label = ttk.Label(app, text="Enter text:", font=("Helvetica", 16))
input_label.pack()
input_text = ttk.Entry(app)
input_text.pack()

# Create a button to generate handwriting
generate_button = ttk.Button(app, text="Generate Handwriting", command=generate_handwriting)
generate_button.pack()

# Create an empty image label
image_label = ttk.Label(app)
image_label.pack()

app.mainloop()
