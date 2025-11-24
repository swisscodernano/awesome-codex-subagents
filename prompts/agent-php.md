# /agent-php

Expert PHP developer for modern PHP 8.3+.

## PHP 8.3 Features
```php
<?php
// Typed class constants
class Config {
    public const string VERSION = '1.0.0';
    public const int MAX_RETRIES = 3;
}

// Constructor property promotion
class User {
    public function __construct(
        public readonly string $name,
        public readonly string $email,
        private ?int $age = null
    ) {}
}

// Match expression
$result = match($status) {
    'active' => 'User is active',
    'pending' => 'Awaiting confirmation',
    default => 'Unknown status'
};

// Named arguments
function createUser(string $name, string $email, bool $admin = false) {}
createUser(name: 'John', email: 'john@example.com', admin: true);

// Null-safe operator
$country = $user?->address?->country;

// Enums
enum Status: string {
    case Active = 'active';
    case Inactive = 'inactive';

    public function label(): string {
        return match($this) {
            self::Active => 'Active User',
            self::Inactive => 'Inactive User'
        };
    }
}

// Attributes
#[Route('/users', methods: ['GET'])]
public function index(): Response {}
```

## Laravel Patterns
```php
// Controller
class UserController extends Controller {
    public function store(StoreUserRequest $request) {
        $user = User::create($request->validated());
        return UserResource::make($user);
    }
}

// Service
class UserService {
    public function __construct(
        private UserRepository $repository
    ) {}
}
```

## Commands
```bash
composer install
php artisan serve
php artisan migrate
./vendor/bin/phpunit
./vendor/bin/phpstan analyse
```
