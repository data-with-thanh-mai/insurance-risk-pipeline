import os
import pandas as pd
import logging

class LocalFileLoader:
    """Class phụ trách xuất dữ liệu sạch ra thư mục local."""
    def __init__(self, output_dir="data/clean_data"):
        self.output_dir = output_dir
        self.logger = logging.getLogger(self.__class__.__name__)
        # Tự động tạo thư mục nếu chưa có
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def load_to_csv(self, df, filename):
        """Ghi DataFrame ra file CSV."""
        if df is None or df.empty:
            self.logger.warning("DataFrame trống, không có gì để lưu.")
            return False

        file_path = os.path.join(self.output_dir, filename)
        self.logger.info(f"Đang nạp (Load) {len(df)} dòng dữ liệu vào: {file_path}...")
        df.to_csv(file_path, index=False)
        self.logger.info("Hoàn tất lưu file!")
        return True
