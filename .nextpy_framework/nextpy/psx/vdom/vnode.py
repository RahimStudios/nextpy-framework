"""
PSX Virtual DOM - Optimized Virtual DOM Implementation for NextPy
Features: Efficient diffing, patching, batching, and performance optimizations
"""

import time
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
from ..core.parser import PSXElement


class VDOMNodeType(Enum):
    """Node types for Virtual DOM (renamed to avoid conflict with core)"""
    ELEMENT = "element"
    TEXT = "text"
    COMPONENT = "component"
    FRAGMENT = "fragment"


@dataclass
class VNode:
    """Virtual DOM Node - Optimized for performance"""
    type: Union[str, VDOMNodeType]
    props: Dict[str, Any] = field(default_factory=dict)
    children: List['VNode'] = field(default_factory=list)
    key: Optional[str] = None
    ref: Optional[Dict[str, Any]] = None
    _dom_node: Optional[Any] = None  # Reference to real DOM node
    _component_instance: Optional[Any] = None  # Component instance reference
    
    def __post_init__(self):
        """Optimize node creation"""
        if isinstance(self.props, dict):
            # Freeze props for performance
            self.props = dict(self.props)
    
    @property
    def is_element(self) -> bool:
        """Check if this is an element node"""
        return self.type == VDOMNodeType.ELEMENT or isinstance(self.type, str)
    
    @property
    def is_text(self) -> bool:
        """Check if this is a text node"""
        return self.type == VDOMNodeType.TEXT
    
    @property
    def is_component(self) -> bool:
        """Check if this is a component node"""
        return self.type == VDOMNodeType.COMPONENT
    
    @property
    def is_fragment(self) -> bool:
        """Check if this is a fragment node"""
        return self.type == VDOMNodeType.FRAGMENT


class VDOMDiff:
    """Virtual DOM Diffing Algorithm - Optimized for performance"""
    
    @staticmethod
    def diff(old_vnode: Optional[VNode], new_vnode: Optional[VNode]) -> List['Patch']:
        """
        Diff two virtual DOM trees and generate patches
        Uses optimized algorithms for better performance
        """
        patches = []
        
        if old_vnode is None and new_vnode is not None:
            # New node - create patch
            patches.append(Patch(PatchType.CREATE, None, new_vnode))
        elif old_vnode is not None and new_vnode is None:
            # Node removed - remove patch
            patches.append(Patch(PatchType.REMOVE, old_vnode, None))
        elif old_vnode is not None and new_vnode is not None:
            # Both exist - compare and generate patches
            VDOMDiff._diff_node(old_vnode, new_vnode, patches, [])
        
        return patches
    
    @staticmethod
    def _diff_node(old_vnode: VNode, new_vnode: VNode, patches: List['Patch'], path: List[int]):
        """Diff two nodes recursively"""
        
        # Check if node type changed
        if old_vnode.type != new_vnode.type:
            patches.append(Patch(PatchType.REPLACE, old_vnode, new_vnode, path.copy()))
            return
        
        # Handle different node types
        if old_vnode.is_text and new_vnode.is_text:
            # Text nodes - check content
            if old_vnode.props.get('text') != new_vnode.props.get('text'):
                patches.append(Patch(PatchType.UPDATE_TEXT, old_vnode, new_vnode, path.copy()))
        
        elif old_vnode.is_element and new_vnode.is_element:
            # Element nodes - check props and children
            VDOMDiff._diff_element_props(old_vnode, new_vnode, patches, path)
            VDOMDiff._diff_children(old_vnode, new_vnode, patches, path)
        
        elif old_vnode.is_component and new_vnode.is_component:
            # Component nodes - check props
            if old_vnode.props != new_vnode.props:
                patches.append(Patch(PatchType.UPDATE_COMPONENT, old_vnode, new_vnode, path.copy()))
    
    @staticmethod
    def _diff_element_props(old_vnode: VNode, new_vnode: VNode, patches: List['Patch'], path: List[int]):
        """Diff element props efficiently"""
        old_props = old_vnode.props
        new_props = new_vnode.props
        
        # Find changed and removed props
        changed_props = {}
        removed_props = set()
        
        # Check for changed and removed props
        for key, old_value in old_props.items():
            if key not in new_props:
                removed_props.add(key)
            elif new_props[key] != old_value:
                changed_props[key] = new_props[key]
        
        # Check for new props
        for key, new_value in new_props.items():
            if key not in old_props:
                changed_props[key] = new_value
        
        # Create patch if props changed
        if changed_props or removed_props:
            patches.append(Patch(
                PatchType.UPDATE_PROPS, 
                old_vnode, 
                new_vnode, 
                path.copy(),
                {
                    'changed': changed_props,
                    'removed': removed_props
                }
            ))
    
    @staticmethod
    def _diff_children(old_vnode: VNode, new_vnode: VNode, patches: List['Patch'], path: List[int]):
        """Diff children using optimized key-based algorithm"""
        old_children = old_vnode.children
        new_children = new_vnode.children
        
        # Use key-based diffing for better performance
        if VDOMDiff._has_keys(old_children) or VDOMDiff._has_keys(new_children):
            VDOMDiff._diff_children_with_keys(old_children, new_children, patches, path)
        else:
            VDOMDiff._diff_children_without_keys(old_children, new_children, patches, path)
    
    @staticmethod
    def _has_keys(children: List[VNode]) -> bool:
        """Check if any children have keys"""
        return any(child.key is not None for child in children)
    
    @staticmethod
    def _diff_children_with_keys(old_children: List[VNode], new_children: List[VNode], patches: List['Patch'], path: List[int]):
        """Diff children using key-based algorithm for optimal performance"""
        
        # Build key maps
        old_key_map = {child.key: child for child in old_children if child.key}
        new_key_map = {child.key: child for child in new_children if child.key}
        
        # Find moved, added, and removed children
        moved_children = []
        added_children = []
        removed_children = []
        
        # Check each new child
        for i, new_child in enumerate(new_children):
            if new_child.key and new_child.key in old_key_map:
                old_child = old_key_map[new_child.key]
                # Check if child moved
                old_index = old_children.index(old_child)
                if old_index != i:
                    moved_children.append((old_index, i, new_child))
                # Diff the child
                child_path = path + [i]
                VDOMDiff._diff_node(old_child, new_child, patches, child_path)
            else:
                added_children.append((i, new_child))
        
        # Check for removed children
        for old_child in old_children:
            if old_child.key and old_child.key not in new_key_map:
                removed_children.append(old_child)
        
        # Create patches for moved children
        for old_index, new_index, child in moved_children:
            patches.append(Patch(
                PatchType.MOVE,
                None,
                child,
                path.copy() + [new_index],
                {'old_index': old_index, 'new_index': new_index}
            ))
        
        # Create patches for added children
        for index, child in added_children:
            child_path = path + [index]
            patches.append(Patch(PatchType.CREATE, None, child, child_path))
        
        # Create patches for removed children
        for child in removed_children:
            patches.append(Patch(PatchType.REMOVE, child, None))
    
    @staticmethod
    def _diff_children_without_keys(old_children: List[VNode], new_children: List[VNode], patches: List['Patch'], path: List[int]):
        """Diff children without keys using simple algorithm"""
        max_len = max(len(old_children), len(new_children))
        
        for i in range(max_len):
            child_path = path + [i]
            
            if i >= len(old_children):
                # Child added
                patches.append(Patch(PatchType.CREATE, None, new_children[i], child_path))
            elif i >= len(new_children):
                # Child removed
                patches.append(Patch(PatchType.REMOVE, old_children[i], None))
            else:
                # Diff existing child
                VDOMDiff._diff_node(old_children[i], new_children[i], patches, child_path)


class PatchType(Enum):
    """Patch types for Virtual DOM updates"""
    CREATE = "create"
    REMOVE = "remove"
    REPLACE = "replace"
    UPDATE_PROPS = "update_props"
    UPDATE_TEXT = "update_text"
    UPDATE_COMPONENT = "update_component"
    MOVE = "move"


@dataclass
class Patch:
    """Patch operation for Virtual DOM updates"""
    type: PatchType
    old_vnode: Optional[VNode]
    new_vnode: Optional[VNode]
    path: List[int] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)


class VDOMRenderer:
    """Virtual DOM Renderer with performance optimizations"""
    
    def __init__(self):
        self.component_cache = {}  # Cache for component instances
        self.node_cache = {}  # Cache for DOM nodes
        self.render_count = 0
        self.last_render_time = 0
    
    def render(self, vnode: VNode, container: Any = None) -> Any:
        """
        Render a virtual DOM node to real DOM
        Optimized for performance with caching and batching
        """
        start_time = time.time()
        
        # Create real DOM node
        dom_node = self._create_dom_node(vnode)
        
        # Cache the node
        if vnode.key:
            self.node_cache[vnode.key] = dom_node
        
        # Update performance metrics
        self.render_count += 1
        self.last_render_time = time.time() - start_time
        
        return dom_node
    
    def patch(self, patches: List[Patch], container: Any = None):
        """
        Apply patches to real DOM
        Optimized batching for better performance
        """
        start_time = time.time()
        
        # Sort patches by path for efficient processing
        patches.sort(key=lambda p: len(p.path))
        
        # Apply patches in batch
        for patch in patches:
            self._apply_patch(patch, container)
        
        # Update performance metrics
        patch_time = time.time() - start_time
        return patch_time
    
    def _create_dom_node(self, vnode: VNode) -> Any:
        """Create real DOM node from virtual node"""
        if vnode.is_text:
            return self._create_text_node(vnode)
        elif vnode.is_element:
            return self._create_element_node(vnode)
        elif vnode.is_component:
            return self._create_component_node(vnode)
        elif vnode.is_fragment:
            return self._create_fragment_node(vnode)
        else:
            raise ValueError(f"Unknown vnode type: {vnode.type}")
    
    def _create_text_node(self, vnode: VNode) -> Any:
        """Create text node"""
        text = vnode.props.get('text', '')
        # In real implementation, would create actual DOM text node
        return f"TEXT:{text}"
    
    def _create_element_node(self, vnode: VNode) -> Any:
        """Create element node with children"""
        # In real implementation, would create actual DOM element
        props_str = " ".join(f'{k}="{v}"' for k, v in vnode.props.items() if k != 'children')
        children_html = "".join(self._create_dom_node(child) for child in vnode.children)
        return f"<{vnode.type} {props_str}>{children_html}</{vnode.type}>"
    
    def _create_component_node(self, vnode: VNode) -> Any:
        """Create component node"""
        # Check cache first
        cache_key = str(vnode.type) + str(vnode.props)
        if cache_key in self.component_cache:
            return self.component_cache[cache_key]
        
        # Render component
        component_html = f"COMPONENT:{vnode.type}"
        
        # Cache result
        self.component_cache[cache_key] = component_html
        return component_html
    
    def _create_fragment_node(self, vnode: VNode) -> Any:
        """Create fragment node"""
        children_html = "".join(self._create_dom_node(child) for child in vnode.children)
        return f"FRAGMENT:{children_html}"
    
    def _apply_patch(self, patch: Patch, container: Any = None):
        """Apply a single patch to real DOM"""
        if patch.type == PatchType.CREATE:
            self._apply_create_patch(patch, container)
        elif patch.type == PatchType.REMOVE:
            self._apply_remove_patch(patch, container)
        elif patch.type == PatchType.REPLACE:
            self._apply_replace_patch(patch, container)
        elif patch.type == PatchType.UPDATE_PROPS:
            self._apply_update_props_patch(patch, container)
        elif patch.type == PatchType.UPDATE_TEXT:
            self._apply_update_text_patch(patch, container)
        elif patch.type == PatchType.UPDATE_COMPONENT:
            self._apply_update_component_patch(patch, container)
        elif patch.type == PatchType.MOVE:
            self._apply_move_patch(patch, container)
    
    def _apply_create_patch(self, patch: Patch, container: Any = None):
        """Apply create patch"""
        dom_node = self._create_dom_node(patch.new_vnode)
        # In real implementation, would append to container
        pass
    
    def _apply_remove_patch(self, patch: Patch, container: Any = None):
        """Apply remove patch"""
        # In real implementation, would remove from container
        pass
    
    def _apply_replace_patch(self, patch: Patch, container: Any = None):
        """Apply replace patch"""
        new_dom_node = self._create_dom_node(patch.new_vnode)
        # In real implementation, would replace old node
        pass
    
    def _apply_update_props_patch(self, patch: Patch, container: Any = None):
        """Apply props update patch"""
        # In real implementation, would update element attributes
        pass
    
    def _apply_update_text_patch(self, patch: Patch, container: Any = None):
        """Apply text update patch"""
        # In real implementation, would update text content
        pass
    
    def _apply_update_component_patch(self, patch: Patch, container: Any = None):
        """Apply component update patch"""
        # In real implementation, would re-render component
        pass
    
    def _apply_move_patch(self, patch: Patch, container: Any = None):
        """Apply move patch"""
        # In real implementation, would move element
        pass
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return {
            'render_count': self.render_count,
            'last_render_time': self.last_render_time,
            'component_cache_size': len(self.component_cache),
            'node_cache_size': len(self.node_cache)
        }


class VDOMScheduler:
    """Virtual DOM Scheduler for optimized rendering"""
    
    def __init__(self):
        self.render_queue = []
        self.is_rendering = False
        self.batch_size = 50  # Number of patches to apply per frame
        self.target_fps = 60
        self.frame_time = 1000 / self.target_fps
    
    def schedule_render(self, patches: List[Patch], renderer: VDOMRenderer, container: Any = None):
        """Schedule rendering with performance optimization"""
        self.render_queue.append({
            'patches': patches,
            'renderer': renderer,
            'container': container,
            'timestamp': time.time()
        })
        
        if not self.is_rendering:
            self._process_render_queue()
    
    def _process_render_queue(self):
        """Process render queue with frame budgeting"""
        self.is_rendering = True
        
        while self.render_queue:
            start_time = time.time()
            
            # Process one render job
            job = self.render_queue.pop(0)
            patches = job['patches']
            renderer = job['renderer']
            container = job['container']
            
            # Apply patches in batches
            for i in range(0, len(patches), self.batch_size):
                batch = patches[i:i + self.batch_size]
                renderer.patch(batch, container)
                
                # Check if we've exceeded frame budget
                if time.time() - start_time > self.frame_time:
                    # Schedule next frame
                    import threading
                    threading.Timer(0.016, self._process_render_queue).start()  # ~60fps
                    return
            
            # Small delay to prevent blocking
            time.sleep(0.001)
        
        self.is_rendering = False


# Global Virtual DOM instances
_vdom_renderer = VDOMRenderer()
_vdom_scheduler = VDOMScheduler()


def create_vnode(type: Union[str, VDOMNodeType], props: Dict[str, Any] = None, children: List[VNode] = None, key: str = None) -> VNode:
    """Create a virtual DOM node"""
    return VNode(
        type=type,
        props=props or {},
        children=children or [],
        key=key
    )


def create_element(tag: str, props: Dict[str, Any] = None, *children) -> VNode:
    """Create element vnode (React.createElement equivalent)"""
    # Flatten children
    flat_children = []
    for child in children:
        if isinstance(child, list):
            flat_children.extend(child)
        else:
            flat_children.append(child)
    
    # Convert children to vnodes if needed
    vnode_children = []
    for child in flat_children:
        if isinstance(child, VNode):
            vnode_children.append(child)
        elif isinstance(child, str):
            vnode_children.append(create_vnode(VDOMNodeType.TEXT, {'text': child}))
        else:
            vnode_children.append(create_vnode(VDOMNodeType.TEXT, {'text': str(child)}))
    
    return create_vnode(tag, props, vnode_children)


def render(vnode: VNode, container: Any = None) -> Any:
    """Render vnode to container"""
    return _vdom_renderer.render(vnode, container)


def update(old_vnode: VNode, new_vnode: VNode, container: Any = None) -> float:
    """Update DOM with new vnode"""
    patches = VDOMDiff.diff(old_vnode, new_vnode)
    return _vdom_scheduler.schedule_render(patches, _vdom_renderer, container)


def get_vdom_metrics() -> Dict[str, Any]:
    """Get Virtual DOM performance metrics"""
    return _vdom_renderer.get_performance_metrics()


# Export Virtual DOM components
__all__ = [
    'VNode', 'VDOMNodeType', 'VDOMDiff', 'Patch', 'PatchType',
    'VDOMRenderer', 'VDOMScheduler', 'create_vnode', 'create_element',
    'render', 'update', 'get_vdom_metrics'
]
