# querypool

Execution pool with caching and early return for python.

Query pools let a query run in the background when it doesn't return
within a given timeout. In that case the result of the previous query
is returned or raised. If there is no result, the default value is returned.

```python
import requests
from querypool.pools import CooperativeQueryPool

pool = CooperativeQueryPool(timeout=0.001)
url = "https://jsonplaceholder.typicode.com/photos"

# Returns None because the query times out.
response = pool.execute(requests.get, args=(url,), default=None)
assert response is None

# Increase the timeout to let the query finish.
# The same function with the same arguments is still running so
# all this does is wait for the result of the previous call.
response = pool.execute(requests.get, args=(url,), default=None, timeout=3)
response.raise_for_status()

# Returns the previous result because the query times out.
response = pool.execute(requests.get, args=(url,), default=None)
response.raise_for_status()
```

## Documentation

https://querypool.readthedocs.io/
