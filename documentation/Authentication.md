<h3 align="center">Monta API Authentication</h3>

### Acquire Token

- Endpoint: `POST /api/auth/token/`
- Request Body: `{"username": "username", "password": "password"}`
- Response Body: `{"token": "token"}`
- Response Headers: `{"Authorization": "Token token"}`
- Response Status: `200 OK`
- Description: Acquires a token for the user with the given username and password. The token is returned in the response
  body and is also set as the Authorization header.
- Example Request:

```json
{
  "username": "username",
  "password": "password"
}
```

- Example Response:

```json
{
  "token": "token"
}
```

### Verify Token

- Endpoint: `GET /api/auth/token/verify/`
- Request Headers: `{"Authorization": "Token token"}`
- Response Status: `200 OK`
- Description: Verifies that the given token is valid. Returns a 200 OK status if the token is valid, and a 401
  Unauthorized status if the token is invalid.
- Example Request:

```bash
curl -X GET -H "Authorization: Token token" http://localhost:8000/api/auth/token/verify/
```

### Refresh Token

- Endpoint: `POST /api/auth/token/refresh/`
- Request Headers: `{"Authorization": "Token token"}`
- Response Body: `{"token": "token"}`
- Response Headers: `{"Authorization": "Token token"}`
- Response Status: `200 OK`
- Description: Refreshes the given token. The new token is returned in the response body and is also set as the
  Authorization header.
- Example Request:

```bash
curl -X POST -H "Authorization: Token token" http://localhost:8000/api/auth/token/refresh/
```

- Example Response:

```json
{
  "token": "token"
}
```

### Revoke Token

- Endpoint: `POST /api/auth/token/revoke/`
- Request Headers: `{"Authorization": "Token token"}`
- Response Status: `204 No Content`
- Description: Revokes the given token. Returns a 204 No Content status if the token is successfully revoked, and a 401
  Unauthorized status if the token is invalid.
- Example Request:

```bash
curl -X POST -H "Authorization: Token token" http://localhost:8000/api/auth/token/revoke/
```

### Acquire Password Reset Token

- Endpoint: `POST /api/auth/password/reset/`
- Request Body: `{"email": "email"}`
- Response Status: `204 No Content`
- Description: Acquires a password reset token for the user with the given email. Returns a 204 No Content status if the
  email is valid, and a 400 Bad Request status if the email is invalid.
- Example Request:

```json
{
  "email": "email"
}
```

### Reset Password

- Endpoint: `POST /api/auth/password/reset/confirm/`
- Request Body: `{"token": "token", "new_password": "new_password"}`
- Response Status: `204 No Content`
- Description: Resets the password for the user with the given password reset token. Returns a 204 No Content status if
  the token is valid, and a 400 Bad Request status if the token is invalid.
- Example Request:

```json
{
  "token": "token",
  "new_password": "new_password"
}
```

### Acquire Email Verification Token

- Endpoint: `POST /api/auth/email/verify/`
- Request Body: `{"email": "email"}`
- Response Status: `204 No Content`
- Description: Acquires an email verification token for the user with the given email. Returns a 204 No Content status
  if the email is valid, and a 400 Bad Request status if the email is invalid.
- Example Request:

```json
{
  "email": "email"
}
```

### Verify Email

- Endpoint: `POST /api/auth/email/verify/confirm/`
- Request Body: `{"token": "token"}`
- Response Status: `204 No Content`
- Description: Verifies the email for the user with the given email verification token. Returns a 204 No Content status
  if the token is valid, and a 400 Bad Request status if the token is invalid.
- Example Request:

```json
{
  "token": "token"
}
```