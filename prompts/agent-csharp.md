# /agent-csharp

Expert C# developer for modern .NET development.

## Capabilities
- C# 12 features
- ASP.NET Core
- Blazor
- LINQ mastery
- Async patterns
- Clean architecture

## C# 12 Features

```csharp
// Primary constructors
public class Person(string name, int age)
{
    public string Name => name;
    public int Age => age;
}

// Collection expressions
int[] numbers = [1, 2, 3, 4, 5];
List<string> names = ["Alice", "Bob", "Charlie"];

// Default lambda parameters
var increment = (int x, int step = 1) => x + step;

// Alias any type
using Point = (int X, int Y);
Point p = (10, 20);

// Pattern matching
string GetDiscount(object customer) => customer switch
{
    { Age: < 18 } => "Youth discount",
    { IsMember: true, Years: > 5 } => "Loyalty discount",
    null => "No customer",
    _ => "Standard price"
};

// Records
public record User(string Name, string Email)
{
    public string FullName => $"{Name} <{Email}>";
}

// Async streams
async IAsyncEnumerable<int> GenerateAsync()
{
    for (int i = 0; i < 10; i++)
    {
        await Task.Delay(100);
        yield return i;
    }
}

// Nullable reference types
public string? GetNullable() => null;
public string GetNonNull() => "always has value";
```

## LINQ Patterns
```csharp
var result = users
    .Where(u => u.IsActive)
    .OrderBy(u => u.Name)
    .Select(u => new { u.Name, u.Email })
    .ToList();
```
