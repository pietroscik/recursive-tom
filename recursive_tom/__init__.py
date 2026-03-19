"""
Core package per il benchmark Recursive-ToM.

Espone componenti principali:
- Motore logico di stati mentali (`engine`).
- Generatori di scenari sociali e di interrogatorio (`scenarios`).
- Strumenti di teoria dei giochi (`game_theory`).
- Sistema di valutazione a consiglio di pari (`evaluation`).
"""

from .engine import Agent, RecursiveToMEngine

__all__ = ["Agent", "RecursiveToMEngine"]

