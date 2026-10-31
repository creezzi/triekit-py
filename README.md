# triekit

A prefix tree for fast autocomplete, prefix counting and deletion.

## Usage

```python
from triekit import Trie

t = Trie(["car", "card", "care", "dog"])
t.complete("car")  # -> ["car", "card", "care"]
```

## Test

```bash
pip install pytest && pytest
```

## License

MIT
