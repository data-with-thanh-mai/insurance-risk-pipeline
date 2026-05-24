import pandas as pd
import logging
import os
class DataLoader:
    """
    Quản lý việc tải dữ liệu từ nhiều định dạng khác nhau (CSV, Excel, JSON).
    """

    def __init__(self, file_path, **kwargs):
        """
        Khởi tạo đối tượng DataLoader (Constructor).
        Args:
            file_path (str): Đường dẫn tới file dữ liệu.
            **kwargs: Các tham số tùy chọn sẽ được truyền trực tiếp vào hàm đọc của Pandas 
                      (ví dụ: encoding='utf-8', header=None, ...).
        """
        self.file_path = file_path
        self.kwargs = kwargs
        self.logger = logging.getLogger(self.__class__.__name__)
        self._dataframe = None

    # 1. CLASS METHODS (Factory Methods - Tạo đối tượng theo cấu hình)
    @classmethod
    def from_csv(cls, file_path, sep=',', **kwargs):
        """
        Khởi tạo DataLoader chuyên dụng cho file CSV.
        Args:
            file_path (str): Đường dẫn file CSV.
            sep (str, optional): Dấu phân cách. Mặc định là dấu phẩy (',').
            **kwargs: Các tham số khác (encoding, index_col, ...). 
        Returns:
            DataLoader: Một instance mới của DataLoader được cấu hình cho CSV.
        """
        if not file_path.lower().endswith('.csv'):
             print(f"[Cảnh báo] File '{file_path}' có thể không phải là CSV.")
        
        # Gọi __init__ với sep được thêm vào kwargs
        return cls(file_path, sep=sep, **kwargs)

    @classmethod
    def from_excel(cls, file_path, sheet_name=0, **kwargs):
        """
        Khởi tạo DataLoader chuyên dụng cho file Excel.
        Args:
            file_path (str): Đường dẫn file Excel (.xls, .xlsx).
            sheet_name (str/int, optional): Tên sheet hoặc chỉ số sheet cần đọc. Mặc định là 0 (sheet đầu).
            **kwargs: Các tham số khác.   
        Returns:
            DataLoader: Một instance mới của DataLoader được cấu hình cho Excel.
        """
        if not file_path.lower().endswith(('.xls', '.xlsx')):
             print(f"[Cảnh báo] File '{file_path}' có thể không phải là Excel.")
             
        return cls(file_path, sheet_name=sheet_name, **kwargs)

    @classmethod
    def from_json(cls, file_path, orient='records', **kwargs):
        """
        Khởi tạo DataLoader chuyên dụng cho file JSON.
        Args:
            file_path (str): Đường dẫn file JSON.
            orient (str, optional): Định dạng cấu trúc JSON. Mặc định là 'records'.
            **kwargs: Các tham số khác. 
        Returns:
            DataLoader: Một instance mới của DataLoader được cấu hình cho JSON.
        """
        return cls(file_path, orient=orient, **kwargs)
        
    # 2. PROPERTIES & INSTANCE METHODS (Xử lý dữ liệu)
    @property
    def data(self):
        """
        Thuộc tính trả về DataFrame (Lazy Loading).
        Dữ liệu chỉ được đọc từ ổ cứng khi thuộc tính này được gọi lần đầu tiên.
        Returns:
            pd.DataFrame: Dữ liệu đã tải.
        """
        if self._dataframe is None:
            self._load_data()
        return self._dataframe
    
    @property
    def shape(self):
        """Trả về kích thước dữ liệu mà không cần truy cập trực tiếp biến private"""
        return self.data.shape if self._dataframe is not None else (0, 0)

    def _load_data(self):
        """
        Hàm nội bộ: Thực hiện logic đọc file thực tế dựa trên phần mở rộng (extension).
        Raises:
            FileNotFoundError: Nếu file không tồn tại.
            ValueError: Nếu định dạng file không được hỗ trợ.
            Exception: Các lỗi khác trong quá trình đọc file (pandas errors).
        """
        self.logger.info(f"Đang tải dữ liệu từ: {self.file_path}")
        
        if not os.path.exists(self.file_path):
             self.logger.error(f"Lỗi: Không tìm thấy file '{self.file_path}'")
             raise FileNotFoundError(f"File not found: {self.file_path}")

        # Lấy đuôi file bằng static method
        ext = self._get_extension(self.file_path)

        try:
            if ext == '.csv':
                # **self.kwargs sẽ bung các tham số (như sep, encoding) vào hàm read_csv
                self._dataframe = pd.read_csv(self.file_path, **self.kwargs)
            elif ext in ['.xls', '.xlsx']:
                self._dataframe = pd.read_excel(self.file_path, **self.kwargs)
            elif ext == '.json':
                self._dataframe = pd.read_json(self.file_path, **self.kwargs)
            else:
                raise ValueError(f"Định dạng file '{ext}' chưa được hỗ trợ.")
            self.logger.info(f"Tải thành công. Shape: {self._dataframe.shape}")
            
        except Exception as e:
            self.logger.error(f"Lỗi đọc file: {e}")
            raise e

    # 3. STATIC METHODS (Hàm tiện ích)
    @staticmethod
    def _get_extension(file_path):
        """
        Hàm tiện ích tĩnh: Trích xuất phần mở rộng của file.
        Args:
            file_path (str): Đường dẫn file.   
        Returns:
            str: Phần mở rộng (ví dụ: '.csv', '.xlsx') ở dạng chữ thường.
        """
        _, ext = os.path.splitext(file_path)
        return ext.lower()
