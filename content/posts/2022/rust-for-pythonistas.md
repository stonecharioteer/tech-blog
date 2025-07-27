---
date: '2022-03-26T00:00:00+05:30'
draft: false
title: 'Explicit is Better than Implicit: Rust for Pythonistas'
description: "A comprehensive introduction to Rust for Python developers, covering why Rust matters, memory management, ownership, borrowing, and practical code examples."
tags:
  - "rust"
  - "python"
  - "programming"
  - "learning"
---

```bash
$ python -m this | sed -n '4p'
Explicit is better than implicit.
```

{{< info title="Talk Resources" >}}
This post is based on my talk delivered at BangPypers on March 26, 2022.

**📹 [Watch the talk on YouTube](https://www.youtube.com/watch?v=62yfBiHrUis)**  
**📄 [Download the slides (PDF)](/talks/Explicit%20is%20Better%20than%20Implicit_%20Rust%20for%20Pythonistas.pdf)**  
**💻 [View the code examples](/code/talks/2022/bangpypers/rust_for_pythonistas/)**
{{< /info >}}

## About Me

Hi! I'm Vinay Keerthi, I go by ~~@stonecharioteer~~[^1] everywhere. I blog at stonecharioteer.com and am self-taught. I have been using Python for 8 years, building web applications (Flask), command line tools (Click), sometimes GUIs (PyQt5/Plotly Dash), and automating pipelines (Airflow, flask-scheduler).

At the time of this talk, I was doing Data Engineering at Merkle Science, a cryptocurrency analytics firm. Previously I worked at Visa, GKN Driveline, and Flipkart. I'd been writing Rust code for ~30 days when I gave this talk. *Beware the errors.*

## What's with the Title?

The Zen of Python states "Explicit is better than implicit." Rust embodies this principle to a fault, and is a natural successor to this ideal.

{{< warning title="This is not a Rust tutorial" >}}
This post covers why you might want to learn Rust as a Python developer, what it looks like, and how to get started. It's not a comprehensive tutorial.
{{< /warning >}}

## What This Talk Covers

- Why Rust?
- I already know Python - why would I learn Rust?
- Why not Go/Java/C++?
- What does Rust look like?
- How do I learn?
- Memory management concepts
- Strings in Rust
- The module system

## Why Rust?

I've been writing Python code my entire career and wanted to try something new. I'd tried some Go resources, but kept coming back to Rust. I first heard about Rust on Hacker News.

What did I know going in?
- Rust is *fast*
- Rust has a steep learning curve
- It's *low level*
- It's got something called the *borrow checker*
- *Strings are weird?*

## But I Already Know Python!

And that's **good**. Use what you know for problems you want to solve quickly. Python can do almost anything. If you need to scale, think about distributing your tasks across workers.

- Use Pandas, NumPy, and other libraries designed for speed over native data types
- Use Cython or PyCuda to write faster code
- Try PyPy for JIT - it's faster

## Then Why Would I Learn Rust?

### Shipping Python Applications is Getting Harder

There's a paradox of choice: poetry, pyenv, virtualenvwrapper, flit, conda. There are ways to ship a single binary, but they ship the Python interpreter with them.

### Learning Lower-Level Concepts

If you're self-taught like me, you should learn a lower-level language:
- Python doesn't teach you about memory management
- What *are* threads, really?
- How do you implement a truly safe multi-threaded application?
- How does the memory model work?

### Other Benefits

- Rust gives you simple and safe concurrency
- It makes you a better programmer (more on this later)

## Why Not X?

X is usually Go, Java, C++, or C. Follow your instinct - learn what you want to.

**Performance matters, and it should.** Ownership and borrowing is interesting. Have you seen *really* small binaries? Cargo is an amazing package manager that does everything for you.

## What Does It Look Like?

Let's start with the classic hello world:

```rust
fn main() {
    println!("ನಮಸ್ಕಾರ, BangPypers!");
}
```

Here's some real code - a simple function that calculates sale prices:

```rust
// This store is having a sale where if the price is an even number, you get
// 10 Rustbucks off, but if it's an odd number, it's 5 Rustbucks off.

// This is the function that is triggered when you're building a binary, a CLI or a server
// instance for example.
fn main() {
    let original_price = 51;
    println!("Your sale price is {}", sale_price(original_price));
}

// This function takes an i32 integer and returns an i32 integer.
// Rust's typing is extremely strict. If it looks like a duck, don't trust it.
// If you want something that quacks, then don't ask for a duck. Ask for something
// that quacks.
fn sale_price(price: i32) -> i32 {
    if is_even(price) {
        price - 10
    } else {
        price - 5
    }
}

// This function takes an i32 and returns a boolean value.
// Even the number size really matters. Rust showed me that we use inconsistent
// database schemas in some places because I was using u32 (unsigned integer 32 bit),
// and one particular database schema returned a u64 instead. That's an error you wouldn't get
// with Python.
fn is_even(num: i32) -> bool {
    num % 2 == 0
}
```

Here's a more complex example showing structs and implementations:

```rust
#[derive(Debug)]
struct Package {
    sender_country: String,
    recipient_country: String,
    weight_in_grams: i32,
}

impl Package {
    fn new(sender_country: String, recipient_country: String, weight_in_grams: i32) -> Package {
        if weight_in_grams <= 0 {
            panic!("uh-oh! what do you mean that the weight is negative?");
        } else {
            return Package {
                sender_country,
                recipient_country,
                weight_in_grams,
            };
        }
    }

    fn is_international(&self) -> bool {
        self.sender_country != self.recipient_country
    }

    fn get_fees(&self, cents_per_gram: i32) -> i32 {
        self.weight_in_grams * cents_per_gram
    }
}
```

## Memory Management in Rust: Scope and Mutability

```rust
let x = 10;
{
    let mut x = 15;
    println!("x = {}", x);
    x = 18;
    println!("x = {}", x);
}
println!("x = {}", x)
```

Variables have scopes, and you must explicitly declare them as mutable with `mut`.

## Memory Management in Rust: Movement

You can't keep passing variables around and copying them without thinking. Rust's memory model is centered around **Ownership** and **Borrowing**.

```rust
fn main() {
    let x: String = "hello".to_string();
    println!("x = {}", x);
    let y = x;
    println!("y = {}", y);
    println!("x = {}", x); // ERROR: This won't even compile because x has "moved" into y.
}
```

The Rust analyzer tells us that we can't use the value of x because it has moved, and that String doesn't implement the `Copy` trait.

### Traits

Traits are *abilities* types and structs can have in Rust. You can implement a trait on any datatype. Some are derivable while others need to be implemented manually. You can override traits to give your datatypes not-so-obvious features.

Think of it like overriding or implementing `__dunder__` methods in Python. **Note that this is a gross trivialization of what traits are.**

## Memory Management in Rust: Borrowing

```rust
fn borrow_a_string(x: &str) {
    println!("I've only borrowed a string. The value is {}", x);
}

fn move_a_string(x: String) {
    println!("I've taken ownership of a string. The value is {}", x);
}

fn main() {
    let v = String::from("The cake is a lie!");
    borrow_a_string(&v); // v is still in scope because this is just a borrow.
    move_a_string(v); // v is a move, so it cannot be used after this.
    println!("v={}", v); // if you try this, the compiler will complain.
}
```

## Memory Management in Rust: Mutable Borrowing

```rust
fn append_to_a_vector(v: &mut Vec<u32>, a: u32) {
    v.push(a);
}

pub fn run() {
    let mut x = vec![10, 20, 30, 40];
    println!("Initial Vector: {:?}", x);
    append_to_a_vector(&mut x, 10);
    println!("Final Vector: {:?}", x);
}
```

## Strings in Rust

Strings are UTF-8 encoded in Rust, so a string length might not be what you think it is. [The docs explain this well](https://doc.rust-lang.org/book/ch08-02-strings.html). They use the Devanagari script as an example of why this is not straightforward.

For example: `ನಮಸ್ಕಾರ` would not be just 4 characters.

```rust
pub fn run() {
    let x = "ನಮಸ್ಕಾರ";
    println!("{} = {:?}", x, x.as_bytes());
    println!("{} = {:?}", x, x.chars().collect::<Vec<char>>());
}
```

Here's a practical example showing string slices vs owned strings:

```rust
// Ok, here are a bunch of values-- some are `String`s, some are `&str`s. Your
// task is to call one of these two functions on each value depending on what
// you think each value is. That is, add either `string_slice` or `string`
// before the parentheses on each line. If you're right, it will compile!

fn string_slice(arg: &str) {
    println!("{}", arg);
}

fn string(arg: String) {
    println!("{}", arg);
}

pub fn run() {
    string_slice("blue");
    string("red".to_string());
    string(String::from("hi"));
    string("rust is fun!".to_owned());
    string("nice weather".into());
    string(format!("Interpolation {}", "Station"));
    string_slice(&String::from("abc")[0..1]);
    string_slice("  hello there ".trim());
    string("Happy Monday!".to_string().replace("Mon", "Tues"));
    string("mY sHiFt KeY iS sTiCkY".to_lowercase());
}
```

## How Does Rust Make Me a Better Programmer?

### Types Are Not Suggestions Anymore

- Datatypes really matter
- Trait or interface-oriented programming teaches you to think in terms of what an object *can do* and not what it *is*

### Variable Scope Awareness

I've never thought about how my variables move in and out of scopes before:
- Closures are fun
- Having control over which parts of your code *can* and *cannot* modify your variables lets you think in a way you haven't before

### Accounting for Everything

I need to account for everything I've written:
- When I use an enum variant in a match statement, I need to match for each and every case
- I need to account for errors in the same way
- I can define functions as having a return value that *must be used* and not ignored

## How Do I...?

Common questions new Rustaceans ask:

- **Create a GUI?** - Try [egui](https://crates.io/crates/egui), [tauri](https://tauri.app/), or [iced](https://crates.io/crates/iced)
- **Create a CLI?** - Use [clap](https://crates.io/crates/clap) for argument parsing
- **Write ML code?** - Check out [candle](https://crates.io/crates/candle) or [tch](https://crates.io/crates/tch)
- **Connect to a database?** - Use [sqlx](https://crates.io/crates/sqlx) for async SQL or [diesel](https://crates.io/crates/diesel) for ORM
- **Create a game?** - Try [bevy](https://crates.io/crates/bevy) or [macroquad](https://crates.io/crates/macroquad)
- **Write a linked list?** - Learn from [Learning Rust With Entirely Too Many Linked Lists](https://rust-unofficial.github.io/too-many-lists/)
- **Create a web application?** - Use [axum](https://crates.io/crates/axum), [warp](https://crates.io/crates/warp), or [rocket](https://crates.io/crates/rocket)
- **Connect to Ethereum?** - Try [ethers-rs](https://crates.io/crates/ethers) or [web3](https://crates.io/crates/web3)
- **Configure my IDE?** - [rust-analyzer](https://rust-analyzer.github.io/) works with VS Code, vim, emacs, and most editors
- **Write async code?** - Learn from the [Async Book](https://rust-lang.github.io/async-book/)
- **Write WebAssembly?** - Check the [Rust and WebAssembly Book](https://rustwasm.github.io/docs/book/)
- **Start learning?** - Begin with [The Rust Book](https://doc.rust-lang.org/book/) and [Rustlings](https://github.com/rust-lang/rustlings)

The Rust ecosystem has excellent crates (libraries) for all of these use cases, and [crates.io](https://crates.io/) is the central repository.

## Resources

Here are the resources I recommend for learning Rust:

### Essential Resources

1. [The Rust Book](https://doc.rust-lang.org/book/) (Official Docs)
2. [A Half-Hour to Learn Rust](https://fasterthanli.me/articles/a-half-hour-to-learn-rust) (Blog Article)
3. [Rustlings - Interactive Exercises](https://github.com/rust-lang/rustlings) (Official companion exercises)
4. [Let's Get Rusty - The Rust Lang Book](https://www.youtube.com/c/LetsGetRusty) (Videos)

### Books

5. [Rust in Action](https://www.manning.com/books/rust-in-action)
6. [Rust for Rustaceans](https://nostarch.com/rust-rustaceans)
7. [Zero to Production in Rust](https://www.zero2prod.com/)

### Academic Resources

8. [CS 4414 - Operating Systems - Using Rust for an Undergrad OS Course](http://rust-class.org/) (Reasons to Use Rust)

### Code Examples

9. The [example code and project structure](/code/talks/2022/bangpypers/rust_for_pythonistas/) from this talk

## Conclusion

Rust embodies the Python principle of "explicit is better than implicit" in a way that makes you think differently about programming. While it has a steep learning curve, it teaches valuable concepts about memory management, type safety, and error handling that make you a better programmer overall.

The key is not to abandon Python, but to add Rust as another tool in your toolkit for problems where its strengths shine: systems programming, performance-critical applications, and anywhere you need the confidence that comes with compile-time guarantees.

**Related Posts:**
- [Learning Rust](/posts/2022/learning-rust/) - My initial journey into Rust
- [So Far So Rust](/posts/2022/so-far-so-rust/) - A deeper dive after 145 days of Rust

[^1]: I no longer use Twitter or other social media platforms. Read more about [why I left social networks](https://stonecharioteer.com/no-social-media).