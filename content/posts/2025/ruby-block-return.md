---
date: '2025-09-29T11:55:18+05:30'
lastmod: '2025-10-20T22:33:22+05:30'
draft: false
title: 'Returning from Ruby Blocks, Procs and Lambdas'
description: 'How does `return` work within blocks, procs and lambda?'
tags:
  - "ruby"
---

I was watching a [youtube video about Ruby Blocks, Procs, and
Lambdas](https://www.youtube.com/watch?v=SADF5diqAJk) and noticed something
interesting.

Let's do this with some Ruby code.

```ruby
fruits = ["apple", "orange", "kiwi", "mango", "banana"]

fruits.each do |fruit|
  puts "I like to eat #{fruit}" unless fruit == "kiwi"
end
```

This is a simple block, and if you don't feel you understand them because
you're new to Ruby (like me at the time of this writing), you should read [this
StackOverflow answer](https://stackoverflow.com/a/4911787).

Let's add a return to this.
```ruby
fruits = %w[apple orange kiwi mango banana]

fruits.each do |fruit|
  puts "I like to eat #{fruit}" unless fruit == "kiwi"
  return "unacceptable" if fruit == "kiwi"
end
```

The `return` here works like a `break` in a traditional loop. It doesn't
really `return` anything since the `each` method isn't returning
anything. However, this exits out of the scope that's using the block.
Which means that this `return` is just exitting out of my script here.

Let's put this inside a function to make things easier for us to snoop around.

```ruby
def main
  fruits = %w[apple orange kiwi mango banana]

  fruits.each do |fruit|
    puts "I like to eat #{fruit}" unless fruit == 'kiwi'
    return fruit if fruit == 'kiwi'
  end
end

fave_fruit = main
puts "I love #{fave_fruit}!"
```

Here, the method exits after 2 runs, and I get the value of `fave_fruit`.

The `return` exits us out of the scope that it's called it. Quite neat.
But I'm certain this is going to trip me up some day so I'm writing it down.

If I were to do this with a Proc:

```ruby
def main
  fruits = %w[apple orange kiwi mango banana]

  fruit_proc = Proc.new do |fruit|
    puts "I like to eat #{fruit}" unless fruit == 'kiwi'
    return fruit if fruit == 'kiwi'
  end

  fruits.each(&fruit_proc)
  puts "I've processed all the fruits."
end

fave_fruit = main
puts "I love #{fave_fruit}!"
```
```
$ ruby code/posts/ruby-block-return/ex_1.rb
I like to eat apple
I like to eat orange
I love kiwi!
```

This block does the same thing, with procs. Notice how the `puts "I've
processed all the fruits."` line is not printing.

Let's try this with a lambda:

```ruby
def main
  fruits = %w[apple orange kiwi mango banana]
  fruit_lambda = lambda do |fruit|
    puts "I like to eat #{fruit}" unless fruit == 'kiwi'
    fruit if fruit == 'kiwi'
  end
  fruits.each(&fruit_lambda)
  puts "I've processed all the fruits."
end
fave_fruit = main
puts "I love #{fave_fruit}!" unless fave_fruit.nil?
```

The output is very different now.
```
❯ ruby code/posts/ruby-block-return/ex_1.rb
I like to eat apple
I like to eat orange
I like to eat mango
I like to eat banana
I've processed all the fruits.
```

It doesn't get the return value `fruit if fruit == 'kiwi'` at all now.

A `lambda` is useful when you want to eject only out of the current loop call,
not the entire scope that you're calling this from.

I don't really have many more observations, but if I do, I'll write another
post.

---

## Other Posts in This Series

- [Ruby]({{< ref "ruby.md" >}})
- [Ruby Blocks]({{< ref "ruby-blocks.md" >}})
- [Some Smalltalk about Ruby Loops]({{< ref "ruby-loops.md" >}})
