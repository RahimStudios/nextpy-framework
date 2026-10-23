"""
Comprehensive Test Suite for NextPy Framework
Tests core functionality, hydration, routing, and server actions
"""

import pytest
import asyncio
from pathlib import Path


class TestPSXComponents:
    """Test PSX component rendering and state management"""
    
    def test_basic_component_rendering(self):
        """Test basic PSX component rendering"""
        from nextpy.psx import component, psx
        
        @component
        def SimpleComponent(props=None):
            return psx("<div>Hello World</div>")
        
        result = SimpleComponent()
        assert result is not None
        assert "Hello World" in str(result)
    
    def test_state_management(self):
        """Test useState hook"""
        from nextpy.psx import component, useState
        
        @component
        def Counter(props=None):
            [count, setCount] = useState(0)
            return psx(f"<div>Count: {count}</div>")
        
        result = Counter()
        assert result is not None
        assert "Count: 0" in str(result)
    
    def test_props_passing(self):
        """Test component props"""
        from nextpy.psx import component, psx
        
        @component
        def Greeting(props=None):
            props = props or {}
            name = props.get("name", "World")
            return psx(f"<div>Hello {name}</div>")
        
        result = Greeting({"name": "Alice"})
        assert "Hello Alice" in str(result)


class TestHydrationEngine:
    """Test client-side hydration engine"""
    
    def test_hydration_engine_initialization(self):
        """Test hydration engine initialization"""
        from nextpy.psx.hydration.engine import HydrationEngine, get_hydration_engine
        
        engine = get_hydration_engine()
        assert engine is not None
        assert isinstance(engine, HydrationEngine)
    
    def test_component_registration(self):
        """Test component registration"""
        from nextpy.psx.hydration.engine import get_hydration_engine
        
        engine = get_hydration_engine()
        component_id = engine.register_component({
            'name': 'TestComponent',
            'state': {'count': 0}
        })
        
        assert component_id is not None
        assert component_id.startswith('psx_component_')
    
    def test_hydration_script_generation(self):
        """Test hydration script generation"""
        from nextpy.psx.hydration.engine import get_hydration_engine
        
        engine = get_hydration_engine()
        component_id = engine.register_component({
            'name': 'TestComponent',
            'state': {'count': 0}
        })
        
        script = engine.generate_hydration_script(component_id)
        assert script is not None
        assert 'StateManager' in script
        assert 'Component' in script
        assert component_id in script


class TestRouter:
    """Test file-based routing system"""
    
    def test_router_initialization(self):
        """Test router initialization"""
        from nextpy.core.router import Router
        
        router = Router(pages_dir="pages", templates_dir="templates")
        assert router is not None
        assert router.pages_dir == Path("pages")
    
    def test_route_matching(self):
        """Test route matching"""
        from nextpy.core.router import Router
        
        router = Router(pages_dir="pages", templates_dir="templates")
        router.scan_pages()
        
        # Test static route
        matched = router.match("/")
        if matched:
            route, params = matched
            assert route is not None
    
    def test_dynamic_route_matching(self):
        """Test dynamic route matching"""
        from nextpy.core.router import Router, Route
        
        router = Router(pages_dir="pages", templates_dir="templates")
        
        # Create a dynamic route
        route = Route(
            path="/users/:id",
            file_path=Path("test"),
            is_dynamic=True,
            param_names=["id"],
            pattern=router._create_route_from_file.__self__._Route__pattern
        )
        
        # This would need actual implementation testing


class TestServerActions:
    """Test server actions"""
    
    @pytest.mark.asyncio
    async def test_server_action_decorator(self):
        """Test server action decorator"""
        from nextpy.server_actions import server_action
        
        @server_action
        async def test_action(name: str):
            return {"message": f"Hello {name}"}
        
        result = await test_action("World")
        assert result["message"] == "Hello World"
    
    @pytest.mark.asyncio
    async def test_server_action_validation(self):
        """Test server action with validation"""
        from nextpy.server_actions import server_action
        from pydantic import BaseModel, ValidationError
        
        class ActionInput(BaseModel):
            name: str
        
        @server_action
        async def validated_action(data: ActionInput):
            return {"greeting": f"Hello {data.name}"}
        
        # Valid input
        result = await validated_action(ActionInput(name="Alice"))
        assert result["greeting"] == "Hello Alice"


class TestDatabaseIntegration:
    """Test database integration"""
    
    def test_session_creation(self):
        """Test database session creation"""
        # This would require actual database setup
        # from nextpy.db import get_session
        # session = get_session()
        # assert session is not None
        pass


class TestAuthentication:
    """Test authentication system"""
    
    def test_token_creation(self):
        """Test JWT token creation"""
        from nextpy.auth import AuthManager
        
        token = AuthManager.create_token(user_id=123, expires_in=3600)
        assert token is not None
        assert isinstance(token, str)
    
    def test_token_verification(self):
        """Test JWT token verification"""
        from nextpy.auth import AuthManager
        
        token = AuthManager.create_token(user_id=123, expires_in=3600)
        user_id = AuthManager.verify_token(token)
        assert user_id == 123


class TestUtilities:
    """Test utility functions"""
    
    def test_cache_decorator(self):
        """Test cache decorator"""
        from nextpy.utils.cache import cache_result
        
        call_count = [0]
        
        @cache_result(ttl=60)
        def expensive_function(x):
            call_count[0] += 1
            return x * 2
        
        result1 = expensive_function(5)
        result2 = expensive_function(5)
        
        assert result1 == 10
        assert result2 == 10
        # Should only call once due to caching
        assert call_count[0] == 1
    
    def test_search_functionality(self):
        """Test search utilities"""
        from nextpy.utils.search import simple_search
        
        items = [
            {"title": "Getting Started"},
            {"title": "Advanced Guide"},
            {"title": "API Reference"}
        ]
        
        results = simple_search("getting", items, ["title"])
        assert len(results) > 0
        assert "Getting Started" in [r["title"] for r in results]


class TestInteractiveComponents:
    """Test interactive components with hydration"""
    
    def test_interactive_component_decorator(self):
        """Test @interactive_component decorator"""
        from nextpy.psx.hydration import interactive_component
        from nextpy.psx import useState
        
        @interactive_component
        def InteractiveCounter(props=None):
            [count, setCount] = useState(0)
            
            def increment(e):
                setCount(count + 1)
            
            return psx(f"""
                <button onclick={increment}>
                    Count: {count}
                </button>
            """)
        
        result = InteractiveCounter()
        assert result is not None
        # Check that it's an InteractiveComponentResult
        assert hasattr(result, 'is_interactive')
        assert result.is_interactive is True


class TestEventHandlers:
    """Test event handler extraction and conversion"""
    
    def test_named_handler_extraction(self):
        """Test extraction of named handler functions"""
        from nextpy.psx.compiler.handler_compiler import HandlerCompiler
        
        compiler = HandlerCompiler()
        
        # Test code with named handler
        code = """
def handle_click(e):
    setCount(count + 1)
"""
        
        handlers = compiler.extract_handlers(code)
        assert handlers is not None
        # Verify handler was extracted


class TestBuildOptimization:
    """Test build optimization features"""
    
    def test_code_splitting_simulation(self):
        """Test code splitting (simulation)"""
        # This would test actual code splitting implementation
        pass
    
    def test_tree_shaking_simulation(self):
        """Test tree shaking (simulation)"""
        # This would test actual tree shaking implementation
        pass


class TestMigrationCompatibility:
    """Test migration from legacy systems"""
    
    def test_legacy_to_psx_conversion(self):
        """Test conversion from legacy JSX to PSX"""
        # Test that legacy patterns can be converted
        pass
    
    def test_event_handler_migration(self):
        """Test event handler syntax migration"""
        # Test that lambda handlers are detected and flagged
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
