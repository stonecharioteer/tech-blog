---
date: 2018-09-09T10:00:00+05:30
draft: false
title: "Learn the Kana Using Python and a Raspberry Pi"
description:
  "Building an interactive Hiragana quiz using Python, Raspberry Pi, and a
  WaveShare e-Paper display to practice Japanese characters."
tags:
  - raspberry-pi
  - japanese
  - python
  - e-paper
  - pillow
  - hardware
  - language-learning
---

I have been attempting to learn Nihongo (Japanese). It is a failing attempt
really, since I have so little time lately.

However, I wanted to make myself flash cards or a simple test for the Hiragana.

Around that time, I bought a WaveShare e-Paper hat for the Raspberry Pi, and was
having fun developing interfaces for it.

One of the uses that I figured I could put the Pi to was a test. A simple
Hiragana quiz.

## The Hardware Setup

The WaveShare e-paper screen has three colors: White, Black and Red. This
tricolor variant is a little slow, compared to the Kindle for example. However
it works quite well.

It is controlled using images, so you can display anything you can represent as
an image.

That's sort of easier said than done, though. If not for the Python-Pillow
library, I wouldn't know where to begin.

## Implementation Details

### Character Dictionary

The first step was a simple Python function to get a dictionary of hiragana
characters against their roman equivalents.

This was a lot easier than hard coding the dictionary into the program.

### Quiz Logic

The next steps were randomly selecting a kana character and displaying it on
screen with a possible question. I had to also randomize the answer's position.

Again, fairly simple, granted what I wanted to achieve.

The `test_romaji_hiragana` function took care of the interactions with the
Raspberry Pi's GPIO library. The function also handled the actual displaying of
the question on the screen.

### Working with the Display

The epd library is WaveShare's own library for the e-paper display. It has some
Python 2.7 dependencies, which I need to weed out in the future. I'm skeptical
of WaveShare's software support, since their documentation leaves much for the
user to discover on their own. However, their hardware is quite fun to use!

Python-PIL, as always, is fun to use. The epd library takes two Image objects:
one for the blacks, and another for the reds. Needless to say, the rest of the
space with a 100% transparency, is the white region.

## The Tomodachi Project

The rest of the code is available at my personal library for this project. I've
named it [Tomodachi](https://github.com/stonecharioteer/tomodachi), Japanese for
friend. It has some bugs, I'll admit, but it was quite fun to work on. I will be
going back to this project to tinker with it some more, perhaps for the
PiFaceCAD module next, or the WaveShare Game Hat.

One of the things I want to make is a mario-styled sidescroller game to teach me
the Kana. Perhaps I'll use the GameHat for that. It would be a great project.

## Learning from Mistakes

There is joy in going wrong also. You learn something new.

The project taught me several valuable lessons:

- Hardware interaction can be surprisingly satisfying
- Image generation with PIL/Pillow is more powerful than I initially thought
- Physical interfaces add a tangible element to learning that screens can't
  replicate
- The e-paper display's slow refresh rate actually works well for quiz scenarios

## Future Improvements

Looking back at this project, there are several enhancements I'd like to make:

1. **Port to Python 3**: Remove the Python 2.7 dependencies
2. **Add Katakana**: Expand beyond just Hiragana characters
3. **Progress Tracking**: Keep score and track learning progress
4. **Audio Support**: Add pronunciation audio for each character
5. **Game Mechanics**: Implement the mario-style sidescroller idea

## Technical Reflections

This project was one of my early forays into combining hardware and software in
a meaningful way. The constraints of the e-paper display—limited colors, slow
refresh rate—actually enhanced the experience by forcing focus on each question.

The tactile nature of physical buttons combined with the visual feedback of the
e-paper display created an engaging learning environment that pure software
solutions often lack.

## Resources

- [Pillow Python Library](https://pillow.readthedocs.io/en/stable/)
- [WaveShare e-Paper Display Documentation](https://www.waveshare.com/wiki/E-Paper_Driver_HAT)
- [Tomodachi Project Repository](https://github.com/stonecharioteer/tomodachi)
