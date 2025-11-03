---
date: "2025-11-03T15:36:29+05:30"
draft: false
title: "A Soiree into Symbols in Ruby"
description: "A Pythonista opens `irb` and looks at all the symbols in Ruby. Or so the joke begins."
tags:
  - "ruby"
---

## Symbols and Why You Should Care

I should start, aptly, with [the manual.](https://ruby-doc.org/3.4.1/Symbol.html)

> A `Symbol` object represents a named identifier inside the Ruby interpreter.

Okay, it's a token of a sort, I think.

I've been befuddled when seeing `:name` instead of `name` and I didn't know what it was at first.
I spent some time reading Michael Hartl's Learn Enough Ruby and I cannot really say I understood Symbols,
so I wanted to RTFM.

> The same `Symbol` object will be created for a given name or string for the duration of a program's execution,
> regardless of the context or meaning of that name. Thus, if `Fred` is a constant in one context , a method in another,
> and a class in a third, the `Symbol` `:Fred` will be the same object in all three contexts.

{{< code language="ruby" source="code/ruby-symbols/symbol_identity.rb" >}}

Running this code shows:

```
18152204
18152204
18152204
```

All three symbols have the **exact same object_id**, proving they're the same object in memory despite `Fred`
being a class, a constant, and a method in different contexts.

Does that mean all three symbols are the exact same object? At first glance, `:Fred` seems to be the thing that identifies
the class, variable or the method. But let's expand our example to version 2, where each module has a method that uses
the symbol `:Fred` to interact with whatever `Fred` means in that context.

{{< code language="ruby" source="code/ruby-symbols/symbol_identity_v2.rb" >}}

Running this shows:

```
=== Using the symbol :Fred in different contexts ===

In module One, using symbol :Fred to get the class
const_get(:Fred) returns: Class
Creating instance: Hello from Fred the class!
Returned symbol object_id: 18152204

In module Two, using symbol :Fred to get the constant
const_get(:Fred) returns: Integer with value 42
Calculating 42 * 2 = 84
Returned symbol object_id: 18152204

In module Three, using symbol :Fred to call the method
send(:Fred) returns: I'm the Fred method!
Returned symbol object_id: 18152204

=== The symbol :Fred is the same everywhere ===
All three object_ids match: true
```

What is even going on here? `:Fred` has the same `object_id` but when we consume it, it calls different things.
I originally assumed `:Fred` was like atoms in Erlang, which I have a bare understanding of. But that doesn't seem
to be the case.

To _reiterate_ if you haven't understood, `:Fred` is a `Symbol` object. It doesn't _directly_ reference the actual
method, class or variable that we are seeing in these code snippets, but it's pointing to the name of these objects
itself. In a real-world setting, you could conceptualize `:Fred` as a name tag itself with "Fred" written on it.
In one situation, `Fred` could be the key in a dictionary that you could look up. In another it could be a name in a
contacts app, or a name in a class roster at university. The symbol `:Fred` is the word itself, not what it points to.

It's Ruby's way of turning identifiers into first-class objects. In [the loops post]({{< ref "ruby-loops.md" >}}),
I've written about `.send(:times)`. Ruby makes this possible _because_ `:times` is the method name as an object.

In Python, you'd need to use strings for this purpose. There's no sense of meaning in the string other than the context
that tells someone reading your code that you're trying to get a method or attribute. And even that is a frail way of
expressing intent in my opinion.

| Python                                                       | Ruby                                                  |
| ------------------------------------------------------------ | ----------------------------------------------------- |
| `getattr(obj, "method_name")`                                | `obj.send(:method_name)`                              |
| `"method_name"` is a string - could be data or an identifier | `:method_name` is a symbol - explicitly an identifier |

I've written before about [Ruby's preference for protocol over syntax]({{< ref "ruby-loops.md" >}}).
This falls perfectly in line with that.

I want to understand symbols a lot better though. What drove this design choice?

Smalltalk method names are symbols, message dispatch is a symbol-based lookup. That's yet another thing Ruby inherited
from it. Lisp/Scheme have symbols as first-class citizens. All function names are symbols. Clojure has `:keyword` style
symbols just like Ruby. The dispatch mechanics are also very similar.

When I first started learning Ruby last month, I looked at the `:symbol` syntax and my brain immediately thought of
Erlang's **atoms.** Erlang calls them `atom`, and Elixir (which runs on the Erlang VM) uses the more familiar `:atom`
syntax.

Erlang though, has atoms rooted even more deeply into its syntax. Consider the following Elixir code:

```elixir

# booleans are atoms
true # actually :true
false # actually :false

# return valules are tagged with atoms
{:ok, result}
{:error, result}

# Pattern matching uses atoms as tags
case File.read("data.txt") do
  {:ok, contents} -> process(contents)
  {:error, reason} -> handle_error(reason)
end

# module and function names are atoms

:lists.map(fn x -> x * 2 end, [1, 2, 3])

```

Erlang's atoms are designed for its actor model. They are used to tag messages and data structures for pattern matching
in concurrent systems. Using `:ok` or `:error` isn't just convention, it's how Erlang allows communication between processes.

Ruby's symbols are designed for metaprogramming. With symbols, identifiers become objects you can manipulate at runtime.
`send(:method_name)` or `define_method(:foo)` would not work without symbols as first-class citizens.

Interestingly, Both languages share a historical bug: creating symbols/atoms dynamically from user input could exhaust memory,
since the symbol/atom table was never garbage collected.
[Erlang still warns about this in its efficiency guide](https://erlang.org/documentation/doc-5.8.4/doc/efficiency_guide/advanced.html),
as atoms remain permanent for the VM's lifetime. Ruby [fixed this in version 2.2](https://bugs.ruby-lang.org/issues/7791)
by adding garbage collection for dynamically created symbols.

## Symbols in Ruby

I think the first place you'd see symbols in Ruby are in hashmaps.

```ruby
user = { "name" => "Alice", "age" => 30 }  # String keys
user = { :name => "Alice", :age => 30 }    # Symbol keys
```

These are two ways to create hash objects with different key types. But when you're writing software that
_indicates intent_, there's a glaring difference between the two.

`:name` is a stronger indication of what you want to do than `'name'`.

Modern ruby forgoes the arrow syntax to allow you to use symbols like this.

```ruby
user = { name: "Alice", age: 30 }
```

That uses symbols for `:name` and `:age` internally.

Symbols aren't interchangeable though.

```ruby
user = { name: "Alice", age: 30 }
puts user[:name] # Alice
puts user["name"] # nil
```

But where they're really powerful is when you _reuse the keys_.

```ruby
1000.times { { "name" => "Alice" } }  # Creates 1000 "name" strings
1000.times { { name: "Alice" } }      # Uses the same :name symbol
```

Remember what I said about the symbol reusing the same memory space?
The second example uses only one instance of `:name`, while the first one
creates `"name"` 1000 times.

### Metaprogramming 101

Another example of how symbols empower Ruby is with the helper methods I use
within a class.

```ruby
class Person
  attr_accessor :name
end
```

This is equivalent of writing:

```ruby
class Person
  def name
    @name
  end

  def name=(value)
    @name = value
  end
end
```

In this example, Ruby uses the symbol `:name` to dynamically create getter and setter methods at runtime.

`attr_accessor` is a class method that takes a symbol and uses metaprogramming to define methods.

```ruby
class Module
  def attr_accessor(name) # name is a symbol here
    # define getter method
    define_method(name) do
      instance_variable_get("@#{name}")
    end

    # define setter method
    define_method("#{name}=") do |value|
      instance_variable_set("@#{name}", value)
    end
  end
end
```

I'm hand-waving a lot of the details there, but this is a very clean example of
how powerful symbols are.

While it is easy to think of `attr_accessor` as special syntax, it _is just a method
that takes symbols_ as arguments and writes code at runtime.

### Fun with Symbols

I felt I still didn't understand the power of symbols over strings and accessing
attributes with them so I spun up `irb` and decided to write some Ruby.

#### Symbols are callable

I've seen this before:

```ruby
[1,2,3].map(&:to_s)
```

I didn't think much of it, but now I understand that this calls `:to_s` on these
items. That's cool, but what else can I use this way?

```ruby
add_one = :+.to_proc
add_one.call(5,1) # 6
```

I knew that operators are methods, we can do `5.+(3)` instead of `5 + 3`, which is why this works. I understood that but seeing it like this... _is so **cool!**_

The `&` operator calls `.to_proc` on the symbol, which returns a proc that calls the method: `{ |obj, arg| obj.send(:+, arg) }`

Am I rambling? I'm certain I am, but let's go on.

#### Can I chain symbols?

I've done stuff like this:

```ruby
["hello", "world"].map(&:upcase).map(&:reverse)
```

But we can also do this.

```ruby
["hello", "world"].map { |s| s.upcase.reverse }
```

Then does that mean we can do this?

```ruby

users.map(&:name).map(&:upcase) # This works
users.map { |u| u.name.upcase } # This is more efficient though
```

It's always nice to ask ourselves if we _should_, just because we _could_.

#### More Operator Foo

```ruby

5.send(:+, 3)
10.send(:*, 2)
[1,2].send(:<<, 3)
```

But wait...

```ruby
operators = [:+, :-, :*, :/]
operators.map { |op| 10.send(op, 2)}
```

Well, if I see code like that in a PR, I'm going to call DHH personally. I don't have his number though.

#### Wait, where are the enums?

I have been wondering, where are the Enums in Ruby? Rust loves Enums, and
any good python code needs to leverage it.

I think I've seen enums in Rails, and yes I know I haven't touched that yet in my posts but I'm going to, soon.

```ruby
# without rails

status = :pending # or :active, or :completed

# In Rails

class User < ApplicationRecord
  enum status: [:pending, :active, :suspended, :deleted]
end

user.status # :pending
user.pending? # true
user.active! # Changes status to active
```

I just had to check the [Rails source code to see if it was actually a new
type or...](https://api.rubyonrails.org/v7.2.2/classes/ActiveRecord/Enum.html)

```ruby
# File activerecord/lib/active_record/enum.rb, line 216
def enum(name = nil, values = nil, **options)
  if name
    values, options = options, {} unless values
    return _enum(name, values, **options)
  end

  definitions = options.slice!(:_prefix, :_suffix, :_scopes, :_default, :_instance_methods)
  options.transform_keys! { |key| :"#{key[1..-1]}" }

  definitions.each { |name, values| _enum(name, values, **options) }

  ActiveRecord.deprecator.warn(<<~MSG)
    Defining enums with keyword arguments is deprecated and will be removed
    in Rails 8.0. Positional arguments should be used instead:

    #{definitions.map { |name, values| "enum :#{name}, #{values}" }.join("\n")}
  MSG
end
```

Dang it, Ruby. You never cease to amaze me!

That's a _method!_ This is so cool. I was just thinking how cool
it would be to define an Enum in ruby so that I could give it a list of accepted
values as symbols and it would then say something is not a valid option, and
this exists. So cool!

## Symbols and what they mean

You don't have to be Robert Langdon to appreciate symbols in Ruby. I could spend
so much more time on them, writing about `Symbols.all_symbols` (Ruby's internal symbol table), method introspection (with `method()`, `.respond_to?`), and runtime reflection. I am sure I'll have more to say about symbols in the future, once I start writing about metaprogramming. Can you tell I'm excited about that post already?

---

## Other Posts in This Series

- [Ruby]({{< ref "ruby.md" >}})
- [Returning from Ruby Blocks, Procs and Lambdas]({{< ref "ruby-block-return.md" >}})
- [Ruby Blocks]({{< ref "ruby-blocks.md" >}})
- [Some Smalltalk about Ruby Loops]({{< ref "ruby-loops.md" >}})
