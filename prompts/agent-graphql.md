# /agent-graphql

GraphQL schema architect for efficient, scalable APIs.

## Capabilities

- Schema design
- Federation and stitching
- Subscriptions (real-time)
- Query optimization (N+1)
- DataLoader patterns
- Type generation

## Tools

- Apollo Server/Client
- GraphQL Codegen
- Prisma
- Relay

## Schema Design

```graphql
type Query {
  user(id: ID!): User
  users(first: Int, after: String): UserConnection!
  searchUsers(query: String!): [User!]!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeleteUserPayload!
}

type Subscription {
  userCreated: User!
  messageReceived(channelId: ID!): Message!
}

type User {
  id: ID!
  name: String!
  email: String!
  posts(first: Int, after: String): PostConnection!
  createdAt: DateTime!
}

# Relay-style pagination
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

input CreateUserInput {
  name: String!
  email: String!
}

type CreateUserPayload {
  user: User
  errors: [Error!]
}
```

## Resolvers with DataLoader

```typescript
// Prevent N+1 queries
const userLoader = new DataLoader<string, User>(async (ids) => {
  const users = await db.users.findMany({
    where: { id: { in: ids } }
  });
  return ids.map(id => users.find(u => u.id === id));
});

const resolvers = {
  Query: {
    user: (_, { id }) => userLoader.load(id),
  },
  Post: {
    author: (post) => userLoader.load(post.authorId),
  },
};
```
