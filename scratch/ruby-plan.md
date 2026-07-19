# Ruby Blog Post Series Plan

A roadmap for exploring Ruby's design philosophy, coming from a Python
background.

## Post 4: Ruby Loops - Protocol Over Syntax

Ruby doesn't really have loops the way Python does. Sure, there's a `for`
keyword, but nobody uses it, and it's just syntactic sugar that delegates to
`.each` anyway. The real story is about Ruby's philosophy: protocol over syntax.

When you implement `.each` on a class, you don't just get iteration - you unlock
an entire ecosystem. Include the `Enumerable` module and suddenly your class has
`map`, `select`, `reduce`, `filter`, `any?`, `all?`, and 40+ other methods. All
for free. All because Enumerable's methods call your `.each` implementation.

This is Ruby's secret sauce: instead of baking features into language keywords,
everything is methods on objects following protocols. The `for` loop? It
requires `.each`. Custom iteration patterns? Just methods that take blocks. Want
to iterate over your own data structure? Implement `.each` and you're done.

Compare this to Python where `for` is a language keyword that uses the iterator
protocol (`__iter__` and `__next__`), but you can't easily extend it. Ruby's
approach is more composable - iteration is just another method, and methods
chain naturally.

The post will explore:

- How `for` loops are syntactic sugar for `.each`
- The Enumerable protocol and what you get for free
- Building custom iterable classes
- Comparison with Python's iteration model
- Why `5.times { }` and `10.downto(1)` work
- Internal vs external iteration
- Method chaining and composability

Key takeaway: In Ruby, iteration isn't special syntax - it's a protocol that any
object can implement. This makes the language more consistent and extensible.

## Post 5: Symbols - Why `:user` Isn't a String

Symbols are the most confusing thing for developers coming from Python or
JavaScript. They look like strings with a colon, but they're fundamentally
different. Understanding symbols is essential because they appear everywhere in
Ruby - hash keys, method names, Rails code, pattern matching.

A symbol is an immutable, interned identifier. When you write `:name`, Ruby
creates it once and reuses that same object every time. Two strings `"name"` and
`"name"` are different objects in memory. Two symbols `:name` and `:name` are
the exact same object. This makes symbols perfect for identifiers - things that
represent names or concepts rather than text data.

Python has interned strings, but they're an implementation detail you rarely
think about. In Ruby, symbols are a first-class language feature. You use them
constantly: `{ name: "Ruby" }` is actually `{ :name => "Ruby" }`. Method names
are symbols. ActiveRecord uses symbols for column names. Pattern matching uses
symbols for matching.

The mental model: if you're representing data that someone will read (user
input, text content), use strings. If you're representing an identifier (hash
keys, method names, constants, config options), use symbols.

This matters for performance too - comparing symbols is a pointer comparison
(O(1)), while comparing strings requires checking each character. Hash lookups
with symbol keys are faster. But more importantly, symbols make your intent
clear: "this is an identifier, not data."

The post will cover:

- What symbols are (immutable identifiers)
- Memory and performance characteristics
- When to use symbols vs strings
- How hashes use symbols
- Symbols in method names and Rails
- Converting between strings and symbols
- Common pitfalls and gotchas

Key takeaway: Symbols aren't syntax sugar for strings - they're a different type
for a different purpose.

## Post 6: Ruby's Object Model - Objects All The Way Down

In Python, classes are special. They're objects too (instances of `type`), but
you don't think about that much in daily code. In Ruby, the fact that classes
are objects is fundamental to how the language works. Once you understand Ruby's
object model, everything else clicks into place.

Classes are objects. They're instances of `Class`. Methods are objects. Modules
are objects. Even `nil`, `true`, and `false` are objects with methods. When you
call a method, Ruby looks it up in a chain: the object's class, included
modules, parent classes, all the way up to `BasicObject`.

This explains so much Ruby weirdness. Why can you call methods on classes
themselves? Because classes are objects. How does `include` add methods to your
class? It inserts the module into the ancestor chain. What's the singleton class
(eigenclass)? It's where an individual object's unique methods live.

Understanding the object model reveals the method lookup path. When you call
`obj.method_name`, Ruby:

1. Checks the object's singleton class
2. Checks the object's class
3. Walks up included modules (in reverse order of inclusion)
4. Checks parent classes and their modules
5. Repeats until it finds the method or hits `BasicObject`

This is why metaprogramming works - you can insert methods anywhere in this
chain. It's why monkey patching works - classes are never closed, you can always
reopen them. It's why mixins work - modules slot into the lookup chain.

The post will explore:

- Everything is an object (classes, methods, nil, booleans)
- The ancestor chain and method lookup
- Singleton classes (eigenclass/metaclass)
- `class << self` syntax
- How this enables metaprogramming
- Comparison with Python's object model

Key takeaway: Ruby's object model is simpler than it looks - it's just objects
sending messages to objects, all the way down.

## Post 7: Ruby Modules - Not Your Python Imports

When Python developers hear "module," they think of files you import. Ruby
modules are completely different - they're about composition, not organization.
A module is a collection of methods that can be mixed into classes. This is how
Ruby does inheritance without multiple inheritance's problems.

There are three ways to mix in a module: `include`, `extend`, and `prepend`.
Each puts the module in a different place in the ancestor chain. `include` adds
the module as a parent class, so the module's methods become instance methods.
`extend` adds methods to the object's singleton class, making them class
methods. `prepend` is like `include` but puts the module before the class in the
lookup chain.

This is how `Enumerable` works. When you `include Enumerable`, Ruby inserts that
module into your class's ancestor chain. Now when you call `.map`, Ruby walks up
the chain, finds `Enumerable#map`, and calls it. That method calls your `.each`
implementation. One method unlocks 40+ methods.

Modules enable mixin-based composition. Instead of building deep inheritance
hierarchies, you compose behavior from modules. Rails uses this pattern
everywhere - `ActiveRecord::Persistence`, `ActiveRecord::Validations`,
`ActiveRecord::Callbacks` are all modules mixed into your model classes.

The pattern is powerful: define a protocol (like `.each`), implement it once,
include a module, get dozens of methods for free. It's composition without the
complexity of multiple inheritance.

The post will cover:

- Modules as mixins vs namespaces
- `include` vs `extend` vs `prepend`
- Ancestor chain changes from each
- How Enumerable really works
- Building your own mixin modules
- Rails' use of concerns
- Comparison with Python's multiple inheritance

Key takeaway: Modules are Ruby's answer to composition - safer than multiple
inheritance, more powerful than single inheritance.

## Post 8: Ruby Metaprogramming - How The Magic Works

Now we can finally answer the question from the loops post: HOW does
`include Enumerable` add 40+ methods to your class? The answer is
metaprogramming - code that writes code at runtime.

Ruby's metaprogramming capabilities are legendary. When you `include` a module,
Ruby's `Module#include` method modifies your class's ancestor chain. When you
call `attr_accessor :name`, you're calling a method that calls `define_method`
to create getter and setter methods. When Rails lets you call undefined methods
like `User.find_by_email(...)`, it uses `method_missing` to catch and handle
them.

The core metaprogramming techniques:

- `define_method` - create methods dynamically
- `method_missing` - catch calls to undefined methods
- `instance_eval` and `class_eval` - run code in a different context
- `send` - call methods by name (string or symbol)
- Open classes - reopen and modify existing classes

This explains how Ruby DSLs work. When you write Rails routing code,
`resources :users` is calling a method that uses metaprogramming to define
routes. RSpec's `describe` and `it` use `instance_eval` to run your blocks in a
special context. ActiveRecord's dynamic finders use `method_missing`.

But metaprogramming has dangers. Open classes enable monkey patching - modifying
core Ruby classes. This can cause namespace collisions and make debugging
nightmarish. Modern Ruby offers refinements as a safer alternative - scoped
monkey patching that only affects files that opt in.

The post will explore:

- How `include` modifies the ancestor chain
- `define_method` and building `attr_accessor` yourself
- `method_missing` for dynamic methods
- `instance_eval` for DSL magic
- Monkey patching: the good, bad, and ugly
- Refinements as the modern alternative
- How Rails uses metaprogramming everywhere
- When to use (and avoid) metaprogramming

Key takeaway: Ruby's magic isn't magic - it's metaprogramming. Understanding it
reveals how Rails works and makes you a better Ruby developer.

## Post 9: Pattern Matching - Ruby 3's Killer Feature

Ruby 3.0 brought pattern matching to the language, and it's transforming how we
write Ruby code. If you've used pattern matching in Elixir, Rust, or modern
Python (3.10+), you know how powerful it is. Ruby's implementation is elegant,
practical, and very Ruby.

Pattern matching uses `case`/`in` syntax (not `case`/`when`). You can
destructure arrays, hashes, and objects. You can use guards for additional
conditions. You can match on types, values, or structure. And because this is
Ruby, it integrates beautifully with symbols, blocks, and the rest of the
language.

Basic patterns match values and types. Array patterns destructure:
`in [first, *rest]` captures the first element and remaining elements. Hash
patterns extract keys: `in { name:, age: }` captures those values. You can
combine patterns, nest them, use guards (`if`/`unless`), and match on object
attributes.

This makes certain code dramatically cleaner. Parsing JSON responses, handling
different data shapes, implementing state machines - all become more readable
with pattern matching. Compare the old `case`/`when` approach (checking values,
manually extracting data) with pattern matching's declarative style.

Python 3.10 added similar features with `match`/`case`. Ruby's version is more
expressive - better hash matching, better integration with the language. But the
real win is that pattern matching feels natural in Ruby. It uses symbols for
keys. It works with Ruby's duck typing. It composes with blocks.

The post will cover:

- Basic `case`/`in` syntax
- Array destructuring patterns
- Hash matching with symbols
- Guard clauses and advanced patterns
- Matching object attributes
- When to use vs traditional conditionals
- Comparison with Python's match/case
- Real-world examples from Rails apps

Key takeaway: Pattern matching shows Ruby is evolving while staying Ruby -
modern features that feel natural in the language.

---

## Series Arc

**Foundation**: Loops and Symbols - practical concepts you need immediately

**System**: Object Model and Modules - how Ruby actually works under the hood

**Advanced**: Metaprogramming and Pattern Matching - mastery and modern features

Each post builds on previous ones while remaining independently readable.
Cross-reference frequently to create a cohesive narrative: "Remember from the
loops post..." or "This is why we learned about symbols..."

The goal: help Python developers truly _get_ Ruby by revealing its design
philosophy and internal consistency.
