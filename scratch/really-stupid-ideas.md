# Really Stupid Ideas

I want to write a series of posts, around the concept "really stupid". This came
out of a discussion during an interview where a recruiter asked me why I chose
to implement a message queue the conventional way with a HTTP service and not
something more creative like
[`FUSE`](https://www.cs.nmsu.edu/~pfeiffer/fuse-tutorial/) or something. He said
someone he spoke to built this in `git`.

While I think that's an admirable idea, I wouldn't be doing that in an
interview, non-conventional, _hackey_ ideas are scorned upon in the industry.
But I like the idea, and while listening to the
[Just Use Postgres!](https://www.manning.com/books/just-use-postgres) author on
the [Database School](https://youtu.be/IdyK8XB2l6g) podcast, I realized that I
would have fun writing a series of posts albeit like a
[book](https://rust-lang.github.io/mdBook/) instead.

I like this idea, and I'd like to do that. I'm not sure when, though, but I'd
like to do this for different things, starting with message queues.

## Really Stupid Message Queues - The Idea

For each of these ideas, I'd like to write code that _stress-tests_ them. I want
to try mimicking using them in prod, and trying to use VMs to distribute them?
I'm not sure if the second bit is a little _too-ambitious_. Perhaps it is.

1. A Message Queue in a File
2. A Message Queue in SQLLite
3. A Message Queue in PostgreSQL
4. A Message Queue in `git`
5. A Message Queue using FUSE
6. A Message Queue using linux system logs? I don't know

I haven't thought hard enough about this problem, but this is something I could
extend to _a lot of other things_. Like databases, key-value stores/caches.

It reminds me of trying out some coding tests before joining Visa, Geekbench?
No, Geek something. Their questions said "make an API" and they were describing
a CLI and that got me thinking. Perhaps when people say API they don't always
mean a HTTP API. I am older now and I know that much, but back then it was an
assumption that I had in my head.

So this is the idea, I think I could do this, but naturally I want to work on
the Rust download manager first.
