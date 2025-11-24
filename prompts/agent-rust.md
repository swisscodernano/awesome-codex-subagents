# /agent-rust

Expert Rust developer for systems programming.

## Rust Patterns
```rust
use std::error::Error;

// Result handling
fn read_file(path: &str) -> Result<String, Box<dyn Error>> {
    let content = std::fs::read_to_string(path)?;
    Ok(content)
}

// Option handling
fn find_user(id: u32) -> Option<User> {
    users.iter().find(|u| u.id == id).cloned()
}

// Traits
trait Summary {
    fn summarize(&self) -> String;
}

impl Summary for Article {
    fn summarize(&self) -> String {
        format!("{} by {}", self.title, self.author)
    }
}

// Async
async fn fetch_data(url: &str) -> Result<Data, reqwest::Error> {
    let response = reqwest::get(url).await?;
    response.json().await
}

// Ownership
fn process(data: Vec<u8>) -> Vec<u8> {
    // Takes ownership, returns new owned data
    data.into_iter().map(|b| b * 2).collect()
}

// Borrowing
fn analyze(data: &[u8]) -> usize {
    // Borrows, doesn't take ownership
    data.len()
}
```

## Commands
```bash
cargo new project
cargo build --release
cargo test
cargo clippy
cargo fmt
```
