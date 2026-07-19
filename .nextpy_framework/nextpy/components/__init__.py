"""NextPy Components - Reusable UI components - Updated for JSX system"""

# Legacy components (still available)
from nextpy.components.head import Head
from nextpy.components.link import Link
from nextpy.components.image import Image

# New JSX-compatible components
from nextpy.components.form import (
    Input, TextArea, Select, Checkbox, Radio, RadioGroup, Form, FormGroup, FileInput,
    NumberInput, DateInput, TimeInput, PasswordInput, RangeInput, ColorInput, SubmitButton
)

from nextpy.components.layout import (
    Container, Grid, Flex, Stack, Sidebar, MainContent, Section, Article, 
    Header, Footer, Navigation, Center, Spacer, Divider, AspectRatio, Card
)

from nextpy.components.ui import (
    Button, Badge, Avatar, Icon, Alert, Progress, Skeleton, Tooltip, Chip, 
    Breadcrumb, Table, Code, Blockquote
)

from nextpy.components.navigation import (
    Navbar, Sidebar as NavSidebar, Menu, Dropdown, Tabs, Pagination, 
    SearchBar, BreadcrumbNav
)

# Legacy feedback components
from nextpy.components.feedback import Alert as LegacyAlert, Badge as LegacyBadge, Progress as LegacyProgress

# Legacy loader components
from nextpy.components.loader import spinner, skeleton, progress_bar, loading_screen

# Legacy toast components
from nextpy.components.toast import Toast, get_toast, toast_html

# Legacy visual components
from nextpy.components.visual import (
    Tabs as LegacyTabs, Accordion, Dropdown as LegacyDropdown, Modal, 
    Card as LegacyCard, Breadcrumb as LegacyBreadcrumb, Pagination as LegacyPagination
)

# Hooks provider
from nextpy.components.hooks_provider import HooksProvider, HooksContext, with_hooks

__all__ = [
    # Core components
    "Head", "Link", "Image",
    
    # Form components (NEW)
    "Input", "TextArea", "Select", "Checkbox", "Radio", "RadioGroup", "Form", "FormGroup", "FileInput",
    "NumberInput", "DateInput", "TimeInput", "PasswordInput", "RangeInput", "ColorInput", "SubmitButton",
    
    # Layout components (NEW)
    "Container", "Grid", "Flex", "Stack", "Sidebar", "MainContent", "Section", "Article", 
    "Header", "Footer", "Navigation", "Center", "Spacer", "Divider", "AspectRatio", "Card",
    
    # UI components (NEW)
    "Button", "Badge", "Avatar", "Icon", "Alert", "Progress", "Skeleton", "Tooltip", "Chip", 
    "Breadcrumb", "Table", "Code", "Blockquote",
    
    # Navigation components (NEW)
    "Navbar", "NavSidebar", "Menu", "Dropdown", "Tabs", "Pagination", 
    "SearchBar", "BreadcrumbNav",
    
    # Legacy components (still available)
    "LegacyAlert", "LegacyBadge", "LegacyProgress",
    "spinner", "skeleton", "progress_bar", "loading_screen",
    "Toast", "get_toast", "toast_html",
    "LegacyTabs", "Accordion", "LegacyDropdown", "Modal", 
    "LegacyCard", "LegacyBreadcrumb", "LegacyPagination",
    "HooksProvider", "HooksContext", "with_hooks"
]
