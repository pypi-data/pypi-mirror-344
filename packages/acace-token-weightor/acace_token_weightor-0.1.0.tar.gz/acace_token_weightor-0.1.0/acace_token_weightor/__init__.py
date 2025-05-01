"""
ACACE Token Weightor: Assigns semantic weights to tokens.

This module provides functionality to assess the importance of tokens
by assigning them weights based on various semantic criteria.
"""

from .weightor import TokenWeightor, assign_weights

__all__ = ["TokenWeightor", "assign_weights"]
__version__ = "0.1.0"
