import hdbscan

from backend._5_cluster._clusterer import BaseClusterer
from numpy import ndarray
from typing import Any


def does_support_hdbscan(model: Any) -> bool:
  if isinstance(model, hdbscan.HDBSCAN):
    return True

  model_type: str = str(type(model)).lower()
  if "cuml" in model_type and "hdbscan" in model_type:
    return True

  return False
