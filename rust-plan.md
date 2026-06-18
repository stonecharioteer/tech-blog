# Blog Post Series TODO: Relearning Rust by Building an Overengineered Download Manager

## Series Overview

A deep dive into Rust idioms and patterns through building a download manager
from scratch. Each post follows a git tag, exploring **advanced Rust patterns**,
**design decisions**, and **lessons learned** along the way. This is a learning
exercise—documenting discoveries, mistakes, and insights about how Rust shapes
system design.

**Tone**: Expert practitioner revisiting fundamentals and discovering depth.
Focus on **why Rust idioms matter**, **design tradeoffs**, and **patterns that
emerge** when you stop fighting the language. Technical, opinionated, and
reflective.

---

## Post 1: Starting Simple - The Blocking MVP

**Git Tag**: `v0.1-task1-blocking-mvp` **Working Title**: "Write_all vs Write:
Why Rust Forces You to Think About Partial Writes"

### Rust Patterns & Discoveries:

- [ ] **write_all() vs write() semantics** - The subtle correctness guarantee
  - write() can succeed with partial writes
  - write_all() guarantees all bytes or error
  - Why this matters for data integrity
  - The pattern: use write_all() for correctness, write() for flow control
- [ ] **Error context and ergonomics** - The unwrap() → ? evolution
  - Starting with unwrap() to get things working
  - Adding context with expect()
  - Discovering ? for propagation
  - When each approach is appropriate
- [ ] **Resume logic and HTTP Range** - Idiomatic status code handling
  - Pattern matching on status codes (200, 206, 416)
  - Using match to handle the happy path and error paths
  - Why enums would be better than raw status codes (preview)
- [ ] **Streaming vs buffering** - Memory-efficient file operations
  - Chunked reading/writing instead of loading entire file
  - The tradeoff: memory vs code complexity
  - Why streaming hash calculation matters
- [ ] **Debug vs Release performance** - The actual cost of safety checks
  - 3x CPU difference between builds
  - Where the overhead comes from (bounds checks, assertions)
  - When to use which build

### Design Decisions:

- Why blocking first? (Simpler mental model, fewer moving parts)
- SHA256 streaming calculation (memory-efficient from the start)
- Resume detection using file metadata + HTTP Range headers
- indicatif for progress (good API, stays out of the way)

### Writing Notes:

- **Lead with a concrete decision**: "write_all() wasn't just convenience. It
  was correctness."
- Focus on **design tradeoffs**: "I could buffer the entire response. But why?"
- **The discovery**: "Debug builds were using 30% CPU. Release builds: 8%. Where
  did 22% go?"
- Emphasize **patterns over syntax**: "This is how you think in Rust, not just
  how you write it."

---

## Post 2: Enter Async - tokio::select! and the Send Bound

**Git Tag**: `v0.2-task2-async-complete` **Working Title**: "tokio::select!:
Racing Futures Without Going Insane"

### Rust Patterns & Discoveries:

- [ ] **tokio::select! as control flow** - Concurrent polling pattern
  - Racing stream.next() vs interval.tick() vs interrupt check
  - Why you don't .await in arms (select! does it for you)
  - The loop + select! pattern for continuous polling
  - Cancellation safety: what happens to non-selected branches?
- [ ] **Send + Sync bounds in practice** - The actual error and the fix
  - The compiler error: "future cannot be sent between threads safely"
  - Why: Box<dyn Error> isn't Send
  - The fix: anyhow::Error or Box<dyn Error + Send + Sync>
  - Pattern: async functions return futures that must be Send
- [ ] **bytes_stream() vs manual reads** - Ergonomic async streaming
  - reqwest's bytes_stream() as an async Stream
  - Polling with stream.next().await
  - Why this is cleaner than manual buffer management
  - The tradeoff: less control over chunk sizes
- [ ] **tokio::time::interval vs manual timing** - Structured periodic tasks
  - interval.tick().await as a periodic future
  - No more Instant::now() and duration checks
  - Composing with select! for responsive progress updates
- [ ] **anyhow for error ergonomics** - Type-erased Send errors
  - anyhow::Result<T> = Result<T, anyhow::Error>
  - .context() for adding error context chains
  - When type erasure beats concrete error types

### Design Decisions:

- Why async? (Enables concurrent operations without threads)
- select! over explicit polling (cleaner, more structured)
- anyhow over custom error types (pragmatic for applications)
- tokio::fs over std::fs (async all the way down)

### Writing Notes:

- **Lead with select!**: "This macro changed how I think about concurrency"
- **The Send bound error**: "Show the actual error message. Decode it. Fix it."
- **Discovery**: "select! arms race. The first ready wins. Others are
  cancelled."
- **Pattern recognition**: "loop { select! { ... } } is the async event loop
  pattern"

---

## Post 3: Range Support - OpenOptions and the Builder Pattern

**Git Tag**: `v0.3-task3-range-support` **Working Title**: "OpenOptions: When
Rust's Standard Library Teaches API Design"

### Rust Patterns & Discoveries:

- [ ] **OpenOptions builder pattern** - Fluent API in std
  - File::open() vs OpenOptions::new().read(true).append(true).open()
  - Why separate methods instead of mode bits
  - Type-safe configuration vs integer flags
  - The pattern: builders for complex configuration
- [ ] **Option combinators in practice** - Handling missing Content-Length
  - .ok_or() to convert Option to Result
  - .and_then() for chaining fallible operations
  - Pattern matching vs combinator chains
  - When each approach reads better
- [ ] **PathBuf for path manipulation** - Cross-platform path building
  - PathBuf::join() vs string concatenation
  - Why this matters (Windows vs Unix paths)
  - Path vs PathBuf (borrowed vs owned)
  - Pattern: use PathBuf when constructing, &Path for passing
- [ ] **HTTP status code handling** - match vs if chains
  - Matching on status.as_u16() for 200, 206, 416
  - Why not an enum? (HTTP crate doesn't provide one)
  - Exhaustive match with \_ wildcard for error cases
  - The tradeoff: type safety vs external API constraints

### Design Decisions:

- Explicit range flags (--range-start, --range-end) for testing
- OpenOptions over File::open for precise file mode control
- PathBuf::join() for part file names (not string concat)
- Status code match as foundation for future enum refactor

### Writing Notes:

- **Lead with OpenOptions**: "This is how you design configurable APIs"
- **Builder pattern insight**: "Not just ergonomics. It's impossible to get
  wrong."
- **Discovery**: "Option combinators avoid nested if-let. When to use which?"
- **Pattern**: "Status codes as integers are a code smell. But sometimes you're
  stuck with them."

---

## Post 4: Decoupling with Atomics - Relaxed vs SeqCst

**Git Tag**: `v0.4-task8-modular-codebase` **Working Title**: "Memory Ordering:
When Relaxed is Fine and When It Isn't"

### Rust Patterns & Discoveries:

- [ ] **Arc<AtomicUsize> for lock-free progress** - Why not Mutex?
  - Progress updates are high-frequency, single-value writes
  - Atomics provide lock-free .load() and .store()
  - Cloning Arc is cheap (atomic refcount increment)
  - Pattern: Arc<Atomic\*> for simple shared counters
- [ ] **Memory ordering semantics** - Relaxed vs SeqCst in practice
  - Ordering::Relaxed for progress bytes (metrics, best-effort)
  - Ordering::SeqCst for interrupt flag (correctness, total ordering)
  - Why relaxed is safe for counters (no dependent operations)
  - Why SeqCst for control flow (visibility guarantees matter)
  - The performance difference: often negligible for throttled reads
- [ ] **Decoupling UI from logic** - Pure functions + atomics
  - Download functions only .store() to atomics
  - Separate task polls atomics for UI updates
  - Pattern: business logic updates state, UI observes state
  - Benefits: testability, reusability, clarity
- [ ] **Module visibility boundaries** - pub(crate) for internal APIs
  - Public modules: cli, download
  - Internal utilities: pub(crate) in download module
  - Re-exporting with pub use in mod.rs
  - Pattern: wide modules, narrow public APIs
- [ ] **Refactoring toward testability** - No UI in business logic
  - Functions return PathBuf, not ()
  - No println!, no progress bar methods in downloads
  - CLI orchestrates, downloads execute
  - Pattern: separate IO from computation

### Design Decisions:

- Arc<Atomic*> over Arc<Mutex<*>> for simple counters (lock-free)
- Relaxed ordering for metrics (performance, correctness not critical)
- SeqCst for control flow (correctness over micro-optimization)
- Spawned progress reporter task (separation of concerns)

### Writing Notes:

- **Lead with memory ordering**: "I cargo-culted SeqCst everywhere. Then I
  learned when Relaxed is fine."
- **The insight**: "Atomics aren't just faster Mutexes. They're different
  tools."
- **Discovery**: "Relaxed for counters. SeqCst for flags. Acquire/Release for
  synchronization."
- **Pattern**: "Arc<Atomic\*> + separate observer task = clean decoupling"

---

## Post 5: Concurrent Workers - The Sorting Bug and join_all Order

**Git Tag**: `v0.5-task4-multi-worker` **Working Title**: "join_all Preserves
Order: The Bug I Introduced By Not Trusting It"

### Rust Patterns & Discoveries:

- [ ] **The sorting bug** - When defensive programming breaks correctness
  - File parts: part.0-70778879, part.70778880-141557759, part.141557760-...
  - String sort: "141557760" comes before "70778880" (lexicographic)
  - The wrong fix: sort the filenames
  - The right fix: don't sort! join_all preserves spawn order
  - Pattern: trust your data structures, don't add defensive complexity
- [ ] **futures::join_all order guarantee** - Critical for correctness
  - join_all returns results in spawn order
  - This is documented but easy to miss
  - Why it matters: file assembly depends on byte range order
  - Pattern: when order matters, rely on combinators that preserve it
- [ ] **into_iter() for spawning tasks** - Ownership in loops
  - .iter() borrows, spawned tasks need 'static
  - into_iter() consumes Vec, gives owned values
  - Cloning Arc before moving into async move block
  - Pattern: into_iter() + enumerate() for indexed spawning
- [ ] **move closures in tokio::spawn** - Capturing by ownership
  - async move { ... } moves captured variables
  - Why: tasks are 'static, can't borrow from parent scope
  - Cloning Arc is cheap, moving is ownership transfer
  - Pattern: clone Arc outside spawn, move clone inside

### Design Decisions:

- N workers via tokio::spawn (green threads, not OS threads)
- Part file naming: filename.part.start-end (includes range for debugging)
- join_all for waiting (not manual JoinHandle collection)
- No sorting (trust the structure)

### Writing Notes:

- **Lead with the bug**: "Show the lexicographic sort output. Show the SHA256
  mismatch."
- **The realization**: "join_all preserves order. I didn't trust it. I broke
  it."
- **Lesson**: "Defensive programming can introduce bugs when you don't trust
  your tools."
- **Pattern**: "into_iter().enumerate() is the idiomatic way to spawn indexed
  tasks"

---

## Post 6: Type-State with Enums - Mixing Mutex and Atomics

**Git Tag**: `v0.6-task5-progress-viz` **Working Title**: "When to Mutex, When
to Atomic: Building a Chunk Progress Bar"

### Rust Patterns & Discoveries:

- [ ] **Enums as state machines** - Downloading { worker_id }
  - ChunkState enum: Pending | Downloading { worker_id } | Completed | Failed
  - Data in enum variants (not just tags)
  - Pattern matching extracts the worker_id
  - Pattern: enums model state transitions with associated data
- [ ] **Mixing Mutex and Atomics** - Different tools for different data
  - Arc<Mutex<Vec<ChunkState>>> for complex state (enum transitions)
  - Vec<Arc<AtomicUsize>> for per-chunk byte counters
  - Why Mutex here: can't atomically update enum variant
  - Why Atomics here: high-frequency counter updates
  - Pattern: Mutex for structure changes, Atomics for simple values
- [ ] **Trait bounds for shared types** - Send + Sync + Clone
  - ProgressTracker trait with these bounds
  - Send: can move to spawned tasks
  - Sync: can share references across tasks (&T)
  - Clone: can duplicate handles (Arc cloning)
  - Pattern: trait bounds document threading requirements
- [ ] **Separate rendering from state** - Observer pattern
  - ChunkProgressBar owns state, exposes update methods
  - Separate task calls .render() in loop
  - Workers only call .set_chunk_state() and .update_chunk_bytes()
  - Pattern: state owner + observer task = clean separation

### Design Decisions:

- Mutex for ChunkState Vec (need to update enum variants)
- Atomics for byte counters (high-frequency, lock-free)
- Trait abstraction (ProgressTracker) for different progress types
- Background render task (spawned, polls state, updates display)

### Writing Notes:

- **Lead with the tradeoff**: "I needed both Mutex and Atomics. Here's why."
- **The insight**: "Mutex lets me update complex data. Atomics let me count
  lock-free."
- **Discovery**: "Enums with data model state machines naturally in Rust"
- **Pattern**: "Separate state updates from rendering. Always."

---

## Post 7: Patterns That Emerged - Rust Idioms in Practice

**Git Tag**: Current HEAD (beyond v0.6) **Working Title**: "The Patterns That
Emerged: Lessons from 6 Git Tags"

### Patterns Synthesized:

- [ ] **Correctness by construction** - Using types to prevent bugs
  - write_all() over write()
  - Option forces None handling
  - Enums model states, prevent invalid transitions
  - Builder patterns make misconfiguration impossible
  - Pattern: make wrong code not compile
- [ ] **Explicit over implicit** - Data flow is visible
  - Error handling with Result and ?
  - Ownership transfer with move closures
  - Memory ordering (Relaxed vs SeqCst) is explicit
  - Pattern: if it matters, make it explicit in types
- [ ] **Lock-free when possible, locks when necessary** - Right tool for job
  - Atomics for simple counters
  - Mutex for complex state updates
  - Know when you need synchronization vs atomic operations
  - Pattern: understand your data access patterns first
- [ ] **Separate state from observation** - Observer pattern everywhere
  - Download functions update state
  - UI tasks observe state
  - Workers update progress
  - Renderer reads progress
  - Pattern: state updates and rendering are separate concerns
- [ ] **Trust your data structures** - Don't add defensive complexity
  - join_all preserves order (don't sort!)
  - Type system enforces correctness (don't validate!)
  - Compiler catches errors (don't guard against impossible states!)
  - Pattern: trust the guarantees, don't code defensively

### Lessons Learned:

- **Rust shapes design**: Ownership forces you to think about data lifetime
  upfront
- **Compiler feedback loop**: Error messages teach patterns
- **Performance is compositional**: Zero-cost abstractions mean clean code is
  fast code
- **Types document intent**: Reading signatures tells you what's possible

### What's Next:

- Pause/resume with state persistence (serde for serialization)
- HTTP control plane with Axum (shared state patterns)
- gRPC streaming (tonic, broadcast channels)

### Writing Notes:

- **Lead with synthesis**: "After 6 tags, patterns emerged. Here's what I
  learned."
- **Be specific**: Reference actual code from previous posts
- **Opinionated**: "This is how I think about Rust now."
- **Invite reflection**: "What patterns have you discovered?"

---

## Series Meta

- [ ] **Create series landing page** - Index of all posts with brief
      descriptions
- [ ] **Consistent tagging** - `rust`, `learning`, `download-manager`, `async`,
      `tokio`
- [ ] **Cross-linking** - Each post links to previous/next in series
- [ ] **Code snippets** - Use external code shortcode where possible, point to
      specific git tags
- [ ] **Admonitions** - Use tip, warning, info, note for key concepts
- [ ] **Performance data** - Include actual benchmarks where relevant
- [ ] **Git tag references** - Link to specific commits on GitHub
- [ ] **Asciicast recordings** - Record demos for visual posts

## Writing Guidelines

- [ ] Start each post with "why this matters"
- [ ] Use analogies for complex concepts (compare to Ruby/Python where relevant)
- [ ] Show mistakes and corrections (learning journey, not just final solution)
- [ ] Include "aha!" moments and realizations
- [ ] Code snippets should be runnable or reference real commits
- [ ] Explain Rust concepts in context of the project, not abstractly
- [ ] Keep tone conversational but technical
- [ ] Use your Ruby post style: clear structure, practical examples, personal
      voice
- [ ] Each post should be self-contained but reference the series
- [ ] End each post with "what's next" to build anticipation

## Technical Checklist

- [ ] Verify all git tags exist and are stable
- [ ] Test code snippets against actual tag states
- [ ] Create asciicast recordings for visual features
- [ ] Extract key code sections for blog post examples
- [ ] Prepare benchmark data and performance comparisons
- [ ] Set up external code examples in `/code/` directory if needed
- [ ] Review FEATURES.md for accurate future roadmap
- [ ] Update implementation.md as posts are written

## Timeline Notes

- Posts should be written **after** download manager is more complete
- Current state: v0.6 (Task 5 complete, Task 6 in progress)
- Wait for at least Task 6 (pause/resume) to be complete before starting
- This TODO serves as roadmap and content outline
- Revisit and refine topics as implementation evolves
- Don't rush - better to write comprehensive posts later than rushed posts now
