"""
Built-in NextPy Plugins
Commonly used plugins for JSX processing
"""

import re
from typing import List, Dict, Any
from pathlib import Path

from .base import JSXPlugin, PluginContext, PluginResult, PluginPriority


class TailwindPlugin(JSXPlugin):
    """Plugin for Tailwind CSS class optimization"""
    
    def __init__(self):
        super().__init__("tailwind", "1.0.0")
        self.priority = PluginPriority.HIGH
        
    def transform(self, context: PluginContext) -> PluginResult:
        """Optimize Tailwind CSS classes"""
        content = context.file_content
        errors = []
        warnings = []
        metadata = {}
        
        try:
            # Extract and optimize Tailwind classes
            optimized_content = self._optimize_tailwind_classes(content)
            
            # Collect statistics
            metadata.update({
                "classes_optimized": self._count_optimizations(content, optimized_content),
                "classes_removed": self._count_removed_classes(content, optimized_content)
            })
            
            return PluginResult(
                success=True,
                content=optimized_content,
                metadata=metadata,
                errors=errors,
                warnings=warnings
            )
            
        except Exception as e:
            errors.append(f"Tailwind optimization failed: {str(e)}")
            return PluginResult(
                success=False,
                content=content,
                metadata=metadata,
                errors=errors,
                warnings=warnings
            )
    
    def _optimize_tailwind_classes(self, content: str) -> str:
        """Optimize Tailwind CSS classes"""
        # Handle both className and class attributes
        class_pattern = r'(className|class)="([^"]+)"'
        
        def optimize_classes(match):
            attr_name = match.group(1)  # className or class
            classes = match.group(2).split()
            # Remove duplicates while preserving order
            seen = set()
            unique_classes = []
            for cls in classes:
                if cls not in seen:
                    seen.add(cls)
                    unique_classes.append(cls)
            return f'{attr_name}="{" ".join(unique_classes)}"'
        
        return re.sub(class_pattern, optimize_classes, content)
    
    def _count_optimizations(self, original: str, optimized: str) -> int:
        """Count how many optimizations were made"""
        original_classes = len(re.findall(r'\b\w+\b', original))
        optimized_classes = len(re.findall(r'\b\w+\b', optimized))
        return max(0, original_classes - optimized_classes)
    
    def _count_removed_classes(self, original: str, optimized: str) -> int:
        """Count removed duplicate classes"""
        return self._count_optimizations(original, optimized)


class TypeScriptPlugin(JSXPlugin):
    """Plugin for TypeScript-like type checking in JSX"""
    
    def __init__(self):
        super().__init__("typescript", "1.0.0")
        self.priority = PluginPriority.NORMAL
        
    def transform(self, context: PluginContext) -> PluginResult:
        """Add TypeScript-like type checking"""
        content = context.file_content
        errors = []
        warnings = []
        metadata = {}
        
        try:
            # Add type annotations where missing
            typed_content = self._add_type_annotations(content)
            
            # Check for common type issues
            type_issues = self._check_type_issues(typed_content)
            warnings.extend(type_issues)
            
            metadata.update({
                "annotations_added": self._count_annotations(content, typed_content),
                "type_issues_found": len(type_issues)
            })
            
            return PluginResult(
                success=True,
                content=typed_content,
                metadata=metadata,
                errors=errors,
                warnings=warnings
            )
            
        except Exception as e:
            errors.append(f"TypeScript processing failed: {str(e)}")
            return PluginResult(
                success=False,
                content=content,
                metadata=metadata,
                errors=errors,
                warnings=warnings
            )
    
    def _add_type_annotations(self, content: str) -> str:
        """Add type annotations to function parameters"""
        # Add type annotations to function definitions
        lines = content.split('\n')
        typed_lines = []
        
        for line in lines:
            # Look for function definitions without type annotations
            if 'def ' in line and '(' in line and ')' in line:
                if '->' not in line and ':' not in line.split('(')[1].split(')')[0]:
                    # Add basic type annotation
                    typed_line = line.replace('def ', 'def -> None: ')
                    typed_lines.append(typed_line)
                else:
                    typed_lines.append(line)
            else:
                typed_lines.append(line)
        
        return '\n'.join(typed_lines)
    
    def _check_type_issues(self, content: str) -> List[str]:
        """Check for common type issues"""
        issues = []
        
        # Check for undefined props usage
        if 'props.get(' in content and 'props.get(' not in content:
            issues.append("Consider using props.get() for safer prop access")
        
        # Check for missing return types
        if 'def ' in content and 'return ' in content and '->' not in content:
            issues.append("Consider adding return type annotations")
        
        return issues
    
    def _count_annotations(self, original: str, typed: str) -> int:
        """Count added type annotations"""
        return typed.count('->') - original.count('->')


class StylePlugin(JSXPlugin):
    """Plugin for CSS-in-JS style processing"""
    
    def __init__(self):
        super().__init__("style", "1.0.0")
        self.priority = PluginPriority.NORMAL
        
    def transform(self, context: PluginContext) -> PluginResult:
        """Process CSS-in-JS styles"""
        content = context.file_content
        errors = []
        warnings = []
        metadata = {}
        
        try:
            # Convert style objects to CSS strings
            styled_content = self._process_style_objects(content)
            
            metadata.update({
                "styles_processed": self._count_style_objects(content)
            })
            
            return PluginResult(
                success=True,
                content=styled_content,
                metadata=metadata,
                errors=errors,
                warnings=warnings
            )
            
        except Exception as e:
            errors.append(f"Style processing failed: {str(e)}")
            return PluginResult(
                success=False,
                content=content,
                metadata=metadata,
                errors=errors,
                warnings=warnings
            )
    
    def _process_style_objects(self, content: str) -> str:
        """Convert style objects to CSS strings"""
        # Simple style object to CSS conversion
        style_pattern = r'style=\{([^}]+)\}'
        
        def convert_style(match):
            style_obj = match.group(1)
            # Convert Python dict syntax to CSS
            css_style = style_obj.replace("'", '').replace('"', '')
            css_style = css_style.replace(': ', ':').replace(', ', '; ')
            return f'style="{css_style}"'
        
        return re.sub(style_pattern, convert_style, content)
    
    def _count_style_objects(self, content: str) -> int:
        """Count style objects in content"""
        return len(re.findall(r'style=\{', content))


class ComponentPlugin(JSXPlugin):
    """Plugin for component validation and enhancement"""
    
    def __init__(self):
        super().__init__("component", "1.0.0")
        self.priority = PluginPriority.HIGH
        
    def transform(self, context: PluginContext) -> PluginResult:
        """Validate and enhance components"""
        content = context.file_content
        errors = []
        warnings = []
        metadata = {}
        
        try:
            # Validate component structure
            validation_result = self._validate_component(content)
            errors.extend(validation_result["errors"])
            warnings.extend(validation_result["warnings"])
            
            # Add component enhancements
            enhanced_content = self._enhance_component(content)
            
            metadata.update({
                "component_validated": True,
                "enhancements_added": self._count_enhancements(content, enhanced_content)
            })
            
            return PluginResult(
                success=len(errors) == 0,
                content=enhanced_content,
                metadata=metadata,
                errors=errors,
                warnings=warnings
            )
            
        except Exception as e:
            errors.append(f"Component validation failed: {str(e)}")
            return PluginResult(
                success=False,
                content=content,
                metadata=metadata,
                errors=errors,
                warnings=warnings
            )
    
    def _validate_component(self, content: str) -> Dict[str, List[str]]:
        """Validate component structure"""
        errors = []
        warnings = []
        
        # Check for required default export
        if 'default = ' not in content:
            errors.append("Component must have a default export")
        
        # Check for proper function definition
        if 'def ' not in content:
            errors.append("Component must define a function")
        
        # Check for JSX return
        if 'return (' not in content and 'return <' not in content:
            warnings.append("Component should return JSX")
        
        return {"errors": errors, "warnings": warnings}
    
    def _enhance_component(self, content: str) -> str:
        """Add component enhancements"""
        # Add docstring if missing
        if '"""' not in content and "'''" not in content:
            lines = content.split('\n')
            enhanced_lines = []
            
            for i, line in enumerate(lines):
                if line.strip().startswith('def '):
                    enhanced_lines.append(line)
                    enhanced_lines.append('    """Enhanced component"""')
                else:
                    enhanced_lines.append(line)
            
            return '\n'.join(enhanced_lines)
        
        return content
    
    def _count_enhancements(self, original: str, enhanced: str) -> int:
        """Count added enhancements"""
        return enhanced.count('"""') - original.count('"""')


class ValidationPlugin(JSXPlugin):
    """Plugin for JSX syntax validation"""
    
    def __init__(self):
        super().__init__("validation", "1.0.0")
        self.priority = PluginPriority.HIGHEST
        
    def transform(self, context: PluginContext) -> PluginResult:
        """Validate JSX syntax"""
        content = context.file_content
        errors = []
        warnings = []
        metadata = {}
        
        try:
            # Validate JSX syntax
            validation_result = self._validate_jsx_syntax(content)
            errors.extend(validation_result["errors"])
            warnings.extend(validation_result["warnings"])
            
            metadata.update({
                "syntax_valid": len(errors) == 0,
                "tags_validated": validation_result["tags_count"],
                "attributes_validated": validation_result["attributes_count"]
            })
            
            return PluginResult(
                success=len(errors) == 0,
                content=content,
                metadata=metadata,
                errors=errors,
                warnings=warnings
            )
            
        except Exception as e:
            errors.append(f"JSX validation failed: {str(e)}")
            return PluginResult(
                success=False,
                content=content,
                metadata=metadata,
                errors=errors,
                warnings=warnings
            )
    
    def _validate_jsx_syntax(self, content: str) -> Dict[str, Any]:
        """Validate JSX syntax"""
        errors = []
        warnings = []
        tags_count = 0
        attributes_count = 0
        
        # Check for unclosed tags
        open_tags = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Find JSX tags
            tag_matches = re.finditer(r'<[^>]+>', line)
            
            for match in tag_matches:
                tag = match.group()
                tags_count += 1
                
                if tag.startswith('</'):
                    # Closing tag
                    if not open_tags:
                        errors.append(f"Line {line_num}: Unexpected closing tag {tag}")
                    else:
                        expected_tag = open_tags.pop()
                        if expected_tag != tag[2:]:
                            errors.append(f"Line {line_num}: Mismatched closing tag. Expected {expected_tag}, got {tag}")
                elif tag.endswith('/>'):
                    # Self-closing tag
                    pass
                else:
                    # Opening tag
                    tag_name = re.match(r'<(\w+)', tag)
                    if tag_name:
                        open_tags.append(f"</{tag_name.group(1)}>")
                
                # Count attributes
                attrs = re.findall(r'\w+="[^"]*"', tag)
                attributes_count += len(attrs)
        
        # Check for unclosed tags
        for unclosed_tag in open_tags:
            errors.append(f"Unclosed tag: {unclosed_tag}")
        
        # Check for common issues
        if 'className=' in content and 'class=' in content:
            warnings.append("Mixed className and class attributes found")
        
        return {
            "errors": errors,
            "warnings": warnings,
            "tags_count": tags_count,
            "attributes_count": attributes_count
        }
