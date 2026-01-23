---
date: "2026-01-23T23:07:15+05:30"
title: "Data Structures & Algorithms - Overcoming Inertia"
description: "My progress"
tags:
  - "interviews"
  - "data structures"
  - "data visualization"
---

I won't call it a fear, but I would like to overcome interview anxiety. I do not
enjoy DSA interviews, it comes with some performance anxiety for me. I overcame
my fear of swimming, and that's a _real_ fear for me. I get anxiety in
interviews because I don't enjoy them, and I decided to address this.

My plan is gradual progress. I want to code out different data structures and
algorithms step by step. To that aim, I'm maintain
[this repo](https://github.com/stonecharioteer/interview-prep).

I originally wanted to track my progress here, but I have a very simple way of
doing that now, by linking to the public image.

![DSA Prep Practice](https://github.com/stonecharioteer/interview-prep/raw/main/progress.png)

This image will be constantly updated in the repo to showcase what I'm learning
and when it was last updated, the story of how I got to this image is pretty
interesting, but not relevant to the task of learning. Yet, I'm going to share
it below.

## Visualizing DSA Progress using Claude

I was using Claude for housekeeping in that repo:

- Updating test fixtures for my code, to ensure that it has all the edgedcases
  for my "gradual learning exercises"
- Updating tooling for the repo so I can run tests using a justfile without
  worrying about what broke and when.
- Generating placeholder functions for me to fill in, ensuring those functinos
  do not have type hints (in python), but just enough of a docstring to get me
  started.
- Updating the TODO section of my README so that I can focus on doing the
  exercises

When doing the last step in the above list, I realized I could now plot the
progress in some way to show it off.

I asked claude to make a single PNG file that had two plots:

1. A progress-bar view that showed different topics and how many exercises I was
   doing on them.
2. A github-style commit view that showed when I was actively studying and
   highlighting my streaks.

At the first attempt, it used Pillow to generate the image, and I dind't bother
saving that image since it looked pretty boring. I asked it to do the same thing
using Matplotlib, and it made this.

![Claude DSA Image Trial 1](/images/posts/dsa-prep/claude-dsa-image-trial-1.webp)

I liked it, it was more than I could sit and do in matplotlib myself (I do not
enjoy writing any matplotlib code!), and I was happy making tiny adjustments to
it.

I next tried to have it clean up the legends, make the charts more visible and
suggested some size/position improvements. At the same time I asked it to clean
up the matplotlib code and write it in the eyes of someone who’s seasoned in
data viz and in the intracracies of matplotlib.

![Claude DSA Image Trial 2](/images/posts/dsa-prep/claude-dsa-image-trial-2.webp)

This is what I got when I asked it to "think like a data storyteller".

Then, my friend recommended trying the `frontend-design` skill to ask it to
redesign the graphic from the ground up, and the `simplify-code` plugin to make
the code more modular and less convoluted.

![Claude DSA Image Trial 3](/images/posts/dsa-prep/claude-dsa-image-trial-3.webp)

I was wowed by this. I'm not anything of a data visualization expert, and I'm
sure a human could do a far, _far_ better job, but this was really good for me.
If it makes studying DSA easier for me, that's tokens well spent for me.

![Claude DSA Image Trial 4](/images/posts/dsa-prep/claude-dsa-image-trial-4.webp)

If you'd like to look at the code that visualizes this, be warned, it's
completely vibe-coded and plenty esoteric, but it's
[available here](https://github.com/stonecharioteer/interview-prep/blob/main/scripts/progress_calendar.py)
