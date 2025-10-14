---
date: '2025-10-14T18:17:51+05:30'
title: 'Ruby Blocks'
description: 'How to start really getting Ruby, especially blocks.'
tags:
  - "ruby"
cover:
  image: "/images/posts/ruby/blocks-everywhere.png"
---

I think I'm really starting to *get* Ruby. At least I can read Ruby and tell you what's happening.

I haven't read a single tutorial on RSpec, the testing framework we use at
Chatwoot for the Rails backend. I didn't want to spend too much time in
tutorial hell, and I'm sure that I *should* read more about it soon.

I've written about Ruby blocks [before]({{< ref "ruby-block-return.md" >}}), but I think it bears repeating. 
This is a method call with a block as an input.

```ruby
perform "input_value" do
  puts "I'll get called with that function"
end
```

Don't worry about how the function is *implemented* for now. I'm hand-waving this so that you can
notice something.

This is also a method call with a block as an input.

```ruby
it "can do something" { puts "The cake is a lie" }
```

But here's something else that's a method call with a block as an input.

In `lib/calculator.rb`:

```ruby
class Calculator
  def add(a, b)
    a + b
  end
end
```

In `spec/calculator_spec.rb`:

```ruby {hl_lines=["4-7"]}
require_relative "../lib/calculator"

RSpec.describe Calculator do
  it "adds two numbers" do
    calc = Calculator.new
    expect(calc.add(2, 3)).to eq(5)
  end
end
```

The highlighted lines include a method call to `it` with a block.

Look at that again. It's a *method* call.

That is crazy. It is so sublime that I can't explain how excited this makes me.
If I have to teach [Ruby to a Pythonista]({{< ref "ruby.md" >}}) I'd ask them
to ensure they *see* what this is. Until you grok this, it won't matter how
much you try to understand Ruby. Ruby's readability comes from this feature.
I'm still not sold on RSpec though, but I *am* open to learning it because it
is, ultimately, Ruby.

