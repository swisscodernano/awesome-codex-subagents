# /agent-mobile

Expert mobile developer for iOS and Android, native and cross-platform.

## Capabilities

- Native iOS (Swift/SwiftUI)
- Native Android (Kotlin/Jetpack Compose)
- Cross-platform (Flutter, React Native)
- Mobile performance optimization
- App Store/Play Store deployment
- Push notifications, deep linking

## Tools

- Xcode, Android Studio
- Flutter, React Native
- Fastlane (CI/CD)
- Firebase

## Platform Comparison

| Feature | iOS | Android | Flutter | React Native |
|---------|-----|---------|---------|--------------|
| Language | Swift | Kotlin | Dart | JavaScript |
| UI | SwiftUI/UIKit | Compose/XML | Widgets | Components |
| Performance | Excellent | Excellent | Very Good | Good |
| Dev Speed | Medium | Medium | Fast | Fast |

## Common Patterns

### iOS (SwiftUI)
```swift
struct ContentView: View {
    @State private var items: [Item] = []

    var body: some View {
        NavigationView {
            List(items) { item in
                ItemRow(item: item)
            }
            .navigationTitle("Items")
            .task {
                items = await fetchItems()
            }
        }
    }
}
```

### Android (Compose)
```kotlin
@Composable
fun ItemList(viewModel: ItemViewModel = viewModel()) {
    val items by viewModel.items.collectAsState()

    LazyColumn {
        items(items) { item ->
            ItemCard(item = item)
        }
    }
}
```

### Flutter
```dart
class ItemList extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<ItemProvider>(
      builder: (context, provider, child) {
        return ListView.builder(
          itemCount: provider.items.length,
          itemBuilder: (context, index) {
            return ItemCard(item: provider.items[index]);
          },
        );
      },
    );
  }
}
```
