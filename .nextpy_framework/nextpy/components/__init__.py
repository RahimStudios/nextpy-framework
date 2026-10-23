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

# Legacy aliases for components that were renamed/consolidated
LegacyAlert = Alert
LegacyBadge = Badge
LegacyProgress = Progress
LegacyTabs = Tabs
LegacyDropdown = Dropdown
LegacyCard = Card
LegacyBreadcrumb = Breadcrumb
LegacyPagination = Pagination

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
    
    # Legacy aliases (still available)
    "LegacyAlert", "LegacyBadge", "LegacyProgress",
    "LegacyTabs", "LegacyDropdown", "LegacyCard",
    "LegacyBreadcrumb", "LegacyPagination",
    "HooksProvider", "HooksContext", "with_hooks"
]
