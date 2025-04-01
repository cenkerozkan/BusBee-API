# Backend

Backend of the Atılım Service Management Project

# Bus Operations API Documentation

A FastAPI-based authentication and user management system with support for End Users, Admin Users, and Driver Users.

## Base URL
```
https://busops-acb3c422b0e4.herokuapp.com/api
```
All endpoints described in this documentation should be prefixed with this base URL.

For example, to access the end user login endpoint:
```
POST https://busops-acb3c422b0e4.herokuapp.com/api/auth/end_user/login
```

## Table of Contents
- [Authentication Services](#authentication-services)
- [Global Error Handling](#global-error-handling)
- [End User Authentication Endpoints](#end-user-authentication-endpoints)
  - [Register End User](#register-end-user)
  - [Login End User](#login-end-user)
  - [Logout End User](#logout-end-user)
  - [Delete End User Account](#delete-end-user-account)
  - [Validate End User Token](#validate-end-user-token)
- [Admin User Authentication Endpoints](#admin-user-authentication-endpoints)
  - [Login Admin User](#login-admin-user)
  - [Logout Admin User](#logout-admin-user)
  - [Delete Admin User Account](#delete-admin-user-account)
  - [Validate Admin Token](#validate-admin-token)
  - [Add Admin User](#add-admin-user)
  - [Remove Admin User](#remove-admin-user)
- [Admin Driver Management Endpoints](#admin-driver-management-endpoints)
  - [Get All Drivers](#get-all-drivers)
  - [Add Driver](#add-driver)
  - [Delete Driver](#delete-driver)
  - [Update Driver Password](#update-driver-password)
  - [Update Driver Phone Number](#update-driver-phone-number)
- [Data Models](#data-models)
  - [End User Model](#end-user-model)
  - [Admin User Model](#admin-user-model)
  - [Driver User Model](#driver-user-model)

## Authentication Services

The API implements three separate authentication services:
- End User Authentication Service
- Admin User Authentication Service
- Driver User Management Service

Each service has its own MongoDB collection and Firebase authentication integration.

## Global Error Handling

The API implements global exception handling for HTTP errors with these status codes:

| Status Code | Message |
| ----------- | ------- |
| 404 | Not found |
| 401 | Unauthorized |
| 403 | Not authenticated |
| 500 | Internal server error |

All responses follow the `ResponseModel` format:
```json
{
  "success": boolean,
  "message": string,
  "data": object | null,
  "error": string | null
}
```

## End User Authentication Endpoints

### Register End User
`POST /api/auth/end_user/register`

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Success Response:**
- Status: 200
- Headers: 
  - `refresh_token`: Firebase refresh token
  - `id_token`: Firebase ID token
- Body: ResponseModel with user data

**Success Response Example:**
```json
{
  "success": true,
  "message": "Registration successful",
  "data": {
    "uid": "firebase-uid-123",
    "created_at": "2025-03-29T10:00:00",
    "last_active": "2025-03-29T10:00:00",
    "role": "END_USER",
    "email": "user@example.com"
  },
  "error": null
}
```

**Error Responses:**
- 400: Invalid email format
- 500: Registration failed

**Error Response Example:**
```json
{
  "success": false,
  "message": "Invalid email format",
  "data": null,
  "error": "INVALID_EMAIL"
}
```

### Login End User
`POST /api/auth/end_user/login`

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Success Response:**
- Status: 200
- Headers:
  - `refresh_token`: Firebase refresh token
  - `id_token`: Firebase ID token
- Body: ResponseModel with user data

**Success Response Example:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "uid": "firebase-uid-123",
    "created_at": "2025-03-29T10:00:00",
    "last_active": "2025-03-29T10:00:00",
    "role": "END_USER",
    "email": "user@example.com"
  },
  "error": null
}
```

**Error Responses:**
- 400: Invalid email format
- 500: Login failed

**Error Response Example:**
```json
{
  "success": false,
  "message": "Invalid password",
  "data": null,
  "error": "INVALID_PASSWORD"
}
```

### Logout End User
`POST /api/auth/end_user/logout`

**Request Body:**
```json
{
  "user_uid": "string"
}
```

**Headers:**
- `Authorization`: Bearer token

**Success Response:**
- Status: 200
- Body: ResponseModel with success message

**Success Response Example:**
```json
{
  "success": true,
  "message": "Logout successful",
  "data": {},
  "error": null
}
```

**Error Response:**
- 500: Logout failed

**Error Response Example:**
```json
{
  "success": false,
  "message": "Logout failed",
  "data": null,
  "error": "INVALID_UID"
}
```

### Delete End User Account
`DELETE /api/auth/end_user/delete_account`

**Request Body:**
```json
{
  "user_uid": "string"
}
```

**Headers:**
- `Authorization`: Bearer token

**Success Response:**
- Status: 200
- Body: ResponseModel with success message

**Success Response Example:**
```json
{
  "success": true,
  "message": "Account deleted",
  "data": {},
  "error": null
}
```

**Error Response:**
- 500: Failed to delete account

**Error Response Example:**
```json
{
  "success": false,
  "message": "Failed to delete account",
  "data": null,
  "error": "USER_NOT_FOUND"
}
```

### Validate End User Token
`POST /api/auth/end_user/validate_token`

**Headers:**
- `Authorization`: Bearer token

**Success Response:**
- Status: 200
- Body: ResponseModel with validation result

**Success Response Example:**
```json
{
  "success": true,
  "message": "Token is valid",
  "data": {},
  "error": null
}
```

**Error Response:**
- 401: Token is invalid

**Error Response Example:**
```json
{
  "success": false,
  "message": "Token is invalid",
  "data": null,
  "error": "INVALID_TOKEN"
}
```

## Admin User Authentication Endpoints

### Login Admin User
`POST /api/auth/admin_user/login`

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Success Response:**
- Status: 200
- Headers:
  - `refresh_token`: Firebase refresh token
  - `id_token`: Firebase ID token
- Body: ResponseModel with admin user data

**Success Response Example:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "uid": "admin-uid-123",
    "created_at": "2025-03-29T10:00:00",
    "last_active": "2025-03-29T10:00:00",
    "role": "ADMIN_USER",
    "email": "admin@example.com"
  },
  "error": null
}
```

**Error Responses:**
- 400: Invalid email format
- 500: Login failed

**Error Response Example:**
```json
{
  "success": false,
  "message": "Invalid credentials",
  "data": null,
  "error": "INVALID_LOGIN"
}
```

### Logout Admin User
`POST /api/auth/admin_user/logout`

**Request Body:**
```json
{
  "user_uid": "string"
}
```

**Headers:**
- `Authorization`: Bearer token

**Success Response:**
- Status: 200
- Body: ResponseModel with success message

**Success Response Example:**
```json
{
  "success": true,
  "message": "Logout successful",
  "data": {},
  "error": null
}
```

**Error Response:**
- 500: Logout failed

**Error Response Example:**
```json
{
  "success": false,
  "message": "Logout failed",
  "data": null,
  "error": "SESSION_NOT_FOUND"
}
```

### Delete Admin User Account
`DELETE /api/auth/admin_user/delete_account`

**Request Body:**
```json
{
  "user_uid": "string"
}
```

**Headers:**
- `Authorization`: Bearer token

**Success Response:**
- Status: 200
- Body: ResponseModel with success message

**Success Response Example:**
```json
{
  "success": true,
  "message": "Account deleted",
  "data": {},
  "error": null
}
```

**Error Response:**
- 500: Failed to delete account

**Error Response Example:**
```json
{
  "success": false,
  "message": "Failed to delete account",
  "data": null,
  "error": "ADMIN_NOT_FOUND"
}
```

### Validate Admin Token
`POST /api/auth/admin_user/validate_token`

**Headers:**
- `Authorization`: Bearer token

**Success Response:**
- Status: 200
- Body: ResponseModel with validation result

**Success Response Example:**
```json
{
  "success": true,
  "message": "Token is valid",
  "data": {},
  "error": null
}
```

**Error Response:**
- 401: Token is invalid

**Error Response Example:**
```json
{
  "success": false,
  "message": "Token is invalid",
  "data": null,
  "error": "EXPIRED_TOKEN"
}
```

### Add Admin User
`POST /api/auth/admin_user/add_admin_user`

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Headers:**
- `ADMIN-API-KEY`: Admin API key

**Success Response:**
- Status: 200
- Body: ResponseModel with new admin user data

**Success Response Example:**
```json
{
  "success": true,
  "message": "Admin user added",
  "data": {
    "uid": "new-admin-uid-123",
    "created_at": "2025-03-29T10:00:00",
    "last_active": "2025-03-29T10:00:00",
    "role": "ADMIN_USER",
    "email": "newadmin@example.com"
  },
  "error": null
}
```

**Error Responses:**
- 403: Unauthorized
- 500: Failed to add admin user

**Error Response Example:**
```json
{
  "success": false,
  "message": "Failed to add admin user",
  "data": null,
  "error": "EMAIL_ALREADY_EXISTS"
}
```

### Remove Admin User
`DELETE /api/auth/admin_user/remove_admin_user`

**Request Body:**
```json
{
  "user_uid": "string"
}
```

**Headers:**
- `ADMIN-API-KEY`: Admin API key

**Success Response:**
- Status: 200
- Body: ResponseModel with success message

**Success Response Example:**
```json
{
  "success": true,
  "message": "Admin user removed",
  "data": {},
  "error": null
}
```

**Error Responses:**
- 403: Unauthorized
- 500: Failed to remove admin user

**Error Response Example:**
```json
{
  "success": false,
  "message": "Failed to remove admin user",
  "data": null,
  "error": "UNAUTHORIZED_ACCESS"
}
```

## Admin Driver Management Endpoints

### Get All Drivers
`GET /api/admin/management/get_all_drivers`

**Headers:**
- `Authorization`: Bearer token

**Success Response:**
- Status: 200
- Body: ResponseModel with list of drivers

**Success Response Example:**
```json
{
  "success": true,
  "message": "Drivers retrieved",
  "data": {
    "drivers": [
      {
        "uid": "driver-uid-123",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+905551234567",
        "role": "DRIVER_USER",
        "vehicle": null
      }
    ]
  },
  "error": null
}
```

**Error Response:**
- 500: Failed to get drivers

**Error Response Example:**
```json
{
  "success": false,
  "message": "Failed to get drivers",
  "data": null,
  "error": "DATABASE_ERROR"
}
```

### Add Driver
`POST /api/admin/management/add_driver`

**Request Body:**
```json
{
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string",
  "password": "string"
}
```

**Headers:**
- `Authorization`: Bearer token

**Success Response:**
- Status: 200
- Body: ResponseModel with new driver data

**Success Response Example:**
```json
{
  "success": true,
  "message": "Driver user added",
  "data": {
    "uid": "driver-uid-123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+905551234567",
    "role": "DRIVER_USER",
    "assigned_route": {},
    "vehicle": null
  },
  "error": null
}
```

**Error Responses:**
- 400: Invalid phone number format
- 500: Failed to create driver user

**Error Response Example:**
```json
{
  "success": false,
  "message": "Invalid phone number format",
  "data": null,
  "error": null
}
```

### Delete Driver
`DELETE /api/admin/management/delete_driver`

**Request Body:**
```json
{
  "uid": "string"
}
```

**Headers:**
- `Authorization`: Bearer token

**Success Response:**
- Status: 200
- Body: ResponseModel with success message

**Success Response Example:**
```json
{
  "success": true,
  "message": "Driver user deleted",
  "data": {},
  "error": null
}
```

**Error Response:**
- 500: Failed to delete driver user

**Error Response Example:**
```json
{
  "success": false,
  "message": "Failed to delete driver user",
  "data": null,
  "error": null
}
```

### Update Driver Password
`PATCH /api/admin/management/update_driver_password`

**Request Body:**
```json
{
  "uid": "string",
  "new_password": "string"
}
```

**Headers:**
- `Authorization`: Bearer token

**Success Response:**
- Status: 200
- Body: ResponseModel with success message

**Success Response Example:**
```json
{
  "success": true,
  "message": "Driver password updated",
  "data": {},
  "error": null
}
```

**Error Response:**
- 500: Failed to update driver password

**Error Response Example:**
```json
{
  "success": false,
  "message": "Failed to update driver password",
  "data": null,
  "error": "PASSWORD_POLICY_VIOLATION"
}
```

### Update Driver Phone Number
`PATCH /api/admin/management/update_driver_phone_number`

**Request Body:**
```json
{
  "uid": "string",
  "new_phone_number": "string"
}
```

**Headers:**
- `Authorization`: Bearer token

**Success Response:**
- Status: 200
- Body: ResponseModel with updated driver data

**Success Response Example:**
```json
{
  "success": true,
  "message": "Driver phone number updated",
  "data": {},
  "error": null
}
```

**Error Response:**
- 500: Failed to update driver phone number

**Error Response Example:**
```json
{
  "success": false,
  "message": "Failed to update driver phone number",
  "data": null,
  "error": "failed_to_update_driver_phone_number"
}
```

## Data Models

### End User Model
```json
{
  "uid": "string",
  "created_at": "string",
  "last_active": "string",
  "role": "END_USER",
  "email": "string"
}
```

### Admin User Model
```json
{
  "uid": "string",
  "created_at": "string",
  "last_active": "string",
  "role": "ADMIN_USER",
  "email": "string"
}
```

### Driver User Model
```json
{
  "uid": "string",
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string",
  "role": "DRIVER_USER",
  "assigned_route": {},
  "vehicle": null
}
```