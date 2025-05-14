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
  - [Delete End User Account](#delete-end-user-account)
  - [Validate End User Token](#validate-end-user-token)
  - [Create User Endpoint](#create-user-endpoint)
- [Admin User Authentication Endpoints](#admin-user-authentication-endpoints)
  - [Login Admin User](#login-admin-user)
  - [Delete Admin User Account](#delete-admin-user-account)
  - [Add Admin User](#add-admin-user)
  - [Remove Admin User](#remove-admin-user)
  - [Get All Admins](#get-all-admins)
- [Admin Driver Management Endpoints](#admin-driver-management-endpoints)
  - [Get All Drivers](#get-all-drivers)
  - [Add Driver](#add-driver)
  - [Delete Driver](#delete-driver)
  - [Update Driver Phone Number](#update-driver-phone-number)
  - [Assign Vehicle to Driver](#assign-vehicle-to-driver)
  - [Remove Vehicle from Driver](#remove-vehicle-from-driver)
- [Admin Route Management Endpoints](#admin-route-management-endpoints)
  - [Get All Routes](#get-all-routes)
  - [Create Route](#create-route)
  - [Update Route](#update-route)
  - [Delete Route With Route ID](#delete-route-with-route-id)
- [Admin Vehicle Management Endpoints](#admin-vehicle-management-endpoints)
  - [Create Vehicle](#create-vehicle)
  - [Get All Vehicles](#get-all-vehicles)
  - [Update Vehicle](#update-vehicle)
  - [Delete Vehicle](#delete-vehicle)
  - [Delete Vehicle by Plate Number](#delete-vehicle-by-plate-number)
  - [Assign Routes to Vehicle](#assign-routes-to-vehicle)
- [Driver Endpoints](#driver-endpoints)
  - [Get Vehicle](#get-vehicle)
  - [Get Vehicle Route](#get-vehicle-route)
  - [Start Journal](#start-journey)
  - [Stop Journey](#stop-journey)
  - [Websocket Location Updates](#websocket-location-updates)
- [End User Endpoints](#end-user-endpoints)
  - [Get Passenger Information](#get-passenger-information)
  - [Get All Routes](#get-all-routes-for-passengers)
  - [Get All Active Journeys](#get-all-active-journeys)
  - [Fetch Location From Journal](#fetch-location-from-journal)

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
  "success": "boolean",
  "message": "string",
  "data": "object" | null,
  "error": "string" | null
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
  "error": ""
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
  "error": ""
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
  "error": ""
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
  "error": ""
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

### Create User Endpoint
`POST /api/auth/end_user/create_user`
**Request Body:**
```json
{
  "uid": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string"
}
```
**Success Response:**
- Status: 200
- Body: ResponseModel with new user data


**Headers:**
- `Authorization`: Bearer token


**Error Response:**
- 500: Failed to create user
- 400: Invalid email format
**Error Response Example:**
```json
{
  "success": false,
  "message": "Invalid email format",
  "data": {},
  "error": ""
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
  "error": ""
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
  "error": ""
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
  "password": "string",
  "first_name": "string",
  "last_name": "string"
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
    "uid": "cVqvd10OgahjsYtxV5EwzSDkGIw1",
    "created_at": "2025-04-24T23:33:46.765910",
    "last_active": "2025-04-24T23:33:46.765925",
    "first_name": "Cenker",
    "last_name": "Özkan",
    "role": "ADMIN_USER",
    "email": "cenkerozkanse@gmail.com"
  },
  "error": ""
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
  "error": ""
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

### Get All Admins
`GET /api/auth/admin_user/get_all_admins`

Retrieves all registered admin users.

**Headers:**
- `ADMIN-API-KEY`: Admin API key

**Success Response:**
- Status: 200
- Body: ResponseModel with list of admin users

**Success Response Example:**
```json
{
  "success": true,
  "message": "Admins retrieved",
  "data": {
    "admins": [
      {
        "uid": "admin-uid-123",
        "created_at": "2025-03-29T10:00:00",
        "last_active": "2025-03-29T10:00:00",
        "role": "ADMIN_USER",
        "email": "admin@example.com"
      }
    ]
  },
  "error": ""
} 
```
**Error Response:**
- 403: Unauthorized
- 404 : No admins found
- 500: Failed to get admins

```json
{
  "success": false,
  "message": "Failed to get admins",
  "data": null,
  "error": "ERROR"
}
```

## Update Admin User
`PATCH /api/auth/admin_user/update_admin_user`

Updates an existing admin user.
**Request Body:**
```json
{
  "uid": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
}
```

**Headers:**
- `ADMIN-API-KEY`: Admin API key

**Success Response:**
- Status: 200
- Body: ResponseModel with updated admin user data

**Success Response Example:**
```json
{
  "success": true,
  "message": "Admin bilgileri güncellendi",
  "data": {
    "uid": "F4YLPnSWIWZ2MTMTLorqPPX08Fj2",
    "created_at": "2025-04-30T15:35:36.735073",
    "last_active": "2025-05-09T21:31:26.229354",
    "first_name": "Cenker",
    "last_name": "Özkan",
    "role": "ADMIN_USER",
    "email": "cenkerozkan99@gmail.com"
  },
  "error": ""
}
```

**Error Response:**
- 403: Unauthorized
- 500: Admin bilgileri güncellenemedi
- 400: Hatalı Mail Formatı

**Error Response Example:**
```json
{
  "success": false,
  "message": "Hatalı Mail Formatı",
  "data": {},
  "error": ""
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
  "error": ""
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
  "error": ""
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
  "error": ""
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
  "error": ""
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
  "error": ""
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
  "error": ""
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

### Assign Vehicle to Driver
`PATCH /api/admin/management/assign_vehicle_to_driver`
Assigns a vehicle to a driver.

**Request Body:**
```json
{
  "driver_uid": "string",
  "vehicle_uuid": "string"
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
  "message": "Vehicle assigned to driver successfully",
  "data": {
    "driver": {
      "uid": "xSbi0CmrchPQY4qj2lKCblwZoMs2",
      "first_name": "Cenker",
      "last_name": "Özkan",
      "phone_number": "+905343732399",
      "role": "DRIVER_USER",
      "vehicle": {
        "uuid": "e3d95573-6ed7-4d96-9020-bf9312c6eec5",
        "vehicle_brand": "Mercedes",
        "vehicle_model": "Sprinter",
        "vehicle_year": 2024,
        "plate_number": "06 BTU 495",
        "route_uuid": "string"
      }
    }
  },
  "error": ""
}
```
**Error Response:**
- 500: Failed to assign vehicle
- 404: Driver not found

**Error Response Example:**
```json
{
  "success": false,
  "message": "Driver not found",
  "data": null,
  "error": ""
}
```

### Remove Vehicle from Driver
`PATCH /api/admin/management/remove_vehicle_from_driver/{driver_uid}`
Removes a vehicle from a driver.

**Parameters:**
- `driver_uid`: UID of the driver

**Headers:**
- `Authorization`: Bearer token

**Success Response:**
- Status: 200
- Body: ResponseModel with success message

**Success Response Example:**
```json
{
  "success": true,
  "message": "Vehicle removed from driver successfully",
  "data": {
    "driver": {
      "uid": "xSbi0CmrchPQY4qj2lKCblwZoMs2",
      "first_name": "Cenker",
      "last_name": "Özkan",
      "phone_number": "+905343732399",
      "role": "DRIVER_USER",
      "vehicle": null
    }
  },
  "error": ""
}
```

**Error Response:**
- 500: Failed to remove vehicle
- 404: Driver not found
- 400: Driver has no vehicle assigned

**Error Response Example:**
```json
{
  "success": false,
  "message": "Driver not found",
  "data": null,
  "error": ""
}
```



## Admin Route Management Endpoints

### Get All Routes
`GET /api/admin/management/route/get_all`

**Headers:**
- `Authorization`: Bearer token

**Success Response:**
- Status: 200
- Body: ResponseModel with list of routes

**Success Response Example:**
```json
{
  "success": true,
  "message": "Routes retrieved successfully",
  "data": {
    "routes": [
      {
        "uuid": "route-uuid-123",
        "route_name": "Morning Express Route 1",
        "created_at": "2024-03-29T10:00:00",
        "updated_at": "2024-03-29T10:00:00",
        "start_time": "08:00",
        "stops": [
          {
            "lat": 41.0082,
            "lon": 28.9784
          },
          {
            "lat": 41.0055,
            "lon": 28.9773
          }
        ]
      }
    ]
  },
  "error": ""
}
```

**Error Response:**
- 404: No routes found

**Error Response Example:**
```json
{
  "success": false,
  "message": "No routes found",
  "data": {
    "routes": []
  },
  "error": ""
}
```
### Create Route
`POST /api/admin/management/route/create`
**Request Body:**
```json
{
  "route_name": "string",
  "start_time": "string",
  "stops": [
    {
      "lat": 0,
      "lon": 0
    }
  ]
}
```
**Headers:**
- `Authorization`: Bearer token

**Success Response:**
- Status: 200
- Body: ResponseModel with new route data

**Success Response Example:**
```json
{
  "success": true,
  "message": "Route created successfully",
  "data": {
    "uuid": "route-uuid-123",
    "route_name": "Morning Express Route 1",
    "created_at": "2024-03-29T10:00:00",
    "updated_at": "2024-03-29T10:00:00",
    "start_time": "08:00",
    "stops": [
      {
        "lat": 41.0082,
        "lon": 28.9784
      }
    ]
  },
  "error": ""
}
```
**Error Response:**
- 500: Failed to create route

**Error Response Example:**
```json
{
  "success": false,
  "message": "Route name already exists",
  "data": {},
  "error": ""
}
```

### Update Route
`PATCH /api/admin/management/route/update`

**Request Body:**
```json
{
  "uuid": "string",
  "route_name": "string",
  "start_time": "string",
  "stops": [
    {
      "lat": 0,
      "lon": 0,
      "stop_name": "string"
    }
  ]
}
```
**Headers:**
- `Authorization`: Bearer token

**Success Response:**
- Status: 200
- Body: ResponseModel with updated route data
**Success Response Example:**
```json
{
  "success": true,
  "message": "Document updated successfully",
  "data": {
    "route": {
      "uuid": "defa555c-57b5-4453-9c9b-f01538824e37",
      "route_name": "Weekend Special Route 6",
      "created_at": "2025-04-24T22:01:15.333649",
      "updated_at": "2025-04-24T22:12:19.359726",
      "start_time": "10:15",
      "stops": [
        {
          "lat": 41.0411,
          "lon": 29.0084
        },
        {
          "lat": 41.0483,
          "lon": 29.0278
        },
        {
          "lat": 41.0545,
          "lon": 29.0497
        },
        {
          "lat": 41.0858,
          "lon": 29.0433
        },
        {
          "lat": 41.108,
          "lon": 29.0544
        }
      ]
    }
  },
  "error": ""
}
```
**Error Response:**
- 500: Failed to update route

**Error Response Example:**
```json
{
  "success": false,
  "message": "Route does not exist",
  "data": {},
  "error": ""
}
```

### Delete Route With Route ID
`DELETE /api/admin/management/route/delete/{route_id}`

**Parameters:**
- `route_id`: UUID of the route to be deleted

**Headers:**
- `Authorization`: Bearer token

**Success Response:**
- Status: 200
- Body: ResponseModel with success message

**Success Response Example:**
```json
{
  "success": true,
  "message": "Route deleted successfully",
  "data": {},
  "error": ""
}
```
**Error Response:**
- 500: Failed to delete route
- 404: Route not found

**Error Response Example:**
```json
{
  "success": false,
  "message": "Route not found",
  "data": {},
  "error": ""
}
```

## Admin Vehicle Management Endpoints

This section details endpoints for managing vehicles by administrators.

### Create Vehicle
`POST /api/admin/management/vehicle/create`
Creates a new vehicle.
**Request Body:**
```json
{
  "vehicle_brand": "string",
  "vehicle_model": "string",
  "vehicle_year": "string",
  "plate_number": "string",
  "route_uuid": "string"
}
```
**Headers:**
- Status: 200
- Body: ResponseModel with new vehicle data
**Success Response Example:**
```json
{
  "success": true,
  "message": "Vehicle created successfully",
  "data": {
    "vehicle": {
      "uuid": "f5488f20-f1b1-4c5b-9c79-70daa1d3c19c",
      "vehicle_brand": "Mercedes-Benz",
      "vehicle_model": "Conecto",
      "vehicle_year": 2022,
      "plate_number": "34ABC123",
      "route_uuid": null
    }
  },
  "error": ""
}
```
**Error Response:**
- 500: Failed to create vehicle
**Error Response Example:**
```json
{
  "success": false,
  "message": "Failed to create vehicle",
  "data": null,
  "error": ""
}
```

### Get All Vehicles
`GET /api/admin/management/vehicle/get_all`
Retrieves all vehicles.
**Headers:**
- `Authorization`: Bearer token
**Success Response:**
- Status: 200
- Body: ResponseModel with list of vehicles
**Success Response Example:**
```json
{
  "success": true,
  "message": "Vehicles retrieved successfully",
  "data": {
    "vehicles": [
      {
        "uuid": "f5488f20-f1b1-4c5b-9c79-70daa1d3c19c",
        "vehicle_brand": "Mercedes-Benz",
        "vehicle_model": "Conecto",
        "vehicle_year": 2022,
        "plate_number": "34ABC123",
        "route": null
      },
      {
        "uuid": "f082110a-34f5-4745-9ddf-e2c3f465fb05",
        "vehicle_brand": "Mercedes-Benz",
        "vehicle_model": "Conecto",
        "vehicle_year": 2023,
        "plate_number": "34ABC122",
        "route": null
      }
    ]
  },
  "error": ""
}
```
**Error Response:**
- 404: No vehicles found
**Error Response Example:**
```json
{
  "success": false,
  "message": "No vehicles found",
  "data": {
    "vehicles": []
  },
  "error": ""
}
```

### Update Vehicle
`PATCH /api/admin/management/vehicle/update`
Updates an existing vehicle.
**Request Body:**
```json
{
  "uuid": "string",
  "vehicle_brand": "string",
  "vehicle_model": "string",
  "vehicle_year": "string",
  "plate_number": "string",
  "route_uuid": "string" | null
}
```
**Headers:**
- `Authorization`: Bearer token (Admin token required)
**Success Response:**
- Status: 200
- Body: ResponseModel with updated vehicle data
**Success Response Example:**
```json
{
  "success": true,
  "message": "Vehicle updated successfully",
  "data": {
    "uuid": "vehicle-uuid-123",
    "vehicle_brand": "Mercedes",
    "vehicle_model": "Sprinter",
    "vehicle_year": "2023",
    "plate_number": "06 ABC 123",
    "route_uuid": "string" | null
  },
  "error": ""
}
```
**Error Response:**
- 500: Failed to update vehicle
- 404: Vehicle not found
**Error Response Example:**
```json
{
  "success": false,
  "message": "Vehicle not found",
  "data": null,
  "error": ""
}
```

### Delete Vehicle By UUID
`DELETE /api/admin/management/vehicle/delete/{vehicle_uuid}`
Deletes a vehicle by UUID.
**Parameters:**
- `vehicle_uuid`: UUID of the vehicle to be deleted
**Headers:**
- `Authorization`: Bearer token (Admin token required)
**Success Response:**
- Status: 200
- Body: ResponseModel with success message
**Success Response Example:**
```json
{
  "success": true,
  "message": "Vehicle deleted successfully",
  "data": {},
  "error": ""
}
```
**Error Response:**
- 500: Failed to delete vehicle
- 404: Vehicle not found
- 409: Vehicle is assigned to a driver
**Error Response Example:**
```json
{
  "success": false,
  "message": "Vehicle not found",
  "data": null,
  "error": ""
}
```
### Delete Vehicle By Plate Number
`DELETE /api/admin/management/vehicle/delete_plate_number/{plate_number}`
Deletes a vehicle by plate number.
**Parameters:**
- `plate_number`: Plate number of the vehicle to be deleted
**Headers:**
- `Authorization`: Bearer token (Admin token required)
Success Response:
- Status: 200
- Body: ResponseModel with success message
**Success Response Example:**
```json
{
  "success": true,
  "message": "Vehicle deleted successfully",
  "data": {},
  "error": ""
}
```
**Error Responses:**
- 500: Failed to delete vehicle
- 404: Vehicle not found
- 409: Vehicle is assigned to a driver
**Error Response Example:**
```json
{
  "success": false,
  "message": "Vehicle not found",
  "data": null,
  "error": ""
}
```
### Assign Routes to Vehicle
`PATCH /api/admin/management/vehicle/assign_routes`
Assigns routes to a vehicle.
**Request Body:**
```json
{
  "vehicle_uuid": "string",
  "route_uuid": "string"
}
```
**Headers:**
- `Authorization`: Bearer token (Admin token required)
**Success Response:**
- Status: 200
- Body: ResponseModel with success message
**Success Response Example:**
```json
{
  "success": true,
  "message": "Routes assigned successfully",
  "data": {
    "vehicle": {
      "uuid": "vehicle-uuid-123",
      "vehicle_brand": "Mercedes",
      "vehicle_model": "Sprinter",
      "vehicle_year": "2023",
      "plate_number": "06 ABC 123",
      "route_uuid": "string"
    }
  },
  "error": ""
}
```
**Error Response:**
- 500: Failed to assign routes
- 404: Vehicle not found
- 400: Invalid route UUID
- 409: Route already assigned
**Error Response Example:**
```json
{
  "success": false,
  "message": "Vehicle not found",
  "data": {},
  "error": ""
}
```

### Remove Routes from Vehicle
`PATCH /api/admin/management/vehicle/remove_routes`
Assigns routes to a vehicle.
**Request Body:**
```json
{
  "vehicle_uuid": "string",
  "route_uuid": "string"
}
```
**Headers:**
- `Authorization`: Bearer token (Admin token required)
**Success Response:**
- Status: 200
- Body: ResponseModel with success message
**Success Response Example:**
```json
{
  "success": true,
  "message": "Routes assigned successfully",
  "data": {
    "vehicle": {
      "uuid": "vehicle-uuid-123",
      "vehicle_brand": "Mercedes",
      "vehicle_model": "Sprinter",
      "vehicle_year": "2023",
      "plate_number": "06 ABC 123",
      "route_uuid": null
    }
  },
  "error": ""
}
```
**Error Response:**
- 400: Routes not assigned to a vehicle
- 404: Vehicle not found
- 500: A problem occured while removing routes.
**Error Response Example:**
```json
{
  "success": false,
  "message": "Vehicle not found",
  "data": {},
  "error": ""
}
```


## Driver Endpoints
### Get Active Journal
`GET /api/driver/active_journey/{driver_uid}`
Retrieves the active journal for the driver.
**Parameters:**
- `driver_uid`: UID of the driver

**Headers:**
- `Authorization`: Bearer token (Driver token required)

**Success Response:**
- Status: 200
- Body: ResponseModel with journal data

**Success Response Example:**
```json
{
  "success": true,
  "message": "Active journal retrieved successfully",
  "data": {
    "journal_date": "05-05-2025",
    "driver_name": "Cenker",
    "driver_last_name": "Özkan",
    "created_at": "2025-05-05T15:53:38.991755",
    "updated_at": "2025-05-05T15:53:38.991761",
    "journal_uuid": "4f6a5a3b-fa54-4db3-be50-7bf736bcc535",
    "journal_route": {
      "uuid": "5daa2025-3383-47c9-a7c2-da641067fe4d",
      "route_name": "Campus Loop Route",
      "created_at": "2025-04-30T15:46:48.866020",
      "updated_at": "2025-04-30T15:46:48.866025",
      "start_time": "09:30",
      "stops": [
        {
          "lat": 39.970539,
          "lon": 32.83588
        },
        {
          "lat": 39.971234,
          "lon": 32.836012
        },
        {
          "lat": 39.969876,
          "lon": 32.834567
        },
        {
          "lat": 39.968765,
          "lon": 32.83389
        }
      ]
    },
    "journal_vehicle": {
      "uuid": "f5488f20-f1b1-4c5b-9c79-70daa1d3c19c",
      "vehicle_brand": "Mercedes-Benz",
      "vehicle_model": "Conecto",
      "vehicle_year": 2022,
      "plate_number": "34ABC123",
      "route_uuid": "5daa2025-3383-47c9-a7c2-da641067fe4d"
    },
    "is_open": true,
    "driver_uid": "HLAuyB1sGIVV9LuIw6WikOPqLZ42",
    "locations": []
  },
  "error": ""
}
```

**Error Response:**
- 400: No active journal found

**Error Response Example:**
```json
{
  "success": false,
  "message": "No active journal found",
  "data": {},
  "error": ""
}
```

### Get Driver Information
`GET /api/driver/get_driver_information/{driver_uid}`
Retrieves information about the driver.
**Parameters:**
- `driver_uid`: UID of the driver

**Headers:**
- `Authorization`: Bearer token (Driver token required)

**Success Response:**
- Status: 200
- Body: ResponseModel with driver data
```json
{
  "success": true,
  "message": "Driver information retrieved successfully",
  "data": {
    "uid": "HLAuyB1sGIVV9LuIw6WikOPqLZ42",
    "first_name": "Cenker",
    "last_name": "Özkan",
    "phone_number": "+905343732399",
    "role": "DRIVER_USER",
    "vehicle": {
      "uuid": "f5488f20-f1b1-4c5b-9c79-70daa1d3c19c",
      "vehicle_brand": "Mercedes-Benz",
      "vehicle_model": "Conecto",
      "vehicle_year": 2022,
      "plate_number": "34ABC123",
      "route_uuid": "5daa2025-3383-47c9-a7c2-da641067fe4d"
    }
  },
  "error": ""
}
```

**Error Response:**
- 500: Failed to retrieve driver information
- 404: Driver not found

**Error Response Example:**
```json
{
  "success": false,
  "message": "Driver not found",
  "data": {},
  "error": ""
}
```

### Get Vehicle
`GET /api/driver/get_vehicle/{driver_uid}`
Retrieves the vehicle assigned to the driver.

**Parameters:**
- `driver_uid`: UID of the driver
- 
***Headers:**
- `Authorization`: Bearer token (Driver token required)

**Success Response:**
- Status: 200
- Body: ResponseModel with vehicle data

**Success Response Example:**
```json
{
  "success": true,
  "message": "Vehicle retrieved successfully",
  "data": {
    "vehicle": {
      "uuid": "vehicle-uuid-123",
      "vehicle_brand": "Mercedes",
      "vehicle_model": "Sprinter",
      "vehicle_year": "2023",
      "plate_number": "06 ABC 123",
      "route_uuid": "string" | null,
    }
  },
  "error": ""
}
```
**Error Response:**
- 500: Failed to retrieve vehicle
- 404: Vehicle not found

**Error Response Example:**
```json
{
  "success": false,
  "message": "No vehicle assigned to this driver",
  "data": {},
  "error": ""
}
```

### Get Vehicle Route
`GET /api/driver/get_vehicle_route/{driver_uid}`
Retrieves the route assigned to the vehicle of the driver.

**Parameters:**
- `driver_uid`: UID of the driver

**Headers:**
- `Authorization`: Bearer token (Driver token required)

**Success Response:**
- Status: 200
- Body: ResponseModel with route data

**Success Response Example:**
```json
{
  "success": true,
  "message": "Vehicle routes retrieved successfully",
  "data": {
    "route": {
      "uuid": "5daa2025-3383-47c9-a7c2-da641067fe4d",
      "route_name": "Campus Loop Route",
      "created_at": "2025-04-30T15:46:48.866020",
      "updated_at": "2025-04-30T15:46:48.866025",
      "start_time": "09:30",
      "stops": [
        {
          "lat": 39.970539,
          "lon": 32.83588
        },
        {
          "lat": 39.971234,
          "lon": 32.836012
        },
        {
          "lat": 39.969876,
          "lon": 32.834567
        },
        {
          "lat": 39.968765,
          "lon": 32.83389
        }
      ]
    }
  },
  "error": ""
}
```

**Error Response:**
- 500: Failed to retrieve route
- 404: Route not found

**Error Response Example:**
```json
{
  "success": false,
  "message": "Vehicle not found",
  "data": {},
  "error": ""
}
```

### Start Journey
`POST /api/driver/start_journey/{driver_uid}`
Starts the journey for the driver.
**Parameters:**
- `driver_uid`: UID of the driver

**Headers:**
- `Authorization`: Bearer token (Driver token required)

**Success Response:**
```json
{
  "success": true,
  "message": "Journey started successfully",
  "data": {
    "journal": {
      "journal_date": "30-04-2025",
      "driver_name": "Cenker",
      "driver_last_name": "Özkan",
      "created_at": "2025-04-30T21:40:34.342111",
      "updated_at": "2025-04-30T21:40:34.342116",
      "journal_uuid": "88280b2e-8ac4-4603-b2f7-0f28aac73fd7",
      "journal_route": {
        "uuid": "5daa2025-3383-47c9-a7c2-da641067fe4d",
        "route_name": "Campus Loop Route",
        "created_at": "2025-04-30T15:46:48.866020",
        "updated_at": "2025-04-30T15:46:48.866025",
        "start_time": "09:30",
        "stops": [
          {
            "lat": 39.970539,
            "lon": 32.83588
          },
          {
            "lat": 39.971234,
            "lon": 32.836012
          },
          {
            "lat": 39.969876,
            "lon": 32.834567
          },
          {
            "lat": 39.968765,
            "lon": 32.83389
          }
        ]
      },
      "journal_vehicle": {
        "uuid": "f5488f20-f1b1-4c5b-9c79-70daa1d3c19c",
        "vehicle_brand": "Mercedes-Benz",
        "vehicle_model": "Conecto",
        "vehicle_year": 2022,
        "plate_number": "34ABC123",
        "route_uuid": "5daa2025-3383-47c9-a7c2-da641067fe4d"
      },
      "driver_uid": "HLAuyB1sGIVV9LuIw6WikOPqLZ42",
      "locations": []
    }
  },
  "error": ""
}
````

### Stop Journey
`POST /api/driver/stop_journey/{driver_uid}/{journal_uuid}`
Stops the journey for the driver.

**Parameters:**
- `driver_uid`: UID of the driver
- `journal_uuid`: UUID of the journal

**Headers:**
- `Authorization`: Bearer token (Driver token required)

**Success Response:**
- Status: 200
- Body: ResponseModel with success message

**Success Response Example:**
```json
{
  "success": true,
  "message": "Journey stopped successfully",
  "data": {},
  "error": ""
}
```
**Error Response:**
- 500: Failed to stop journey
- 404: Bu şoföre atanmış bir araç bulunamadı
- 400: Bu araç zaten durdurulmuş

**Error Response Example:**
```json
{
  "success": false,
  "message": "Bu araç zaten durdurulmuş",
  "data": {},
  "error": ""
}
```

### Websocket Location Updates
`ws://busops-acb3c422b0e4.herokuapp.com/driver/ws/update_location`

**Authentication**
Include the API key in the request headers as this:
DRIVER-API-KEY: your-api-key-here

**Payload String**
```json
{
  "lat": 39.859570,
  "lon": 32.785186,
  "timestamp": "2024-03-21T14:30:00",
  "journal_uuid": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Success Response:**
```json string
{
  "code": 200,
  "success": true,
  "message": "",
  "error": "",
  "data": {}
}
```
**Error Response:**
```json string
{
  "code": 400,
  "success": false,
  "message": " ",
  "error": "",
  "data": null
}
```

## End User Endpoints
### Get Passenger Information
`GET /api/passenger/get_passenger_information/{uid}`
Retrieves information about the passenger.

**Parameters:**
- `uid`: UID of the passenger

**Headers:**
- `Authorization`: Bearer token (Passenger token required)

**Success Response:**
- Status: 200
- Body: ResponseModel with passenger data

**Success Response Example:**
```json
{
  "success": true,
  "message": "Kullanıcı bilgileri başarıyla alındı",
  "data": {
    "email": "cenkerozkan99@gmail.com",
    "first_name": "Cenker",
    "last_name": "Özkan",
    "saved_routes": []
  },
  "error": ""
}
```

**Error Response:**
- 404: Passenger not found

**Error Response Example:**
```json
{
  "success": false,
  "message": "Böyle bir kullanıcı bulunmamakta",
  "data": null,
  "error": ""
}
```

### Get All Routes For Passengers
`GET /api/passenger/get_all_routes`
Retrieves all routes available for passengers.

**Headers:**
- `Authorization`: Bearer token (Passenger token required)

**Success Response:**
- Status: 200
- Body: ResponseModel with list of routes

**Success Response Example:**
```json
{
  "success": true,
  "message": "Routes retrieved successfully",
  "data": {
    "routes": [
      {
        "uuid": "7625a95d-7af0-44fb-a0e9-40e7be03bd66",
        "route_name": "Downtown Express",
        "created_at": "2025-05-14T00:06:13.584341",
        "updated_at": "2025-05-14T00:06:13.584349",
        "start_time": "08:00",
        "stops": [
          {
            "lat": 39.925533,
            "lon": 32.866287
          },
          {
            "lat": 39.9305,
            "lon": 32.8552
          },
          {
            "lat": 39.935678,
            "lon": 32.844321
          }
        ]
      }
    ]
  },
  "error": ""
}
```
```json
{
  "success": true,
  "message": "Herhangi bir rota bulunmamakta",
  "data": {
    "routes": []
  },
  "error": ""
}
```

**Error Response:**
I did not plan any error response for this endpoint.
If somehow you're getting an error? that means there is some serious
problems with the Database.

### Get All Active Journeys
`GET /api/passenger/get_all_active_journeys`
Retrieves all active journeys for the passenger.

**Headers:**
- `Authorization`: Bearer token (Passenger token required)

**Success Response:**
- Status: 200
- Body: ResponseModel with list of active journeys

**Success Response Example:**
```json
{
  "success": true,
  "message": "Aktif yolculuklar başarıyla alındı",
  "data": {
    "active_journeys": [
      {
        "journal_date": "14-05-2025",
        "driver_name": "Cenker",
        "driver_last_name": "Özkan",
        "created_at": "2025-05-14T13:30:00.001701",
        "updated_at": "2025-05-14T13:30:00.001706",
        "journal_uuid": "324e765b-8954-45e4-a49c-3bd546e63422",
        "journal_route": {
          "uuid": "ceb8aed3-1b4f-4cb3-98d9-cd2e0eaff451",
          "route_name": "Downtown Express",
          "created_at": "2025-05-14T13:01:33.291780",
          "updated_at": "2025-05-14T13:01:33.291794",
          "start_time": "08:00",
          "stops": [
            {
              "lat": 39.925533,
              "lon": 32.866287
            },
            {
              "lat": 39.9305,
              "lon": 32.8552
            },
            {
              "lat": 39.935678,
              "lon": 32.844321
            }
          ]
        },
        "journal_vehicle": {
          "uuid": "f5488f20-f1b1-4c5b-9c79-70daa1d3c19c",
          "vehicle_brand": "Mercedes-Benz",
          "vehicle_model": "Conecto",
          "vehicle_year": 2022,
          "plate_number": "34ABC123",
          "route_uuid": "ceb8aed3-1b4f-4cb3-98d9-cd2e0eaff451"
        },
        "is_open": true,
        "driver_uid": "HLAuyB1sGIVV9LuIw6WikOPqLZ42"
      }
    ]
  },
  "error": ""
}
```
**Error Response:**
I haven't planned any error response for this endpoint.
If somehow you're getting an error? that means there is some serious
problems with the Database.

### Fetch Location From Journal
`ws://busops-acb3c422b0e4.herokuapp.com/passenger/ws/fetch_vehicle_location`

**Authentication** Include the API key in the request headers as this: PASSENGER-API-KEY: your-api-key-here
**Payload String**
```json
{
  "journal_uuid": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Success Response:**
```json string
{
    "code": 200,
    "success": true,
    "message": "Konum başarıyla alındı",
    "error": "",
    "data": {
        "current_location": {
            "lat": 39.85957,
            "lon": 32.785186,
            "time": "2024-03-21T14:30:00"
        }
    }
}
```
**Error Response:**
```json string
{
    "code": 404,
    "success": false,
    "message": "Böyle bir yolculuk bulunmamakta",
    "error": "",
    "data": {}
}
```