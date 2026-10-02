from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from cleaner.pipeline import DataCleaningPipeline

def main():
    root = Path(__file__).resolve().parent.parent.parent
    input_file = root / "data" / "raw" / "raw_data.csv"
    output_file = root / "data" / "processed"

    pipeline = DataCleaningPipeline()
    pipeline.run(input_file=input_file, output_file=output_file)

if __name__ == "__main__":
    main()