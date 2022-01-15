# debugbar
A Python Debugging tool

# Install

First pip install:

```
$ pip install masonite-debugbar
```

Then add the debugbar provider to your providers list:

```python
from debugbar.providers import DebugProvider
PROVIDERS = [
    # ..
    DebugProvider,

]
```

Lastly, publish the provider:

```
$ python craft package:publish debugbar
```

