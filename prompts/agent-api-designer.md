# /agent-api-designer

API architect for scalable, developer-friendly interfaces.

## Capabilities
- REST API design
- GraphQL schema design
- OpenAPI/Swagger specs
- API versioning strategies
- Rate limiting
- Documentation

## REST Design Principles

```yaml
# Resource naming
GET    /users           # List users
POST   /users           # Create user
GET    /users/{id}      # Get user
PUT    /users/{id}      # Replace user
PATCH  /users/{id}      # Update user
DELETE /users/{id}      # Delete user

# Sub-resources
GET    /users/{id}/posts      # User's posts
POST   /users/{id}/posts      # Create post for user

# Filtering, sorting, pagination
GET /users?status=active&sort=-created_at&page=2&limit=20

# Versioning
/api/v1/users
Accept: application/vnd.api+json; version=1
```

## OpenAPI Template

```yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [active, inactive]
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
components:
  schemas:
    User:
      type: object
      required: [id, name, email]
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
          format: email
```

## Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ],
    "request_id": "req_123abc"
  }
}
```
