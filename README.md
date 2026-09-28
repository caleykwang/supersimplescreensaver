# Super Simple Screensaver — Awesome Edition

A beautiful, fullscreen motivational quote screensaver written in Python.
No dependencies beyond the standard library — just Python 3.8+.

## Features

- **65+ curated motivational quotes** with author attribution, built right in
- **Smooth fade-in / hold / fade-out** transitions between quotes (~60 fps)
- **8 hand-crafted colour themes** — midnight, sunset, forest, ocean, rose, monochrome, aurora, golden
- **Gradient backgrounds** with subtle floating particle ambiance
- **Live clock** display
- **Keyboard navigation** — browse quotes, pause, cycle themes, quit
- **Custom quotes file** — bring your own quotes in a simple text format
- **HiDPI-aware** on Windows (crisp fonts on high-resolution displays)
- Classic screensaver behaviour: mouse movement or Esc exits instantly

## Quick start

```
python screensaver.py
```

## Options

```
python screensaver.py [options]

  --theme THEME          Colour theme (default: midnight)
                         Choices: midnight, sunset, forest, ocean,
                                  rose, monochrome, aurora, golden

  --font FONT            Quote font family (default: Georgia)

  --display-time SECS    Seconds to show each quote (default: 8)

  --fade-speed SPEED     Fade speed 0.005 (very slow) – 0.1 (fast)
                         Default: 0.025

  --quotes-file FILE     Path to a plain-text file of custom quotes

  --shuffle              Shuffle quotes at launch

  --mode {fullscreen,borderless}
                         Window mode (default: borderless)
```

## Keyboard controls

| Key | Action |
|-----|--------|
| `←` / `→` | Previous / next quote |
| `Space` | Pause / resume auto-advance |
| `T` | Cycle through colour themes |
| `Esc` | Quit |
| Mouse move | Quit (classic screensaver behaviour) |

## Custom quotes file

Create a plain text file with one quote per line.
Optionally separate the quote from the author with `|`:

```
The journey of a thousand miles begins with one step. | Lao Tzu
Keep going.
# Lines starting with # are ignored
```

Then launch with:

```
python screensaver.py --quotes-file my_quotes.txt
```

## Examples

```bash
# Default midnight theme
python screensaver.py

# Warm sunset theme, shuffled quotes
python screensaver.py --theme sunset --shuffle

# Ocean theme, slow fade, long display time
python screensaver.py --theme ocean --fade-speed 0.01 --display-time 12

# Your own quotes with the golden theme
python screensaver.py --quotes-file my_quotes.txt --theme golden
```
