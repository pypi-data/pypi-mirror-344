from fastapi import HTTPException,status

class DuplicateRoleError(HTTPException):
    def __init__(self, detail: str = "Role already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class DuplicatePermissionError(HTTPException):
    def __init__(self, detail: str = "Permission already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class RoleNotFoundError(HTTPException):
    def __init__(self, detail: str = "Role not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class PermissionNotFoundError(HTTPException):
    def __init__(self, detail: str = "Permission not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class RolePermissionNotFoundError(HTTPException):
    def __init__(self, detail: str = "Role permission not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class PermissionDeniedError(HTTPException):
    def __init__(self, detail: str = "Permission denied for the requested resource"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class ForbiddenError(HTTPException):
    def __init__(self, detail: str = "You are not authorized to perform this action."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)