from triekit import Trie


def test_add_contains_len():
    t = Trie(["car", "card"])
    assert "car" in t and "card" in t and "ca" not in t
    assert len(t) == 2
    assert t.add("car") is False and len(t) == 2


def test_complete_is_sorted_and_limited():
    t = Trie(["care", "car", "card", "dog"])
    assert t.complete("car") == ["car", "card", "care"]
    assert t.complete("car", limit=2) == ["car", "card"]
    assert t.complete("x") == []
    assert t.complete("") == ["car", "card", "care", "dog"]


def test_count_prefix():
    t = Trie(["a", "ab", "abc", "b"])
    assert t.count_prefix("a") == 3
    assert t.count_prefix("abc") == 1
    assert t.count_prefix("z") == 0


def test_remove_keeps_other_words():
    t = Trie(["car", "card"])
    assert t.remove("card") and "car" in t and "card" not in t
    assert t.complete("car") == ["car"]
    assert t.remove("card") is False
    assert len(t) == 1


def test_remove_prefix_word_keeps_longer_word():
    t = Trie(["car", "card"])
    t.remove("car")
    assert "car" not in t and "card" in t


def test_unicode_and_empty_word():
    t = Trie(["café", ""])
    assert "café" in t and "" in t
