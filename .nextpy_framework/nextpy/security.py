"""
NextPy Security Module
Provides XSS protection and input sanitization
"""

import html
import re
from typing import Any, Dict, List, Union
from markupsafe import Markup, escape


class SecurityManager:
    """Manages security features for NextPy applications"""
    
    @staticmethod
    def sanitize_html(content: str) -> str:
        """
        Sanitize HTML content to prevent XSS attacks
        
        Args:
            content: Raw HTML content
            
        Returns:
            Sanitized HTML content
        """
        if not content:
            return ""
        
        # HTML escape the content
        sanitized = html.escape(content)
        
        # Remove potentially dangerous attributes
        dangerous_patterns = [
            r'on\w+\s*=',  # Event handlers
            r'javascript\s*:',  # JavaScript URLs
            r'data\s*:',  # Data URLs
            r'vbscript\s*:',  # VBScript URLs
        ]
        
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    @staticmethod
    def sanitize_jsx_props(props: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize JSX props to prevent XSS
        
        Args:
            props: Raw JSX props
            
        Returns:
            Sanitized props
        """
        sanitized = {}
        
        for key, value in props.items():
            # Skip dangerous attribute names
            if key.lower().startswith('on'):
                continue
            
            # Sanitize string values
            if isinstance(value, str):
                sanitized[key] = SecurityManager.sanitize_html(value)
            # Recursively sanitize nested objects
            elif isinstance(value, dict):
                sanitized[key] = SecurityManager.sanitize_jsx_props(value)
            # Sanitize lists
            elif isinstance(value, list):
                sanitized[key] = [
                    SecurityManager.sanitize_html(item) if isinstance(item, str) else item
                    for item in value
                ]
            else:
                sanitized[key] = value
        
        return sanitized
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL to prevent malicious URLs
        
        Args:
            url: URL to validate
            
        Returns:
            True if URL is safe, False otherwise
        """
        if not url:
            return False
        
        # Block dangerous protocols
        dangerous_protocols = [
            'javascript:',
            'vbscript:',
            'data:',
            'file:',
            'ftp:',
        ]
        
        url_lower = url.lower()
        for protocol in dangerous_protocols:
            if url_lower.startswith(protocol):
                return False
        
        # Allow only http, https, and relative URLs
        allowed_protocols = ['http://', 'https://', '/', './', '../']
        
        for protocol in allowed_protocols:
            if url_lower.startswith(protocol):
                return True
        
        return False
    
    @staticmethod
    def sanitize_css(css: str) -> str:
        """
        Sanitize CSS to prevent CSS injection
        
        Args:
            css: Raw CSS content
            
        Returns:
            Sanitized CSS content
        """
        if not css:
            return ""
        
        # Remove dangerous CSS constructs
        dangerous_patterns = [
            r'javascript\s*:',
            r'expression\s*\(',
            r'@import\s+',
            r'binding\s*:',
        ]
        
        sanitized = css
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    @staticmethod
    def validate_file_upload(filename: str, content_type: str) -> bool:
        """
        Validate file uploads to prevent malicious files
        
        Args:
            filename: Uploaded file name
            content_type: File content type
            
        Returns:
            True if file is safe, False otherwise
        """
        if not filename:
            return False
        
        # Check for dangerous file extensions
        dangerous_extensions = [
            '.exe', '.bat', '.cmd', '.com', '.pif', '.scr',
            '.vbs', '.js', '.jar', '.app', '.deb', '.rpm',
            '.dmg', '.pkg', '.msi', '.php', '.asp', '.jsp'
        ]
        
        filename_lower = filename.lower()
        for ext in dangerous_extensions:
            if filename_lower.endswith(ext):
                return False
        
        # Check content type
        allowed_content_types = [
            'image/', 'text/', 'application/json', 'application/xml',
            'application/pdf', 'application/msword', 'application/vnd'
        ]
        
        content_type_lower = content_type.lower()
        for allowed in allowed_content_types:
            if content_type_lower.startswith(allowed):
                return True
        
        return False
    
    @staticmethod
    def create_csp_header() -> str:
        """
        Create Content Security Policy header
        
        Returns:
            CSP header string
        """
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' data: https:",
            "font-src 'self' data:",
            "connect-src 'self' ws://localhost:* ws://127.0.0.1:*",
            "frame-src 'self'",
            "object-src 'none'",
            "base-uri 'self'",
            "form-action 'self'",
            "frame-ancestors 'none'",
            "upgrade-insecure-requests"
        ]
        
        return '; '.join(csp_directives)


# Global security manager instance
security_manager = SecurityManager()


def sanitize_input(data: Any) -> Any:
    """
    Sanitize input data recursively
    
    Args:
        data: Input data to sanitize
        
    Returns:
        Sanitized data
    """
    if isinstance(data, str):
        return security_manager.sanitize_html(data)
    elif isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    else:
        return data


def safe_html(content: str) -> Markup:
    """
    Return safe HTML content with XSS protection
    
    Args:
        content: HTML content
        
    Returns:
        Safe Markup object
    """
    sanitized = security_manager.sanitize_html(content)
    return Markup(sanitized)


def validate_and_sanitize_props(props: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and sanitize JSX props
    
    Args:
        props: JSX props to validate
        
    Returns:
        Sanitized props
    """
    return security_manager.sanitize_jsx_props(props)
