import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from security import generate_password_hash


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python api/tools/generate_password_hash.py <password>")

    print(generate_password_hash(sys.argv[1]))


if __name__ == "__main__":
    main()
