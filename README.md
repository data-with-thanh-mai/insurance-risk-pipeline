# python-etl-insurance-pipeline
Hệ thống End-to-End Data Pipeline chuyên dụng cho bài toán phân loại rủi ro bảo hiểm xe.

## 🎯Mục tiêu dự án
Xây dựng quy trình ETL: Chuyển đổi dữ liệu thô (raw_data.csv) thành dữ liệu sạch, đảm bảo tính nhất quán qua các bước tiền xử lý.

Tự động hóa Machine Learning (AutoML): Tích hợp quy trình chọn đặc trưng, tinh chỉnh siêu tham số và huấn luyện đa mô hình trong một hệ thống thống nhất.

Đảm bảo tính chính xác: Loại bỏ hiện tượng "học vẹt" (overfitting) do rò rỉ dữ liệu, đảm bảo mô hình có khả năng tổng quát hóa trên dữ liệu thực tế.

## 🏗 Kiến trúc hệ thống
Hệ thống được thiết kế theo kiến trúc phân tầng (Layered Architecture), tách biệt giữa phần xử lý dữ liệu và phần huấn luyện mô hình.

Ingestion Layer: Trích xuất dữ liệu thô an toàn thông qua DataLoader.

Transformation Layer (Core DE): Thực hiện làm sạch (Validation), kỹ thuật đặc trưng (Feature Engineering) và chuẩn hóa dữ liệu.

Storage Layer: Lưu trữ dữ liệu sạch trung gian (data/clean_data/) để tách biệt giữa đội ngũ Data Engineering và Data Science.

Modeling Layer (ML Pipeline): Lựa chọn đặc trưng tự động, tuning mô hình bằng K-Fold CV và đánh giá hiệu suất.

Orchestrator: File main.py đóng vai trò  điều phối toàn bộ luồng vận hành thông qua lệnh CLI.

## 📊 Kết quả đạt được
Mô hình tốt nhất: Random Forest với F1-Score ~0.80.

Độ tin cậy: Precision đạt ~97%, giúp doanh nghiệp giảm thiểu tối đa báo động giả (False Positive) – đảm bảo khi hệ thống cảnh báo rủi ro, đó là dự báo đáng tin cậy.

## 📂 Cấu trúc thư mục 
```
insurance_risk_prediction/
├── 📄 main.py                  # File main chạy toàn bộ chương trình
├── 📄 requirements.txt         # Danh sách thư viện cần thiết
├── 📄 README.md                # Tài liệu hướng dẫn sử dụng
│
├── 📂 config/                  # Nơi lưu cấu hình (cũ là file config.py)
│   ├── etl_config.py           # Lưu my_golden_specs, my_range_rules, v.v.
│   └── ml_config.py            # Lưu cấu hình mô hình (test_size, phương pháp tuning...)
│
├── 📂 data/
│   ├── raw_data.csv            # Dữ liệu gốc
│   └── 📂 clean_data/          # Chứa final_train_data.csv & final_test_data.csv
│
├── 📂 etl_pipeline/            # Team Data Engineering
│   ├── __init__.py             # File trống để Python nhận diện package
│   ├── extract.py              # DataLoader
│   ├── transform.py            # DataCleaner, FeatureEngineer, DataTransformer
│   ├── load.py                 # LocalFileLoader
│   └── etl_manager.py          # DataPreparationPipeline (Logic chính)
│
├── 📂 ml_pipeline/             # Team Data Science
│   ├── __init__.py
│   ├── modeling.py             # ModelTrainer, FeatureWrapperSelector, HyperparameterTuning
│   ├── evaluation.py           # ModelEvaluator, ReportModel, Visualizer
│   └── ml_manager.py           # AutoMLPipeline (Logic chính)
│
├── 📂 utils/
│   ├── __init__.py
│   └── common.py               # SystemLogger, DataSplitter
│
├── 📂 logs/                    # Nơi lưu nhật ký
│   └── automl_run.log
```
## 🛠 Cách sử dụng
Cài đặt thư viện:

```Bash
pip install -r requirements.txt
```
Chạy toàn bộ Pipeline:
```
Bash
python main.py --mode all
```
Các chế độ khác:
```
--mode etl: Chỉ chạy bước làm sạch dữ liệu.
```
```
--mode ml: Chỉ chạy bước huấn luyện mô hình.
```

