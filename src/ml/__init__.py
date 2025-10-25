"""
Subpacote de Machine Learning (EDA, perfis e modelos).
"""
from .labeling import PERFIS, FEATURES, assign_label  # reexporta utilidades principais

__all__ = ["labeling", "perfis", "train_models", "eda", "PERFIS", "FEATURES", "assign_label"]
