import csv
import re
from pathlib import Path
from typing import Dict, List, Tuple


def normalize_name(name: str) -> str:
    """
    Normalize an artist name for matching.

    Applied consistently to:
    - Names from noobai-artists.csv
    - Names from artists.txt
    """
    # Trim and lowercase
    normalized = name.strip().lower()
    # Treat underscores and slashes as spaces
    normalized = normalized.replace("_", " ").replace("/", " ")
    # Collapse multiple spaces
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def build_order_map(all_csv_path: Path) -> Dict[str, int]:
    """
    Build a mapping of normalized artist name -> order index
    based on the order they appear in noobai-artists.csv.
    """
    order: Dict[str, int] = {}

    with all_csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)

        # Skip header
        try:
            next(reader)
        except StopIteration:
            return order

        for idx, row in enumerate(reader):
            if not row:
                continue
            artist = row[0]
            key = normalize_name(artist)
            # Only record the first position for each normalized name
            if key and key not in order:
                order[key] = idx

    return order


def sort_artists_txt(all_csv_path: Path, artists_txt_path: Path) -> None:
    """
    Sort artists.txt according to the order defined by noobai-artists.csv.

    - Matching is done on normalized names (lowercased, stripped).
    - Names not appearing in noobai-artists.csv are placed at the end,
      preserving their original relative order.
    """
    order_map = build_order_map(all_csv_path)

    # Read original artists.txt lines
    with artists_txt_path.open(encoding="utf-8") as f:
        original_lines = f.readlines()

    sortable_rows: List[Tuple[int, int, str]] = []

    for original_index, line in enumerate(original_lines):
        # Keep the line as-is (including newline) for output
        name = line.rstrip("\n")
        key = normalize_name(name)

        if key in order_map:
            # Matched artists: group 0, ordered by noobai-artists.csv index
            sort_group = 0
            sort_key = order_map[key]
        else:
            # Unmatched artists: group 1, preserve original order
            sort_group = 1
            sort_key = original_index

        sortable_rows.append((sort_group, sort_key, line))

    # Sort by group, then by key
    sortable_rows.sort(key=lambda t: (t[0], t[1]))

    # Write back to artists.txt
    with artists_txt_path.open("w", encoding="utf-8") as f:
        for _, _, line in sortable_rows:
            f.write(line)


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent

    noobai_artists_csv_path = project_root / "noobai-artists.csv"
    artists_txt_path = project_root / "artists.txt"

    if not noobai_artists_csv_path.exists():
        raise FileNotFoundError(
            f"noobai-artists.csv not found at: {noobai_artists_csv_path}"
        )
    if not artists_txt_path.exists():
        raise FileNotFoundError(f"artists.txt not found at: {artists_txt_path}")

    sort_artists_txt(noobai_artists_csv_path, artists_txt_path)
    print(f"Sorted artists.txt based on order in {noobai_artists_csv_path.name}")


if __name__ == "__main__":
    main()
