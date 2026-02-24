#!/usr/bin/env python3
"""
Motivational Quote Screensaver — Awesome Edition

Features:
  • 65+ curated motivational quotes with author attribution
  • Smooth fade-in / hold / fade-out transitions
  • Gradient backgrounds with 8 hand-crafted color themes
  • Subtle floating particle ambiance
  • Live clock display
  • Keyboard navigation: ←/→ quotes, Space pause, T theme cycle, Esc quit
  • Mouse-movement exits (classic screensaver behaviour)
  • HiDPI-aware on Windows
  • Load custom quotes from a plain-text file
"""

import argparse
import math
import platform
import random
import sys
import time

import tkinter as tk
from tkinter import font as tkfont


# ─────────────────────────────────────────────────────────
# QUOTE DATABASE
# ─────────────────────────────────────────────────────────

BUILTIN_QUOTES = [
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("In the middle of every difficulty lies opportunity.", "Albert Einstein"),
    ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
    ("Life is what happens when you're busy making other plans.", "John Lennon"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("Strive not to be a success, but rather to be of value.", "Albert Einstein"),
    ("You miss 100% of the shots you don't take.", "Wayne Gretzky"),
    ("Whether you think you can or you think you can't, you're right.", "Henry Ford"),
    ("The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"),
    ("An unexamined life is not worth living.", "Socrates"),
    ("Spread love everywhere you go.", "Mother Teresa"),
    ("When you reach the end of your rope, tie a knot in it and hang on.", "Franklin D. Roosevelt"),
    ("Always remember that you are absolutely unique. Just like everyone else.", "Margaret Mead"),
    ("Don't judge each day by the harvest you reap but by the seeds that you plant.", "Robert Louis Stevenson"),
    ("The future belongs to those who prepare for it today.", "Malcolm X"),
    ("You only live once, but if you do it right, once is enough.", "Mae West"),
    ("In three words I can sum up everything I've learned about life: it goes on.", "Robert Frost"),
    ("Love the life you live. Live the life you love.", "Bob Marley"),
    ("If you look at what you have in life, you'll always have more.", "Oprah Winfrey"),
    ("Opportunities don't happen. You create them.", "Chris Grosser"),
    ("It always seems impossible until it's done.", "Nelson Mandela"),
    ("Act as if what you do makes a difference. It does.", "William James"),
    ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
    ("You are never too old to set another goal or to dream a new dream.", "C.S. Lewis"),
    ("Too many of us are not living our dreams because we are living our fears.", "Les Brown"),
    ("I find that the harder I work, the more luck I seem to have.", "Thomas Jefferson"),
    ("The starting point of all achievement is desire.", "Napoleon Hill"),
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("Your imagination is your preview of life's coming attractions.", "Albert Einstein"),
    ("All our dreams can come true, if we have the courage to pursue them.", "Walt Disney"),
    ("If you do what you always did, you will get what you always got.", "Unknown"),
    ("Success is walking from failure to failure with no loss of enthusiasm.", "Winston Churchill"),
    ("Just when the caterpillar thought the world was ending, it became a butterfly.", "Proverb"),
    ("I have not failed. I've just found 10,000 ways that won't work.", "Thomas Edison"),
    ("Hard work beats talent when talent doesn't work hard.", "Tim Notke"),
    ("Don't wish it were easier. Wish you were better.", "Jim Rohn"),
    ("I am not a product of my circumstances. I am a product of my decisions.", "Stephen Covey"),
    ("You can't use up creativity. The more you use, the more you have.", "Maya Angelou"),
    ("Do one thing every day that scares you.", "Eleanor Roosevelt"),
    ("Well done is better than well said.", "Benjamin Franklin"),
    ("Dream big and dare to fail.", "Norman Vaughan"),
    ("We generate fears while we sit. We overcome them by action.", "Dr. Henry Link"),
    ("The secret of change is to focus all of your energy not on fighting the old, but on building the new.", "Socrates"),
    ("Life is 10% what happens to us and 90% how we react to it.", "Charles R. Swindoll"),
    ("The only limit to our realization of tomorrow is our doubts of today.", "Franklin D. Roosevelt"),
    ("Do not wait to strike till the iron is hot; make it hot by striking.", "William Butler Yeats"),
    ("It is never too late to be what you might have been.", "George Eliot"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("The best revenge is massive success.", "Frank Sinatra"),
    ("People who are crazy enough to think they can change the world are the ones who do.", "Rob Siltanen"),
    ("Failure will never overtake me if my determination to succeed is strong enough.", "Og Mandino"),
    ("We may encounter many defeats but we must not be defeated.", "Maya Angelou"),
    ("Knowing is not enough; we must apply. Wishing is not enough; we must do.", "Johann Wolfgang Von Goethe"),
    ("Imagine your life is perfect in every respect; what would it look like?", "Brian Tracy"),
    ("We can easily forgive a child who is afraid of the dark; the real tragedy of life is when men are afraid of the light.", "Plato"),
    ("Nothing is impossible, the word itself says 'I'm possible'!", "Audrey Hepburn"),
    ("The question isn't who is going to let me; it's who is going to stop me.", "Ayn Rand"),
    ("To see what is right and not do it is a lack of courage.", "Confucius"),
    ("Reading is to the mind, as exercise is to the body.", "Brian Tracy"),
    ("Arise, awake and stop not until the goal is reached.", "Swami Vivekananda"),
    ("The will to win, the desire to succeed, the urge to reach your full potential… these are the keys that will unlock the door to personal excellence.", "Confucius"),
    ("Certain things catch your eye, but pursue only those that capture the heart.", "Ancient Indian Proverb"),
    ("Believe in yourself! Have faith in your abilities!", "Norman Vincent Peale"),
    ("Start where you are. Use what you have. Do what you can.", "Arthur Ashe"),
    ("When you come to the end of your rope, tie a knot and hang on.", "Franklin D. Roosevelt"),
]


# ─────────────────────────────────────────────────────────
# COLOR THEMES
# ─────────────────────────────────────────────────────────

THEMES = {
    "midnight": {
        "bg_top":    "#080818",
        "bg_bottom": "#181838",
        "text":      "#e8e8ff",
        "author":    "#8888cc",
        "clock":     "#4444aa",
        "accent":    "#5566ff",
    },
    "sunset": {
        "bg_top":    "#180800",
        "bg_bottom": "#3a1400",
        "text":      "#ffe8d0",
        "author":    "#ffaa77",
        "clock":     "#aa5533",
        "accent":    "#ff8844",
    },
    "forest": {
        "bg_top":    "#001508",
        "bg_bottom": "#002a12",
        "text":      "#d0ffe8",
        "author":    "#77ffaa",
        "clock":     "#33aa55",
        "accent":    "#44ff88",
    },
    "ocean": {
        "bg_top":    "#000c18",
        "bg_bottom": "#001830",
        "text":      "#d0f0ff",
        "author":    "#77ccff",
        "clock":     "#3388aa",
        "accent":    "#44aaff",
    },
    "rose": {
        "bg_top":    "#18000c",
        "bg_bottom": "#2e0018",
        "text":      "#ffe0f0",
        "author":    "#ff88bb",
        "clock":     "#aa3366",
        "accent":    "#ff5599",
    },
    "monochrome": {
        "bg_top":    "#000000",
        "bg_bottom": "#0e0e0e",
        "text":      "#ffffff",
        "author":    "#aaaaaa",
        "clock":     "#555555",
        "accent":    "#cccccc",
    },
    "aurora": {
        "bg_top":    "#030c10",
        "bg_bottom": "#08181e",
        "text":      "#c0ffee",
        "author":    "#80ddbb",
        "clock":     "#30aa77",
        "accent":    "#00ffcc",
    },
    "golden": {
        "bg_top":    "#0c0700",
        "bg_bottom": "#180e00",
        "text":      "#fff8d0",
        "author":    "#ffdd77",
        "clock":     "#aa8833",
        "accent":    "#ffcc33",
    },
}

THEME_NAMES = list(THEMES.keys())


# ─────────────────────────────────────────────────────────
# COLOR UTILITIES
# ─────────────────────────────────────────────────────────

def hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b) -> str:
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


def lerp_color(c1: str, c2: str, t: float) -> str:
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex(
        r1 + (r2 - r1) * t,
        g1 + (g2 - g1) * t,
        b1 + (b2 - b1) * t,
    )


# ─────────────────────────────────────────────────────────
# LAYOUT HELPERS
# ─────────────────────────────────────────────────────────

def enable_hidpi(root: tk.Tk) -> None:
    if platform.system() == "Windows":
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
    dpi = root.winfo_fpixels("1i")
    root.tk.call("tk", "scaling", dpi / 72)


def wrap_text(text: str, font_obj, max_width: int) -> list:
    """Word-wrap text to fit within max_width pixels."""
    words = text.split()
    lines, current = [], []
    for word in words:
        candidate = " ".join(current + [word])
        if font_obj.measure(candidate) <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines or [""]


def best_font_size(text, family, max_w, max_h, bold=False, upper=300) -> int:
    """Binary-search the largest bold font size where wrapped text still fits."""
    weight = "bold" if bold else "normal"
    lo, hi = 12, upper
    f = tkfont.Font(family=family, size=lo, weight=weight)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        f.configure(size=mid)
        lines = wrap_text(text, f, max_w)
        lh = f.metrics("linespace")
        total_h = lh * len(lines)
        widest = max(f.measure(l) for l in lines)
        if widest <= max_w and total_h <= max_h:
            lo = mid
        else:
            hi = mid - 1
    return lo


def load_quotes_from_file(path: str) -> list:
    """Load quotes from a file.  Format: 'Quote text | Author'  or just 'Quote text'."""
    quotes = []
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "|" in line:
                    q, a = line.split("|", 1)
                    quotes.append((q.strip(), a.strip()))
                else:
                    quotes.append((line, ""))
    except OSError as e:
        print(f"⚠  Could not load quotes file: {e}", file=sys.stderr)
    return quotes


# ─────────────────────────────────────────────────────────
# SCREENSAVER APPLICATION
# ─────────────────────────────────────────────────────────

_FADE_IN  = "fade_in"
_HOLD     = "hold"
_FADE_OUT = "fade_out"

_N_PARTICLES = 55
_N_GRADIENT  = 200
_FRAME_MS    = 16          # ~60 fps


class ScreensaverApp:
    def __init__(self, args):
        self.args = args
        self._theme_name = args.theme
        self.theme = THEMES[self._theme_name]

        # ── Quotes ───────────────────────────────────────
        self.quotes = list(BUILTIN_QUOTES)
        if args.quotes_file:
            custom = load_quotes_from_file(args.quotes_file)
            if custom:
                self.quotes = custom + self.quotes
        if args.shuffle:
            random.shuffle(self.quotes)

        self._idx = 0

        # ── Animation state ──────────────────────────────
        self._state      = _FADE_IN
        self._alpha      = 0.0
        self._hold_left  = 0
        self._hold_total = int(args.display_time * 1000 / _FRAME_MS)
        self._fade_step  = args.fade_speed

        # ── Control ──────────────────────────────────────
        self.paused = False
        self._last_theme = None      # triggers gradient repaint on change
        self._last_idx   = None      # triggers layout recalc on quote change

        # ── Window ───────────────────────────────────────
        self.root = tk.Tk()
        self.root.title("Motivational Screensaver")

        if args.mode == "fullscreen":
            self.root.attributes("-fullscreen", True)
        else:
            self.root.overrideredirect(True)
            self.root.attributes("-topmost", True)

        enable_hidpi(self.root)
        self.root.update_idletasks()
        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()
        self.root.geometry(f"{self.sw}x{self.sh}+0+0")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg=self.theme["bg_bottom"])

        # ── Canvas ───────────────────────────────────────
        self.canvas = tk.Canvas(
            self.root, width=self.sw, height=self.sh,
            bg=self.theme["bg_bottom"], highlightthickness=0,
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # ── Font families ────────────────────────────────
        avail = set(tkfont.families())

        def pick(*candidates):
            for c in candidates:
                if c in avail:
                    return c
            return "Arial"

        self._qfam  = pick(args.font, "Georgia", "Palatino Linotype",
                           "Palatino", "Times New Roman", "Arial")
        self._afam  = pick("Segoe UI", "Helvetica Neue", "Helvetica", "Arial")
        self._cfam  = pick("Consolas", "Courier New", "Courier")

        # ── Mouse exit ───────────────────────────────────
        self._mx = self._my = None

        # ── Build scene ──────────────────────────────────
        self._build_scene()

        # ── Key / mouse bindings ─────────────────────────
        self.root.bind("<Escape>",    lambda _e: self.root.destroy())
        self.root.bind("<space>",     lambda _e: self._toggle_pause())
        self.root.bind("<Right>",     lambda _e: self._jump(+1))
        self.root.bind("<Left>",      lambda _e: self._jump(-1))
        self.root.bind("<t>",         lambda _e: self._cycle_theme())
        self.root.bind("<T>",         lambda _e: self._cycle_theme())
        self.root.bind("<Motion>",    self._on_motion)
        self.root.bind("<Button>",    lambda _e: self.root.destroy())

        # ── Start loop ───────────────────────────────────
        self._tick()
        self.root.mainloop()

    # ── Event handlers ──────────────────────────────────

    def _on_motion(self, event):
        if self._mx is None:
            self._mx, self._my = event.x, event.y
            return
        if abs(event.x - self._mx) > 8 or abs(event.y - self._my) > 8:
            self.root.destroy()

    def _toggle_pause(self):
        self.paused = not self.paused

    def _jump(self, delta):
        self._idx = (self._idx + delta) % len(self.quotes)
        self._state = _FADE_IN
        self._alpha = 0.0

    def _cycle_theme(self):
        i = THEME_NAMES.index(self._theme_name)
        self._theme_name = THEME_NAMES[(i + 1) % len(THEME_NAMES)]
        self.theme = THEMES[self._theme_name]
        self._last_theme = None   # force gradient repaint

    # ── Scene construction ───────────────────────────────

    def _build_scene(self):
        sw, sh = self.sw, self.sh

        # Gradient background strips (drawn first so everything else is on top)
        self._grad = []
        for i in range(_N_GRADIENT):
            r = self.canvas.create_rectangle(
                0, i * sh // _N_GRADIENT,
                sw, (i + 1) * sh // _N_GRADIENT + 1,
                fill="#000000", outline="",
            )
            self._grad.append(r)

        # Particles (above gradient, below text)
        self._parts = []   # [x, y, vx, vy, radius, brightness]
        self._part_items = []
        for _ in range(_N_PARTICLES):
            x  = random.uniform(0, sw)
            y  = random.uniform(0, sh)
            vx = random.uniform(-0.25, 0.25)
            vy = random.uniform(-0.55, -0.10)
            r  = random.choice([1, 1, 1, 2, 2, 3])
            br = random.uniform(0.05, 0.35)
            item = self.canvas.create_oval(
                x - r, y - r, x + r, y + r, fill="#ffffff", outline="",
            )
            self._parts.append([x, y, vx, vy, r, br])
            self._part_items.append(item)

        # Decorative accent rule
        self._rule = self.canvas.create_line(
            sw * 0.2, sh * 0.5, sw * 0.8, sh * 0.5,
            fill="#ffffff", width=1,
        )

        # Quote text
        self._qtxt = self.canvas.create_text(
            sw // 2, sh // 2,
            text="", fill="#ffffff",
            font=(self._qfam, 48, "bold"),
            anchor="center", justify="center",
            width=int(sw * 0.74),
        )

        # Author text
        self._atxt = self.canvas.create_text(
            sw // 2, sh // 2 + 80,
            text="", fill="#888888",
            font=(self._afam, 22),
            anchor="center",
        )

        # Clock (top-right)
        self._ctxt = self.canvas.create_text(
            sw - 44, 44,
            text="", fill="#444488",
            font=(self._cfam, 20),
            anchor="ne",
        )

        # Counter (bottom-left)
        self._ntxt = self.canvas.create_text(
            44, sh - 44,
            text="", fill="#444488",
            font=(self._cfam, 15),
            anchor="sw",
        )

        # Theme label (bottom-right)
        self._ttxt = self.canvas.create_text(
            sw - 44, sh - 44,
            text="", fill="#444488",
            font=(self._cfam, 15),
            anchor="se",
        )

        # Pause overlay
        self._ptxt = self.canvas.create_text(
            sw // 2, sh - 44,
            text="|| PAUSED  (Space to resume)",
            fill="#ffffff",
            font=(self._afam, 18),
            anchor="s", state="hidden",
        )

        # Help hint (fades out after a few seconds)
        self._htxt = self.canvas.create_text(
            sw // 2, sh - 44,
            text="← → navigate   Space pause   T theme   Esc quit",
            fill="#ffffff",
            font=(self._cfam, 14),
            anchor="s",
        )
        self._hint_alpha  = 1.0
        self._hint_active = True

        # Cached layout data (avoids recomputing every frame)
        self._layout = {}

    # ── Layout computation ───────────────────────────────

    def _compute_layout(self, quote: str, author: str) -> dict:
        sw, sh = self.sw, self.sh

        # Author font
        a_size = max(18, sh // 52)
        a_font = tkfont.Font(family=self._afam, size=a_size)
        a_h    = a_font.metrics("linespace") if author else 0

        gap       = sh // 22
        pad_x     = int(sw * 0.22)
        pad_y     = int(sh * 0.22) + a_h + gap
        max_qw    = sw - pad_x
        max_qh    = sh - pad_y

        q_size = best_font_size(
            quote, self._qfam, max_qw, max_qh, bold=True, upper=220,
        )
        q_font  = tkfont.Font(family=self._qfam, size=q_size, weight="bold")
        q_lines = wrap_text(quote, q_font, max_qw)
        q_lh    = q_font.metrics("linespace")
        q_h     = q_lh * len(q_lines)

        block_h  = q_h + gap + a_h
        block_top = (sh - block_h) // 2

        q_cy    = block_top + q_h // 2
        a_cy    = block_top + q_h + gap + a_h // 2
        rule_y  = block_top + q_h + gap // 2

        return {
            "q_size":  q_size,
            "a_size":  a_size,
            "q_cy":    q_cy,
            "a_cy":    a_cy,
            "rule_y":  rule_y,
            "max_qw":  max_qw,
        }

    # ── Per-frame update ─────────────────────────────────

    def _repaint_gradient(self):
        top = self.theme["bg_top"]
        bot = self.theme["bg_bottom"]
        n   = len(self._grad)
        for i, rect in enumerate(self._grad):
            self.canvas.itemconfigure(rect, fill=lerp_color(top, bot, i / (n - 1)))
        self._last_theme = self._theme_name

    def _update_particles(self):
        sw, sh = self.sw, self.sh
        acc = self.theme["accent"]
        bg  = self.theme["bg_bottom"]
        for i, (p, item) in enumerate(zip(self._parts, self._part_items)):
            p[0] += p[2]
            p[1] += p[3]
            if p[1] < -4:
                p[1] = sh + 4
                p[0] = random.uniform(0, sw)
            if p[0] < -4:   p[0] = sw + 4
            if p[0] > sw + 4: p[0] = -4
            r = p[4]
            self.canvas.coords(item, p[0] - r, p[1] - r, p[0] + r, p[1] + r)
            self.canvas.itemconfigure(item, fill=lerp_color(bg, acc, p[5]))

    def _apply_alpha(self):
        a  = self._alpha
        bg = self.theme["bg_bottom"]

        def f(key):
            return lerp_color(bg, self.theme[key], a)

        sw = self.sw
        self.canvas.itemconfigure(self._qtxt, fill=f("text"))
        self.canvas.itemconfigure(self._atxt, fill=f("author"))
        self.canvas.itemconfigure(self._rule, fill=f("accent"))

        # Hint fades independently
        if self._hint_active:
            self._hint_alpha = max(0.0, self._hint_alpha - 0.003)
            if self._hint_alpha <= 0:
                self._hint_active = False
                self.canvas.itemconfigure(self._htxt, state="hidden")
            else:
                hc = lerp_color(bg, self.theme["clock"], self._hint_alpha)
                self.canvas.itemconfigure(self._htxt, fill=hc)

    def _tick(self):
        # ── Gradient refresh (only when theme changes) ──
        if self._last_theme != self._theme_name:
            self._repaint_gradient()

        # ── Layout refresh (only when quote changes) ────
        idx = self._idx
        if self._last_idx != idx:
            quote, author = self.quotes[idx]
            self._layout = self._compute_layout(quote, author)
            lay = self._layout
            sw  = self.sw

            self.canvas.itemconfigure(
                self._qtxt,
                text=quote,
                font=(self._qfam, lay["q_size"], "bold"),
                width=lay["max_qw"],
            )
            self.canvas.coords(self._qtxt, sw // 2, lay["q_cy"])

            author_display = f"\u2014 {author}" if author else ""
            self.canvas.itemconfigure(
                self._atxt,
                text=author_display,
                font=(self._afam, lay["a_size"]),
            )
            self.canvas.coords(self._atxt, sw // 2, lay["a_cy"])

            self.canvas.coords(
                self._rule,
                sw * 0.25, lay["rule_y"],
                sw * 0.75, lay["rule_y"],
            )
            self._last_idx = idx

        # ── Animate state machine ───────────────────────
        if not self.paused:
            if self._state == _FADE_IN:
                self._alpha = min(1.0, self._alpha + self._fade_step)
                if self._alpha >= 1.0:
                    self._state     = _HOLD
                    self._hold_left = self._hold_total

            elif self._state == _HOLD:
                self._hold_left -= 1
                if self._hold_left <= 0:
                    self._state = _FADE_OUT

            elif self._state == _FADE_OUT:
                self._alpha = max(0.0, self._alpha - self._fade_step)
                if self._alpha <= 0.0:
                    self._idx   = (self._idx + 1) % len(self.quotes)
                    self._state = _FADE_IN

        # ── Apply fade alpha ────────────────────────────
        self._apply_alpha()

        # ── Update particles ────────────────────────────
        self._update_particles()

        # ── Static overlays (clock, counter, theme) ─────
        self.canvas.itemconfigure(self._ctxt,
                                  text=time.strftime("%H:%M"),
                                  fill=self.theme["clock"])
        self.canvas.itemconfigure(self._ntxt,
                                  text=f"{self._idx + 1} / {len(self.quotes)}",
                                  fill=self.theme["clock"])
        self.canvas.itemconfigure(self._ttxt,
                                  text=self._theme_name,
                                  fill=self.theme["clock"])

        # ── Pause indicator ─────────────────────────────
        self.canvas.itemconfigure(self._ptxt,
                                  state="normal" if self.paused else "hidden",
                                  fill=self.theme["accent"])

        # ── Schedule next frame ─────────────────────────
        self.root.after(_FRAME_MS, self._tick)


# ─────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Motivational Quote Screensaver - Awesome Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""\
Keyboard controls:
  Left/Right  Previous / next quote
  Space       Pause / resume auto-advance
  T           Cycle colour themes
  Esc         Quit
  Mouse       Move to quit (classic screensaver behaviour)

Available themes: {', '.join(THEME_NAMES)}

Custom quotes file format (plain text, one quote per line):
  The journey of a thousand miles begins with one step. | Lao Tzu
  Keep going.
""",
    )
    parser.add_argument(
        "--theme", default="midnight", choices=THEME_NAMES, metavar="THEME",
        help=f"Colour theme (default: midnight). Choices: {', '.join(THEME_NAMES)}",
    )
    parser.add_argument(
        "--font", default="Georgia",
        help="Quote font family (default: Georgia)",
    )
    parser.add_argument(
        "--display-time", type=float, default=8.0, metavar="SECONDS",
        help="Seconds to show each quote (default: 8)",
    )
    parser.add_argument(
        "--fade-speed", type=float, default=0.025, metavar="SPEED",
        help="Fade speed 0.005 (very slow) to 0.1 (fast). Default: 0.025",
    )
    parser.add_argument(
        "--quotes-file", metavar="FILE",
        help="Path to a plain-text file of custom quotes",
    )
    parser.add_argument(
        "--shuffle", action="store_true",
        help="Shuffle quotes at launch",
    )
    parser.add_argument(
        "--mode", choices=("fullscreen", "borderless"), default="borderless",
        help="Window mode (default: borderless)",
    )

    args = parser.parse_args(argv)
    ScreensaverApp(args)


if __name__ == "__main__":
    main()
