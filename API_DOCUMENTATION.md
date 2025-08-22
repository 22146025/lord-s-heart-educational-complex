# API Documentation - LORD'S HEART EDUCATIONAL COMPLEX

## Base URL
```
http://localhost:8000/api/
```

## Authentication
The API uses Django's session-based authentication. For admin endpoints, users must be authenticated and have staff privileges.

## Response Format
All API responses are in JSON format and follow this structure:
```json
{
    "count": 10,
    "next": "http://localhost:8000/api/admissions/?page=2",
    "previous": null,
    "results": [...]
}
```

## Admissions API

### List Applications
**GET** `/admissions/`

**Description**: Retrieve a list of admission applications. Public users can only see accepted/rejected applications, while admins see all.

**Query Parameters**:
- `status` (string): Filter by status (pending, reviewed, accepted, rejected)
- `gender` (string): Filter by gender (male, female)
- `class_before_admission` (string): Filter by previous class
- `search` (string): Search in surname, first_name, other_names, father_name, mother_name
- `ordering` (string): Order by field (application_date, created_at, surname, first_name)
- `page` (integer): Page number for pagination

**Response**:
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "surname": "DOE",
            "first_name": "John",
            "full_name": "DOE John Michael",
            "age": 8,
            "gender": "male",
            "class_before_admission": "Class 2",
            "status": "pending",
            "application_date": "2024-01-15T10:30:00Z",
            "created_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

### Create Application
**POST** `/admissions/`

**Description**: Submit a new admission application (public access).

**Request Body**:
```json
{
    "surname": "DOE",
    "first_name": "John",
    "other_names": "Michael",
    "date_of_birth": "2015-05-15",
    "age": 8,
    "gender": "male",
    "place_of_birth": "Accra",
    "region_of_birth": "Greater Accra",
    "home_town": "Kumasi",
    "region_of_home_town": "Ashanti",
    "last_school_attended": "Test Primary School",
    "location_of_last_school": "Accra",
    "class_before_admission": "Class 2",
    "religious_denomination": "Christian",
    "hobbies": "Reading, Swimming",
    "disability_or_allergy": "None",
    "father_name": "John Doe Sr.",
    "mother_name": "Jane Doe",
    "father_occupation": "Engineer",
    "mother_occupation": "Teacher",
    "father_contact": "+233123456789",
    "mother_contact": "+233987654321",
    "father_email": "father@test.com",
    "mother_email": "mother@test.com",
    "postal_address": "P.O. Box 123, Accra",
    "place_of_residence": "Accra",
    "house_number": "A123"
}
```

**Response**: 201 Created with full application details

### Get Application Details
**GET** `/admissions/{id}/`

**Description**: Retrieve detailed information about a specific application (admin only).

**Response**:
```json
{
    "id": 1,
    "surname": "DOE",
    "first_name": "John",
    "other_names": "Michael",
    "date_of_birth": "2015-05-15",
    "age": 8,
    "gender": "male",
    "place_of_birth": "Accra",
    "region_of_birth": "Greater Accra",
    "home_town": "Kumasi",
    "region_of_home_town": "Ashanti",
    "last_school_attended": "Test Primary School",
    "location_of_last_school": "Accra",
    "class_before_admission": "Class 2",
    "religious_denomination": "Christian",
    "hobbies": "Reading, Swimming",
    "disability_or_allergy": "None",
    "father_name": "John Doe Sr.",
    "mother_name": "Jane Doe",
    "father_occupation": "Engineer",
    "mother_occupation": "Teacher",
    "father_contact": "+233123456789",
    "mother_contact": "+233987654321",
    "father_email": "father@test.com",
    "mother_email": "mother@test.com",
    "postal_address": "P.O. Box 123, Accra",
    "place_of_residence": "Accra",
    "house_number": "A123",
    "status": "pending",
    "application_date": "2024-01-15T10:30:00Z",
    "reviewed_date": null,
    "reviewed_by": null,
    "notes": null,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "full_name": "DOE John Michael",
    "is_pending": true,
    "is_accepted": false,
    "is_rejected": false
}
```

### Update Application
**PUT/PATCH** `/admissions/{id}/`

**Description**: Update application status and notes (admin only).

**Request Body**:
```json
{
    "status": "accepted",
    "notes": "Application approved after review"
}
```

### Delete Application
**DELETE** `/admissions/{id}/`

**Description**: Delete an application (admin only).

### Get Statistics
**GET** `/admissions/statistics/`

**Description**: Get admission statistics for dashboard (admin only).

**Response**:
```json
{
    "total_applications": 10,
    "pending_applications": 3,
    "accepted_applications": 5,
    "rejected_applications": 2,
    "recent_applications": 4,
    "gender_statistics": [
        {"gender": "male", "count": 6},
        {"gender": "female", "count": 4}
    ],
    "class_statistics": [
        {"class_before_admission": "Class 1", "count": 3},
        {"class_before_admission": "Class 2", "count": 4},
        {"class_before_admission": "Class 3", "count": 3}
    ]
}
```

### Get Pending Applications
**GET** `/admissions/pending/`

**Description**: Get all pending applications (admin only).

### Approve Application
**POST** `/admissions/{id}/approve/`

**Description**: Approve an application (admin only).

### Reject Application
**POST** `/admissions/{id}/reject/`

**Description**: Reject an application (admin only).

## Contact API

### List Messages
**GET** `/contact/`

**Description**: Retrieve a list of contact messages (admin only).

**Query Parameters**:
- `status` (string): Filter by status (new, read, replied, archived)
- `search` (string): Search in name, email, message
- `ordering` (string): Order by field (created_at, name, email)
- `page` (integer): Page number for pagination

### Create Message
**POST** `/contact/`

**Description**: Submit a new contact message (public access).

**Request Body**:
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "message": "I would like to inquire about admission for my child."
}
```

**Response**: 201 Created with message details

### Get Message Details
**GET** `/contact/{id}/`

**Description**: Retrieve detailed information about a specific message (admin only).

**Response**:
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "message": "I would like to inquire about admission for my child.",
    "status": "new",
    "ip_address": "127.0.0.1",
    "user_agent": "Mozilla/5.0...",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "read_at": null,
    "replied_at": null
}
```

### Update Message
**PUT/PATCH** `/contact/{id}/`

**Description**: Update message status (admin only).

**Request Body**:
```json
{
    "status": "read"
}
```

### Delete Message
**DELETE** `/contact/{id}/`

**Description**: Delete a message (admin only).

### Get Statistics
**GET** `/contact/statistics/`

**Description**: Get contact message statistics (admin only).

**Response**:
```json
{
    "total_messages": 15,
    "new_messages": 5,
    "read_messages": 7,
    "replied_messages": 2,
    "archived_messages": 1,
    "recent_messages": 8,
    "status_statistics": [
        {"status": "new", "count": 5},
        {"status": "read", "count": 7},
        {"status": "replied", "count": 2},
        {"status": "archived", "count": 1}
    ],
    "daily_statistics": [
        {"day": "2024-01-15", "count": 3},
        {"day": "2024-01-16", "count": 2}
    ]
}
```

### Get New Messages
**GET** `/contact/new/`

**Description**: Get all new messages (admin only).

### Mark as Read
**POST** `/contact/{id}/mark_as_read/`

**Description**: Mark a message as read (admin only).

### Mark as Replied
**POST** `/contact/{id}/mark_as_replied/`

**Description**: Mark a message as replied (admin only).

### Archive Message
**POST** `/contact/{id}/archive/`

**Description**: Archive a message (admin only).

## Users API

### List Users
**GET** `/users/`

**Description**: Retrieve a list of users (admin only).

**Query Parameters**:
- `is_active` (boolean): Filter by active status
- `is_staff` (boolean): Filter by staff status
- `search` (string): Search in username, email, first_name, last_name
- `ordering` (string): Order by field (username, email, date_joined)
- `page` (integer): Page number for pagination

### Create User
**POST** `/users/`

**Description**: Create a new user (admin only).

**Request Body**:
```json
{
    "username": "newuser",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "profile": {
        "role": "teacher",
        "phone_number": "+233123456789",
        "department": "Mathematics"
    }
}
```

### Get User Details
**GET** `/users/{id}/`

**Description**: Retrieve detailed information about a specific user (admin only).

### Update User
**PUT/PATCH** `/users/{id}/`

**Description**: Update user information (admin only).

### Delete User
**DELETE** `/users/{id}/`

**Description**: Delete a user (admin only).

### Get Current User Profile
**GET** `/users/me/`

**Description**: Get current user's profile (authenticated users).

### Update Current User Profile
**PUT** `/users/update_me/`

**Description**: Update current user's profile (authenticated users).

### Change Password
**POST** `/users/change_password/`

**Description**: Change current user's password (authenticated users).

**Request Body**:
```json
{
    "old_password": "currentpassword",
    "new_password": "newpassword123",
    "new_password_confirm": "newpassword123"
}
```

### Get User Statistics
**GET** `/users/statistics/`

**Description**: Get user statistics (admin only).

**Response**:
```json
{
    "total_users": 25,
    "active_users": 23,
    "staff_users": 8,
    "recent_users": 5,
    "role_statistics": [
        {"role": "admin", "count": 2},
        {"role": "staff", "count": 3},
        {"role": "teacher", "count": 8},
        {"role": "parent", "count": 10},
        {"role": "student", "count": 2}
    ]
}
```

## Error Responses

### 400 Bad Request
```json
{
    "field_name": ["Error message for this field"]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
    "detail": "Internal server error."
}
```

## Rate Limiting
Currently, no rate limiting is implemented. Consider implementing rate limiting for production use.

## CORS
CORS is configured to allow requests from:
- http://localhost:3000
- http://127.0.0.1:3000

For production, update CORS settings in Django settings.

## Testing the API

### Using curl
```bash
# Create an admission application
curl -X POST http://localhost:8000/api/admissions/ \
  -H "Content-Type: application/json" \
  -d '{"surname":"DOE","first_name":"John",...}'

# Get applications (public)
curl http://localhost:8000/api/admissions/

# Get applications (admin)
curl -H "Cookie: sessionid=your-session-id" http://localhost:8000/api/admissions/
```

### Using Python requests
```python
import requests

# Create admission application
response = requests.post('http://localhost:8000/api/admissions/', json={
    'surname': 'DOE',
    'first_name': 'John',
    # ... other fields
})

# Get applications
response = requests.get('http://localhost:8000/api/admissions/')
applications = response.json()
```

### Using JavaScript fetch
```javascript
// Create admission application
fetch('http://localhost:8000/api/admissions/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        surname: 'DOE',
        first_name: 'John',
        // ... other fields
    })
})
.then(response => response.json())
.then(data => console.log(data));
```
