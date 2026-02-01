"""
Logging Middleware for FastAPI
Automatically logs all API requests with timing and context
"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
from app.utils.logger import log_api_request, error


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all API requests"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        # Start timing
        start_time = time.time()
        
        # Get user_id from request state if available
        user_id = None
        try:
            if hasattr(request.state, "user"):
                user_id = request.state.user.get("user_id")
        except:
            pass
        
        # Process request
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            # Log successful request
            log_api_request(
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration=duration,
                user_id=user_id
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            
            # Log failed request
            error(
                f"Request failed: {request.method} {request.url.path}",
                exc_info=True,
                method=request.method,
                path=request.url.path,
                duration=duration,
                user_id=user_id
            )
            raise
