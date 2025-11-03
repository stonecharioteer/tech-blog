---
date: '2025-09-26T15:20:33+05:30'
lastmod: '2025-10-20T22:33:22+05:30'
draft: false
title: 'Ruby'
description: 'How I started learning Ruby and Ruby on Rails in 2025 and what my experience has been like so far.'
tags:
  - "ruby"
  - "programming-languages"
cover:
  image: "/images/posts/ruby/ruby-and-python.png"
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

Before I begin though, I'd like to preface that I'm not pedantic about
language. I like to compare language philosophies in my head so I understand
how they work internally, not just superficially. I could skim through
everything, navigate code using Claude Code or Gemini CLI, and then make the
changes I need, claiming that isn't Vibe Coding, but I instead want to commit.
Contrasting Ruby with Python is my way of saying, I'm giving this a real go,
and not just trying superficially.

That being said, I'll try to sound like myself, and add in a few memes.

![*whistles*](/images/posts/ruby/ruby-meme-1.jpeg)

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

![Ruby vs Python](/images/posts/ruby/ruby-meme-4.jpeg)

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

That being said, I can write a lot of Ruby already. *Et voila!*

![Hello World!](/images/posts/ruby/hello-world-0.png)

And inside `hello_world.erb`.

![Hello World!](/images/posts/ruby/hello-world-1.png)

What surprised me is that this was easier than I thought it'd be. That's scary.

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

### Editor and LSP

I experimented with LSPs for neovim, having tried
[`sorbet`](https://sorbet.org/docs/overview) and
[`solargraph`](https://github.com/castwide/solargraph), I settled on
[`ruby-lsp`](https://github.com/Shopify/ruby-lsp). I think Solargraph had some
problem with resolving tests in a rails project, I'm not sure what it was, but
I installed Ruby-LSP and it worked without any tweaks. I prefer that for now,
but my preference might change eventually.

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
bundle config set --local path 'vendor/bundle'
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
managed that. Let's focus on that.

I first ran into something related when I installed a different version of Rails and wanted to downgrade
to match the version in the tutorial.

![Multiple rails versions](/images/posts/ruby/multiple-versions.png)

Now that made my neurons fire at full power. *What?* **WHAT?** _***WHAT?!**_

Those are multiple versions of Rails, all installed on my computer, but not on the same environment.

Notice that I did `bundle config set --local path 'vendor/bundle'` earlier, and I did that because
my Python brain told me to look for a way to isolate my local installs.

I didn't know that I *did not **need** to.*

Ruby can manage multiple versions of packages -- called Gems (eat poop Gemini!) -- globally.
That leads us down a very interesting rabbithole.

![Choosing versions](/images/posts/ruby/choosing_versions.png)

How is this happening? This specific version of Ruby I'm using says I can choose the library version!

I decided to inspect what `gem list` would output.

```
$ gem list

abbrev (0.1.2)
actioncable (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
actionmailbox (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
actionmailer (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
actionpack (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
actiontext (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
actionview (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
activejob (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
activemodel (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
activerecord (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
activestorage (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
activesupport (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
addressable (2.8.7)
ansi (1.5.0)
ast (2.4.3)
base64 (0.3.0, 0.2.0)
benchmark (0.4.1, default: 0.4.0)
bigdecimal (3.2.3, 3.1.8)
bindex (0.8.1)
bootsnap (1.18.6)
brakeman (7.1.0)
builder (3.3.0)
bundler (default: 2.6.9, 2.4.19, 2.3.14, 2.3.10)
capybara (3.40.0)
cgi (default: 0.4.2)
childprocess (4.1.0)
coderay (1.1.3)
concurrent-ruby (1.3.5)
connection_pool (2.5.4)
crass (1.0.6)
csv (3.3.2)
date (3.4.1)
debug (1.11.0)
delegate (default: 0.4.0)
did_you_mean (default: 2.0.0)
digest (default: 3.2.0)
drb (2.2.3, 2.2.1)
english (default: 0.8.0)
erb (5.0.2, default: 4.0.4)
error_highlight (default: 0.7.0)
erubi (1.13.1)
etc (default: 1.4.6)
fcntl (default: 1.2.0)
ffi (1.17.2 x86_64-linux-gnu)
fiddle (default: 1.1.6)
fileutils (default: 1.7.3)
find (default: 0.2.0)
formatador (1.2.1)
forwardable (default: 1.3.3)
getoptlong (0.2.1)
globalid (1.3.0)
guard (2.19.1)
guard-compat (1.2.1)
guard-minitest (2.4.6)
i18n (1.14.7)
importmap-rails (2.2.2)
io-console (0.8.1)
io-nonblock (default: 0.3.2)
io-wait (default: 0.3.2)
ipaddr (default: 1.2.7)
irb (1.15.2, default: 1.14.3)
jbuilder (2.14.1)
json (2.15.0, default: 2.9.1)
language_server-protocol (3.17.0.5)
lint_roller (1.1.0)
listen (3.9.0)
logger (1.7.0, default: 1.6.4)
loofah (2.24.1)
lumberjack (1.4.2)
mail (2.8.1)
marcel (1.1.0)
matrix (0.4.3, 0.4.2)
method_source (1.1.0)
mini_mime (1.1.5)
mini_portile2 (2.8.9)
minitest (5.25.5, 5.25.4)
minitest-reporters (1.7.1, 1.2.0)
msgpack (1.8.0)
mustermann (2.0.2)
mutex_m (0.3.0)
nenv (0.3.0)
net-ftp (0.3.8)
net-http (default: 0.6.0)
net-imap (0.5.10, 0.5.8)
net-pop (0.1.2)
net-protocol (0.2.2)
net-smtp (0.5.1)
nio4r (2.7.4)
nkf (0.2.0)
nokogiri (1.18.10 x86_64-linux-gnu)
notiffany (0.1.3)
observer (0.1.2)
open-uri (default: 0.5.0)
open3 (default: 0.2.1)
openssl (default: 3.3.0)
optparse (default: 0.6.0)
ostruct (0.6.3, default: 0.6.1)
parallel (1.27.0)
parser (3.3.9.0)
pathname (default: 0.4.0)
power_assert (2.0.5)
pp (0.6.2)
prettyprint (0.2.0)
prime (0.1.3)
prism (1.5.1)
pry (0.15.2)
pstore (default: 0.1.4)
psych (5.2.6, default: 5.2.2)
public_suffix (6.0.2)
puma (7.0.4, 5.6.5)
racc (1.8.1)
rack (3.2.1, 3.1.16, 2.2.17)
rack-protection (2.2.2)
rack-session (2.1.1)
rack-test (2.2.0)
rackup (2.2.1)
rails (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
rails-controller-testing (1.0.5)
rails-dom-testing (2.3.0)
rails-html-sanitizer (1.6.2)
railties (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
rainbow (3.1.1)
rake (13.3.0, 13.2.1)
rb-fsevent (0.11.2)
rb-inotify (0.11.1)
rbs (3.8.0)
rdoc (6.14.2, default: 6.14.0)
readline (default: 0.0.4)
regexp_parser (2.11.3)
reline (0.6.2, default: 0.6.0)
repl_type_completor (0.1.9)
resolv (default: 0.6.2)
resolv-replace (0.1.1)
rexml (3.4.4, 3.4.0)
rinda (0.2.0)
rss (0.3.1)
rubocop (1.81.0, 1.80.2)
rubocop-ast (1.47.1)
rubocop-performance (1.26.0)
rubocop-rails (2.33.3)
rubocop-rails-omakase (1.1.0)
ruby-progressbar (1.13.0)
ruby2_keywords (default: 0.0.5)
rubyzip (3.1.0)
securerandom (0.4.1)
selenium-webdriver (4.35.0, 4.1.0)
set (default: 1.1.1)
shellany (0.0.1)
shellwords (default: 0.2.2)
sinatra (2.2.2)
singleton (default: 0.3.0)
sprockets (4.2.2)
sprockets-rails (3.5.2)
sqlite3 (2.7.4 x86_64-linux-gnu, 1.7.3)
stimulus-rails (1.3.4)
stringio (3.1.7, default: 3.1.2)
strscan (default: 3.1.2)
syntax_suggest (default: 2.0.2)
syslog (0.2.0)
tempfile (default: 0.3.1)
test-unit (3.6.7)
thor (1.4.0)
tilt (2.6.1)
time (default: 0.4.1)
timeout (0.4.3)
tmpdir (default: 0.3.1)
tsort (default: 0.2.0)
turbo-rails (2.0.16)
typeprof (0.30.1)
tzinfo (2.0.6)
un (default: 0.3.0)
unicode-display_width (3.2.0)
unicode-emoji (4.1.0)
uri (default: 1.0.3)
useragent (0.16.11)
weakref (default: 0.1.3)
web-console (4.2.1)
webdrivers (5.3.1)
websocket (1.2.11)
websocket-driver (0.8.0)
websocket-extensions (0.1.5)
xpath (3.2.0)
yaml (default: 0.4.0)
zeitwerk (2.7.3)
zlib (default: 3.2.1)
```

Oh boy. My eyes are still spinning.

```
$ gem list  | grep ','

actioncable (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
actionmailbox (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
actionmailer (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
actionpack (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
actiontext (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
actionview (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
activejob (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
activemodel (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
activerecord (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
activestorage (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
activesupport (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
base64 (0.3.0, 0.2.0)
benchmark (0.4.1, default: 0.4.0)
bigdecimal (3.2.3, 3.1.8)
bundler (default: 2.6.9, 2.4.19, 2.3.14, 2.3.10)
drb (2.2.3, 2.2.1)
erb (5.0.2, default: 4.0.4)
irb (1.15.2, default: 1.14.3)
json (2.15.0, default: 2.9.1)
logger (1.7.0, default: 1.6.4)
matrix (0.4.3, 0.4.2)
minitest (5.25.5, 5.25.4)
minitest-reporters (1.7.1, 1.2.0)
net-imap (0.5.10, 0.5.8)
ostruct (0.6.3, default: 0.6.1)
psych (5.2.6, default: 5.2.2)
puma (7.0.4, 5.6.5)
rack (3.2.1, 3.1.16, 2.2.17)
rails (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
railties (7.2.2.2, 7.1.5.2, 7.1.3, 7.0.4, 7.0.0)
rake (13.3.0, 13.2.1)
rdoc (6.14.2, default: 6.14.0)
reline (0.6.2, default: 0.6.0)
rexml (3.4.4, 3.4.0)
rubocop (1.81.0, 1.80.2)
selenium-webdriver (4.35.0, 4.1.0)
sqlite3 (2.7.4 x86_64-linux-gnu, 1.7.3)
stringio (3.1.7, default: 3.1.2)
```

These libraries all have multiple versions and no-doubt they know how to choose their dependencies
according to what they need. Because what sane language would allow multiple versions without
being able to resolve the version as needed?

I can't imagine doing this in Python.

How does Ruby do this?

I went looking -- and in 2025, that means I asked an LLM -- and I found the files here.

```
$ ls ~/.local/share/mise/installs/ruby/3.4.6/lib/ruby/gems/3.4.0/gems/

abbrev-0.1.2/           activemodel-7.1.3/      coderay-1.1.3/                jbuilder-2.14.1/                    openssl-3.3.0/                   railties-7.1.3/               singleton-0.3.0/
actioncable-7.0.0/      activemodel-7.1.5.2/    concurrent-ruby-1.3.5/        json-2.15.0/                        open-uri-0.5.0/                  railties-7.1.5.2/             sprockets-4.2.2/
actioncable-7.0.4/      activemodel-7.2.2.2/    connection_pool-2.5.4/        json-2.9.1/                         optparse-0.6.0/                  railties-7.2.2.2/             sprockets-rails-3.5.2/
actioncable-7.1.3/      activerecord-7.0.0/     crass-1.0.6/                  language_server-protocol-3.17.0.5/  ostruct-0.6.1/                   rainbow-3.1.1/                sqlite3-1.7.3/
actioncable-7.1.5.2/    activerecord-7.0.4/     csv-3.3.2/                    lint_roller-1.1.0/                  ostruct-0.6.3/                   rake-13.2.1/                  sqlite3-2.7.4-x86_64-linux-gnu/
actioncable-7.2.2.2/    activerecord-7.1.3/     date-3.4.1/                   listen-3.9.0/                       parallel-1.27.0/                 rake-13.3.0/                  stimulus-rails-1.3.4/
actionmailbox-7.0.0/    activerecord-7.1.5.2/   debug-1.11.0/                 logger-1.6.4/                       parser-3.3.9.0/                  rb-fsevent-0.11.2/            stringio-3.1.2/
actionmailbox-7.0.4/    activerecord-7.2.2.2/   delegate-0.4.0/               logger-1.7.0/                       pathname-0.4.0/                  rb-inotify-0.11.1/            stringio-3.1.7/
actionmailbox-7.1.3/    activestorage-7.0.0/    did_you_mean-2.0.0/           loofah-2.24.1/                      power_assert-2.0.5/              rbs-3.8.0/                    strscan-3.1.2/
actionmailbox-7.1.5.2/  activestorage-7.0.4/    digest-3.2.0/                 lumberjack-1.4.2/                   pp-0.6.2/                        rdoc-6.14.0/                  syntax_suggest-2.0.2/
actionmailbox-7.2.2.2/  activestorage-7.1.3/    drb-2.2.1/                    mail-2.8.1/                         prettyprint-0.2.0/               rdoc-6.14.2/                  syslog-0.2.0/
actionmailer-7.0.0/     activestorage-7.1.5.2/  drb-2.2.3/                    marcel-1.1.0/                       prime-0.1.3/                     readline-0.0.4/               tempfile-0.3.1/
actionmailer-7.0.4/     activestorage-7.2.2.2/  english-0.8.0/                matrix-0.4.2/                       prism-1.5.1/                     regexp_parser-2.11.3/         test-unit-3.6.7/
actionmailer-7.1.3/     activesupport-7.0.0/    erb-4.0.4/                    matrix-0.4.3/                       pry-0.15.2/                      reline-0.6.0/                 thor-1.4.0/
actionmailer-7.1.5.2/   activesupport-7.0.4/    erb-5.0.2/                    method_source-1.1.0/                pstore-0.1.4/                    reline-0.6.2/                 tilt-2.6.1/
actionmailer-7.2.2.2/   activesupport-7.1.3/    error_highlight-0.7.0/        mini_mime-1.1.5/                    psych-5.2.2/                     repl_type_completor-0.1.9/    time-0.4.1/
actionpack-7.0.0/       activesupport-7.1.5.2/  erubi-1.13.1/                 mini_portile2-2.8.9/                psych-5.2.6/                     resolv-0.6.2/                 timeout-0.4.3/
actionpack-7.0.4/       activesupport-7.2.2.2/  etc-1.4.6/                    minitest-5.25.4/                    public_suffix-6.0.2/             resolv-replace-0.1.1/         tmpdir-0.3.1/
actionpack-7.1.3/       addressable-2.8.7/      fcntl-1.2.0/                  minitest-5.25.5/                    puma-5.6.5/                      rexml-3.4.0/                  tsort-0.2.0/
actionpack-7.1.5.2/     ansi-1.5.0/             ffi-1.17.2-x86_64-linux-gnu/  minitest-reporters-1.2.0/           puma-7.0.4/                      rexml-3.4.4/                  turbo-rails-2.0.16/
actionpack-7.2.2.2/     ast-2.4.3/              fiddle-1.1.6/                 minitest-reporters-1.7.1/           racc-1.8.1/                      rinda-0.2.0/                  typeprof-0.30.1/
actiontext-7.0.0/       base64-0.2.0/           fileutils-1.7.3/              msgpack-1.8.0/                      rack-2.2.17/                     rss-0.3.1/                    tzinfo-2.0.6/
actiontext-7.0.4/       base64-0.3.0/           find-0.2.0/                   mustermann-2.0.2/                   rack-3.1.16/                     rubocop-1.80.2/               un-0.3.0/
actiontext-7.1.3/       benchmark-0.4.0/        formatador-1.2.1/             mutex_m-0.3.0/                      rack-3.2.1/                      rubocop-1.81.0/               unicode-display_width-3.2.0/
actiontext-7.1.5.2/     benchmark-0.4.1/        forwardable-1.3.3/            nenv-0.3.0/                         rack-protection-2.2.2/           rubocop-ast-1.47.1/           unicode-emoji-4.1.0/
actiontext-7.2.2.2/     bigdecimal-3.1.8/       getoptlong-0.2.1/             net-ftp-0.3.8/                      rack-session-2.1.1/              rubocop-performance-1.26.0/   uri-1.0.3/
actionview-7.0.0/       bigdecimal-3.2.3/       globalid-1.3.0/               net-http-0.6.0/                     rack-test-2.2.0/                 rubocop-rails-2.33.3/         useragent-0.16.11/
actionview-7.0.4/       bindex-0.8.1/           guard-2.19.1/                 net-imap-0.5.10/                    rackup-2.2.1/                    rubocop-rails-omakase-1.1.0/  weakref-0.1.3/
actionview-7.1.3/       bootsnap-1.18.6/        guard-compat-1.2.1/           net-imap-0.5.8/                     rails-7.0.0/                     ruby2_keywords-0.0.5/         web-console-4.2.1/
actionview-7.1.5.2/     brakeman-7.1.0/         guard-minitest-2.4.6/         net-pop-0.1.2/                      rails-7.0.4/                     ruby-progressbar-1.13.0/      webdrivers-5.3.1/
actionview-7.2.2.2/     builder-3.3.0/          i18n-1.14.7/                  net-protocol-0.2.2/                 rails-7.1.3/                     rubyzip-3.1.0/                websocket-1.2.11/
activejob-7.0.0/        bundler-2.3.10/         importmap-rails-2.2.2/        net-smtp-0.5.1/                     rails-7.1.5.2/                   securerandom-0.4.1/           websocket-driver-0.8.0/
activejob-7.0.4/        bundler-2.3.14/         io-console-0.8.1/             nio4r-2.7.4/                        rails-7.2.2.2/                   selenium-webdriver-4.1.0/     websocket-extensions-0.1.5/
activejob-7.1.3/        bundler-2.4.19/         io-nonblock-0.3.2/            nkf-0.2.0/                          rails-controller-testing-1.0.5/  selenium-webdriver-4.35.0/    xpath-3.2.0/
activejob-7.1.5.2/      bundler-2.6.9/          io-wait-0.3.2/                nokogiri-1.18.10-x86_64-linux-gnu/  rails-dom-testing-2.3.0/         set-1.1.1/                    yaml-0.4.0/
activejob-7.2.2.2/      capybara-3.40.0/        ipaddr-1.2.7/                 notiffany-0.1.3/                    rails-html-sanitizer-1.6.2/      shellany-0.0.1/               zeitwerk-2.7.3/
activemodel-7.0.0/      cgi-0.4.2/              irb-1.14.3/                   observer-0.1.2/                     railties-7.0.0/                  shellwords-0.2.2/             zlib-3.2.1/
activemodel-7.0.4/      childprocess-4.1.0/     irb-1.15.2/                   open3-0.2.1/                        railties-7.0.4/                  sinatra-2.2.2/
```

Every gem, irrespective of whether it has multiple versions, has its version
number suffixed to the folder. This helps me understand a lot more.

At install time, Ruby would have no *need* to overwrite the older installs.
Python would just overwrite stuff since it doesn't have a concept of versions
*at import time*. Everything in Python is "installed" in the `site-packages`
folder, after all. I'm doing some hand-wavey stuff with the actual
implementation logic, but at the very least `import pandas` doesn't take any
identifier for the version of the package
[its looking for.](https://docs.python.org/3/reference/import.html#searching)

Ruby's version means that you can have multiple versions of a Gem installed globally, and
you do not need to worry about your new project changing something for another project
just because you ran `bundle install`. You do not need isolated environments.

Now, I don't think virtual environments are bad, they're fine if you're the kind of developer
who only has one project going on at any given point of time. But if you're like me, you
probably have a couple dozen `venv`s in your computer at any given point of time, some of
which have the same versions of a particular dependency.

The solution, by the way, is not Docker either.

I've also run into issues when two branches of the same project use different
versions of dependencies. It happens when you're trying to upgrade a dependency
and trying some functionality out, but you need to switch back to the other
branch that uses the older version. It's an ugly world out there, folks.

"The Ruby Way" ensures that you don't have to nuke your local environment to see if you
can upgrade Rails. That line I spent a bit figuring out because I was concerned the tutorial
didn't introduce me to early on?

```
$ bundle config set --local path 'vendor/bundle'
```

Turns out, it was never necessary!

Multiple versions of your dependencies *can* co-exist. There's no reason for
them no to, and you don't need environments taking space all over your
computer. And you certainly don't need a tool that you need to run to find all the
different environments you have created to free up space on your home directory.
[`cargo-sweep`](https://crates.io/crates/cargo-sweep), I'm looking at you.

### `irb` doesn't have a `vim` mode

There isn't much to say about this. I don't expect to use `irb` much. I barely
use the Python interpreter these days. It's not a big loss, but even Python's
interpreter doesn't have vim mode out of the box either. I'd need to play with
`readline`'s settings or use the IPython shell, which is what I use when I
really want to spend time on the interpreter anyway.

### A tiny web server

![Sinatra](/images/posts/ruby/sinatra.png)

Okay, this makes the Flask lover in me giggle.

When I was trying this exercise out, I didn't understand a LOT.

1. The `()` after a function call are optional.
2. Ruby's `blocks` are *like* Python's `contextmanager` blocks, but also no.
3. My head hurts.

{{< note >}}
Your brain hurting in this context is a good thing. It takes a LOT of effort for your
grey cells to unlearn things and be uncomfortable. That *is* a good thing.
I've felt this way learning Rust too, and that was about 4 years ago. I don't think
there's a shortcut to this, and if you want to grow, you learn.
{{< /note >}}

### Rubyisms

#### Method Names?

```ruby
"hello".include? "lo"
```

That gave me pause. In many ways, it reminded me of my trip to Cambodia. The
Khmer language is very similar to Tamil, Sinhalese and Malayalam to an eye that
cannot differentiate between them. In a sad example of the
[Dunning-Kruger effect](https://en.wikipedia.org/wiki/Dunning%E2%80%93Kruger_effect)
I felt confident enough to surmise that the `?` is some sort of function
operator, when the true solution was far, far more simpler.

{{< info title="From the Ruby Docs" >}}
[Method Names (Ruby Docs)](https://docs.ruby-lang.org/en/master/syntax/methods_rdoc.html#label-Method+Names)

Method names may end with a `!` (bang or exclamation mark), a `?` (question
mark), or `=` (equals sign).

{{< /info >}}

Everyone fixates on this when I ask them about Ruby and tells me that `user.admin?` is *sublime*.
I agree, but I wanted to understand whether this was convention or actual grammar that enforced the rules.

{{<info title="From the Ruby docs">}}
[Method Names (Ruby Docs)](https://docs.ruby-lang.org/en/master/syntax/methods_rdoc.html#label-Method+Names)

The bang methods (`!` at the end of the method name) are called and executed just
like any other method. However, by convention, a method with an exclamation
point or bang is considered dangerous. In Ruby’s core library the dangerous
method implies that when a method ends with a bang (`!`), it indicates that
unlike its non-bang equivalent, permanently modifies its receiver. Almost
always, the Ruby core library will have a non-bang counterpart (method name
which does NOT end with `!`) of every bang method (method name which does end
with `!`) that does not modify the receiver. This convention is typically true
for the Ruby core library but may or may not hold true for other Ruby
libraries.

Methods that end with a question mark by convention return boolean, but they
may not always return just true or false. Often, they will return an object to
indicate a true value (or “truthy” value).

Methods that end with an equals sign indicate an assignment method.
{{</info>}}

That cleared it. Those could annotate what a function is *supposed* to do, but doesn't
enforce it in any way. But you could say that the lines are drawn so strongly in
convention that it would seem almost like a rule. The Python alternative, `is_admin`
while it follows the same spirit, doesn't have something tacked on at the end that almost
alienates the idea of not following convention.

But this makes me think. The one thing that everyone told me I'd love going
into Ruby was this syntax. This makes the code readable. I don't have enough
experience writing Ruby to agree or disagree, but it also takes something away
from the developer writing the code. Not Ruby I mean, but this idea that a
language is what pushes you to write good code. I certainly can imagine a
developer not caring for Ruby's conventions and writing absolutely ludicrous
code using these conventions. The SOLID principles have existed for decades and
developers still refuse to follow them.

That doesn't take away from Ruby's goal of coaxing developers to thinking that
it *requires* (Hey, I made a Ruby pun!) them to write code this way, but since
developers do not RTFM anyway, I'm certain that false belief that the Ruby
interpreter will yell at them for doing anything otherwise, (Or maybe DHH will,
who knows?) is a good thing.

#### Blocks

I admit I'm not sure I get blocks quite yet. I'm hoping by the time I write
this part of this post, I'd have understood them somewhat.

```ruby
def twice
  yield
  yield
end


twice {puts "hello"}
```

This outputs:

```
hello
hello
```

Okay, I could do this in Python like so:

```python

def twice(callback):
  callback()
  callback()

twice(lambda: print("hello"))
```

But here's something Ruby can do that just blows my mind.

```ruby
def twice(param_1, param_2)
  puts param_1, param_2
  yield
  yield
end

twice(1,2) {puts "hello there"}

# This prints out
# 1,2
# hello there
# hello there
```

Look at that line really, really, hard. Now let's do that in Python.

```python
def twice(param_1, param_2, callback):
  print(param_1, param_2)
  callback()
  callback()

twice(1,2, lambda: print("hello there"))
```

Now, I'm not expecting Python to do exactly what Ruby does. I don't even think Python *should* do something like this.
But it's a feature that is a very interesting choice. Notice that the Ruby equivalent didn't have a named parameter.

In face, I could even do this:

```ruby
def twice(param_1, param_2, &block)
  puts param_1, param_2
  block.call
  block.call
end

twice(1,2) {puts "hello there"}
```

This is functionally the same, but now we have a named parameter that you `call` explicitly. This named parameter is unnecessary if you just want
to call the function, `yield` works just as well, but you can have a named parameter and use that however you want, perhaps even passing in arguments
when it is called.

This feature is something you don't need until someone shows it to you, like cooled car seating in your car when stuck in Bengaluru traffic in summer.

But what's even cooler is what `&` is doing. Without `&`, blocks are used
through `yield` using a *Rubyism* (my term). It's not an object there. When you
pass a block in with `&`, you're telling the function definition that you can
convert the given block into a *procedure*, a [`Proc` object.](https://docs.ruby-lang.org/en/master/Proc.html)
You'd call this a *callable* perhaps? But what's cool is now this is a Ruby object,
and can be passed around as we see fit.

I'll write more about Procs once I understand them.


#### Loop-de-loop

I think I'm going strongly out of order here, but I started writing this
article after completing the Ruby tutorial and at the starting of the Rails
tutorial. Or how else would you explain me getting to loops now?

When I first saw the `for` loop syntax, I was stumped with this.

![Ruby loops](/images/posts/ruby/loops.png)

I understand that no one writes Ruby like this, but that's besides the point.
The first loop, when consumed, *evaluates* to the loop itself. It evaluates to `0..1000`.
And so does the second one. And so will every run through this loop!

I could do this:

```ruby
x = for y in 0..5
  puts y
end
puts x == 0..5
```

And this would be true? That's magic!

I've seen this before though, and it's a good segui into how Rust has a lot of
Rubyisms, but I'll talk about that when I talk about module resolution.

#### Module Resolution
Now I'm stepping into things I *really* like.

You have the `require` method, which loads a gem from the
[`$LOAD_PATH`](https://docs.ruby-lang.org/en/3.4/globals_rdoc.html#label-24LOAD_PATH+-28Load+Path-29),
or you can use `relative_require`, which loads the module from the current path. 

I *love* `relative_require`. I've always hated the `from .. import module` in
python syntax a lot. I ensure my modules don't have that level of entanglement,
but it's easy to see why developers would use. There's nothing wrong in it,
as long as you've invested time into the language.

That being said, there's one bit that really tripped me up in Rust that I later
realized came from Ruby and that made me feel violated as someone who "thought Python".

```rust
use log::{debug, error, log_enabled, info, Level};

env_logger::init(); // watch this line

debug!("this is a debug {}", "message");
error!("this is printed by default");

if log_enabled!(Level::Info) {
    let x = 3 * 4; // expensive computation
    info!("the answer was: {}", x);
}
```

This above snippet is in Rust, and it's from the docs from [`env_logger`](https://docs.rs/env_logger/latest/env_logger/).
This tripped me up when I first read it, because in all the tutorials I'd read so far, everyone used `use $module`
and that seemed to mimic `import $module` in Python.

This one line `env_logger::init()` felt *wrong*.

Where did this come from? I didn't *import* (*sic* `use`) `env_logger` anywhere.

```rust
use env_logger

env_logger::init()
```

I thought this is how Rust was written. I asked about this on Reddit and the first response was, "Ah, you haven't used Ruby have you?"

That was back in 2021 I think.

To my shock, this was considered *natural* in Ruby? I had **strong** feelings against it. I thought `import $module` made it clear
where it came from. Why would you not want to state that at the top of the file?

But after using Rust for a while, I've mellowed on this. In fact, I even like
this method, since it makes it clear where something has come from as well.

```ruby
require 'logger'

logger = Logger.new(STDOUT)
logger.info("hello")
```

Having `require 'logger'` bring the `Logger` class into the namespace feels
like it's going to be hard to say where a particular object comes from. 

```ruby
require 'logger'
require 'lumberjack'

logger = Logger.new() # which Logger is this? It's from `lumberjack`, because that was the last one in.
```

I'm still not sure how I'd address this.

I haven't used modules enough to have stronger opinions, but I'm certain to
write about this later.

#### `return` is Optional

Another Rubyism I noticed in Rust was the fact that `return` is optional. This
took me a bit of time to learn in Rust as well, but since I'd seen it there, I
was less shocked by it here. In fact, given how loops resolve into values, I
can agree that it's quite elegant.

#### `include`

Now for something I *love*. I'm going to use an example from the Learn Enough Ruby to be Dangerous tutorial.

```ruby

module Palindrome
  # Returns true if the string is a boolean, else false
  def palindrome?
    processed_content == processed_content.reverse
  end

  private

  # cleans the string for testing if it's a palindrome
  def processed_content
    to_s.downcase.gsub(/[^a-z0-9]/, "")
  end
end

class String
  include Palindrome
end

class Integer
  include Palindrome
end
```

Now *this* is elegant. Using `obj.class.ancestors` (a method I absolutely love after `is_a?`)
for `String`, I get
`[String, Palindrome, Comparable, Object, Kernel, BasicObject]`.

For `Integer`, I get `[Integer, Palindrome, Numeric, Comparable, Object, Kernel, BasicObject]`.

This makes me so happy, since Ruby injected `Palindrome` into the ancestor chain, so that integers are _still_
integers, instead of needing a new constructor like `Palindrome.new(10)`, every Integer we use has become
a Palindrome.

But that also brings us to the monke.

#### Monkey Patching

Ah yes. If Ruby is on Rails, Rails is on the monke.

There's so damned much I think I'll want to say about this, and whether it's good or bad, but for now, I'll accept this as
a Rubyism. I know that's not a climactic response to this, but I think it's something I might learn to love but be wary of.
Like I said above, I really like the `include` method of injecting behaviour into an object.

Thankfully though, I've loved Rust's `impl` syntax.

```ruby
class Integer
  def squared
    self * self
  end
end
```

```rust
impl i32 {
    fn squared(self) -> i32 {
        self * self
    }
}
```

But what I'm worried about is that Rust does this at compile time, and that
prevents one library (Rust's crates) from overwriting another crate's behaviour
at runtime. But with Ruby, we can truly let the monke loose.

## Where to next?

I'm still learning Rails, so I will have a lot to say about that when I
complete it and start using it in a while. I hope to write another post a month
later, showcasing how I feel so far about Ruby.

For what it's worth, I'm going to try to grok the Rails way. I would like to
understand where the bones are, and I am sure that there are a lot of parallels
to Django. I haven't used enough Django though, just a smidge, but I think
understanding where things come from and where they go will be a challenge.
I want to understand these things because that'll drive home first-principles about
Ruby and Ruby on Rails.

To paraphrase what a friend and I said together, coming from Python to Ruby
felt like moving to another city, I feel a huge culture shock in a lot of ways.
But at the same time, it feels like I'm in a new city where if you have a
problem with the potholes on the roads, you're welcome to patching them
yourselves.

---

## Other Posts in This Series

- [Returning from Ruby Blocks, Procs and Lambdas]({{< ref "ruby-block-return.md" >}})
- [Ruby Blocks]({{< ref "ruby-blocks.md" >}})
- [Some Smalltalk about Ruby Loops]({{< ref "ruby-loops.md" >}})
- [Symbolic Ruby]({{< ref "ruby-symbols.md" >}})
