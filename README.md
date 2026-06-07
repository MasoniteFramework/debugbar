# ⚠️ This repository is no longer maintained

> **Masonite Debugbar development continues at [masonitedev/debugbar](https://github.com/masonitedev/debugbar)** as part of Masonite 5 (a new PyPI package name is coming soon).
> This repository covers `masonite-debugbar` ≤ 1.0.1, which will receive **no further updates** (including security fixes).
>
> - 📖 Masonite documentation: <https://docs.masonite.dev/official-packages/masonite-debugbar/>
>
> ❤️ In memory of [Joseph "Joe" Mancuso](https://github.com/josephmancuso), creator of Masonite.

---

# Masonite Debugbar

A Masonite Python Debugging Tool

<img width="1792" alt="Screen Shot 2022-01-17 at 6 53 40 PM" src="https://user-images.githubusercontent.com/20172538/149849594-f6d13c0a-51c5-4d10-91cc-c2cbddc98741.png">

# Install

First pip install:

```
$ pip install masonite-debugbar
```

Then add the debugbar provider to your providers list **LAST** (as the last provider in the list):

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



