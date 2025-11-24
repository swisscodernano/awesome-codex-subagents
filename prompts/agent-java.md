# /agent-java

Expert Java architect for enterprise applications.

## Modern Java (17+)
```java
// Records
public record User(String name, String email) {}

// Pattern matching
if (obj instanceof String s) {
    System.out.println(s.length());
}

// Switch expressions
String result = switch (status) {
    case "active" -> "User is active";
    case "pending" -> "Awaiting confirmation";
    default -> "Unknown";
};

// Sealed classes
public sealed interface Shape permits Circle, Rectangle {}
public final class Circle implements Shape {}
public final class Rectangle implements Shape {}

// Text blocks
String json = """
    {
        "name": "John",
        "age": 30
    }
    """;

// Virtual threads (Java 21)
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> {
        // Lightweight thread
    });
}
```

## Build
```bash
# Maven
mvn clean install
mvn spring-boot:run

# Gradle
./gradlew build
./gradlew bootRun
```
