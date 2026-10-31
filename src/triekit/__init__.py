"""Prefix tree with autocomplete."""
from __future__ import annotations

from typing import Dict, Iterable, Iterator, List, Optional

__all__ = ["Trie"]


class _Node:
    __slots__ = ("children", "terminal", "count")

    def __init__(self) -> None:
        self.children: Dict[str, "_Node"] = {}
        self.terminal = False
        self.count = 0  # number of stored words passing through this node


class Trie:
    def __init__(self, words: Iterable[str] = ()):
        self._root = _Node()
        self._size = 0
        for word in words:
            self.add(word)

    def __len__(self) -> int:
        return self._size

    def _find(self, prefix: str) -> Optional[_Node]:
        node = self._root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def add(self, word: str) -> bool:
        """Insert `word`; returns False if it was already present."""
        if word in self:
            return False
        node = self._root
        node.count += 1
        for ch in word:
            node = node.children.setdefault(ch, _Node())
            node.count += 1
        node.terminal = True
        self._size += 1
        return True

    def __contains__(self, word: object) -> bool:
        node = self._find(word) if isinstance(word, str) else None
        return bool(node and node.terminal)

    def remove(self, word: str) -> bool:
        if word not in self:
            return False
        node = self._root
        node.count -= 1
        path = []
        for ch in word:
            path.append((node, ch))
            node = node.children[ch]
            node.count -= 1
        node.terminal = False
        for parent, ch in reversed(path):  # prune branches that no longer lead anywhere
            if parent.children[ch].count == 0:
                del parent.children[ch]
        self._size -= 1
        return True

    def count_prefix(self, prefix: str) -> int:
        node = self._find(prefix)
        return node.count if node else 0

    def complete(self, prefix: str, limit: Optional[int] = None) -> List[str]:
        """Words starting with `prefix`, in alphabetical order."""
        node = self._find(prefix)
        if node is None:
            return []
        out: List[str] = []
        for word in self._walk(node, prefix):
            out.append(word)
            if limit is not None and len(out) >= limit:
                break
        return out

    def _walk(self, node: _Node, path: str) -> Iterator[str]:
        if node.terminal:
            yield path
        for ch in sorted(node.children):
            yield from self._walk(node.children[ch], path + ch)
