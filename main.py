from pathlib import Path
import shutil




EXTENSION_MAP = {
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",

    ".mp3": "Music",
    ".wav": "Music",

    ".mp4": "Videos",
    ".mkv": "Videos",
    ".avi": "Videos",

    ".pdf": "Documents",
    ".txt": "Documents",
    ".docx": "Documents",

    ".exe": "Applications",

    ".zip": "Archives",
    ".rar": "Archives",

    ".csv": "Spreadsheets",
    ".xlsx": "Spreadsheets"
}




def get_folder():

    folder_input = input("Enter folder path: ").strip()

    if not folder_input:
        print("Error: You did not enter a folder path.")
        return None

    folder = Path(folder_input)

    if not folder.exists():
        print("Error: Folder does not exist.")
        return None

    if not folder.is_dir():
        print("Error: The path is not a folder.")
        return None

    return folder




def determine_category(item):

    extension = item.suffix.lower()

    if extension == "":
        return "Others"

    category = EXTENSION_MAP.get(extension)

    if category is None:
        return "Others"

    return category




def scan_files(folder):

    files_to_move = []
    files_found = 0
    folders_skipped = 0

    for item in folder.iterdir():

        if item.is_dir():
            folders_skipped += 1
            continue

        if item.is_file():

            files_found += 1

            category = determine_category(item)

            category_folder = folder / category

            destination = category_folder / item.name

            counter = 1

            while destination.exists():

                new_name = f"{item.stem}_{counter}{item.suffix}"

                destination = category_folder / new_name

                counter += 1

            files_to_move.append(
                (item, destination, category)
            )

    return files_to_move, files_found, folders_skipped




def show_preview(files_to_move):

    print("\n--- PREVIEW ---")

    for source, destination, category in files_to_move:

        print(f"{source.name} → {destination}")




def move_files(files_to_move):

    files_moved = 0
    errors = 0

    category_counts = {}

    print("\n--- MOVING FILES ---")

    for source, destination, category in files_to_move:

        try:

            destination.parent.mkdir(exist_ok=True)

            shutil.move(source, destination)

            files_moved += 1

            category_counts[category] = (
                category_counts.get(category, 0) + 1
            )

            print(
                f"Moved: {source.name} → {destination.name}"
            )

        except Exception as e:

            errors += 1

            print(f"ERROR: Could not move {source.name}")
            print(f"Reason: {e}")

    return files_moved, errors, category_counts




def show_summary(
    files_found,
    files_moved,
    folders_skipped,
    errors,
    category_counts
):

    print("\n========== SUMMARY ==========")

    print(f"Files found:     {files_found}")
    print(f"Files moved:     {files_moved}")
    print(f"Folders skipped: {folders_skipped}")
    print(f"Errors:          {errors}")

    print("\nFiles by category:")

    for category, count in category_counts.items():

        print(f"{category}: {count}")

    print("=============================")




def main():

    folder = get_folder()

    if folder is None:
        return

    files_to_move, files_found, folders_skipped = scan_files(folder)

    if not files_to_move:

        print("\nNo files need to be organized.")
        return

    show_preview(files_to_move)

    print(f"\nTotal files found: {files_found}")

    choice = input(
        "\nProceed with moving files? (y/n): "
    ).strip().lower()

    if choice != "y":

        print("Operation cancelled. No files were moved.")
        return

    files_moved, errors, category_counts = move_files(
        files_to_move
    )

    show_summary(
        files_found,
        files_moved,
        folders_skipped,
        errors,
        category_counts
    )



if __name__ == "__main__":
    main()