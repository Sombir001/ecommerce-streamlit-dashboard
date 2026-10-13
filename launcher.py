"""
E-Commerce Analytics Dashboard Launcher

Prepares the compressed CSV dataset and launches
the existing Streamlit application.

Run:
    streamlit run launcher.py
"""

from pathlib import Path
import runpy
import sys
import zipfile


PROJECT_DIR = Path(__file__).resolve().parent
ZIP_PATH = PROJECT_DIR / "data.zip"
DATA_DIR = PROJECT_DIR / "data"

REQUIRED_FILES = (
    "fact_sales.csv",
    "dim_customers.csv",
    "dim_products.csv",
    "dim_stores.csv",
    "dim_promotions.csv",
)


def prepare_data() -> None:
    """Extract required CSV files from the GitHub ZIP."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    missing = [
        name
        for name in REQUIRED_FILES
        if not (DATA_DIR / name).is_file()
    ]

    if not missing:
        return

    if not ZIP_PATH.is_file():
        raise FileNotFoundError(
            "data.zip was not found in the project root."
        )

    with zipfile.ZipFile(ZIP_PATH, "r") as archive:
        members = [
            member
            for member in archive.infolist()
            if not member.is_dir()
        ]

        for filename in missing:
            matches = [
                member
                for member in members
                if Path(member.filename).name == filename
            ]

            if len(matches) != 1:
                raise ValueError(
                    f"Expected exactly one {filename} "
                    f"in data.zip, found {len(matches)}."
                )

            member = matches[0]
            destination = DATA_DIR / filename
            temporary = DATA_DIR / (filename + ".tmp")

            try:
                with archive.open(member) as source:
                    with temporary.open("wb") as target:
                        import shutil
                        shutil.copyfileobj(source, target)

                temporary.replace(destination)

            finally:
                if temporary.exists():
                    temporary.unlink()


def main() -> None:
    prepare_data()

    if str(PROJECT_DIR) not in sys.path:
        sys.path.insert(0, str(PROJECT_DIR))

    runpy.run_path(
        str(PROJECT_DIR / "app.py"),
        run_name="__main__",
    )


if __name__ == "__main__":
    main()
