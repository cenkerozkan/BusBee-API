error_messages = {
    # Authentication Errors
    "INVALID_TOKEN": "Invalid token provided",
    "TOKEN_EXPIRED": "Token has expired",
    "TOKEN_REVOKED": "Token has been revoked",

    # Login Errors
    "INVALID_CREDENTIALS": "Invalid email or password",
    "ACCOUNT_DISABLED": "Account has been disabled",
    "USER_NOT_FOUND": "User not found",

    # Registration Errors
    "EMAIL_EXISTS": "Email already exists",
    "WEAK_PASSWORD": "Password should be at least 6 characters",
    "INVALID_EMAIL": "Invalid email format",

    # Email Verification
    "EMAIL_NOT_VERIFIED": "Email not verified",
    "VERIFICATION_FAILED": "Email verification failed",
    "VERIFICATION_EXPIRED": "Verification code expired",

    # Firebase specific errors
    "INVALID_LOGIN_CREDENTIALS": "Email or password is incorrect",
    "EMAIL_EXISTS": "Email already exists",
    "INVALID_PASSWORD": "Invalid password provided",
    "USER_DISABLED": "User account has been disabled",
    "USER_NOT_FOUND": "No user found with this email",
    "WEAK_PASSWORD": "Password should be at least 6 characters",
    "INVALID_EMAIL": "Invalid email format"

    # Other errors
}

def get_error_message(error_code: str) -> str:
    """Get the error message for a given error code."""
    return error_messages.get(error_code.upper(), "Internal server error occurred") if error_messages.get(error_code.upper(), "Internal server error occurred") else "UNKNOWN ERROR"