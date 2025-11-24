# /agent-nextjs

Expert Next.js developer for full-stack React.

## App Router (Next.js 14+)
```typescript
// app/users/page.tsx (Server Component)
async function UsersPage() {
  const users = await db.users.findMany();
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

// app/users/[id]/page.tsx
async function UserPage({ params }: { params: { id: string } }) {
  const user = await db.users.findUnique({ where: { id: params.id } });
  return <UserProfile user={user} />;
}

// Server Actions
'use server';

async function createUser(formData: FormData) {
  const name = formData.get('name');
  await db.users.create({ data: { name } });
  revalidatePath('/users');
}

// Client Component
'use client';

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

## API Routes
```typescript
// app/api/users/route.ts
export async function GET() {
  const users = await db.users.findMany();
  return Response.json(users);
}

export async function POST(request: Request) {
  const data = await request.json();
  const user = await db.users.create({ data });
  return Response.json(user, { status: 201 });
}
```

## Commands
```bash
npx create-next-app@latest
npm run dev
npm run build
npm start
```
