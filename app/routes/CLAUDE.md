# Users API Routes Documentation

## RESTful API Endpoints

### Base URL
`/users/v1/api/users/`

### Endpoints

#### 1. List All Users
- **URL**: `/users/v1/api/users/`
- **Method**: `GET`
- **Description**: Retrieve a list of all users
- **Query Parameters**:
  - `page` (integer, optional): Page number for pagination (default: 1)
  - `limit` (integer, optional): Number of items per page (default: 20)
  - `sort` (string, optional): Sort field (e.g., 'name', 'created_at')
  - `order` (string, optional): Sort order ('asc' or 'desc', default: 'asc')
- **Response**: 
  ```json
  {
    "data": [
      {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "pages": 5
    }
  }
  ```
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (invalid query parameters)

#### 2. Get Single User
- **URL**: `/users/v1/api/users/{id}`
- **Method**: `GET`
- **Description**: Retrieve a specific user by ID
- **Path Parameters**:
  - `id` (integer, required): User ID
- **Response**:
  ```json
  {
    "data": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
  ```
- **Status Codes**:
  - 200: Success
  - 404: User not found

#### 3. Create User
- **URL**: `/users/v1/api/users/`
- **Method**: `POST`
- **Description**: Create a new user
- **Request Body**:
  ```json
  {
    "username": "jane_doe",
    "email": "jane@example.com",
    "password": "securepassword"
  }
  ```
- **Response**:
  ```json
  {
    "data": {
      "id": 2,
      "username": "jane_doe",
      "email": "jane@example.com",
      "created_at": "2024-01-02T00:00:00Z",
      "updated_at": "2024-01-02T00:00:00Z"
    }
  }
  ```
- **Status Codes**:
  - 201: Created
  - 400: Bad Request (validation errors)
  - 409: Conflict (username or email already exists)

#### 4. Update User
- **URL**: `/users/v1/api/users/{id}`
- **Method**: `PUT`
- **Description**: Update an entire user resource
- **Path Parameters**:
  - `id` (integer, required): User ID
- **Request Body**:
  ```json
  {
    "username": "jane_updated",
    "email": "jane_new@example.com",
    "password": "newsecurepassword"
  }
  ```
- **Response**:
  ```json
  {
    "data": {
      "id": 2,
      "username": "jane_updated",
      "email": "jane_new@example.com",
      "created_at": "2024-01-02T00:00:00Z",
      "updated_at": "2024-01-03T00:00:00Z"
    }
  }
  ```
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation errors)
  - 404: User not found
  - 409: Conflict (username or email already exists)

#### 5. Partial Update User
- **URL**: `/users/v1/api/users/{id}`
- **Method**: `PATCH`
- **Description**: Partially update a user resource
- **Path Parameters**:
  - `id` (integer, required): User ID
- **Request Body**:
  ```json
  {
    "email": "newemail@example.com"
  }
  ```
- **Response**:
  ```json
  {
    "data": {
      "id": 2,
      "username": "jane_updated",
      "email": "newemail@example.com",
      "created_at": "2024-01-02T00:00:00Z",
      "updated_at": "2024-01-04T00:00:00Z"
    }
  }
  ```
- **Status Codes**:
  - 200: Success
  - 400: Bad Request (validation errors)
  - 404: User not found
  - 409: Conflict (email already exists)

#### 6. Delete User
- **URL**: `/users/v1/api/users/{id}`
- **Method**: `DELETE`
- **Description**: Delete a user
- **Path Parameters**:
  - `id` (integer, required): User ID
- **Response**:
  ```json
  {
    "message": "User deleted successfully"
  }
  ```
- **Status Codes**:
  - 200: Success
  - 404: User not found

## Service Layer Architecture

The Users API follows a service-oriented architecture:

```
app/
├── routes/
│   └── users.py          # API route handlers
├── services/
│   └── user_service.py   # Business logic layer
├── models/
│   └── users.py          # Data models
└── repositories/
    └── user_repository.py # Database access layer
```

### Service Layer Responsibilities

1. **Routes Layer** (`routes/users.py`):
   - Handle HTTP requests/responses
   - Request validation
   - Response formatting
   - Error handling

2. **Service Layer** (`services/user_service.py`):
   - Business logic implementation
   - Data validation and transformation
   - Orchestration of repository calls
   - Transaction management

3. **Repository Layer** (`repositories/user_repository.py`):
   - Database operations
   - Query building
   - Data persistence

## Error Response Format

All error responses follow this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional error details"
    }
  }
}
```

## Authentication

All endpoints require authentication via Bearer token in the Authorization header:
```
Authorization: Bearer <token>
```

## Rate Limiting

- Rate limit: 1000 requests per hour per API key
- Headers returned:
  - `X-RateLimit-Limit`: Maximum requests per hour
  - `X-RateLimit-Remaining`: Remaining requests in current window
  - `X-RateLimit-Reset`: Timestamp when the rate limit resets
