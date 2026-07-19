# Performance Optimization in NextPy

NextPy includes built-in performance optimization utilities.

## Caching

```python
from nextpy.utils.cache import cache_result

@cache_result(ttl=3600)
async def get_user(user_id: int):
    # This result will be cached for 1 hour
    return await fetch_from_db(user_id)
```

## Timing

```python
from nextpy.performance import timeit

@timeit
async def slow_operation():
    # Execution time will be logged
    await asyncio.sleep(1)
```

## Batch Processing

```python
from nextpy.performance import batch_processor

@batch_processor(batch_size=50)
async def process_item(item):
    return item * 2

results = await process_item(list(range(1000)))
```

## Rate Limiting

```python
from nextpy.performance import rate_limiter

async def api_endpoint(request):
    if not rate_limiter.is_allowed(request.client.host):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    # Process request...
```

## Best Practices

- Use SSG for static pages
- Cache frequently accessed data
- Use async/await for I/O operations
- Batch database queries
- Monitor performance with @timeit
- Use pagination for large datasets
