# backend/app/models/node.py

from dataclasses import dataclass, field

@dataclass(order=True, frozen=True)
class Node:
  id: int
  parent_id: int = field(default=-1)
  topic: str = field(default="")
  content: str = field(default="")
