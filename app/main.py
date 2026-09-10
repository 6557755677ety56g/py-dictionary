from typing import Any, List, Optional, Tuple


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


class Dictionary:

    def __init__(self, capacity: int = 8, load_factor: float = 0.66) -> None:
        self.capacity: int = capacity
        self.load_factor: float = load_factor
        self.size: int = 0
        self.buckets: List[Optional[Tuple[int, Any, Any]]] = [
            None
        ] * self.capacity

    def __setitem__(self, key: Any, value: Any) -> None:
        h = hash(key)
        idx = h % self.capacity

        while True:
            node = self.buckets[idx]
            if node is None:
                self.buckets[idx] = (h, key, value)
                self.size += 1
                if self.size / self.capacity > self.load_factor:
                    self._resize()
                return

            node_hash, node_key, _ = node
            if node_hash == h and node_key == key:
                self.buckets[idx] = (h, key, value)
                return

            idx = (idx + 1) % self.capacity

    def __getitem__(self, key: Any) -> Any:
        h = hash(key)
        idx = h % self.capacity
        attempts = 0
        while attempts < self.capacity:
            node = self.buckets[idx]
            if node is None:
                raise KeyError(key)
            node_hash, node_key, node_val = node
            if node_hash == h and node_key == key:
                return node_val

            idx = (idx + 1) % self.capacity
            attempts += 1

        raise KeyError(key)

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key: Any) -> bool:
        try:
            _ = self[key]
            return True
        except KeyError:
            return False

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        items = [f"{node[1]}: {node[2]}"
                 for node in self.buckets
                 if node is not None]
        return f"Dictionary({{{', '.join(items)}}})"

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_buckets: List[Optional[Tuple[int, Any, Any]]] = [
            None
        ] * new_capacity
        for node in self.buckets:
            if node is None:
                continue
            h, key, value = node
            idx = h % new_capacity
            while new_buckets[idx] is not None:
                idx = (idx + 1) % new_capacity
            new_buckets[idx] = (h, key, value)
        self.capacity = new_capacity
        self.buckets = new_buckets
