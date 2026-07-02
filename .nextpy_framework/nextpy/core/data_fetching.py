"""
NextPy Data Fetching - Server-side data fetching inspired by Next.js
Implements:
- getServerSideProps (SSR) - Fetch data on every request
- getStaticProps (SSG) - Fetch data at build time
- getStaticPaths - Generate dynamic routes at build time
"""

import asyncio
import functools
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union
from dataclasses import dataclass
from pydantic import BaseModel


class PropsResult(BaseModel):
    """Result from getServerSideProps or getStaticProps"""
    props: Dict[str, Any] = {}
    redirect: Optional[Dict[str, str]] = None
    not_found: bool = False
    revalidate: Optional[int] = None


class StaticPathsResult(BaseModel):
    """Result from getStaticPaths"""
    paths: List[Dict[str, Any]] = []
    fallback: Union[bool, str] = False


@dataclass
class PageContext:
    """Context passed to data fetching functions"""
    params: Dict[str, str]
    query: Dict[str, str]
    req: Optional[Any] = None
    res: Optional[Any] = None
    preview: bool = False
    preview_data: Optional[Dict[str, Any]] = None
    locale: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        """Support dict-style access for existing page modules."""
        if key == "params":
            return self.params
        if key == "query":
            return self.query
        if key == "req" or key == "request":
            return self.req
        if key == "res":
            return self.res
        if key == "preview":
            return self.preview
        if key == "preview_data":
            return self.preview_data
        if key == "locale":
            return self.locale
        return default

    def __getitem__(self, key: str) -> Any:
        if key in {"params", "query", "req", "request", "res", "preview", "preview_data", "locale"}:
            return self.get(key)
        raise KeyError(key)

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, str):
            return False
        return key in {"params", "query", "req", "request", "res", "preview", "preview_data", "locale"}


T = TypeVar("T", bound=Callable)


def get_server_side_props(func: T) -> T:
    """
    Decorator to mark a function as getServerSideProps
    This function will be called on every request
    
    Usage:
        @get_server_side_props
        async def get_data(context: PageContext) -> PropsResult:
            data = await fetch_from_api()
            return PropsResult(props={"data": data})
    """
    func._is_server_side_props = True
    func._data_fetching_type = "ssr"
    
    @functools.wraps(func)
    async def wrapper(context: PageContext) -> PropsResult:
        if asyncio.iscoroutinefunction(func):
            result = await func(context)
        else:
            result = func(context)
            
        if isinstance(result, dict):
            result = PropsResult(**result)
        elif not isinstance(result, PropsResult):
            result = PropsResult(props={"data": result})
            
        return result
        
    wrapper._is_server_side_props = True
    wrapper._data_fetching_type = "ssr"
    return wrapper


def get_static_props(func: T) -> T:
    """
    Decorator to mark a function as getStaticProps
    This function will be called at build time (SSG)
    
    Usage:
        @get_static_props
        async def get_data(context: PageContext) -> PropsResult:
            data = await fetch_from_cms()
            return PropsResult(
                props={"data": data},
                revalidate=60  # ISR: regenerate every 60 seconds
            )
    """
    func._is_static_props = True
    func._data_fetching_type = "ssg"
    
    @functools.wraps(func)
    async def wrapper(context: PageContext) -> PropsResult:
        if asyncio.iscoroutinefunction(func):
            result = await func(context)
        else:
            result = func(context)
            
        if isinstance(result, dict):
            result = PropsResult(**result)
        elif not isinstance(result, PropsResult):
            result = PropsResult(props={"data": result})
            
        return result
        
    wrapper._is_static_props = True
    wrapper._data_fetching_type = "ssg"
    return wrapper


def get_static_paths(func: T) -> T:
    """
    Decorator to mark a function as getStaticPaths
    Used with dynamic routes to generate paths at build time
    
    Usage:
        @get_static_paths
        async def get_paths() -> StaticPathsResult:
            posts = await fetch_all_posts()
            return StaticPathsResult(
                paths=[{"params": {"slug": p.slug}} for p in posts],
                fallback=False
            )
    """
    func._is_static_paths = True
    
    @functools.wraps(func)
    async def wrapper() -> StaticPathsResult:
        if asyncio.iscoroutinefunction(func):
            result = await func()
        else:
            result = func()
            
        if isinstance(result, dict):
            result = StaticPathsResult(**result)
        elif isinstance(result, list):
            result = StaticPathsResult(paths=result)
        elif not isinstance(result, StaticPathsResult):
            result = StaticPathsResult(paths=[])
            
        return result
        
    wrapper._is_static_paths = True
    return wrapper


async def execute_data_fetching(
    module: Any,
    context: PageContext
) -> Dict[str, Any]:
    """
    Execute the appropriate data fetching function for a page module
    Returns the props to pass to the template
    """
    props = {}
    
    for name in ["getServerSideProps", "get_server_side_props", "getStaticProps", "get_static_props"]:
        if hasattr(module, name):
            func = getattr(module, name)
            
            if asyncio.iscoroutinefunction(func):
                result = await func(context)
            else:
                result = func(context)
                
            if isinstance(result, PropsResult):
                if result.not_found:
                    raise PageNotFoundError()
                if result.redirect:
                    raise RedirectError(
                        result.redirect.get("destination", "/"),
                        result.redirect.get("permanent", False)
                    )
                props.update(result.props)
            elif isinstance(result, dict):
                if result.get("not_found"):
                    raise PageNotFoundError()
                if result.get("redirect"):
                    raise RedirectError(
                        result["redirect"].get("destination", "/"),
                        result["redirect"].get("permanent", False)
                    )
                if "props" in result:
                    props.update(result["props"])
                else:
                    props.update(result)
            break
            
    return props


async def get_static_paths_for_route(module: Any) -> StaticPathsResult:
    """
    Get static paths for a dynamic route module
    """
    for name in ["getStaticPaths", "get_static_paths"]:
        if hasattr(module, name):
            func = getattr(module, name)
            
            if asyncio.iscoroutinefunction(func):
                result = await func()
            else:
                result = func()
                
            if isinstance(result, StaticPathsResult):
                return result
            elif isinstance(result, dict):
                return StaticPathsResult(**result)
            elif isinstance(result, list):
                return StaticPathsResult(paths=result)
                
    return StaticPathsResult(paths=[], fallback=False)


class PageNotFoundError(Exception):
    """Raised when a page returns not_found: True"""
    pass


class RedirectError(Exception):
    """Raised when a page returns a redirect"""
    def __init__(self, destination: str, permanent: bool = False):
        self.destination = destination
        self.permanent = permanent
        super().__init__(f"Redirect to {destination}")
