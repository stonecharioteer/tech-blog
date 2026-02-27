---
date: "2026-02-27T12:12:17+05:30"
draft: false
title: "Merrilin - We built an app to read books"
description: "We built Merrilin, an AI-powered reading app with spoiler-free book companions, live sync, and beautiful themes."
tags:
  - "AI"
  - "ebooks"
  - "merrilin"
  - "reading"
  - "epub"
cover:
  image: "/images/posts/merrilin/merrilin-hero.webp"
  alt: "Merrilin - AI-powered reading app"
---

## Trying to Read War and Peace

I have been trying to read War and Peace for years. I know nothing about
Napoleonic history, but that didn't keep me from enjoying _The Count of Monte
Cristo_, which was one of my favourite books growing up. But _War and Peace_
comes with some rather strange baggage.

I was always told it's the book _everyone_ gives up on.

I bought a copy in the early noughts. I tried to read 2 pages perhaps. I didn't
make much headway. There were other things to read.

I didn't have this problem with Dostoevsky so it wasn't a Russian Literature
problem. I've read _The Brothers Karamazov_ at 14, not sure how much of the
philosophical diatribes into patricide I got, but it's something.

I think I might have done better with _War and Peace_ if I had cliff's notes or
something. Perhaps an annotated edition? I'm not sure. And I've not done well
with annotated editions of other books either. I think it's just a problem with
knowing _how_ to read some things.

## Trying to Read War and Peace ft. LLMs

In June 2024, I tried something _fun_.

![Asking ChatGPT if it had training data on War and Peace](/images/posts/merrilin/chatgpt.webp)

I shouldn't have been surprised at this answer frankly. So I set myself to
reading War and Peace with ChatGPT on the side.

![Side-by-Side GPT and War and Peace](/images/posts/merrilin/chatgpt-war-and-peace.webp)

I got about 4 chapters in, which was farther than I ever had until that point.

I began thinking then that there was something here.

Now I'd tried NotebookLM when it came out, and I haven't been very happy with
the experience. Both using ChatGPT and NotebookLM involved having to take my
attention away from my reading app, and then having to constantly tell the
models to _not_ spoil me.

It's funny though. Asking to _not_ be spoiled about _War and Peace_? Imagine if
someone didn't want to be spoiled about _Dracula_!

## Being Opinionated about Reading Apps

I own about 2500 books. My personal library keeps growing, but I predominantly
read digitally nowadays. I own several reading devices, and even love reading on
my phone, a OnePlus Open. I think reading on any device should be easy and it
should get certain things _right_.

A reading app should:

1. _sync_ your books, annotations (bookmarks, notes and highlights) and progress
   across books;
2. allow you to read on any device;
3. allow you to organize your library into collections in a meaningful way;
4. provide you a choice of themes that account for a variety of accessibility
   options;
5. have easy-to-discover menu options and not be a UI clusterf\*ck;
6. provide _accurate_ estimates of reading time; and, most importantly,
7. get out of your way and allow you to read.

You'd think that out of all the reading apps out there, _one_ would meet these
criteria. None do, really. I have tried them all. Sync is broken, or it is
_manual_. And even if it works, you need to set up scripts to export stuff like
highlights or, dear Vishnu in Vaikunta,
[write code](https://github.com/stonecharioteer/kollector) to get it to work.
And themes. As a developer, I have access to an insane number of themes that are
optimized to naraka and back. Why on earth can't reading apps give me _those_
themes? It's like the folks who write the reading apps _do not use them_.

And some of the apps are just plain _bad_. I haven't seen some in _ages_, and I
opened them specifically to research for this post, and they were _just_
**hideous**.

I'm not being very nice here. And I don't think I want to be. Reading is an
important activity, especially in today's world. They say don't judge a book by
its cover but bibliophiles _do_. I have strong opinions about which hardcovers
to buy. I own multiple copies of _the Lord of the Rings._ I even want to get
some pretty hardcovers which use a decently sized font for _War and Peace_.

It is abysmal that our reading apps are not that well made. Some are good. I've
used them for years. But I've had separate apps for different styles of books.
And sync has _always_ been broken.

I even had to watch YouTube tutorials to get my head around one of them, and
that forever had broken sync, and don't even get me _started_ about that
travesty of a built-in keyboard. I stopped taking notes in my books!

I have always wanted to build a reading app. It's not the fanciest of ideas, but
it _is_ deeply personal to me.

## Merrilin

This idea began 2 years ago, when I tried to read _War and Peace_ with ChatGPT.
But it also began when dominant reading apps could not retain my attention. They
_all_ lacked something.

When [`@loststoic`](https://loststoic.com) and I kept talking about "something to
build" as a side project, even early in 2025, I always rounded myself towards "a
reading app".

The laundry list of features was always very high. I couldn't be satisfied with
just having an EPUB reader with an AI companion. I wanted _the very best_ AI
companion you could have for reading a book.

That meant: if I'm reading fiction, I do not want to be spoilt, but I'd like to
ask questions. If I'm reading nonfiction, I'd like to "look ahead", and see if
this book is nothing more than a glorified blogpost.

I don't want to take my book and then go to NotebookLM and ask questions there.
I want to tell my app what line I'm reading, and then ask a question about that
specific line.

I want to ask _previous_ books in an epic fantasy series "when the hell did this
happen?", because life is complicated these days and our minds wander. Would you
believe I didn't know _Mat_ was carrying the Horn of Valere when I first read
the Great Hunt as a kid?

But I _also_ wanted good themes, sync across devices (I own plenty), and I
wanted the app to look good on monochromatic e-ink devices like the Boox Palma.
One of my favourite apps wouldn't work in Dark mode on those devices after an
update. And I'd paid for the premium version as well!

This laundry list evolved and it became one of those ideas that don't really sit
down quietly to be honest. They have a habit of doing things, almost in a
Seussian way. They give you Grand Purpose, perhaps. At least they did to me.

Whenever [`@loststoic`](https://loststoic.com) asked if I "had any ideas", I'd
always come back to "The Idea."

I never really thought that the idea would come to fruition to be honest with
you.

A plethora of themes? Check.

![Theme Selector](/images/posts/merrilin/theme-picker.webp)

Ask questions of my book without fear of spoilers? Check.

![Spoiler Gate 1 Book](/images/posts/merrilin/spoiler-gate-dracula.webp)

Ask questions of an entire book series? Check.

![Spoiler Gate Series](/images/posts/merrilin/the-vicomte-de-bragelonne-series-question.webp)

Ask questions of nonfiction books that have nothing to do with each other, but I
still want to make queries anyway? Why the hell not?

![Series Nonfiction Question](/images/posts/merrilin/meditations-sun-tzu-machiavelli-tablet.webp)

Live sync across devices? I was hoping for sync without me having to press sync,
but _this_ is what Dr. Frankenstein felt, I suppose.

{{< youtube IdPDcr0fgwY >}}

Share quotes with your friends and family without needing _another_ service to
collect them? Check.

![Share Quote](/images/posts/merrilin/quote-sun-tzu.webp)

And, of course, support for the Boox Palma and any other low-ppi,
low-refresh-rate, e-ink/e-paper devices? Check.

![Boox Palma](/images/posts/merrilin/boox-palma-merrilin.webp)

Did I mention that I can predict just how many minutes a day a user is likely to
read using statistics? You'll have to see it to believe it.

I've read 2 books on this app so far myself in the last week, and I have started
reading _War and Peace_ on it already.

![War and Peace spoiler safety](/images/posts/merrilin/war-and-peace-spoiler-safety.webp)

## Register for the Wait List

[Merrilin](https://merrilin.ai) is currently open for signups for the
newsletter, but I'll reach out to whoever signs up in the upcoming weeks for a
limited trial.

## Gallery

{{< gallery >}}
<div class="box">
  <figure itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject">
    <div class="img" style="background-image: url('/images/posts/merrilin/desktop-shelf-view-library.webp');">
      <img itemprop="thumbnail" src="/images/posts/merrilin/desktop-shelf-view-library.webp" alt="Desktop shelf view" />
    </div>
    <figcaption><p>Desktop Shelf View</p></figcaption>
    <a href="/images/posts/merrilin/desktop-shelf-view-library.webp" itemprop="contentUrl"></a>
  </figure>
</div>
<div class="box">
  <figure itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject">
    <div class="img" style="background-image: url('/images/posts/merrilin/desktop-shelf-view-library-theme-2.webp');">
      <img itemprop="thumbnail" src="/images/posts/merrilin/desktop-shelf-view-library-theme-2.webp" alt="Desktop shelf view alternate theme" />
    </div>
    <figcaption><p>Shelf View Alternate Theme</p></figcaption>
    <a href="/images/posts/merrilin/desktop-shelf-view-library-theme-2.webp" itemprop="contentUrl"></a>
  </figure>
</div>
<div class="box">
  <figure itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject">
    <div class="img" style="background-image: url('/images/posts/merrilin/desktop-list-view.webp');">
      <img itemprop="thumbnail" src="/images/posts/merrilin/desktop-list-view.webp" alt="Desktop list view" />
    </div>
    <figcaption><p>Desktop List View</p></figcaption>
    <a href="/images/posts/merrilin/desktop-list-view.webp" itemprop="contentUrl"></a>
  </figure>
</div>
<div class="box">
  <figure itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject">
    <div class="img" style="background-image: url('/images/posts/merrilin/desktop-thumbnail-view.webp');">
      <img itemprop="thumbnail" src="/images/posts/merrilin/desktop-thumbnail-view.webp" alt="Desktop thumbnail view" />
    </div>
    <figcaption><p>Desktop Thumbnail View</p></figcaption>
    <a href="/images/posts/merrilin/desktop-thumbnail-view.webp" itemprop="contentUrl"></a>
  </figure>
</div>
<div class="box">
  <figure itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject">
    <div class="img" style="background-image: url('/images/posts/merrilin/reader-desktop-wide.webp');">
      <img itemprop="thumbnail" src="/images/posts/merrilin/reader-desktop-wide.webp" alt="Reader desktop wide view" />
    </div>
    <figcaption><p>Reader Wide View</p></figcaption>
    <a href="/images/posts/merrilin/reader-desktop-wide.webp" itemprop="contentUrl"></a>
  </figure>
</div>
<div class="box">
  <figure itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject">
    <div class="img" style="background-image: url('/images/posts/merrilin/reader-desktop-narrow.webp');">
      <img itemprop="thumbnail" src="/images/posts/merrilin/reader-desktop-narrow.webp" alt="Reader desktop narrow view" />
    </div>
    <figcaption><p>Reader Narrow View</p></figcaption>
    <a href="/images/posts/merrilin/reader-desktop-narrow.webp" itemprop="contentUrl"></a>
  </figure>
</div>
<div class="box">
  <figure itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject">
    <div class="img" style="background-image: url('/images/posts/merrilin/reader-desktop-narrow-light-theme.webp');">
      <img itemprop="thumbnail" src="/images/posts/merrilin/reader-desktop-narrow-light-theme.webp" alt="Reader light theme" />
    </div>
    <figcaption><p>Reader Light Theme</p></figcaption>
    <a href="/images/posts/merrilin/reader-desktop-narrow-light-theme.webp" itemprop="contentUrl"></a>
  </figure>
</div>
<div class="box">
  <figure itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject">
    <div class="img" style="background-image: url('/images/posts/merrilin/reader-desktop-narrow-sepia.webp');">
      <img itemprop="thumbnail" src="/images/posts/merrilin/reader-desktop-narrow-sepia.webp" alt="Reader sepia theme" />
    </div>
    <figcaption><p>Reader Sepia Theme</p></figcaption>
    <a href="/images/posts/merrilin/reader-desktop-narrow-sepia.webp" itemprop="contentUrl"></a>
  </figure>
</div>
<div class="box">
  <figure itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject">
    <div class="img" style="background-image: url('/images/posts/merrilin/light-theme-mobile.webp');">
      <img itemprop="thumbnail" src="/images/posts/merrilin/light-theme-mobile.webp" alt="Mobile light theme" />
    </div>
    <figcaption><p>Mobile Light Theme</p></figcaption>
    <a href="/images/posts/merrilin/light-theme-mobile.webp" itemprop="contentUrl"></a>
  </figure>
</div>
<div class="box">
  <figure itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject">
    <div class="img" style="background-image: url('/images/posts/merrilin/series-page.webp');">
      <img itemprop="thumbnail" src="/images/posts/merrilin/series-page.webp" alt="Series page" />
    </div>
    <figcaption><p>Series Page</p></figcaption>
    <a href="/images/posts/merrilin/series-page.webp" itemprop="contentUrl"></a>
  </figure>
</div>
<div class="box">
  <figure itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject">
    <div class="img" style="background-image: url('/images/posts/merrilin/analytics-1.webp');">
      <img itemprop="thumbnail" src="/images/posts/merrilin/analytics-1.webp" alt="Analytics overview" />
    </div>
    <figcaption><p>Analytics Overview</p></figcaption>
    <a href="/images/posts/merrilin/analytics-1.webp" itemprop="contentUrl"></a>
  </figure>
</div>
<div class="box">
  <figure itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject">
    <div class="img" style="background-image: url('/images/posts/merrilin/analytics-reader-profile.webp');">
      <img itemprop="thumbnail" src="/images/posts/merrilin/analytics-reader-profile.webp" alt="Analytics reader profile" />
    </div>
    <figcaption><p>Reader Profile</p></figcaption>
    <a href="/images/posts/merrilin/analytics-reader-profile.webp" itemprop="contentUrl"></a>
  </figure>
</div>
<div class="box">
  <figure itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject">
    <div class="img" style="background-image: url('/images/posts/merrilin/analytics-most-likely-reading-time.webp');">
      <img itemprop="thumbnail" src="/images/posts/merrilin/analytics-most-likely-reading-time.webp" alt="Most likely reading time analytics" />
    </div>
    <figcaption><p>Reading Time Analytics</p></figcaption>
    <a href="/images/posts/merrilin/analytics-most-likely-reading-time.webp" itemprop="contentUrl"></a>
  </figure>
</div>
{{< /gallery >}}
{{< load-photoswipe >}}
