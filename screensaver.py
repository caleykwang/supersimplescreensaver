import tkinter as tk
from tkinter import font
import argparse

def create_screensaver():
    parser = argparse.ArgumentParser(description='Simple Screensaver Maker')
    parser.add_argument('--color', type=str, default='black', help='Background color (name or hex)')
    parser.add_argument('--resolution', type=str, default='800x600', help='Window resolution (e.g., 1920x1080)')
    parser.add_argument('--text', type=str, default='', help='Text to display')
    args = parser.parse_args()

    # Parse resolution
    width, height = map(int, args.resolution.split('x'))

    # Create window
    root = tk.Tk()
    root.configure(bg=args.color)
    root.attributes('-fullscreen', True)
    root.bind('<Any-KeyPress>', lambda e: root.destroy())
    root.bind('<Motion>', lambda e: root.destroy())

    # Create canvas
    canvas = tk.Canvas(root, width=width, height=height, bg=args.color, highlightthickness=0)
    canvas.pack(expand=True, fill=tk.BOTH)

    # Calculate text size
    test_font = font.Font(family='Arial', size=12)
    min_size = 1
    max_size = 300
    padding = 20  # Add some padding

    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Binary search for optimal font size
    optimal_size = 12
    for size in range(1, 300):
        test_font.configure(size=size)
        text_width = test_font.measure(args.text)
        text_height = test_font.metrics("ascent") + test_font.metrics("descent")
        
        if text_width > (screen_width - padding) or text_height > (screen_height - padding):
            optimal_size = size - 1
            break
        optimal_size = size

    # Create font with optimal size
    final_font = font.Font(family='Arial', size=optimal_size)
    text_height = final_font.metrics("ascent") + final_font.metrics("descent")

    # Calculate vertical position
    y_position = screen_height // 2 - text_height // 2 + final_font.metrics("ascent") // 2

    # Create text
    canvas.create_text(screen_width // 2, y_position, 
                       text=args.text, 
                       fill='black' if args.color.lower() == 'white' else 'white',
                       font=final_font,
                       anchor='center')

    root.mainloop()

if __name__ == '__main__':
    create_screensaver()