---
date: "2025-10-20T10:10:10+05:30"
lastmod: "2025-10-20T22:33:22+05:30"
draft: false
title: "Some Smalltalk about Ruby Loops"
description: "Sending a message about why you shouldn't write `for` loops in Ruby."
tags:
  - "Ruby"
---

Let's talk about loops.

```ruby
for i in (1..10) do
  puts "i= #{i}"
end
```

Three weeks ago, when I was new to Ruby, I focussed on this. This was a loop. I
mean, I come from Python and that's what loops look like.

I was wrong, wasn't I?

```ruby
10.times { |i| puts "i = #{i}" }
```

If you haven't read [my post on Ruby blocks,]({{< ref "ruby-blocks.md" >}}) you should. And then come back to this.

Damn, Ruby. Why do you need to be scratching my brain in ways I didn't think were possible all the time?

Where's that meme?

![Khaby Lazy Meme](/images/posts/ruby/loops-khaby.jpg)

What's so great about this? Either you've never written Ruby before or you have your eyes closed.

That wasn't a "loop" now was it? It looks like you're simply saying "do this 10
times", but I'm fresh off the heels of diving into blocks and I know that
`.times` is *a method call* and the `{ |i| puts "i = #{i}" }` is a *block.*

We can inspect the class of a Ruby object like this:

```ruby
puts 10.class # Integer
puts 10.respond_to?(:times) # true
```

Those are method calls. But what *is* a method call?


I come from Python, and in Python, a method call looks like this:
```python
object.method(argument)
```

I'm hand-waving a lot of the details away, but here, we're calling a method on
an object. The object *has* the method. The method *does something*.

In Ruby, that analogy isn't exactly right. You're not calling a method. You're
sending a message.

```ruby
10.times { puts "hi" }
10.send(:times) { puts "hi" }
```

If you use `.send` you might understand this better. You are sending the
message `:times` to the object `10`.

The object 10 receives that message and then decides what to do with it. You
could say this is a segue into philosophy.

How do you code? You write logic in a form that the computer can understand,
and you use the tools you've been given by the language of your choice. It's
electronic telepathy, albeit an extremely broken form of it. The code
represents what you want to do.

By saying:

```python
for i in range(10)
  print(f"i = {i}")
```

You are not saying "print 5 times", although that's what your brain interprets
it as.

You are saying:

* Make an iterable object that yields integers from 0 to 9.
* Iterate through this object, and assign the yielded value to i at each turn.
* Upon each iteration, print `"i = #{i}"` to the screen. 
* Break out of the loop when you exhaust the iterator.

That's a mouthful. It *might* indicate the same thing as:

```ruby
10.times { |i| puts "i = #{i}" }
```

But it isn't.

In the ruby block, you are saying:

* Call the `:times` method on the `Integer` object of value `10`;
* For each iteration, pass the block `{ |i| puts "i = #{i}" }`.

That... is lesser?

No, it's *different*.

In Python, you indicate your purpose by *controlling* the loop. The code
doesn't attach the intent to the number 10 or to the `range(10)` iterator.

In Ruby, you are *asking the object to do something*. You are directly
attaching the meaning of your code to the *`Integer` of value `10`*.

`.send` is the inner mechanic that orchestrates this. If you've done any amount
of Python metaprogramming, you might have seen something like

```python
method = obj.getattr("method_name")
method.__call__(args)
```

Note the difference in names here. It's subtle enough to blink and miss. Python
says `__call__`. Ruby says `__send__`.

If you've sat on the Erlang fence for as long as I have (I'll learn it yet one
day!), your *message passing* alarms are going off, aren't they?

But this isn't from Erlang, in fact there's nothing similar besides the
metaphor, it's from Smalltalk. And this style of programming philosophy is
*Protocol over Syntax*.

## Meet Smalltalk

I've had a bunch of people tell me that Ruby is inspired by
[Smalltalk](https://learnxinyminutes.com/smalltalk). I'd never written or read
a line of Smalltalk before today, but I thought I'd check it out to understand
Ruby's philosophy a little.

```smalltalk
5 timesRepeat: [ Transcript show: 'Hello' ].
```

Okay, that's familiar enough, isn't it?

```smalltalk
1 to: 10 do [:i | Transcript show: i].
```

Okay, that looks similar to:

```ruby
1.upto(10) { |i| puts i }
```

How about iterating over a list?

```smalltalk
#(1 2 3 4 5) do: [:each | Transcript show: each ].
```

```ruby
[1, 2, 3, 4, 5].each { |each| puts each }
```

To understand this paradigm, consider a `PseudoInteger` class that behaves like
an integer but overwrites the `times` method. For brevity I'm not going to
implement any of the other methods.

```ruby
class PseudoInteger
  def initialize(value)
    @value = value
  end

  def times(&block)
    puts "I'm going to run #{@value} times"

    @value.times do |y|
      block.call(y)
    end
    puts "Done with the block calls."
  end
end

i = PseudoInteger.new(10)
i.times { |x| puts x }

# I'm going to run 10 times
# 0
# 1
# 2
# 3
# 4
# 5
# 6
# 7
# 8
# 9
# Done with the block calls.
```

I've said this earlier, but here, the object `PseudoInteger` *controls the
iteration* through `.times`. But what if the object chose to lie to you about
what it's doing?

```ruby
class LyingPseudoInteger
  def initialize(value)
    @value = value
  end

  def times(&block)
    puts "I'm going to run #{@value} times"
    block.call(0)
    puts "Done with the block calls."
  end
end

i = LyingPseudoInteger.new(10)
i.times { |x| puts x }

# I'm going to run 10 times
# 0
# Done with the block calls
```

The new class `LyingPseudoInteger` *does not do what it says it does*. 

Leaving the handling of the loop to the method allows us to add behaviour to
loops that are controlled by the object and not by the user. This is a nice way
to add side-effects.

*But what does this have to do with message-passing?*

In most languages, methods are **bound to objects at compile time** (or at
least, the languages pretend they are). In Smalltalk, and by association Ruby,
methods are looked up at runtime in response to messages.

In Python, Java or C++, calling `object.method()` asks the compiler to find the
method in the class and call it.

In Ruby, `10.times { puts 'hi' }` is **literally interpreted as
`10.send(:times) { puts 'hi' }`.**, which is equivalent to
[`10.public_send(:times) { puts 'hi' }`](https://stackoverflow.com/questions/30401970/what-is-the-difference-between-rubys-send-and-public-send-methods).

The `:times` is a symbol. I haven't written about Symbols yet, that's a whole
other rabbithole that I have yet to go down in.

But with this sort of implementation, we *could* (but shouldn't), do **this**:

```ruby
class Integer
  undef_method :times
end

10.times { puts 'hi' } # -> NoMethodError : undefined method 'times' for 10:Integer
```

The Ruby interpreter is saying "I have received a message `:times` but I don't
know how to respond to it."

But I'm still not convinced, so let's try this.

```ruby
class Integer
  def method_missing(method_name, *args, &block)
    puts "I received a message I don't understand: #{method_name}"
    puts "I could do anything here - respond, forward it, ignore it..."
    puts "This is message passing - the message exists independently of the method"
  end
end

10.foobar # I received a message I don't understand: foobar...
```

In traditional method calling, this would be a compile-time error. This method
doesn't exist, so compilation fails. In message passing, the message got sent.
The object receives it and then says "I do not know this message." This is what
we can catch.

But Python also looks up methods at runtime. Does that mean Python also does
message passing?

Not quite.

In Python, you'd access methods like this:

```python
class MyClass:
    def my_method(self):
      return "Hello"

obj = MyClass()

# Methods are just attributes here.
print(obj.__dict__) # {}
print(MyClass.__dict__) # {... 'my_method': <function>...}

method = getattr(obj, "my_method")
method()
```

However, `getattr` is generic, it's for *all* attributes. Not just methods. You
could call `getattr(obj, 'anything)` and get a property called `anything` on the
object.

In Python, "calling a method" is interpreted as "look up an attribute that implements `__call__`".

Ruby does something different.

```ruby
class MyClass

  def my_method
    "hello"
  end
end

obj = MyClass.new
```

You can *explicitly SEND messages*: `obj.send(:my_method)`.

The language has built-in constructs for message handling.

```ruby
obj.respond_to?(:my_method)     # -> Can you respond to this message?
obj.method(:my_method)          # -> Give me the method that corresponds to this message
```

And we can intercept unknown messages with `.method_missing` as shown above.
Ruby *treats* "calling a method" as "sending a message to an object."

While Python is also interpreted, any attempt to attach middleware to this sort
of method resolution is wrapped in *attribute access interception*. You are
always *getting attributes*.

```python
class Spy:
    def __getattribute__(self, name):
        print(f"Looking up attribute: {name}")
        return super().__getattribute__(name)

    def hello(self):
        return "hi"

spy = Spy()
spy.hello()
# Looking up attribute: hello
# "hi"
```

In Ruby, you're *intercepting messages*.

```ruby
class Spy
  def method_missing(name, *args, &block)
    puts "Received message: #{name}"
    super
  end

  def hello
    "hi"
  end
end

spy = Spy.new
spy.hello
# "hi"

spy.foobar
# Received message: foobar
```

The difference is in the philosophy. Python gets the attribute `method` on
`obj` and if it's callable, it calls it. Ruby sends the `:method` message to
`obj`. This emphasizes object autonomy: the object receives a message and
chooses its response.

This is taken to the extreme when you realize that Ruby has primitives
(Symbols) that you can use to treat message passing like the first class
concept that it is in Ruby.

```ruby
msg = :times
puts msg.class          # Symbol

# You can get the method that will respond
method = 10.method(msg) 
puts method.class       # Method

# You can call it later
method.call { |i| puts i }

# You can see what messages an object responds to:

puts 10.methods.grep(/time/) # [:times]
```

In Python, doing this is rather roundabout.

```python
method = getattr(10, "times", None)

# method is None

# You can use `dir()` to get all the attributes in an object, but you'd have to filter them for methods yourself.
```

## But what *is* a loop?

In Ruby, you can iterate through anything that *includes* `Enumerable`.

```ruby
class Countdown
  include Enumerable
  def initialize(from)
    @from = from
  end

  def each
    current = @from
    while current > 0
      yield current
      current -= 1
    end
  end
end

c = Countdown.new(5)
c.each { |x| puts x }
c.map { |x| x * 2 }
c.select { |x| x.even? }
c.reduce(:*)
```

By including `Enumerable` and by implementing `each`, we get access to so many
methods that we didn't need to manually implement. This is the same as the
Collection protocol from Smalltalk - implementing `:do:` gives us the methods
we need.

## Why `For` Feels Like It Doesn't Belong

By now, you should look at `for` as an *alien* thing. It doesn't feel like it belongs. But why is that?

`for` is syntax, and Ruby, by design, encourages message passing.

```ruby
[1, 2, 3].each { |x| y = x }
puts y                        # NameError

for x in [1, 2, 3]
  y = x
end
puts y # 3
```

Using `for` pollutes the namespace, spilling variables over to the including
scope. But that's not the only thing. `for` is syntactical sugar. It's not
message passing.

In a sense, the familiarity of the loop construct deceives you. I reached
towards `for` in my first days learning Ruby thinking that's the way to loop.
Yet, Rubyists encouraged me to look into `.each` and `.times` to write loops. I
wanted to understand that choice better. It's a different paradigm, because you
*could do* something in Python that does the same thing, but it's still not the
same. You'd still shoehorn in the loop syntax and use that. And of course it
also begs the question: why should you?


## The Beauty of Protocol Over Syntax


In Smalltalk, there is no `for` loop. Everything is message passing.

To loop 5 times you *send* `:timesRepeat` to `5`.

To iterate over a collection, *send* `:do:` to the collection.

To filter, *send* `:select:` to the collection.

Matz took this philosophy and ran with it.

```ruby
5.times { puts 'Hello' }         # timesRepeat:
[1, 2, 3].each { |x| puts x }    # do:
[1, 2, 3].select { |x| x.even? } # select:
[1, 2, 3].map { |x| x * 2 }      # collect: 
```

Understanding the message passing philosophy helps you map Ruby's choices.

- Integers have `.times` because they need respond to iteration messages.
- Arrays have `.each` for the same reason.
- Adding `.countdown` to an Integer teaches it to respond to a new message.
- Adding `include Enumerable` to a class and implementing `.each` gives you the
ability to send multiple types of iterative messages to objects of that class,
because that implements the Collection Protocol.
- `for` doesn't send messages the same way.


Writing Ruby in Ruby and Python in Python is important. I've been a strong
believer of learning how to write idiomatic code in a programming language. You
cannot transplant features between languages without coding with an "accent".

Asking an object to iterate over itself allows objects to develop interfaces that dictate
how to iterate. This is at the heart of the message passing paradigm that Ruby and Smalltalk
use.

Writing Ruby encourages you to embrace this, and that helps you build a sense of style that it
comes with.

I've noticed this of Ruby. Python, a language I love, looks different depending
on who's writing it. Ruby coaxes you to develop this sense of style, whether
you want to spend a weekend learning *why* it does this or not.

And now, when I see:

```ruby
10.times { |i| puts "i = #{i}" }
```

I do not see a loop anymore. I see an object responding to a message. I see
Smalltalk's legacy. I see protocol over syntax.

---

## Other Posts in This Series

- [Ruby]({{< ref "ruby.md" >}})
- [Returning from Ruby Blocks, Procs and Lambdas]({{< ref "ruby-block-return.md" >}})
- [Ruby Blocks]({{< ref "ruby-blocks.md" >}})
