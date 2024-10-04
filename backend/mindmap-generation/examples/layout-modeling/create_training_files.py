# backend/mindmap-generation/examples/layout-modeling/create_training_files.py

# %%
import json
import os

from typing import Dict

# %%
for file in os.listdir("./data/annots_n_relations"):
  if file.endswith(".json"):
    file_path: str = os.path.join("./data/annots_n_relations", file)

    # Open and load the JSON data.
    with open(file_path, "r") as f:
      data: Dict[str, str] = json.load(f)

    # Pretty print the JSON data with indentation and save it back to the file.
    with open(file_path, "w") as f:
      json.dump(data, f, indent=2)

    print(f"Formatted and saved {file_path}")
