# /agent-golang

Expert Go developer for high-performance systems.

## Go Patterns
```go
// Error handling
func readFile(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("read file %s: %w", path, err)
    }
    return data, nil
}

// Interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

// Goroutines and channels
func worker(jobs <-chan int, results chan<- int) {
    for j := range jobs {
        results <- j * 2
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)

    // Start workers
    for w := 0; w < 3; w++ {
        go worker(jobs, results)
    }

    // Send jobs
    for j := 0; j < 5; j++ {
        jobs <- j
    }
    close(jobs)

    // Collect results
    for a := 0; a < 5; a++ {
        <-results
    }
}

// Context for cancellation
func fetch(ctx context.Context, url string) error {
    req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    return nil
}
```

## Commands
```bash
go mod init module-name
go build
go test ./...
go run main.go
go fmt ./...
golangci-lint run
```
