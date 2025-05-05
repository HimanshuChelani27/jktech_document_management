# Document Management System Backend

A FastAPI-based backend service for managing documents with authentication, authorization, and document processing capabilities.

## Technology Stack

- **Framework**: FastAPI
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Migration Tool**: Alembic
- **Testing**: pytest
- **Docker Support**: Yes

## Project Structure

```
backend/
├── alembic/                  # Database migration files
├── app/                      # Main application directory
│   ├── api/                  # API endpoints
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── documents.py     # Document management endpoints
│   │   └── users.py         # User management endpoints
│   ├── core/                # Core functionality
│   │   ├── config.py        # Application configuration
│   │   ├── database.py      # Database connection
│   │   └── security.py      # Security utilities
│   ├── crud/                # Database CRUD operations
│   │   ├── document.py      # Document operations
│   │   └── user.py         # User operations
│   ├── models/              # SQLAlchemy models
│   │   ├── document.py      # Document model
│   │   ├── role.py         # Role model
│   │   └── user.py         # User model
│   ├── schemas/             # Pydantic schemas
│   │   ├── document.py      # Document schemas
│   │   ├── response.py      # Response schemas
│   │   └── user.py         # User schemas
│   ├── services/            # Business logic services
│   │   └── ingestion_service.py  # Document ingestion service
│   └── utils/               # Utility functions
├── tests/                   # Test files
├── Dockerfile              # Docker configuration
└── requirements.txt        # Python dependencies
```

## Key Features

1. **Authentication & Authorization**
   - JWT-based authentication
   - Role-based access control
   - Secure password hashing
   - Token refresh mechanism

2. **User Management**
   - User registration and login
   - Profile management
   - Role management
   - Password reset functionality

3. **Document Management**
   - Document upload and storage
   - Document metadata management
   - Document search and retrieval
   - Version control
   - Access control

4. **API Endpoints**

### Authentication Endpoints
- `POST /api/auth/register` - Register a new user
  - Request Body: `{ "email": string, "password": string, "role_id": int }`
  - Response: `{ "status": "success", "details": UserOut, "message": "Registration successful" }`

- `POST /api/auth/login` - User login
  - Request Body: `{ "email": string, "password": string }`
  - Response: `{ "status": "success", "details": { "access_token": string, "token_type": "bearer" }, "message": "Login successful" }`

### User Endpoints
- `GET /api/users/roles` - Get all available roles
  - Response: `{ "status": "success", "details": [RoleBase], "message": null }`

### Document Endpoints
- `POST /api/documents/upload_document` - Upload a new document
  - Headers: `Authorization: Bearer <token>`
  - Form Data: 
    - `file`: File upload
    - `title`: string
  - Response: `{ "status": "success", "details": DocumentOut, "message": null }`

- `GET /api/documents/documents` - List all documents
  - Headers: `Authorization: Bearer <token>`
  - Response: `{ "status": "success", "details": [DocumentOut], "message": null }`

### Response Format
All API responses follow a standard format:
```json
{
    "status": "success" | "error",
    "details": object | null,
    "message": string | null
}
```

### Error Responses
```json
{
    "status": "error",
    "message": "Error description",
    "details": null
}
```

Common HTTP Status Codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Environment Variables**
   Create a `.env` file with:
   ```
   DATABASE_URL=mysql://user:password@localhost/dbname
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. **Database Setup**
   ```bash
   alembic upgrade head
   python seed_data.py  # Optional: Load sample data
   ```

5. **Run Development Server**
   ```bash
   uvicorn app.main:app --reload --port 9000
   ```

6. **Docker Setup**
   ```bash
   docker build -t document-management-backend .
   docker run -p 9000:9000 document-management-backend
   ```

## Testing

Run tests using pytest:
```bash
pytest
```

## API Documentation

Once the server is running, access the API documentation at:
- Swagger UI: `http://localhost:9000/docs`
- ReDoc: `http://localhost:9000/redoc`

## Database Migrations

1. **Create a New Migration**
   ```bash
   alembic revision --autogenerate -m "description"
   ```

2. **Apply Migrations**
   ```bash
   alembic upgrade head
   ```

3. **Rollback Migration**
   ```bash
   alembic downgrade -1
   ```

## Security Features

1. **Password Security**
   - Passwords are hashed using bcrypt
   - Minimum password requirements enforced
   - Password reset functionality

2. **JWT Security**
   - Short-lived access tokens
   - Refresh token mechanism
   - Token blacklisting for logout

3. **API Security**
   - CORS protection
   - Rate limiting
   - Input validation
   - SQL injection protection

## Error Handling

The application uses standardized error responses:
```json
{
    "status": "error",
    "message": "Error description",
    "details": null
}
```

## Environment Variables

Create a `.env` file in the root of the backend directory with the following variables:

### Database Configuration
```
DATABASE_URL=mysql://user:password@localhost/dbname
```
- Format: `mysql://username:password@host:port/database_name`
- Default port: 3306
- Required: Yes

### JWT Authentication
```
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```
- `SECRET_KEY`: Used for JWT token signing (should be a strong, random string)
- `ALGORITHM`: JWT signing algorithm (HS256 recommended)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token validity period
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token validity period
- Required: Yes

### Azure Blob Storage (for document storage)
```
AZURE_STORAGE_CONNECTION_STRING=your-azure-storage-connection-string
AZURE_STORAGE_CONTAINER_NAME=your-container-name
```
- Required if using Azure Blob Storage for document storage
- Required: No (if using local storage)

### Application Settings
```
DEBUG=True
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:4200,http://localhost:3000
API_PREFIX=/api
```
- `