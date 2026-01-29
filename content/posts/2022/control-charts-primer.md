---
date: "2022-05-12T10:00:00+05:30"
draft: false
title: "A Primer on Control Charts"
description:
  "An introduction to statistical quality control using control charts and
  Shewhart charts. Understanding process variation, control limits, and
  statistical manufacturing principles."
tags:
  - "statistics"
  - "manufacturing"
  - "quality-control"
  - "learning"
---

I'm a trained statistician. I worked on a motorcycle manufacturing shop floor
for 3 years of my early career, and compared to tech companies, that was _hell_.
However, the lessons I learnt there have moulded me forever.

The most important lessons revolved around a statistical quality tool called
_control charts_ or _Shewart charts_, named after
[Walter A. Shewart](https://en.wikipedia.org/wiki/Walter_A._Shewhart), who
pioneered them. Shewart's name is spoken in the same tones as that of
[Deming](https://en.wikipedia.org/wiki/W._Edwards_Deming), who is responsible
for the
[14 Principles of Management](https://mitpress.mit.edu/books/out-crisis).

## What Are Control Charts?

A control chart, in its multiple forms, monitors a process for changes in a
_specific_ parameter, designated as the _control_ parameter. This parameter
helps us measure a desired outcome of a process. If a factory wishes to produce
a shaft of diameter 25mm with a tolerance of 1mm on either side, then they
should strive to make shafts from 24-26mm in size. While that's a worthwhile
exercise, it's better to _further_ limit the manufacturing process so that while
the process sticks to the design requirements, it is also consistent within
itself. This doesn't mean you're striving for a better design tolerance, but it
speaks about _whether_ your process even _allows_ for better tolerances.

The _control chart_ is a line plot that measures this parameter, or a statistic
associated with it such as the average of a couple of readings taken at
consistent timestamps. Control charts are divided into 2 areas, a portion of the
chart is _above_ a line called the control limit (CL), and the range of values
is bounded on either side by an Upper Control Limit (UCL), and a Lower Control
Limit (LCL), which tell us _how_ much our process is _capable_ of fluctuating.

![Control Charts](/images/posts/two-of-three/control-charts.png)

_A sample control chart, marking the limits and showing how a process is slowly
deviation from its control limits._

These limits aren't decided by us. Indeed, they have _nothing_ to do with the
tolerances that the design engineer has set. Instead, they have everything to do
with the statistical limits of your process. That means that the last 25
readings you take in your process decide the UCL, CL and LCL for the next couple
of readings.

{{< tip title="Statistical Viability" >}} 25 is an arbitrary number, mind you.
It is the _bare minimum_ that you need to start plotting charts. However, it is
not even statistically viable to do this. Instead start with a 100 readings if
you want to do some meaningful analytics of process control study. {{< /tip >}}

## Interpreting Control Charts

If 7 consecutive readings on a control chart fall on one side of the limits,
that's your chart telling you that you have _serious_ problems. Your process is
slowly deviating to one side of your limits. It doesn't need to be negative by
the way. Perhaps you _want_ your process to shift in one direction. This is an
indication that whatever you're doing to your process is shifting the metric to
one side.

These shifts are _predicatable_, and they also indicate a shift in your process
that could arise from inherent causes. However, there are sudden shifts that
could happen because of uncontrollable causes. These problems will not cause
long-lasting errors in your readings, and they're usually the sort that need a
lot of brain-wracking to solve immediately. If they're not addressed
immediately, this will indicate that something is really wrong with your process
management, and not really reflect whether your process is doing well or now.

## Applications Beyond Manufacturing

While a control chart is something you can definitely use in technology
companies -- in fact, control charts are strongly associated with LEAN
manufacturing, but I'm not experienced enough at Software applications in LEAN
to say whether these are actually used in a tech company -- the principles
behind control charts extend far beyond manufacturing processes.

The core insight is that any process has inherent variation, and understanding
that variation helps you distinguish between normal fluctuations and meaningful
changes that require intervention. This thinking can be applied to software
metrics, team performance, and even career decisions.

## References

These are a list of books I love recommending if you're interested in the topic
of statistics and process control:

1. [Edward Deming - Out of the Crisis](https://www.goodreads.com/book/show/566574.Out_of_the_Crisis)
2. [Walter A. Shewart - Statistical Method From the Viewpoint of Quality Control](https://www.goodreads.com/book/show/944744.Statistical_Method_from_the_Viewpoint_of_Quality_Control)
3. [Taiichi Ohno - Toyota Production System: Beyond Large-Scale Production](https://www.goodreads.com/book/show/376237.Toyota_Production_System)
4. [Taiichi Ohno - Workplace Management](https://www.goodreads.com/book/show/1199345.Taiichi_Ohno_s_Workplace_Management)

These books were written in a time where statistical quality control was applied
predominantly to manufacturing processes, but I'd recommend looking at them
through the lens of a general engineer, as opposed to a software engineer. If
you ever find yourself wanting to discuss these topics, I'm always available.
