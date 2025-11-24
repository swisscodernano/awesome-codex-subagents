# /agent-flutter

Expert Flutter developer for cross-platform apps.

## Flutter Patterns
```dart
// StatefulWidget
class Counter extends StatefulWidget {
  @override
  _CounterState createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  int _count = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $_count'),
        ElevatedButton(
          onPressed: () => setState(() => _count++),
          child: Text('Increment'),
        ),
      ],
    );
  }
}

// Provider state management
class UserProvider extends ChangeNotifier {
  User? _user;
  User? get user => _user;

  Future<void> login(String email, String password) async {
    _user = await authService.login(email, password);
    notifyListeners();
  }
}

// Consumer widget
Consumer<UserProvider>(
  builder: (context, provider, child) {
    if (provider.user == null) return LoginScreen();
    return HomeScreen(user: provider.user!);
  },
)
```

## Commands
```bash
flutter create app_name
flutter run
flutter build apk
flutter build ios
flutter test
flutter pub get
```
