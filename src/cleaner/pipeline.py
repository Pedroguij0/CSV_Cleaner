from pathlib import Path
from .config import PipelineConfig
from cleaner.core.logger import setup_logger
from cleaner.transformator import (
    CurrencyCleaner,
    DateNormalizer,
    Deduplicator,
    MissingValuesHandler,
    StringCleaner
    )
from cleaner.quality import ReportGenerator, DataAuditor
from cleaner.exporter.writer import DataExporter
from cleaner.reader.loader import DataLoader


class DataCleaningPipeline:
    def __init__(self, config: PipelineConfig | None = None):
        self.config = config or PipelineConfig()
        self.logger = setup_logger("Pipeline")

    def run(self, input_file: Path, output_file: Path) -> None:
        self.logger.info(f"Starting the cleaning processing of: {input_file}")
        output_file.mkdir(parents=True, exist_ok=True)
        df = DataLoader.load(input_file)
        initial_count = len(df)
        self.logger.info(f"Initial Records Count:{initial_count}")
        df, duplicates_removed = Deduplicator.deduplicate(df)
        self.logger.info(f"Removed Duplicates: {duplicates_removed}")
        df = StringCleaner.format_email(df, self.config.email_columns)
        df = StringCleaner.format_title(df, self.config.text_columns)
        self.logger.info("Text and Email Columns Standardized")
        df = CurrencyCleaner.to_float(df, self.config.currency_columns)
        self.logger.info("Unity Prices Normalized to Float")
        df = DateNormalizer.to_iso(df,self.config.date_columns)
        self.logger.info("Dates Converted to ISO format")
        df = MissingValuesHandler.apply_logical_defaults(df, self.config.logical_defaults)
        df = MissingValuesHandler.apply_placeholder(df, self.config.placeholder)
        self.logger.info("Missing Values Treateds and Placeholder Applieds")
        anomalies = DataAuditor.run_audit(df)
        md_path = output_file / "AUDIT.md"
        ReportGenerator.generate_markdow(
            md_path, 
            initial_count=initial_count, 
            final_count=len(df),
            duplicates_removed=duplicates_removed, 
            anomalies=anomalies
        )
        # 2. Gera o relatório visual em PDF (.pdf)
        pdf_path = output_file / "AUDIT.pdf"
        ReportGenerator.generate_pdf(
            pdf_path, 
            initial_count=initial_count, 
            final_count=len(df),
            duplicates_removed=duplicates_removed, 
            anomalies=anomalies
        )
        self.logger.info(f"Audit Reports generated in:\n - {md_path}\n - {pdf_path}")
        csv_out, xlsx_out = DataExporter.export(df,output_file)
        self.logger.info(f"Final Archives succesfully exported:\n-CSV:{csv_out}\n-XLSX:{xlsx_out}")
