# /agent-typescript

Expert TypeScript developer for type-safe code.

## TypeScript Patterns
```typescript
// Interfaces
interface User {
  id: number;
  name: string;
  email?: string; // optional
  readonly createdAt: Date;
}

// Type aliases
type Status = 'active' | 'inactive' | 'pending';
type Handler<T> = (data: T) => void;

// Generics
function first<T>(array: T[]): T | undefined {
  return array[0];
}

// Utility types
type PartialUser = Partial<User>;
type RequiredUser = Required<User>;
type ReadonlyUser = Readonly<User>;
type UserKeys = keyof User;
type NameOnly = Pick<User, 'name'>;
type WithoutEmail = Omit<User, 'email'>;

// Discriminated unions
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: Error };

// Type guards
function isUser(obj: unknown): obj is User {
  return typeof obj === 'object' && obj !== null && 'id' in obj;
}

// Satisfies operator
const config = {
  port: 3000,
  host: 'localhost'
} satisfies Record<string, string | number>;

// Const assertions
const STATUSES = ['active', 'inactive'] as const;
type StatusType = typeof STATUSES[number];
```

## tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```
