import argparse
import logging
import os

from utils.common import SystemLogger
from config.etl_config import *
from config.ml_config import ML_CONFIG

from etl_pipeline.transform import DataCleaner, FeatureEngineer, DataTransformer
from etl_pipeline.etl_manager import DataPreparationPipeline
from ml_pipeline.ml_manager import AutoMLPipeline

def run_etl(raw_data_path):
    """Kích hoạt luồng ETL"""
    cleaner = DataCleaner(golden_specs=my_golden_specs, range_rules=my_range_rules, cols_to_drop=cols_to_drop,
                          max_drop_ratio=max_drop_ratio, imputation_strategy=imputation_strategy, fuzzy_threshold=fuzzy_threshold)
    engineering = FeatureEngineer()
    transformer = DataTransformer(scaling_strategy=scaling_strategy, outlier_strategies=my_outlier_strategies,
                                  ordinal_mappings=my_ordinal_mappings, nominal_cols=nominal_columns, ignore_cols=ignore_cols)

    etl = DataPreparationPipeline(file_path=raw_data_path, cleaner=cleaner, featuring=engineering, transformer=transformer, target_col='OUTCOME')
    etl.run(test_size=ML_CONFIG['test_size'])

def run_ml():
    """Kích hoạt luồng Machine Learning"""
    train_file = "data/clean_data/final_train_data.csv"
    test_file = "data/clean_data/final_test_data.csv"
    
    if not os.path.exists(train_file) or not os.path.exists(test_file):
        logging.error("Không tìm thấy dữ liệu sạch! Vui lòng chạy luồng ETL trước (--mode etl).")
        return

    automl = AutoMLPipeline(
        train_file=train_file, 
        test_file=test_file, 
        tuning_method=ML_CONFIG['tuning_method'], 
        feature_method=ML_CONFIG['feature_method'], 
        n_features=ML_CONFIG['n_features']
    )
    automl.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="End-to-End Data Pipeline & ML System")
    parser.add_argument("--mode", type=str, choices=["etl", "ml", "all"], default="all",
                        help="Chọn luồng để chạy: 'etl' (Làm sạch), 'ml' (Train Model), 'all' (Chạy toàn bộ)")
    parser.add_argument("--file", type=str, default="data/raw_data.csv", help="Đường dẫn file dữ liệu thô")
    args = parser.parse_args()

    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Chỉ định đường dẫn file log nằm trong thư mục logs
    SystemLogger("logs/automl_run.log")

    if args.mode in ["etl", "all"]:
        run_etl(args.file)
    
    if args.mode in ["ml", "all"]:
        run_ml()
