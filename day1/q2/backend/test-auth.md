# 🔐 Authentication API Testing Guide

## 1. Register a New User

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Srinivasan",
    "email": "srinivasan@example.com",
    "password": "password123"
  }'
```

**Expected Response:**
```json
{
  "message": "User registered successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "65f8a1b2c3d4e5f6a7b8c9d0",
    "name": "Srinivasan",
    "email": "srinivasan@example.com"
  }
}
```

## 2. Login with Existing User

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "srinivasan@example.com",
    "password": "password123"
  }'
```

**Expected Response:**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "65f8a1b2c3d4e5f6a7b8c9d0",
    "name": "Srinivasan",
    "email": "srinivasan@example.com"
  }
}
```

## 3. Get Current User Info (Protected Route)

```bash
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Expected Response:**
```json
{
  "user": {
    "id": "65f8a1b2c3d4e5f6a7b8c9d0",
    "name": "Srinivasan",
    "email": "srinivasan@example.com"
  }
}
```

## 4. Test Error Cases

### Invalid Email Format:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "invalid-email",
    "password": "password123"
  }'
```

### Short Password:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "123"
  }'
```

### Wrong Login Credentials:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "srinivasan@example.com",
    "password": "wrongpassword"
  }'
```

### Access Protected Route Without Token:
```bash
curl -X GET http://localhost:5000/api/auth/me
```

## 🎯 **Using the Token for Other APIs**

Once you get a token from register/login, use it for protected routes:

### Track Product Interaction:
```bash
curl -X POST http://localhost:5000/api/interactions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "productId": 1,
    "action": "viewed",
    "duration": 30
  }'
```

### Get Search History:
```bash
curl -X GET http://localhost:5000/api/search/history \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get Interaction Stats:
```bash
curl -X GET http://localhost:5000/api/interactions/stats \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🔒 **Security Features**

- ✅ Password hashing with bcrypt
- ✅ JWT tokens with 7-day expiration
- ✅ Input validation
- ✅ Duplicate email prevention
- ✅ Secure error messages (no password exposure) 