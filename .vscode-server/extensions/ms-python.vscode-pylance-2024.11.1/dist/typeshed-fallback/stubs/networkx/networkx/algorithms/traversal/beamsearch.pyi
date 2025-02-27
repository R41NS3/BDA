from _typeshed import Incomplete
from collections.abc import Generator

from networkx.utils.backends import _dispatchable

@_dispatchable
def bfs_beam_edges(G, source, value, width: Incomplete | None = None) -> Generator[Incomplete, Incomplete, Incomplete]: ...
