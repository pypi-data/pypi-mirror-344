import sys
from pathlib import Path

# Add the parent directory to the Python module search path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tools.github import GitHub, GIToolError

if __name__ == "__main__":
    try:
        github = GitHub()
        github.create_asset()
    except GIToolError:
        print("Exiting")
        exit(1)
