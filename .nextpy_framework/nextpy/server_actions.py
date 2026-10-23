"""
NextPy Server Actions - Enhanced Client-Server Communication
Provides seamless server-side function execution from client components
"""

import asyncio
import inspect
import json
from typing import Any, Callable, Dict, Optional, TypeVar, get_type_hints
from functools import wraps
from datetime import datetime

from fastapi import Request, HTTPException
from nextpy.db import get_session
from nextpy.auth import AuthManager, get_user_from_request

T = TypeVar('T')


class ServerActionError(Exception):
    """Custom exception for server action errors"""
    def __init__(self, message: str, code: str = "SERVER_ACTION_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationError(Exception):
    """Validation error for server actions"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"Validation failed for {field}: {message}")


class ServerAction:
    """
    Decorator and manager for server actions that can be called from client components
    Provides automatic serialization, validation, and error handling
    """
    
    _actions: Dict[str, Callable] = {}
    _validators: Dict[str, Callable] = {}
    _schemas: Dict[str, Any] = {}
    _auth: Dict[str, Any] = {}
    _roles: Dict[str, Any] = {}

    @classmethod
    def register(
        cls,
        name: Optional[str] = None,
        validate: Optional[Callable] = None,
        *,
        schema: Any = None,
        auth: bool = False,
        roles: Optional[tuple] = None,
    ):
        """
        Decorator to register a server action.

        Args:
            name: Custom action name (defaults to function name)
            validate: Optional validation function
            schema: Optional Pydantic model or :class:`ActionSchema`
            auth: Require an authenticated user
            roles: Optional tuple/set of allowed user roles
        """
        def decorator(func: Callable) -> Callable:
            action_name = name or func.__name__
            cls._actions[action_name] = func
            if validate:
                cls._validators[action_name] = validate
            if schema is not None:
                cls._schemas[action_name] = schema
            if auth or roles:
                cls._auth[action_name] = True
            if roles:
                cls._roles[action_name] = set(roles)
            
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    # Run validation if provided
                    if validate:
                        validation_result = validate(**kwargs)
                        if validation_result is not True:
                            if isinstance(validation_result, dict):
                                raise ValidationError(
                                    validation_result.get('field', 'unknown'),
                                    validation_result.get('message', 'Validation failed')
                                )
                            else:
                                raise ValidationError('input', str(validation_result))
                    
                    # Execute the action
                    if inspect.iscoroutinefunction(func):
                        result = await func(*args, **kwargs)
                    else:
                        result = func(*args, **kwargs)
                    
                    return {
                        "success": True,
                        "data": result,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
                except ValidationError as e:
                    return {
                        "success": False,
                        "error": {
                            "type": "validation",
                            "field": e.field,
                            "message": e.message
                        },
                        "timestamp": datetime.utcnow().isoformat()
                    }
                except ServerActionError as e:
                    return {
                        "success": False,
                        "error": {
                            "type": "server_action",
                            "code": e.code,
                            "message": e.message
                        },
                        "timestamp": datetime.utcnow().isoformat()
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "error": {
                            "type": "internal",
                            "message": str(e)
                        },
                        "timestamp": datetime.utcnow().isoformat()
                    }
            
            # Store original function for direct access
            wrapper._original_func = func
            wrapper._action_name = action_name
            return wrapper
        
        return decorator
    
    @classmethod
    def get_action(cls, name: str) -> Optional[Callable]:
        """Get a registered action by name"""
        return cls._actions.get(name)
    
    @classmethod
    def list_actions(cls) -> Dict[str, str]:
        """List all registered actions with their docstrings"""
        return {
            name: (func.__doc__ or "No description").strip()
            for name, func in cls._actions.items()
        }
    
    @classmethod
    async def execute(cls, name: str, request: Request, response=None, params=None) -> Dict[str, Any]:
        """
        Execute a server action
        
        Args:
            name: Action name
            request: FastAPI request object
            response: FastAPI response object (for setting cookies, headers, etc.)
            params: Action parameters as dict
            
        Returns:
            Action result as dictionary
        """
        if params is None:
            params = {}
        if not isinstance(params, dict):
            raise HTTPException(status_code=400, detail="Action params must be an object")

        action = cls.get_action(name)
        if not action:
            raise HTTPException(status_code=404, detail=f"Action '{name}' not found")

        func = getattr(action, '_original_func', action)
        sig = inspect.signature(func)
        kwargs = cls._filter_params(sig, params)

        schema = cls._schemas.get(name)
        if schema is not None:
            validated = cls._validate_schema(schema, kwargs)
            if validated is not None:
                return validated

        if cls._auth.get(name):
            user = get_user_from_request(request)
            if user is None:
                raise HTTPException(status_code=401, detail="Authentication required")
            allowed_roles = cls._roles.get(name)
            if allowed_roles and getattr(user, 'role', None) not in allowed_roles:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            request.state.user = user
            request.state.user_id = user.id
            if 'user' in sig.parameters:
                kwargs['user'] = user

        # Add request context if function accepts it
        if 'request' in sig.parameters:
            kwargs['request'] = request

        # Add response context if function accepts it
        if response is not None and 'response' in sig.parameters:
            kwargs['response'] = response

        # Add database session if function accepts it
        session_obj = None
        if 'session' in sig.parameters or 'db' in sig.parameters:
            session_obj = get_session()
            if 'session' in sig.parameters:
                kwargs['session'] = session_obj
            if 'db' in sig.parameters:
                kwargs['db'] = session_obj

        try:
            wrapper = cls._actions[name]
            if hasattr(wrapper, '_original_func'):
                if inspect.iscoroutinefunction(wrapper):
                    return await wrapper(**kwargs)
                return wrapper(**kwargs)

            if inspect.iscoroutinefunction(action):
                result = await action(**kwargs)
            else:
                result = action(**kwargs)
            return {
                "success": True,
                "data": result,
                "timestamp": datetime.utcnow().isoformat()
            }
        finally:
            if session_obj is not None:
                session_obj.close()

    @staticmethod
    def _filter_params(sig: inspect.Signature, params: Dict[str, Any]) -> Dict[str, Any]:
        """Drop unknown keys and client-supplied context arguments."""
        injected = {'request', 'response', 'session', 'db', 'user'}
        accepts_kwargs = any(
            p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()
        )
        allowed = {
            p.name for p in sig.parameters.values()
            if p.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)
        }
        return {
            key: value for key, value in params.items()
            if key not in injected and (accepts_kwargs or key in allowed)
        }

    @staticmethod
    def _validate_schema(schema: Any, kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Validate against Pydantic v1/v2 or :class:`ActionSchema`.

        Returns ``None`` when validation succeeds, otherwise a serialized error
        response.  On success the validated data is stored in ``kwargs``.
        """
        try:
            if hasattr(schema, 'model_validate'):
                model = schema.model_validate(kwargs)
                kwargs.clear()
                kwargs.update(model.model_dump())
                return None
            if hasattr(schema, 'parse_obj'):
                model = schema.parse_obj(kwargs)
                kwargs.clear()
                kwargs.update(model.dict())
                return None
            if isinstance(schema, ActionSchema):
                valid, errors = schema.validate(kwargs)
                if not valid:
                    return {
                        "success": False,
                        "error": {
                            "type": "validation",
                            "fields": errors or {},
                            "message": "Validation failed",
                        },
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                return None
        except Exception as exc:
            return {
                "success": False,
                "error": {
                    "type": "validation",
                    "message": str(exc),
                },
                "timestamp": datetime.utcnow().isoformat(),
            }
        return None


# Convenience decorator
server_action = ServerAction.register


# Built-in common server actions
@server_action()
async def get_health_status():
    """Health check action"""
    return {
        "status": "healthy",
        "version": "5.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@server_action()
async def get_current_user(request: Request):
    """Get the currently authenticated user, or ``None``."""
    try:
        user = get_user_from_request(request)
        if user is None:
            return None
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": getattr(user, "role", None),
        }
    except Exception:
        return None


class FormValidator:
    """Form validation utilities for server actions"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not any(c.isupper() for c in password):
            return False, "Password must contain uppercase letters"
        if not any(c.islower() for c in password):
            return False, "Password must contain lowercase letters"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain digits"
        return True, ""
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: list) -> tuple[bool, str]:
        """Validate that required fields are present and non-empty"""
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Field '{field}' is required"
        return True, ""


# Schema-based validation
class ActionSchema:
    """Schema definition for server action validation"""
    
    def __init__(self, **fields):
        self.fields = fields
    
    def validate(self, data: Dict[str, Any]) -> tuple[bool, Optional[Dict[str, str]]]:
        """
        Validate data against schema
        
        Returns:
            Tuple of (is_valid, errors_dict)
        """
        errors = {}
        
        for field_name, field_config in self.fields.items():
            if field_name not in data:
                if field_config.get('required', False):
                    errors[field_name] = f"Field '{field_name}' is required"
                continue
            
            value = data[field_name]
            field_type = field_config.get('type')
            
            # Type validation
            if field_type and not isinstance(value, field_type):
                errors[field_name] = f"Field '{field_name}' must be of type {field_type.__name__}"
                continue
            
            # Custom validation
            if 'validator' in field_config:
                validator = field_config['validator']
                if callable(validator):
                    is_valid, error_msg = validator(value)
                    if not is_valid:
                        errors[field_name] = error_msg
        
        return len(errors) == 0, errors if errors else None


__all__ = [
    'ServerAction',
    'server_action', 
    'ServerActionError',
    'ValidationError',
    'FormValidator',
    'ActionSchema',
    'get_health_status',
    'get_current_user',
]