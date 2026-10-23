"""
NextPy Link Component - Client-side navigation with prefetching
Supports both HTMX and NextPy native client-side router
"""

from typing import Any, Optional
from markupsafe import Markup


class Link:
    """
    Link component for client-side navigation.
    
    Uses the NextPy client-side router for SPA navigation when available,
    with HTMX fallback and plain anchor as final fallback.
    
    Usage in templates:
        {{ Link("/about", "About Us", prefetch=True) }}
        {{ Link("/blog/" + post.slug, post.title, class_="text-blue-500") }}
    
    In PSX components:
        <Link href="/about">About</Link>
        <Link href="/dashboard" prefetch={True} replace={True}>Dashboard</Link>
    """
    
    def __init__(
        self,
        href: str,
        text: Optional[str] = None,
        prefetch: bool = True,
        replace: bool = False,
        scroll: bool = True,
        class_: Optional[str] = None,
        target: Optional[str] = None,
        use_htmx: bool = False,
        use_router: bool = True,
        transition: Optional[str] = None,
        **kwargs: Any,
    ):
        self.href = href
        self.text = text
        self.prefetch = prefetch
        self.replace = replace
        self.scroll = scroll
        self.class_ = class_
        self.target = target
        self.use_htmx = use_htmx
        self.use_router = use_router
        self.transition = transition
        self.extra_attrs = kwargs
        
    def render(self, children: Optional[str] = None) -> str:
        """Render the link as an HTML anchor tag"""
        content = children or self.text or self.href
        
        attrs = [f'href="{self._escape(self.href)}"']
        
        if self.class_:
            attrs.append(f'class="{self._escape(self.class_)}"')
            
        if self.target:
            attrs.append(f'target="{self._escape(self.target)}"')
            
        # Client-side router attributes (primary navigation method)
        if self.use_router and not self.target:
            attrs.append('data-nextpy-link="true"')
            if self.replace:
                attrs.append('data-nextpy-replace="true"')
            if not self.scroll:
                attrs.append('data-nextpy-scroll="false"')
            if self.transition:
                attrs.append(f'data-nextpy-transition="{self._escape(self.transition)}"')
            if self.prefetch:
                attrs.append('data-prefetch="true"')
                
        # HTMX fallback (when router is disabled)
        elif self.use_htmx and not self.target:
            attrs.append(f'hx-get="{self._escape(self.href)}"')
            attrs.append('hx-target="#app"')
            attrs.append('hx-swap="innerHTML"')
            attrs.append('hx-push-url="true"')
            
            if self.prefetch:
                attrs.append('hx-trigger="mouseenter, click"')
                attrs.append('preload="true"')
                
        elif self.prefetch:
            attrs.append('data-prefetch="true"')
            
        for key, value in self.extra_attrs.items():
            attr_name = key.replace("_", "-")
            if value is True:
                attrs.append(attr_name)
            elif value is not False and value is not None:
                attrs.append(f'{attr_name}="{self._escape(str(value))}"')
                
        attrs_str = " ".join(attrs)
        return f"<a {attrs_str}>{content}</a>"
        
    def __html__(self) -> str:
        """Make the component work with Jinja2's autoescape"""
        return self.render()
        
    def __str__(self) -> str:
        return self.render()
        
    def __call__(
        self, 
        href: Optional[str] = None, 
        text: Optional[str] = None,
        **kwargs: Any
    ) -> Markup:
        """Allow calling Link() in templates with arguments"""
        if href:
            self.href = href
        if text:
            self.text = text
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                self.extra_attrs[key] = value
        return Markup(self.render())
        
    @staticmethod
    def _escape(value: str) -> str:
        """Escape HTML special characters"""
        return (
            str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#x27;")
        )


def link(href: str, text: Optional[str] = None, **kwargs: Any) -> Markup:
    """
    Functional helper to create a Link
    
    Usage in templates:
        {{ link("/about", "About Us") }}
    """
    return Markup(Link(href, text, **kwargs).render())
