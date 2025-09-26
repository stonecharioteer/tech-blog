---
date: '2025-09-26T15:20:33+05:30'
draft: true
title: 'Ruby'
description: 'How I started learning Ruby and Ruby on Rails in 2025 and what my experience has been like so far.'
tags:
  - "ruby"
  - "programming-languages"
---

I think everyone needs to learn more programming languages. It's a very fun
experience. In my career, I've tried out a bunch of them, although I've stuck
to mostly Python and Rust. I don't acknowledge that I *know* any of the other
languages, since I've forgotten them mostly. It is a fun experience, and I've
wanted to learn at least one new language every year. That hasn't happened as
I'd like, but when I got a reason to learn something new, I don't deny it.

That brings me to Ruby. I have a lot of thoughts about learning Ruby in 2025,
and while some of them are great, a few of them are related to the language and
how I *almost* ended up choosing Ruby over Python in 2014.

## How I learnt Python

I was in Flipkart, and my team had a few millions of rows of data to deal with
in a CSV file. None of us were developers and the tech team didn't spare anyone
to help us with that data set. Instead of trying to get Excel to manage this, I
decided to try to learn a programming language to do this. I didn't have a
plan, just some friends who were much smarter than I was and who I reached out
to. One told me to do this in Ruby or Python. I wanted to build a small desktop
interface -- I didn't know anything about web UIs or desktop-native UIs to be
honest with you -- and I told my friends this. So the other said that I could
look into using the Qt4 bindings for Python with PyQt4. He mentioned that the
Ruby Qt bindings weren't maintained.

That was all I had to go on to choose Python. I have not used Qt in over 9
years, but it feels weird that the crux of my career came from whether Ruby or
Python had Qt libraries that I could use.

## Ruby People

I've always been curious about Ruby though. There are figures from the Ruby
world I keep running into, at least when I am reading blogs. I began learning
Python from Zed Shaw's book -- Learn Python the Hard Way. It isn't a resource I
recommend to people today, but when I was learning Python, his book made sure
to teach me exactly how I needed to learn. Heck, it's how I learn languages
even today.

1. Don't copy and paste any example code, type it all in every single time.
2. Don't use autocomplete when learning, just type things out.

These two simple tips are enough for me. I continue to teach newcomers this even today.

Zed Shaw used to be the maintainer of the Mongrel web server, which used to be
coupled with Rails a long time ago. I'll not talk about his falling out with
the Rails community, but his article on his way out is... *entertaining* to say
the least.

Another figure I realized was from the Ruby sphere was Steve Klabnik. Steve was
[a maintainer of Rails](https://contributors.rubyonrails.org/contributors/steve-klabnik/commits) back in the day,
but these days he's more known for writing the Rust Book with Carol Nichols. I learnt Rust by reading this book,
and I was also introduced to Steve's thoughts on open source contributions by a friend a few years ago. I recommend
[his article to everyone who wants to get started.](https://steveklabnik.com/writing/how-to-be-an-open-source-gardener/)

Finally, DHH. It is strange that I didn't know who DHH was until 2025. I wasn't
on any Ruby or Rails user groups, and I'd purged my Twitter account completely.
I was never active on Twitter to be honest. But I think it's when he was
interviewed by Les Grossman and later the Primeagen and TJ Devries and the gang
that I heard of him for the first time. Even then I only knew of him as someone
who made Omarchy, his Arch-based Distro that everyone seems to think signals
the coming of the year of the Linux Desktop. Just before I started learning
Ruby, I learnt that he was also the creator of Rails.

## I didn't need Ruby

I strongly believe every programmer should learn multiple programming
languages. I do include shell scripting languages in that group. But I believe
that when you learn, you should try to diversify so you don't learn to use the
same ratchet for every problem.

I had Python work great for me, and honestly it did all I needed it to. I
learnt Rust when I needed something that was typesafe and could compile to
single binary with the lowest latency I could muster. And, I, *cough*, had
Javascript when I needed to write web UIs.

I didn't *need* Ruby, honestly. But a friend used to constantly remind me that
Ruby would teach me programming paradigms that I needed to learn. That was well
and good, but I couldn't, not in this job market, think of learning a language
that seemingly no one was using these days.

I'll be the first to admit that's a bad thing, though. The fact that everything
is shoe-horned into Python is a really bad thing. Python is a great language,
but it also allows you to write what you think is production level code after a
two day bootcamp. That is dangerous. Airflow, notoriously enough, teaches users
to run bash scripts from within its Python environment and treats that as a
normal thing. Operations engineers who first look at it think that they can run
complex shell scripts from airflow and that it's very safe to do. Data
engineers think that data munging with it is easy as pie and then complain that
someone else's DAG brought airflow down.

I still didn't need Ruby though. I have loved Flask ever since I first used it,
and it hid nothing from me. I never brought myself to use Django because it hid a lot
of things from me and that felt very unpythonic. I couldn't understand the lifecycle of
a Django app in terms of the module loading. I didn't like that it was so opinionated.

Something about Django still feels like it's not pythonic. I'm sure it only
feels that way to untrained eyes. I strongly believe that if I have to work in
a team of engineers, I'd pick Django over Flask any day. Flask and Airflow have
a similar problem. They both expect the programmer to be a *good engineer*. But
that's almost never the case. Most programmers aren't good engineers. Most
programmers just want to close the issue and go home. And there's nothing wrong
with that.

Django drew strong lines in the ground for developers to follow. It made
working in a team easier, because it was predictable. If you saw a Django
application, especially one using the Django-Rest-Framework, you knew how it
was structured. You could rely on its structure and scaffolding to navigate
the repository. You didn't need anyone telling you where a particular route
originated from.

The ideas I just spoke about seem almost obvious to us now, but they weren't,
back in the day. Smaller frameworks made developers feel productive, but we
are left writing a lot of code just to do things the right way, or we can
MacGuyver stuff around and YOLO our way into an application that will inevitably
break.

An opinionated framework makes it easier to ensure developers follow the same rules.
Microframeworks like flask only work if you're all part of one echo-chamber of opinions
or if you're a one man show.

I'm certain I have a few friends cackling madly after reading this, but I have
believed this for a long time. The only thing I enjoy about microframeworks is
that they force *responsible* programmers to develop opinions about how to do
things and they also are forced to learn how to structure applications. I learnt
how to structure a Flask app through
[exploreflask.com](https://explore-flask.readthedocs.io/), which has since gone
offline. Do I *recommend* learning Flask this way? Definitely. But do I recommend
spending time in piecing together your own version of Django from Flask?

No. I do not.

I didn't need Ruby, but I discovered that opinionated products tend to have strong
reasons for existing.

## Learning Ruby

When a company asked me to learn Ruby during my trial period there, I was a little
unsure. I wanted to, but I was concerned about a silly thing: [*trends*.](https://survey.stackoverflow.co/2025/technology)
I know it shouldn't matter, but Ruby is declining in popularity, and that makes it
slightly hard to get a job as a Ruby developer. But I decided to give this a go
because I am not a python developer. I never wanted to be a Rust developer either.

Being a `$INSERT_LANGUAGE_HERE` developer is not something I want to do. I want to
be someone who builds performant software, irrespective of language. I strongly believe
far too many companies spend time pivoting to another language in claims that `$INSERT_LANGUAGE_HERE` language
doesn't scale.

I'll bet they've never run a single profiler on their code, let alone on the SQL query their
ORM of choice is spewing.

So I decided to learn Ruby, and Ruby on Rails. I started off by trying to figure out *which* version of Ruby
to learn. I love learning by reading books, having used Zed Shaw's book on Python and Steve Klabnik's for Rust.

12 years ago when I was considering learning Ruby, someone had pointed me to
[Why's Poignant Guide to Ruby](https://poignant.guide/). I know that it's been
years and the language must have changed in that time. I wanted something more
modern. I've also considered reading [The Well-Grounded Rubyist](https://www.manning.com/books/the-well-grounded-rubyist-third-edition),
because I want to learn the Ruby way. Far too many developers come to
`$LANGUAGE_2` and expect to write things the way they wrote them in
`$LANUAGE_1`. I don't want to be that person. If I'm going to be writing Ruby,
I want the code to look like Ruby code, not like Python or Rust.


This led me to [LearnEnough.com](https://learnenough.com), and the [railstutorial.org](https://railstutorial.org),
both by the fantastic Michael Hartl. These tutorials have helped me grok Ruby fairly well, well enough to do
some [exercism](https://exercism.org) exercises with Ruby. I have a long way to go, but I've been [live-xeeting
my experience.](https://xcancel.com/stonecharioteer/status/1970035592076664835)

{{< tweet user="stonecharioteer" id="1970035592076664835" >}}

I have a lot of things to talk about my experience, and I wanted to speak about this at the Bangalore Rust User Group
as well.

## Implicit not Explicit, Ruby from a Pythonista

### Environments

My first question starting off was how do I manage Ruby installations on my computer.
I knew that `rbenv` and `rvm` exist, but I also recall, very vaguely, that I used to have problems
with them when this blog was originally in Jekyll. I've since been using [`mise-en-place`](https://mise.jdx.dev/lang/ruby.html)
for Go and Nodejs on my computers, and I like it so far. I decided to use it for Ruby as well, but I 
had some difficulty getting started.

```
# global installs
mise install ruby@3.4.6 # install ruby 3.4.6
mise use -g ruby@3.4.6 # use 3.4.6 globally
# in a project
mkdir project && cd project
mise install ruby@3.1.1
mise use ruby@3.1.1
gem install bundler -v 2.3.4
bundle init
bundle add logger
```

This is where I'd started, and I figured I could go on this way, but when I discovered that `rails` could
be installed as a global dependency so that I could leverage its scaffolder to generate the project structure,
I had to refine my process a bit.

```
mise install ruby@3.1.1
mise use ruby@3.1.1
gem install bundler -v 2.3.4
gem install rails -v 7.0.4
rails new sample_app --skip-bundle
```

And then I saw some *weird* syntax like this.

```
bundle _2.3.4_ install
rails _7.0.4 new sample_app --skip-bundle
```

I had *so* **many** ***thoughts***!

First of all, *what* is that syntax? It's so strange. I had never seen versioning like that in a CLI.
But after I had gotten over the initial shock, my developer brain immediately wanted to know *how* Ruby
managed that.
