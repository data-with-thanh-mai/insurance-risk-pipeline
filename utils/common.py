import logging
import os
import pandas as pd
from sklearn.model_selection import KFold, train_test_split
class SystemLogger:
    """
    Cấu hình hệ thống log: ghi vào file và in ra màn hình.
    """
    def __init__(self, log_file="training_process.log"):
        """
        Hàm khởi tạo với tên file log.
        Args:
            log_file (str): Tên file log.
        """
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        """
        Hàm thiết lập cấu hình logging.
        """
        # Xóa cấu hình cũ nếu có
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # Định dạng log: [Thời gian] - [Tên Class/Module] - [Level] - Nội dung
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        # Cấu hình logging cơ bản
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'), # Ghi vào file
                logging.StreamHandler()  # In ra màn hình
            ]
        )
class DataSplitter:
    """
    Quản lý việc chia dataframe thành các tập train, tập test băng k_fold_cross_validation
    """
    def __init__(self, dataframe,target_col = None):
        self.dataframe = dataframe
        self.target_col = target_col
        self.logger = logging.getLogger(self.__class__.__name__)

    def kfold_split_data(self, n_splits):
        """
        Chia train/test bằng k_fold_cross_validation

        Args:
        n_splits: số lượng fold

        Returns:
        folds_indices: Một danh sách các tuple, mỗi tuple chứa:
              (train_index, test_index) cho mỗi fold.
        """
        self.logger.info(f"Bắt đầu chia dữ liệu với KFold (n_splits={n_splits}).")
        kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
        folds_indices = []

        for train_index, test_index in kf.split(self.dataframe):
            folds_indices.append((train_index, test_index))

        self.logger.info(f"Đã chia thành {len(folds_indices)} folds thành công.")
        return folds_indices

    def simple_split(self, test_size=0.2):
        self.logger.info(f" Bắt đầu chuẩn bị cắt dữ liệu (Test size: {test_size})...")
        # Có target thì dùng, không có thì thôi
        y_stratify = None

        # Kiểm tra 2 điều kiện:
        # a. Có khai báo target_col không?
        # b. Cột đó có thực sự nằm trong bảng dữ liệu không?
        if self.target_col and self.target_col in self.dataframe.columns:
            self.logger.info(f"[INFO] Chia theo tỷ lệ cân bằng (Stratify) cột: {self.target_col}")
            y_stratify = self.dataframe[self.target_col]
        else:
            self.logger.info("[INFO] Chia ngẫu nhiên (Random Split)")

        # 3. Cắt
        train_df, test_df = train_test_split(
            self.dataframe,
            test_size=test_size,
            random_state=42,
            shuffle=True,
            stratify=y_stratify
        )
        return train_df, test_df
