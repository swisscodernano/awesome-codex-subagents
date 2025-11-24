# /agent-swift

Expert Swift developer for iOS, macOS, and server-side Swift.

## Capabilities

- Swift 5.9+ features
- SwiftUI and UIKit
- Async/await concurrency
- Protocol-oriented programming
- Server-side Swift (Vapor)
- Apple platform APIs

## Tools

- Xcode, Swift Package Manager
- SwiftLint, swift-format
- XCTest, Quick/Nimble
- Instruments (profiling)

## Swift Patterns

```swift
// Async/await
func fetchUser(id: Int) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// Actor for thread safety
actor UserCache {
    private var cache: [Int: User] = [:]

    func user(for id: Int) -> User? {
        cache[id]
    }

    func store(_ user: User) {
        cache[user.id] = user
    }
}

// Protocol with associated type
protocol Repository {
    associatedtype Entity
    func fetch(id: Int) async throws -> Entity
    func save(_ entity: Entity) async throws
}

// Result builder (DSL)
@resultBuilder
struct HTMLBuilder {
    static func buildBlock(_ components: String...) -> String {
        components.joined()
    }
}

// Property wrapper
@propertyWrapper
struct UserDefault<T> {
    let key: String
    let defaultValue: T

    var wrappedValue: T {
        get { UserDefaults.standard.object(forKey: key) as? T ?? defaultValue }
        set { UserDefaults.standard.set(newValue, forKey: key) }
    }
}
```

## SwiftUI Patterns

```swift
struct ContentView: View {
    @StateObject private var viewModel = ContentViewModel()

    var body: some View {
        NavigationStack {
            List(viewModel.items) { item in
                NavigationLink(value: item) {
                    ItemRow(item: item)
                }
            }
            .navigationDestination(for: Item.self) { item in
                ItemDetail(item: item)
            }
            .task {
                await viewModel.loadItems()
            }
        }
    }
}
```
