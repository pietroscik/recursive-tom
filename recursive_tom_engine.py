"""
Compat layer per il motore logico Recursive-ToM.

Espone `RecursiveToMEngine` (e `Agent`) a partire dal package
`recursive_tom.engine`, così che gli script legacy possano continuare a usare:

    from recursive_tom_engine import RecursiveToMEngine
"""

from recursive_tom.engine import RecursiveToMEngine, Agent  # type: ignore[F401]

__all__ = ["RecursiveToMEngine", "Agent"]
