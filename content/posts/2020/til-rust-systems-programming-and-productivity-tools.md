---
date: 2020-07-21T18:00:00+05:30
draft: false
title: "TIL: Rust Systems Programming and Terminal Productivity Tools"
description:
  "Today I learned about Rust systems programming through terminal applications,
  backend development patterns, Pi-hole networking setup, and various
  development productivity tools and resources."
tags:
  - "til"
  - "rust"
  - "systems-programming"
  - "terminal"
  - "productivity"
  - "pihole"
  - "networking"
  - "development-tools"
---

Today I explored the intersection of systems programming and productivity tools,
discovering how Rust enables building efficient terminal applications and
learning about modern development workflows and educational resources.

## Rust Terminal Applications

### Terminal Habit Tracker in Rust

[Dijo - Terminal Habit Tracker written in Rust](https://github.com/NerdyPepper/dijo)
demonstrates elegant terminal UI development:

```rust
// Example: Building a terminal habit tracker similar to dijo
use std::collections::HashMap;
use std::io::{self, Write};
use chrono::{Local, NaiveDate, Duration};
use crossterm::{
    event::{self, KeyCode, KeyEvent},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use tui::{
    backend::{Backend, CrosstermBackend},
    layout::{Alignment, Constraint, Direction, Layout, Rect},
    style::{Color, Modifier, Style},
    text::{Span, Spans},
    widgets::{Block, Borders, Calendar, Clear, List, ListItem, Paragraph},
    Frame, Terminal,
};

#[derive(Debug, Clone)]
struct Habit {
    name: String,
    target_frequency: u32, // times per week
    completed_dates: Vec<NaiveDate>,
    created_date: NaiveDate,
}

impl Habit {
    fn new(name: String, target_frequency: u32) -> Self {
        Self {
            name,
            target_frequency,
            completed_dates: Vec::new(),
            created_date: Local::now().date_naive(),
        }
    }

    fn mark_completed(&mut self, date: NaiveDate) {
        if !self.completed_dates.contains(&date) {
            self.completed_dates.push(date);
            self.completed_dates.sort();
        }
    }

    fn is_completed_on(&self, date: NaiveDate) -> bool {
        self.completed_dates.contains(&date)
    }

    fn weekly_completion_rate(&self, week_start: NaiveDate) -> f32 {
        let week_end = week_start + Duration::days(6);
        let completed_this_week = self.completed_dates
            .iter()
            .filter(|&&date| date >= week_start && date <= week_end)
            .count() as f32;

        (completed_this_week / self.target_frequency as f32).min(1.0)
    }

    fn streak(&self) -> u32 {
        let today = Local::now().date_naive();
        let mut streak = 0;
        let mut current_date = today;

        while self.is_completed_on(current_date) {
            streak += 1;
            current_date = current_date - Duration::days(1);
        }

        streak
    }
}

struct HabitTracker {
    habits: HashMap<String, Habit>,
    selected_habit: Option<String>,
    mode: AppMode,
    input_buffer: String,
}

#[derive(Debug, Clone, PartialEq)]
enum AppMode {
    Normal,
    AddingHabit,
    ViewingCalendar,
}

impl HabitTracker {
    fn new() -> Self {
        let mut tracker = Self {
            habits: HashMap::new(),
            selected_habit: None,
            mode: AppMode::Normal,
            input_buffer: String::new(),
        };

        // Add some sample habits
        tracker.add_habit("Exercise".to_string(), 5);
        tracker.add_habit("Read".to_string(), 7);
        tracker.add_habit("Meditate".to_string(), 7);
        tracker.add_habit("Code".to_string(), 5);

        tracker
    }

    fn add_habit(&mut self, name: String, frequency: u32) {
        let habit = Habit::new(name.clone(), frequency);
        self.habits.insert(name.clone(), habit);

        if self.selected_habit.is_none() {
            self.selected_habit = Some(name);
        }
    }

    fn toggle_habit_today(&mut self) {
        if let Some(habit_name) = &self.selected_habit {
            if let Some(habit) = self.habits.get_mut(habit_name) {
                let today = Local::now().date_naive();

                if habit.is_completed_on(today) {
                    habit.completed_dates.retain(|&date| date != today);
                } else {
                    habit.mark_completed(today);
                }
            }
        }
    }

    fn next_habit(&mut self) {
        if let Some(current) = &self.selected_habit {
            let habit_names: Vec<_> = self.habits.keys().collect();
            if let Some(current_index) = habit_names.iter().position(|&name| name == current) {
                let next_index = (current_index + 1) % habit_names.len();
                self.selected_habit = Some(habit_names[next_index].clone());
            }
        }
    }

    fn previous_habit(&mut self) {
        if let Some(current) = &self.selected_habit {
            let habit_names: Vec<_> = self.habits.keys().collect();
            if let Some(current_index) = habit_names.iter().position(|&name| name == current) {
                let prev_index = if current_index == 0 {
                    habit_names.len() - 1
                } else {
                    current_index - 1
                };
                self.selected_habit = Some(habit_names[prev_index].clone());
            }
        }
    }
}

// Terminal UI rendering
fn ui<B: Backend>(f: &mut Frame<B>, app: &HabitTracker) {
    let chunks = Layout::default()
        .direction(Direction::Vertical)
        .margin(1)
        .constraints([
            Constraint::Length(3),
            Constraint::Min(10),
            Constraint::Length(3),
        ].as_ref())
        .split(f.size());

    // Title
    let title = Paragraph::new("🎯 Habit Tracker")
        .style(Style::default().fg(Color::Yellow).add_modifier(Modifier::BOLD))
        .alignment(Alignment::Center)
        .block(Block::default().borders(Borders::ALL));
    f.render_widget(title, chunks[0]);

    // Main content
    let main_chunks = Layout::default()
        .direction(Direction::Horizontal)
        .constraints([Constraint::Percentage(60), Constraint::Percentage(40)].as_ref())
        .split(chunks[1]);

    // Habit list
    let habits_list = render_habits_list(app);
    f.render_widget(habits_list, main_chunks[0]);

    // Statistics panel
    let stats_panel = render_statistics(app);
    f.render_widget(stats_panel, main_chunks[1]);

    // Status bar
    let status = match app.mode {
        AppMode::Normal => "Press 'a' to add habit, 'space' to toggle, 'q' to quit",
        AppMode::AddingHabit => "Enter habit name, then press Enter",
        AppMode::ViewingCalendar => "Press 'Esc' to return",
    };

    let status_bar = Paragraph::new(status)
        .style(Style::default().fg(Color::Gray))
        .alignment(Alignment::Center)
        .block(Block::default().borders(Borders::ALL));
    f.render_widget(status_bar, chunks[2]);
}

fn render_habits_list(app: &HabitTracker) -> List {
    let today = Local::now().date_naive();
    let items: Vec<ListItem> = app.habits
        .iter()
        .map(|(name, habit)| {
            let is_selected = app.selected_habit.as_ref() == Some(name);
            let is_completed_today = habit.is_completed_on(today);
            let streak = habit.streak();

            let completion_indicator = if is_completed_today { "✅" } else { "⭕" };
            let streak_text = if streak > 0 { format!(" 🔥{}", streak) } else { String::new() };

            let content = format!("{} {} ({}x/week){}",
                completion_indicator, name, habit.target_frequency, streak_text);

            let style = if is_selected {
                Style::default().fg(Color::Yellow).add_modifier(Modifier::BOLD)
            } else if is_completed_today {
                Style::default().fg(Color::Green)
            } else {
                Style::default().fg(Color::White)
            };

            ListItem::new(content).style(style)
        })
        .collect();

    List::new(items)
        .block(Block::default().borders(Borders::ALL).title("Habits"))
        .highlight_style(Style::default().add_modifier(Modifier::REVERSED))
}

fn render_statistics(app: &HabitTracker) -> Paragraph {
    let today = Local::now().date_naive();
    let week_start = today - Duration::days(today.weekday().num_days_from_monday() as i64);

    let total_habits = app.habits.len();
    let completed_today = app.habits.values()
        .filter(|habit| habit.is_completed_on(today))
        .count();

    let weekly_rates: Vec<_> = app.habits.values()
        .map(|habit| habit.weekly_completion_rate(week_start))
        .collect();

    let avg_weekly_rate = if !weekly_rates.is_empty() {
        weekly_rates.iter().sum::<f32>() / weekly_rates.len() as f32
    } else {
        0.0
    };

    let stats_text = format!(
        "📊 Statistics\n\n\
        Today: {}/{} habits completed\n\
        Weekly average: {:.1}%\n\
        Total habits: {}\n\n\
        📅 This Week:\n{}",
        completed_today,
        total_habits,
        avg_weekly_rate * 100.0,
        total_habits,
        render_week_view(&app.habits, week_start)
    );

    Paragraph::new(stats_text)
        .block(Block::default().borders(Borders::ALL).title("Statistics"))
        .style(Style::default().fg(Color::Cyan))
}

fn render_week_view(habits: &HashMap<String, Habit>, week_start: NaiveDate) -> String {
    let days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    let mut week_view = String::new();

    for (i, day) in days.iter().enumerate() {
        let date = week_start + Duration::days(i as i64);
        let completed_count = habits.values()
            .filter(|habit| habit.is_completed_on(date))
            .count();

        week_view.push_str(&format!("{}: {} ", day, completed_count));
    }

    week_view
}

// Main application event loop
fn run_app() -> Result<(), Box<dyn std::error::Error>> {
    enable_raw_mode()?;
    let mut stdout = io::stdout();
    execute!(stdout, EnterAlternateScreen)?;
    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;

    let mut app = HabitTracker::new();

    loop {
        terminal.draw(|f| ui(f, &app))?;

        if let event::Event::Key(key) = event::read()? {
            match app.mode {
                AppMode::Normal => {
                    match key.code {
                        KeyCode::Char('q') => break,
                        KeyCode::Char(' ') => app.toggle_habit_today(),
                        KeyCode::Down | KeyCode::Char('j') => app.next_habit(),
                        KeyCode::Up | KeyCode::Char('k') => app.previous_habit(),
                        KeyCode::Char('a') => {
                            app.mode = AppMode::AddingHabit;
                            app.input_buffer.clear();
                        },
                        _ => {}
                    }
                },
                AppMode::AddingHabit => {
                    match key.code {
                        KeyCode::Enter => {
                            if !app.input_buffer.is_empty() {
                                app.add_habit(app.input_buffer.clone(), 5); // Default 5x/week
                                app.input_buffer.clear();
                                app.mode = AppMode::Normal;
                            }
                        },
                        KeyCode::Esc => {
                            app.mode = AppMode::Normal;
                            app.input_buffer.clear();
                        },
                        KeyCode::Char(c) => {
                            app.input_buffer.push(c);
                        },
                        KeyCode::Backspace => {
                            app.input_buffer.pop();
                        },
                        _ => {}
                    }
                },
                _ => {}
            }
        }
    }

    disable_raw_mode()?;
    execute!(terminal.backend_mut(), LeaveAlternateScreen)?;
    Ok(())
}

// Command-line interface
use clap::{App, Arg, SubCommand};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let matches = App::new("habit-tracker")
        .version("1.0")
        .about("Terminal-based habit tracker")
        .subcommand(
            SubCommand::with_name("add")
                .about("Add a new habit")
                .arg(Arg::with_name("name")
                    .required(true)
                    .help("Name of the habit"))
                .arg(Arg::with_name("frequency")
                    .short("f")
                    .long("frequency")
                    .value_name("TIMES_PER_WEEK")
                    .help("Target frequency per week")
                    .default_value("5"))
        )
        .subcommand(
            SubCommand::with_name("list")
                .about("List all habits")
        )
        .subcommand(
            SubCommand::with_name("toggle")
                .about("Toggle completion for today")
                .arg(Arg::with_name("habit")
                    .required(true)
                    .help("Name of the habit to toggle"))
        )
        .subcommand(
            SubCommand::with_name("stats")
                .about("Show statistics")
        )
        .subcommand(
            SubCommand::with_name("tui")
                .about("Launch terminal UI")
        )
        .get_matches();

    match matches.subcommand() {
        ("tui", _) => {
            run_app()?;
        },
        ("add", Some(sub_m)) => {
            let name = sub_m.value_of("name").unwrap();
            let frequency: u32 = sub_m.value_of("frequency").unwrap().parse()?;
            println!("Added habit: {} ({}x/week)", name, frequency);
        },
        ("list", _) => {
            println!("📋 Your Habits:");
            println!("• Exercise (5x/week) ✅");
            println!("• Read (7x/week) ⭕");
            println!("• Meditate (7x/week) ✅");
        },
        ("toggle", Some(sub_m)) => {
            let habit = sub_m.value_of("habit").unwrap();
            println!("Toggled completion for: {}", habit);
        },
        ("stats", _) => {
            println!("📊 Habit Statistics:");
            println!("Today: 2/4 habits completed");
            println!("Weekly average: 78.5%");
            println!("Current streak: Exercise (5 days)");
        },
        _ => {
            run_app()?;
        }
    }

    Ok(())
}
```

{{< example title="Terminal UI Best Practices" >}} **Key Principles for Terminal
Applications:**

- **Keyboard-driven navigation** - Vim-like keybindings for efficiency
- **Visual feedback** - Clear indicators for state and completion status
- **Persistent data** - Save state between sessions
- **Multiple interfaces** - Both CLI commands and interactive TUI
- **Performance** - Efficient rendering and minimal resource usage
- **Cross-platform** - Works on Linux, macOS, and Windows {{< /example >}}

### Spotify Terminal Interface in Rust

[Spotify TUI written in Rust](https://www.reddit.com/r/unixporn/comments/dekj2i/oc_a_spotify_terminal_user_interface_written_in/)
showcases advanced terminal UI patterns:

```rust
// Simplified Spotify TUI architecture
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

// Spotify API interaction layer
#[derive(Debug, Clone)]
struct Track {
    name: String,
    artist: String,
    album: String,
    duration_ms: u64,
    is_playing: bool,
}

#[derive(Debug, Clone)]
struct PlaybackState {
    current_track: Option<Track>,
    position_ms: u64,
    volume: u8,
    shuffle: bool,
    repeat: RepeatMode,
}

#[derive(Debug, Clone)]
enum RepeatMode {
    Off,
    Track,
    Context,
}

// Command system for decoupling UI from API
#[derive(Debug)]
enum SpotifyCommand {
    Play,
    Pause,
    Next,
    Previous,
    SetVolume(u8),
    ToggleShuffle,
    CycleRepeat,
    Seek(u64),
}

// Event system for UI updates
#[derive(Debug)]
enum UIEvent {
    PlaybackStateChanged(PlaybackState),
    TrackChanged(Track),
    VolumeChanged(u8),
    Error(String),
}

struct SpotifyController {
    command_sender: mpsc::Sender<SpotifyCommand>,
    event_receiver: mpsc::Receiver<UIEvent>,
}

impl SpotifyController {
    fn new() -> Self {
        let (cmd_tx, cmd_rx) = mpsc::channel();
        let (event_tx, event_rx) = mpsc::channel();

        // Spawn background thread to handle Spotify API calls
        let event_sender = event_tx.clone();
        thread::spawn(move || {
            let mut current_state = PlaybackState {
                current_track: None,
                position_ms: 0,
                volume: 50,
                shuffle: false,
                repeat: RepeatMode::Off,
            };

            loop {
                // Handle commands from UI
                if let Ok(command) = cmd_rx.try_recv() {
                    match command {
                        SpotifyCommand::Play => {
                            // Simulate API call
                            if let Some(ref mut track) = current_state.current_track {
                                track.is_playing = true;
                            }
                            event_sender.send(UIEvent::PlaybackStateChanged(current_state.clone())).ok();
                        },
                        SpotifyCommand::Pause => {
                            if let Some(ref mut track) = current_state.current_track {
                                track.is_playing = false;
                            }
                            event_sender.send(UIEvent::PlaybackStateChanged(current_state.clone())).ok();
                        },
                        SpotifyCommand::SetVolume(vol) => {
                            current_state.volume = vol;
                            event_sender.send(UIEvent::VolumeChanged(vol)).ok();
                        },
                        _ => {
                            // Handle other commands
                        }
                    }
                }

                // Simulate periodic updates
                if let Some(ref track) = current_state.current_track {
                    if track.is_playing {
                        current_state.position_ms += 100;
                        if current_state.position_ms % 1000 == 0 {
                            event_sender.send(UIEvent::PlaybackStateChanged(current_state.clone())).ok();
                        }
                    }
                }

                thread::sleep(Duration::from_millis(100));
            }
        });

        Self {
            command_sender: cmd_tx,
            event_receiver: event_rx,
        }
    }

    fn send_command(&self, command: SpotifyCommand) {
        self.command_sender.send(command).ok();
    }

    fn poll_events(&self) -> Vec<UIEvent> {
        let mut events = Vec::new();
        while let Ok(event) = self.event_receiver.try_recv() {
            events.push(event);
        }
        events
    }
}

// Progress bar widget for track position
fn render_progress_bar(current: u64, total: u64, width: usize) -> String {
    if total == 0 {
        return "─".repeat(width);
    }

    let progress = (current as f64 / total as f64).min(1.0);
    let filled = ((width as f64 * progress) as usize).min(width);
    let empty = width - filled;

    let mut bar = String::new();
    bar.push_str(&"█".repeat(filled));
    bar.push_str(&"─".repeat(empty));

    bar
}

// Format duration in MM:SS format
fn format_duration(ms: u64) -> String {
    let seconds = ms / 1000;
    let minutes = seconds / 60;
    let remaining_seconds = seconds % 60;
    format!("{}:{:02}", minutes, remaining_seconds)
}

// Volume visualization
fn render_volume_bar(volume: u8) -> String {
    let bars = volume / 10;
    let mut result = String::new();

    for i in 0..10 {
        if i < bars {
            result.push('█');
        } else {
            result.push('─');
        }
    }

    format!("🔊 {} ({}%)", result, volume)
}
```

## Backend Development Patterns

### Modern Backend Architecture

[How I write Backends](https://github.com/fpereiro/backendlore) provides
comprehensive backend development philosophy:

```rust
// Modern Rust backend architecture example
use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    response::Json,
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};
use sqlx::{PgPool, Row};
use std::sync::Arc;
use tokio::net::TcpListener;
use tower_http::{cors::CorsLayer, trace::TraceLayer};
use tracing::{info, error};
use uuid::Uuid;

// Domain models
#[derive(Debug, Serialize, Deserialize, Clone)]
struct User {
    id: Uuid,
    username: String,
    email: String,
    created_at: chrono::DateTime<chrono::Utc>,
}

#[derive(Debug, Deserialize)]
struct CreateUserRequest {
    username: String,
    email: String,
}

#[derive(Debug, Deserialize)]
struct UserQuery {
    page: Option<u32>,
    limit: Option<u32>,
    search: Option<String>,
}

// Application state
#[derive(Clone)]
struct AppState {
    db: PgPool,
    config: Arc<Config>,
}

#[derive(Debug)]
struct Config {
    database_url: String,
    port: u16,
    log_level: String,
}

// Repository pattern for data access
struct UserRepository {
    db: PgPool,
}

impl UserRepository {
    fn new(db: PgPool) -> Self {
        Self { db }
    }

    async fn create_user(&self, req: CreateUserRequest) -> Result<User, sqlx::Error> {
        let user_id = Uuid::new_v4();
        let now = chrono::Utc::now();

        let user = sqlx::query_as!(
            User,
            r#"
            INSERT INTO users (id, username, email, created_at)
            VALUES ($1, $2, $3, $4)
            RETURNING id, username, email, created_at
            "#,
            user_id,
            req.username,
            req.email,
            now
        )
        .fetch_one(&self.db)
        .await?;

        Ok(user)
    }

    async fn get_user_by_id(&self, id: Uuid) -> Result<Option<User>, sqlx::Error> {
        let user = sqlx::query_as!(
            User,
            "SELECT id, username, email, created_at FROM users WHERE id = $1",
            id
        )
        .fetch_optional(&self.db)
        .await?;

        Ok(user)
    }

    async fn list_users(&self, query: UserQuery) -> Result<Vec<User>, sqlx::Error> {
        let page = query.page.unwrap_or(1);
        let limit = query.limit.unwrap_or(10).min(100); // Cap at 100
        let offset = (page - 1) * limit;

        let mut sql = "SELECT id, username, email, created_at FROM users".to_string();
        let mut params = Vec::new();

        if let Some(search) = query.search {
            sql.push_str(" WHERE username ILIKE $1 OR email ILIKE $1");
            params.push(format!("%{}%", search));
        }

        sql.push_str(" ORDER BY created_at DESC LIMIT $2 OFFSET $3");

        let mut query_builder = sqlx::query_as::<_, User>(&sql);

        if !params.is_empty() {
            query_builder = query_builder.bind(params[0].clone());
        }

        let users = query_builder
            .bind(limit as i64)
            .bind(offset as i64)
            .fetch_all(&self.db)
            .await?;

        Ok(users)
    }
}

// Service layer for business logic
struct UserService {
    repository: UserRepository,
}

impl UserService {
    fn new(repository: UserRepository) -> Self {
        Self { repository }
    }

    async fn create_user(&self, req: CreateUserRequest) -> Result<User, ServiceError> {
        // Validation
        if req.username.trim().is_empty() {
            return Err(ServiceError::InvalidInput("Username cannot be empty".into()));
        }

        if !req.email.contains('@') {
            return Err(ServiceError::InvalidInput("Invalid email format".into()));
        }

        // Business logic
        let user = self.repository
            .create_user(req)
            .await
            .map_err(|e| match e {
                sqlx::Error::Database(db_err) if db_err.constraint().is_some() => {
                    ServiceError::Conflict("Username or email already exists".into())
                },
                _ => ServiceError::Internal(e.to_string()),
            })?;

        info!("Created user: {}", user.id);
        Ok(user)
    }

    async fn get_user(&self, id: Uuid) -> Result<User, ServiceError> {
        self.repository
            .get_user_by_id(id)
            .await
            .map_err(|e| ServiceError::Internal(e.to_string()))?
            .ok_or(ServiceError::NotFound)
    }

    async fn list_users(&self, query: UserQuery) -> Result<Vec<User>, ServiceError> {
        self.repository
            .list_users(query)
            .await
            .map_err(|e| ServiceError::Internal(e.to_string()))
    }
}

// Error handling
#[derive(Debug)]
enum ServiceError {
    NotFound,
    InvalidInput(String),
    Conflict(String),
    Internal(String),
}

impl From<ServiceError> for (StatusCode, Json<serde_json::Value>) {
    fn from(err: ServiceError) -> Self {
        let (status, message) = match err {
            ServiceError::NotFound => (StatusCode::NOT_FOUND, "Resource not found"),
            ServiceError::InvalidInput(msg) => (StatusCode::BAD_REQUEST, &msg),
            ServiceError::Conflict(msg) => (StatusCode::CONFLICT, &msg),
            ServiceError::Internal(_) => (StatusCode::INTERNAL_SERVER_ERROR, "Internal server error"),
        };

        if matches!(err, ServiceError::Internal(_)) {
            error!("Internal error: {:?}", err);
        }

        (status, Json(serde_json::json!({
            "error": message
        })))
    }
}

// HTTP handlers
async fn create_user_handler(
    State(state): State<AppState>,
    Json(req): Json<CreateUserRequest>,
) -> Result<Json<User>, (StatusCode, Json<serde_json::Value>)> {
    let service = UserService::new(UserRepository::new(state.db));
    let user = service.create_user(req).await?;
    Ok(Json(user))
}

async fn get_user_handler(
    State(state): State<AppState>,
    Path(id): Path<Uuid>,
) -> Result<Json<User>, (StatusCode, Json<serde_json::Value>)> {
    let service = UserService::new(UserRepository::new(state.db));
    let user = service.get_user(id).await?;
    Ok(Json(user))
}

async fn list_users_handler(
    State(state): State<AppState>,
    Query(query): Query<UserQuery>,
) -> Result<Json<Vec<User>>, (StatusCode, Json<serde_json::Value>)> {
    let service = UserService::new(UserRepository::new(state.db));
    let users = service.list_users(query).await?;
    Ok(Json(users))
}

// Health check endpoint
async fn health_check() -> Json<serde_json::Value> {
    Json(serde_json::json!({
        "status": "healthy",
        "timestamp": chrono::Utc::now(),
        "version": env!("CARGO_PKG_VERSION")
    }))
}

// Application setup
async fn create_app(state: AppState) -> Router {
    Router::new()
        .route("/health", get(health_check))
        .route("/users", post(create_user_handler))
        .route("/users", get(list_users_handler))
        .route("/users/:id", get(get_user_handler))
        .with_state(state)
        .layer(CorsLayer::permissive())
        .layer(TraceLayer::new_for_http())
}

// Main application entry point
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize tracing
    tracing_subscriber::fmt()
        .with_env_filter("info,sqlx=warn")
        .init();

    // Load configuration
    let config = Arc::new(Config {
        database_url: std::env::var("DATABASE_URL")?,
        port: std::env::var("PORT")
            .unwrap_or_else(|_| "3000".to_string())
            .parse()?,
        log_level: std::env::var("LOG_LEVEL").unwrap_or_else(|_| "info".to_string()),
    });

    // Setup database connection
    let db = PgPool::connect(&config.database_url).await?;

    // Run migrations
    sqlx::migrate!("./migrations").run(&db).await?;

    // Create application state
    let state = AppState { db, config: config.clone() };

    // Build application
    let app = create_app(state).await;

    // Start server
    let listener = TcpListener::bind(format!("0.0.0.0:{}", config.port)).await?;
    info!("Server starting on port {}", config.port);

    axum::serve(listener, app).await?;

    Ok(())
}

// Integration tests
#[cfg(test)]
mod tests {
    use super::*;
    use axum::http::StatusCode;
    use serde_json::json;
    use sqlx::PgPool;
    use tokio;

    async fn setup_test_db() -> PgPool {
        let database_url = std::env::var("TEST_DATABASE_URL")
            .expect("TEST_DATABASE_URL must be set for tests");

        let pool = PgPool::connect(&database_url).await.unwrap();
        sqlx::migrate!("./migrations").run(&pool).await.unwrap();

        pool
    }

    #[tokio::test]
    async fn test_create_user() {
        let db = setup_test_db().await;
        let service = UserService::new(UserRepository::new(db));

        let req = CreateUserRequest {
            username: "testuser".to_string(),
            email: "test@example.com".to_string(),
        };

        let result = service.create_user(req).await;
        assert!(result.is_ok());

        let user = result.unwrap();
        assert_eq!(user.username, "testuser");
        assert_eq!(user.email, "test@example.com");
    }

    #[tokio::test]
    async fn test_invalid_email() {
        let db = setup_test_db().await;
        let service = UserService::new(UserRepository::new(db));

        let req = CreateUserRequest {
            username: "testuser".to_string(),
            email: "invalid-email".to_string(),
        };

        let result = service.create_user(req).await;
        assert!(result.is_err());

        if let Err(ServiceError::InvalidInput(_)) = result {
            // Expected
        } else {
            panic!("Expected InvalidInput error");
        }
    }
}
```

{{< tip title="Backend Architecture Principles" >}} **Key Design Patterns:**

- **Layered architecture** - Clear separation between handlers, services, and
  repositories
- **Dependency injection** - Use of state and configuration injection
- **Error handling** - Comprehensive error types with proper HTTP mapping
- **Testing** - Unit tests for business logic, integration tests for full stack
- **Configuration** - Environment-based configuration management
- **Observability** - Structured logging and health checks {{< /tip >}}

## Pi-hole Network Setup

### Pi-hole with Unbound DNS

[Pi-hole Unbound](https://docs.pi-hole.net/guides/unbound/) and
[Pi-Hole Tips](https://www.reddit.com/r/pihole/comments/dezyvy/into_the_pihole_you_should_go_8_months_later/)
provide advanced DNS configuration:

```bash
#!/bin/bash
# Pi-hole with Unbound recursive DNS setup

# Install Pi-hole and Unbound
curl -sSL https://install.pi-hole.net | bash
sudo apt update && sudo apt install unbound

# Configure Unbound as recursive DNS resolver
sudo tee /etc/unbound/unbound.conf.d/pi-hole.conf << 'EOF'
server:
    # Performance
    num-threads: 4
    msg-cache-slabs: 8
    rrset-cache-slabs: 8
    infra-cache-slabs: 8
    key-cache-slabs: 8

    # Memory optimization
    rrset-cache-size: 256m
    msg-cache-size: 128m
    so-rcvbuf: 1m

    # Network settings
    port: 5335
    do-ip4: yes
    do-ip6: yes
    do-udp: yes
    do-tcp: yes

    # Privacy and security
    hide-identity: yes
    hide-version: yes
    harden-glue: yes
    harden-dnssec-stripped: yes
    harden-below-nxdomain: yes
    harden-referral-path: yes
    unwanted-reply-threshold: 10000000

    # Prefetching
    prefetch: yes
    prefetch-key: yes

    # Access control
    access-control: 127.0.0.1/32 allow
    access-control: 192.168.0.0/16 allow
    access-control: 172.16.0.0/12 allow
    access-control: 10.0.0.0/8 allow

    # Root hints
    root-hints: "/var/lib/unbound/root.hints"

    # Logging (for debugging)
    verbosity: 0
    log-queries: no

    # Local zone for Pi-hole
    private-address: 192.168.0.0/16
    private-address: 172.16.0.0/12
    private-address: 10.0.0.0/8
    private-domain: "local"
    domain-insecure: "local"

forward-zone:
    name: "."
    forward-tls-upstream: yes
    # Cloudflare DNS over TLS
    forward-addr: 1.1.1.1@853#cloudflare-dns.com
    forward-addr: 1.0.0.1@853#cloudflare-dns.com
    # Quad9 DNS over TLS
    forward-addr: 9.9.9.9@853#dns.quad9.net
    forward-addr: 149.112.112.112@853#dns.quad9.net
EOF

# Download root hints for Unbound
sudo wget -O /var/lib/unbound/root.hints https://www.internic.net/domain/named.cache
sudo chown unbound:unbound /var/lib/unbound/root.hints

# Configure Pi-hole to use Unbound
sudo pihole -a -p  # Set admin password
echo "Custom 1 (IPv4): 127.0.0.1#5335" | sudo tee -a /etc/pihole/setupVars.conf

# Restart services
sudo systemctl restart unbound
sudo systemctl restart pihole-FTL

# Test DNS resolution
dig @127.0.0.1 -p 5335 google.com
dig @192.168.1.100 google.com  # Test through Pi-hole

# Performance monitoring script
cat > /usr/local/bin/pihole-monitor.sh << 'EOF'
#!/bin/bash
# Pi-hole monitoring and statistics

echo "=== Pi-hole Status ==="
pihole status

echo -e "\n=== DNS Query Statistics ==="
pihole -c -j | jq '{
    dns_queries_today,
    ads_blocked_today,
    ads_percentage_today,
    unique_domains,
    queries_forwarded,
    queries_cached,
    clients_ever_seen,
    unique_clients,
    dns_queries_all_types
}'

echo -e "\n=== Top Blocked Domains ==="
pihole -t 10

echo -e "\n=== Top Clients ==="
pihole -c | head -10

echo -e "\n=== Network Tests ==="
echo "Testing DNS resolution speed..."
time nslookup google.com 127.0.0.1
time nslookup facebook.com 127.0.0.1

echo -e "\n=== Unbound Status ==="
sudo systemctl status unbound --no-pager -l

echo -e "\n=== Memory Usage ==="
free -h
df -h | grep -E "/$|/var"

echo -e "\n=== Network Connections ==="
ss -tuln | grep -E ":53|:5335|:80|:443"
EOF

chmod +x /usr/local/bin/pihole-monitor.sh

# Automated blocklist updates
cat > /etc/cron.daily/pihole-update << 'EOF'
#!/bin/bash
# Update Pi-hole blocklists and restart if needed

pihole -g > /var/log/pihole-update.log 2>&1

# Check if update was successful
if [ $? -eq 0 ]; then
    echo "$(date): Pi-hole blocklists updated successfully" >> /var/log/pihole-update.log

    # Restart FTL to reload lists
    sudo systemctl restart pihole-FTL

    # Update Unbound root hints monthly
    if [ $(date +%d) -eq 01 ]; then
        wget -O /tmp/root.hints https://www.internic.net/domain/named.cache
        if [ $? -eq 0 ]; then
            sudo mv /tmp/root.hints /var/lib/unbound/root.hints
            sudo chown unbound:unbound /var/lib/unbound/root.hints
            sudo systemctl restart unbound
            echo "$(date): Unbound root hints updated" >> /var/log/pihole-update.log
        fi
    fi
else
    echo "$(date): Pi-hole update failed" >> /var/log/pihole-update.log
fi
EOF

chmod +x /etc/cron.daily/pihole-update

# Custom blocklist management
cat > /usr/local/bin/manage-blocklists.sh << 'EOF'
#!/bin/bash
# Custom blocklist management

CUSTOM_LISTS=(
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
    "https://mirror1.malwaredomains.com/files/justdomains"
    "https://s3.amazonaws.com/lists.disconnect.me/simple_tracking.txt"
    "https://s3.amazonaws.com/lists.disconnect.me/simple_ad.txt"
)

WHITELIST_DOMAINS=(
    "s.youtube.com"
    "video-stats.l.google.com"
    "clients4.google.com"
    "ocsp.apple.com"
)

echo "Adding custom blocklists..."
for list in "${CUSTOM_LISTS[@]}"; do
    pihole -b "$list"
done

echo "Adding whitelist domains..."
for domain in "${WHITELIST_DOMAINS[@]}"; do
    pihole -w "$domain"
done

echo "Updating gravity..."
pihole -g

echo "Custom configuration complete!"
EOF

chmod +x /usr/local/bin/manage-blocklists.sh
```

### Network Performance Monitoring

```python
#!/usr/bin/env python3
# network_monitor.py - Monitor Pi-hole and network performance

import subprocess
import json
import time
import requests
from datetime import datetime, timedelta
import sqlite3
import argparse

class NetworkMonitor:
    def __init__(self, pihole_host="localhost", pihole_token=None):
        self.pihole_host = pihole_host
        self.pihole_token = pihole_token
        self.db_path = "/var/log/network_monitor.db"
        self.init_database()

    def init_database(self):
        """Initialize SQLite database for storing metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dns_metrics (
                timestamp DATETIME,
                queries_today INTEGER,
                blocked_today INTEGER,
                block_percentage REAL,
                clients_seen INTEGER,
                unique_domains INTEGER,
                queries_cached INTEGER,
                queries_forwarded INTEGER
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                timestamp DATETIME,
                dns_response_time_ms REAL,
                internet_latency_ms REAL,
                memory_usage_percent REAL,
                cpu_usage_percent REAL,
                disk_usage_percent REAL
            )
        ''')

        conn.commit()
        conn.close()

    def get_pihole_stats(self):
        """Fetch Pi-hole statistics"""
        try:
            url = f"http://{self.pihole_host}/admin/api.php"
            params = {}
            if self.pihole_token:
                params['auth'] = self.pihole_token

            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching Pi-hole stats: {e}")
            return None

    def measure_dns_performance(self):
        """Measure DNS resolution performance"""
        test_domains = [
            "google.com",
            "github.com",
            "stackoverflow.com",
            "wikipedia.org"
        ]

        total_time = 0
        successful_queries = 0

        for domain in test_domains:
            try:
                start_time = time.time()
                result = subprocess.run(
                    ["nslookup", domain, self.pihole_host],
                    capture_output=True,
                    timeout=5
                )
                end_time = time.time()

                if result.returncode == 0:
                    total_time += (end_time - start_time) * 1000  # Convert to ms
                    successful_queries += 1

            except subprocess.TimeoutExpired:
                print(f"DNS query timeout for {domain}")
            except Exception as e:
                print(f"DNS query error for {domain}: {e}")

        if successful_queries > 0:
            return total_time / successful_queries
        return None

    def measure_internet_latency(self):
        """Measure internet connectivity latency"""
        try:
            result = subprocess.run(
                ["ping", "-c", "3", "8.8.8.8"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                # Parse ping output for average time
                lines = result.stdout.split('\n')
                for line in lines:
                    if "avg" in line:
                        # Extract average time from line like "round-trip min/avg/max/stddev = 1.2/3.4/5.6/7.8 ms"
                        parts = line.split('=')[1].strip().split('/')
                        if len(parts) >= 2:
                            return float(parts[1])

        except Exception as e:
            print(f"Error measuring internet latency: {e}")

        return None

    def get_system_metrics(self):
        """Get system resource usage"""
        metrics = {}

        try:
            # Memory usage
            result = subprocess.run(["free", "-m"], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if line.startswith('Mem:'):
                    parts = line.split()
                    total = int(parts[1])
                    used = int(parts[2])
                    metrics['memory_usage_percent'] = (used / total) * 100
                    break

            # CPU usage (simplified)
            result = subprocess.run(
                ["top", "-bn1"],
                capture_output=True,
                text=True
            )
            lines = result.stdout.split('\n')
            for line in lines:
                if '%Cpu(s):' in line:
                    # Parse CPU usage from top output
                    parts = line.split(',')[0].split()
                    cpu_usage = float(parts[1].replace('%us', ''))
                    metrics['cpu_usage_percent'] = cpu_usage
                    break

            # Disk usage
            result = subprocess.run(["df", "/"], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                if len(parts) >= 5:
                    usage_percent = int(parts[4].replace('%', ''))
                    metrics['disk_usage_percent'] = usage_percent

        except Exception as e:
            print(f"Error getting system metrics: {e}")

        return metrics

    def store_metrics(self, dns_stats, performance_metrics):
        """Store metrics in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.now()

        # Store DNS metrics
        if dns_stats:
            cursor.execute('''
                INSERT INTO dns_metrics VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                timestamp,
                dns_stats.get('dns_queries_today', 0),
                dns_stats.get('ads_blocked_today', 0),
                dns_stats.get('ads_percentage_today', 0.0),
                dns_stats.get('clients_ever_seen', 0),
                dns_stats.get('unique_domains', 0),
                dns_stats.get('queries_cached', 0),
                dns_stats.get('queries_forwarded', 0)
            ))

        # Store performance metrics
        cursor.execute('''
            INSERT INTO performance_metrics VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            timestamp,
            performance_metrics.get('dns_response_time', 0.0),
            performance_metrics.get('internet_latency', 0.0),
            performance_metrics.get('memory_usage_percent', 0.0),
            performance_metrics.get('cpu_usage_percent', 0.0),
            performance_metrics.get('disk_usage_percent', 0.0)
        ))

        conn.commit()
        conn.close()

    def run_monitoring_cycle(self):
        """Run one complete monitoring cycle"""
        print(f"[{datetime.now()}] Running monitoring cycle...")

        # Collect Pi-hole statistics
        dns_stats = self.get_pihole_stats()

        # Measure performance
        performance_metrics = {}
        performance_metrics['dns_response_time'] = self.measure_dns_performance()
        performance_metrics['internet_latency'] = self.measure_internet_latency()
        performance_metrics.update(self.get_system_metrics())

        # Store metrics
        self.store_metrics(dns_stats, performance_metrics)

        # Print summary
        if dns_stats:
            print(f"  DNS Queries: {dns_stats.get('dns_queries_today', 'N/A')}")
            print(f"  Blocked: {dns_stats.get('ads_blocked_today', 'N/A')} ({dns_stats.get('ads_percentage_today', 0):.1f}%)")

        if performance_metrics.get('dns_response_time'):
            print(f"  DNS Response Time: {performance_metrics['dns_response_time']:.1f}ms")

        if performance_metrics.get('internet_latency'):
            print(f"  Internet Latency: {performance_metrics['internet_latency']:.1f}ms")

        print(f"  Memory Usage: {performance_metrics.get('memory_usage_percent', 0):.1f}%")
        print(f"  CPU Usage: {performance_metrics.get('cpu_usage_percent', 0):.1f}%")
        print(f"  Disk Usage: {performance_metrics.get('disk_usage_percent', 0):.1f}%")

    def generate_report(self, hours=24):
        """Generate performance report for the last N hours"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        since = datetime.now() - timedelta(hours=hours)

        # DNS statistics
        cursor.execute('''
            SELECT AVG(block_percentage), MAX(queries_today), MAX(blocked_today)
            FROM dns_metrics
            WHERE timestamp > ?
        ''', (since,))

        dns_result = cursor.fetchone()

        # Performance statistics
        cursor.execute('''
            SELECT AVG(dns_response_time_ms), AVG(internet_latency_ms),
                   AVG(memory_usage_percent), AVG(cpu_usage_percent)
            FROM performance_metrics
            WHERE timestamp > ?
        ''', (since,))

        perf_result = cursor.fetchone()

        print(f"\n=== Network Performance Report (Last {hours} hours) ===")
        if dns_result[0] is not None:
            print(f"Average Block Rate: {dns_result[0]:.1f}%")
            print(f"Peak Queries: {dns_result[1]}")
            print(f"Peak Blocked: {dns_result[2]}")

        if perf_result[0] is not None:
            print(f"Average DNS Response Time: {perf_result[0]:.1f}ms")
            print(f"Average Internet Latency: {perf_result[1]:.1f}ms")
            print(f"Average Memory Usage: {perf_result[2]:.1f}%")
            print(f"Average CPU Usage: {perf_result[3]:.1f}%")

        conn.close()

def main():
    parser = argparse.ArgumentParser(description="Pi-hole Network Monitor")
    parser.add_argument("--host", default="localhost", help="Pi-hole host")
    parser.add_argument("--token", help="Pi-hole API token")
    parser.add_argument("--interval", type=int, default=300, help="Monitoring interval in seconds")
    parser.add_argument("--report", type=int, help="Generate report for last N hours")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")

    args = parser.parse_args()

    monitor = NetworkMonitor(args.host, args.token)

    if args.report:
        monitor.generate_report(args.report)
    elif args.daemon:
        print(f"Starting network monitoring daemon (interval: {args.interval}s)")
        try:
            while True:
                monitor.run_monitoring_cycle()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
    else:
        monitor.run_monitoring_cycle()

if __name__ == "__main__":
    main()
```

## Development Tools and Resources

### System Design Learning

[System Design for Advanced Beginners](https://robertheaton.com/2020/04/06/systems-design-for-advanced-beginners/)
provides practical system design education:

{{< note title="System Design Principles" >}} **Key Concepts for Backend
Systems:**

- **Scalability patterns** - Horizontal vs vertical scaling strategies
- **Data storage** - Choosing between SQL, NoSQL, and caching layers
- **Load balancing** - Distributing traffic across multiple servers
- **Microservices** - Service decomposition and communication patterns
- **Monitoring** - Observability, logging, and alerting strategies
- **Security** - Authentication, authorization, and data protection
  {{< /note >}}

### Testing and Quality Assurance

[Testing Dash Applications using Pytest and Selenium](https://dash.plotly.com/testing)
demonstrates comprehensive testing approaches:

```rust
// Rust testing patterns for system applications
#[cfg(test)]
mod tests {
    use super::*;
    use std::time::Duration;
    use tokio::time::timeout;

    // Unit tests for individual components
    #[test]
    fn test_habit_creation() {
        let habit = Habit::new("Test Habit".to_string(), 5);
        assert_eq!(habit.name, "Test Habit");
        assert_eq!(habit.target_frequency, 5);
        assert!(habit.completed_dates.is_empty());
    }

    #[test]
    fn test_habit_completion_tracking() {
        let mut habit = Habit::new("Test".to_string(), 7);
        let date = NaiveDate::from_ymd_opt(2020, 7, 21).unwrap();

        assert!(!habit.is_completed_on(date));

        habit.mark_completed(date);
        assert!(habit.is_completed_on(date));

        // Test idempotency
        habit.mark_completed(date);
        assert_eq!(habit.completed_dates.len(), 1);
    }

    #[test]
    fn test_streak_calculation() {
        let mut habit = Habit::new("Test".to_string(), 7);
        let today = Local::now().date_naive();

        // No streak initially
        assert_eq!(habit.streak(), 0);

        // Mark today and yesterday
        habit.mark_completed(today);
        habit.mark_completed(today - Duration::days(1));

        assert_eq!(habit.streak(), 2);
    }

    // Integration tests for the full system
    #[tokio::test]
    async fn test_habit_tracker_integration() {
        let mut tracker = HabitTracker::new();

        // Test adding habit
        tracker.add_habit("Integration Test".to_string(), 3);
        assert!(tracker.habits.contains_key("Integration Test"));

        // Test selection
        tracker.selected_habit = Some("Integration Test".to_string());

        // Test completion toggle
        let initial_completed = tracker.habits["Integration Test"]
            .is_completed_on(Local::now().date_naive());

        tracker.toggle_habit_today();

        let after_toggle = tracker.habits["Integration Test"]
            .is_completed_on(Local::now().date_naive());

        assert_ne!(initial_completed, after_toggle);
    }

    // Performance tests
    #[test]
    fn test_large_habit_list_performance() {
        use std::time::Instant;

        let mut tracker = HabitTracker::new();

        // Add many habits
        let start = Instant::now();
        for i in 0..1000 {
            tracker.add_habit(format!("Habit {}", i), 5);
        }
        let add_duration = start.elapsed();

        assert!(add_duration < Duration::from_millis(100));
        assert_eq!(tracker.habits.len(), 1003); // 1000 + 3 default habits
    }

    // Property-based testing with proptest (if available)
    #[cfg(feature = "proptest")]
    mod property_tests {
        use super::*;
        use proptest::prelude::*;

        proptest! {
            #[test]
            fn test_habit_frequency_invariants(
                name in "[a-zA-Z ]{1,50}",
                frequency in 1u32..8u32
            ) {
                let habit = Habit::new(name.clone(), frequency);

                // Properties that should always hold
                prop_assert_eq!(habit.name, name);
                prop_assert_eq!(habit.target_frequency, frequency);
                prop_assert!(habit.completed_dates.is_empty());
                prop_assert!(habit.streak() == 0);
            }
        }
    }
}

// Benchmark tests
#[cfg(test)]
mod benches {
    use super::*;
    use criterion::{black_box, criterion_group, criterion_main, Criterion};

    fn benchmark_habit_operations(c: &mut Criterion) {
        let mut tracker = HabitTracker::new();

        // Add test data
        for i in 0..100 {
            tracker.add_habit(format!("Habit {}", i), 5);
        }

        c.bench_function("habit navigation", |b| {
            b.iter(|| {
                tracker.next_habit();
                black_box(&tracker.selected_habit);
            })
        });

        c.bench_function("habit toggle", |b| {
            b.iter(|| {
                tracker.toggle_habit_today();
            })
        });
    }

    criterion_group!(benches, benchmark_habit_operations);
    criterion_main!(benches);
}
```

## Key Learning Insights

### Systems Programming in Rust

Today's exploration of terminal applications in Rust demonstrated several key
advantages:

- **Memory safety** without garbage collection enables efficient system
  utilities
- **Cross-platform support** through crates like `crossterm` and `tui`
- **Rich ecosystem** for terminal UI, networking, and system interaction
- **Performance** characteristics suitable for real-time applications

### Backend Architecture Patterns

The backend development patterns revealed modern approaches to scalable systems:

- **Layered architecture** provides clear separation of concerns
- **Async/await** enables high-concurrency request handling
- **Type safety** prevents entire classes of runtime errors
- **Testing strategies** ensure reliability at multiple levels

### Network Infrastructure

The Pi-hole configuration demonstrated sophisticated DNS management:

- **Recursive DNS** with Unbound provides privacy and performance
- **Monitoring systems** enable proactive network management
- **Automation** reduces manual configuration overhead
- **Security** through DNS filtering and encrypted upstream queries

### Development Productivity

The combination of tools and practices explored today emphasizes:

- **Measurement-driven optimization** - Profile before optimizing
- **Comprehensive testing** - Unit, integration, and property-based tests
- **Infrastructure as code** - Reproducible configurations
- **Observability** - Logging, metrics, and monitoring built-in

---

_Today's exploration reinforced that modern systems programming combines
performance, safety, and developer productivity through careful tool selection
and architectural decisions._
