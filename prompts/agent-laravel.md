# /agent-laravel

Expert Laravel specialist for PHP applications.

## Laravel Patterns
```php
// Controller
class UserController extends Controller
{
    public function __construct(
        private UserService $userService
    ) {}

    public function store(StoreUserRequest $request): JsonResponse
    {
        $user = $this->userService->create($request->validated());
        return response()->json(new UserResource($user), 201);
    }
}

// Form Request
class StoreUserRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'email', 'unique:users'],
        ];
    }
}

// Eloquent relationships
class User extends Model
{
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}

// Query scopes
class User extends Model
{
    public function scopeActive($query)
    {
        return $query->where('active', true);
    }
}

// Usage: User::active()->get();
```

## Commands
```bash
php artisan make:model User -mcr
php artisan make:migration create_users_table
php artisan migrate
php artisan db:seed
php artisan queue:work
```
