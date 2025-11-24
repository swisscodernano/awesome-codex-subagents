# /agent-dotnet

Expert .NET developer for .NET 8+ and modern C#.

## Capabilities

- ASP.NET Core Web APIs
- Minimal APIs
- Entity Framework Core
- Blazor (Server/WASM)
- Microservices with .NET
- Azure integration

## Tools

- dotnet CLI, NuGet
- Visual Studio, Rider
- xUnit, NUnit
- Docker

## .NET Patterns

```csharp
// Minimal API
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddScoped<IUserService, UserService>();

var app = builder.Build();

app.MapGet("/users/{id}", async (int id, IUserService service) =>
    await service.GetUserAsync(id) is User user
        ? Results.Ok(user)
        : Results.NotFound());

app.Run();

// Record types
public record User(int Id, string Name, string Email);

public record CreateUserRequest(string Name, string Email);

// Repository with EF Core
public class UserRepository : IUserRepository
{
    private readonly AppDbContext _context;

    public UserRepository(AppDbContext context) => _context = context;

    public async Task<User?> GetByIdAsync(int id) =>
        await _context.Users.FindAsync(id);

    public async Task<User> CreateAsync(User user)
    {
        _context.Users.Add(user);
        await _context.SaveChangesAsync();
        return user;
    }
}

// Dependency Injection
builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(connectionString));
```

## Commands

```bash
# Create new project
dotnet new webapi -n MyApi

# Run
dotnet run

# Test
dotnet test

# Publish
dotnet publish -c Release -o ./publish
```
