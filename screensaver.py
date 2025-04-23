#!/usr/bin/env python3
"""
Hi-DPI friendly fullscreen “screensaver”.
  • DPI-aware on Windows (sharp fonts)
  • Canvas auto-sized to real screen resolution
  • True binary search for best font size
  • Graceful fallback when requested family isn’t present
"""
import tkinter as tk
from tkinter import font
import argparse, sys, platform

# ---------- helpers ----------
def enable_hidpi(root: tk.Tk) -> None:
    """Make fonts crisp on HiDPI displays (Windows only)."""
    if platform.system() == "Windows":
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)        # per-monitor v1
        except Exception:
            pass
    # Convert between points and pixels accurately
    dpi = root.winfo_fpixels("1i")  # how many pixels in one inch
    root.tk.call("tk", "scaling", dpi / 72)                # 72 pt = 1 in ≈ 72 px

def best_font_size(text, family, screen_w, screen_h, padding=40, upper=800):
    """Binary-search the largest font size that still fits."""
    lo, hi = 1, upper
    test = font.Font(family=family, size=lo)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        test.configure(size=mid)
        if (test.measure(text) <= screen_w - padding and
            test.metrics("linespace") <= screen_h - padding):
            lo = mid           # fits, try bigger
        else:
            hi = mid - 1       # too big, shrink
    return lo

# ---------- main ----------
def main(argv=None):
    parser = argparse.ArgumentParser(description="Simple Screensaver Maker")
    parser.add_argument("--color", default="black",
                        help="Background color (name or hex)")
    parser.add_argument("--text", default="",
                        help="Text to display")
    parser.add_argument("--font", default="Arial",
                        help='Font family (e.g. "Segoe UI", "Helvetica")')
    parser.add_argument("--textcolor", default=None,
                    help='Color of the text (name or hex). '
                         'If omitted, a readable color is chosen automatically.')
    parser.add_argument("--mode",
                    choices=("fullscreen", "borderless"),
                    default="borderless",
                    help="fullscreen = wm-managed; borderless = no title-bar/borders")
    args = parser.parse_args(argv)

    root = tk.Tk()

    if args.mode == "fullscreen":
        root.attributes("-fullscreen", True)          # works fine on macOS/Linux/Win
    else:
        # borderless, covers primary monitor (or all if you kept --span-all code)
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry(f"{sw}x{sh}+0+0")              # sit above task-bar/dock

    # Explicitly size the window
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{sw}x{sh}+0+0")         
    enable_hidpi(root)                        # crisp rendering
    root.attributes("-fullscreen", True)
    root.configure(bg=args.color)
    root.bind("<Any-KeyPress>", lambda _e: root.destroy())
    root.bind("<Motion>",      lambda _e: root.destroy())

    # Calculate real screen dimensions after scaling is active
    root.update_idletasks()
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()

    # Choose the font family (graceful fallback)
    avail = set(font.families())
    family = args.font if args.font in avail else "Arial"
    if family != args.font:
        print(f"⚠  Font “{args.font}” not found; using {family}", file=sys.stderr)

    size = best_font_size(args.text, family, sw, sh)
    final_font = font.Font(family=family, size=size)

    # Center vertically with correct baseline
    linespace = final_font.metrics("linespace")
    y = sh // 2

    # Create a canvas the full size of the monitor
    canvas = tk.Canvas(root, bg=args.color, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    fg = (args.textcolor or
        ("black" if args.color.lower() == "white" else "white"))

    canvas.create_text(sw // 2, y,
                    text=args.text,
                    fill=fg,
                    font=final_font,
                    anchor="c")

    root.mainloop()

if __name__ == "__main__":
    main()