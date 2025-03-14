#!/usr/bin/env python3
"""
Script to fix imports in generated protobuf files.
Converts absolute imports to relative imports.
"""
import os
import re

# Directory containing generated protobuf files
PROTO_DIR = "protobufs/meshtastic"


def fix_imports(file_path):
    """Fix imports in a single protobuf file"""
    with open(file_path, "r") as f:
        content = f.read()

    # Replace absolute imports with relative imports
    # from meshtastic import xyz_pb2 -> from . import xyz_pb2
    fixed_content = re.sub(
        r"from meshtastic import (\w+_pb2)", r"from . import \1", content
    )

    with open(file_path, "w") as f:
        f.write(fixed_content)

    print(f"Fixed imports in {file_path}")


def main():
    # Find all pb2.py files
    for root, _, files in os.walk(PROTO_DIR):
        for file in files:
            if file.endswith("_pb2.py"):
                file_path = os.path.join(root, file)
                fix_imports(file_path)


if __name__ == "__main__":
    main()
