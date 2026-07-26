"""
Acquire FATF Regulatory Documents

Sprint:
    Sprint 8 - D2

Downloads the latest FATF regulatory documents into the
local knowledge repository.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow importing from src/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.acquisition.document_acquisition_pipeline import (
    DocumentAcquisitionPipeline,
)


def main() -> None:

    print("=" * 70)
    print("Financial Crime Regulatory Intelligence")
    print("FATF Acquisition")
    print("=" * 70)
    print()

    output_folder = PROJECT_ROOT / "knowledge" / "raw" / "regulations" / "fatf"

    output_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    pipeline = DocumentAcquisitionPipeline()

    result = pipeline.acquire(
        output_directory=output_folder,
    )

    print()
    print("=" * 70)
    print("Acquisition Summary")
    print("=" * 70)

    print(f"Documents discovered : {result.documents_discovered}")
    print(f"Documents downloaded : {result.documents_downloaded}")
    print(f"Documents skipped    : {result.documents_skipped}")
    print(f"Errors               : {len(result.errors)}")

    if result.errors:
        print("\nErrors")
        for error in result.errors:
            print(f" - {error}")

    print("\nCompleted.")


if __name__ == "__main__":
    main()