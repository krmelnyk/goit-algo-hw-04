import argparse
import shutil
from pathlib import Path


def get_unique_target_path(target_path: Path) -> Path:
    """
    Return a non-existing target path
    by adding a numeric suffix if needed.
    """
    if not target_path.exists():
        return target_path

    counter = 1
    while True:
        candidate = target_path.with_name(
            f"{target_path.stem}_{counter}{target_path.suffix}"
        )
        if not candidate.exists():
            return candidate
        counter += 1


def copy_and_sort_files(source: Path, destination: Path) -> None:
    """
    Recursively traverse the source directory,
    copy files to the destination, sorting them
    by subdirectories based on their extensions.
    """
    try:
        for item in source.iterdir():
            if item.resolve() == destination.resolve():
                continue

            if item.is_dir():
                copy_and_sort_files(item, destination)

            elif item.is_file():
                extension = item.suffix[1:] if item.suffix else "no_extension"
                target_dir = destination / extension
                target_dir.mkdir(parents=True, exist_ok=True)

                target_path = get_unique_target_path(target_dir / item.name)
                shutil.copy2(item, target_path)

    except OSError as e:
        print(f"An error occurred: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Recursive file sorter")
    parser.add_argument("source", help="Path to source directory")
    parser.add_argument(
        "destination",
        nargs="?",
        default="dist",
        help="Path to destination directory (default: dist)",
    )

    args = parser.parse_args()

    source_path = Path(args.source)
    destination_path = Path(args.destination)

    if not source_path.is_dir():
        print("Source directory does not exist or is not a directory.")
        return

    try:
        destination_path.mkdir(parents=True, exist_ok=True)
        copy_and_sort_files(source_path, destination_path)
    except OSError as e:
        print(f"An error occurred: {e}")
        return

    print("Files sorted successfully.")


if __name__ == "__main__":
    main()
