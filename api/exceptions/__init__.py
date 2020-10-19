from fastapi import HTTPException, status


invalid_api_key = HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'Not authenticated')
