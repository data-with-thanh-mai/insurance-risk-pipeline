import logging
from utils.common import DataSplitter
from etl_pipeline.extract import DataLoader
from etl_pipeline.load import LocalFileLoader

class DataPreparationPipeline:
    def __init__(self, file_path, cleaner, featuring, transformer, target_col=None):
        self.file_path = file_path
        self.cleaner = cleaner
        self.featuring = featuring
        self.transformer = transformer
        self.target_col = target_col
        self.loader_output = LocalFileLoader(output_dir="data/clean_data") # Khởi tạo module Load
        self.logger = logging.getLogger(self.__class__.__name__)

    def run(self, test_size=0.2):
        self.logger.info("="*60)
        self.logger.info("[PIPELINE] KHỞI ĐỘNG HỆ THỐNG XỬ LÝ DỮ LIỆU (ETL)")
        self.logger.info("="*60)

        # 1. EXTRACT (Trích xuất)
        loader = DataLoader(self.file_path)
        df = loader.data

        # 2. TRANSFORM (Biến đổi)
        self.logger.info("Đang xử lí (Cleaner + Engineer)...")
        df = self.cleaner.fit_transform(df)
        df_clean = self.featuring.fit_transform(df)

        self.logger.info(f"Đang chia dữ liệu (Split Train/Test) với tỷ lệ Test={test_size}...")
        splitter = DataSplitter(df_clean, self.target_col)
        train_df, test_df = splitter.simple_split(test_size=test_size)

        self.logger.info("Đang chuẩn hóa dữ liệu chống rò rỉ (Transforming)...")
        self.transformer.fit(train_df)
        df_train_final = self.transformer.transform(train_df)
        df_test_final = self.transformer.transform(test_df)

        # 3. LOAD (Nạp dữ liệu)
        self.loader_output.load_to_csv(df_train_final, "final_train_data.csv")
        self.loader_output.load_to_csv(df_test_final, "final_test_data.csv")

        self.logger.info("[PIPELINE] HOÀN TẤT ETL!")
        return df_train_final, df_test_final
