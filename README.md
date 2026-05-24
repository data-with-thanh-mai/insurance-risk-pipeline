# Insurance Risk Prediction Pipeline

👤**Authors:** * **Thái Ngọc Thanh Mai** (Lead Data Engineer - ETL Pipeline)
* **Nguyễn Đỗ Khánh Ngọc** (Machine Learning Engineer - Modeling & Evaluation)
* **Nguyễn Ngọc Minh** (Data Analyst - EDA & Reporting)

**GitHub:** [data-with-thanh-mai](https://github.com/data-with-thanh-mai)

## 🎯 Project Overview & Objectives
Dự án này xây dựng một hệ thống **End-to-End Data Pipeline** tự động hóa quy trình từ xử lý dữ liệu thô đến huấn luyện mô hình dự báo rủi ro bảo hiểm.

* **Tự động hóa xử lý dữ liệu (ETL Pipeline):** Tự động làm sạch, chuẩn hóa và xử lý dữ liệu từ tập dữ liệu thô (`raw_data.csv`), đảm bảo dữ liệu đầu vào luôn sạch và nhất quán.
* **Hệ thống dự báo thông minh (AutoML):** Tích hợp quy trình chọn lọc đặc trưng và tinh chỉnh mô hình tự động, giúp tìm ra giải pháp dự báo rủi ro chính xác và tối ưu nhất.
* **Đảm bảo tính tin cậy:** Áp dụng các kỹ thuật xử lý chặt chẽ để loại bỏ rò rỉ dữ liệu (data leakage), giúp mô hình đạt hiệu suất cao và ổn định khi triển khai thực tế.

## 🏗 Data Architecture & Pipeline Flow
Hệ thống được thiết kế theo tư duy **Data Engineering**, tách biệt giữa các tầng xử lý để đảm bảo tính module và khả năng mở rộng:



1. **Ingestion Layer:** Trích xuất dữ liệu thô an toàn thông qua `DataLoader`.
2. **Transformation Layer (Core DE):** Thực hiện làm sạch (Validation), kỹ thuật đặc trưng (Feature Engineering) và chuẩn hóa dữ liệu.
3. **Storage Layer:** Lưu trữ dữ liệu sạch trung gian (`data/clean_data/`) để tách biệt giữa đội ngũ Data Engineering và Data Science.
4. **Modeling Layer (ML Pipeline):** Lựa chọn đặc trưng tự động, tuning mô hình bằng K-Fold CV và đánh giá hiệu suất.
5. **Orchestrator:** File `main.py` đóng vai trò điều phối luồng vận hành thông qua giao diện dòng lệnh (CLI).

## 📊 Results Summary
* **Champion Model:** Random Forest đạt **F1-Score ~0.80**.
* **Key Performance:** **Precision đạt ~97%**, giúp doanh nghiệp giảm thiểu tối đa báo động giả (False Positive) – đảm bảo độ tin cậy cao cho quy trình thẩm định.

## 📂 Repository Structure
```text
insurance_risk_prediction/
├── 📄 main.py                  # "Nhạc trưởng" điều phối toàn bộ
├── 📄 requirements.txt         # Danh sách thư viện cần thiết
├── 📄 README.md                # Tài liệu hướng dẫn sử dụng
│
├── 📂 config/                  # Nơi lưu cấu hình (không hard-code)
│   ├── etl_config.py           # Lưu các quy tắc chuẩn hóa, giới hạn dữ liệu
│   └── ml_config.py            # Lưu cấu hình tuning, phương pháp chọn feature
│
├── 📂 data/
│   ├── raw_data.csv            # Dữ liệu gốc
│   └── 📂 clean_data/          # Chứa final_train_data.csv & final_test_data.csv
│
├── 📂 etl_pipeline/            # Team Data Engineering
│   ├── __init__.py
│   ├── extract.py              # DataLoader
│   ├── transform.py            # DataCleaner, FeatureEngineer, DataTransformer
│   ├── load.py                 # LocalFileLoader
│   └── etl_manager.py          # DataPreparationPipeline (Logic chính)
│
├── 📂 ml_pipeline/             # Team Data Science
│   ├── modeling.py             # ModelTrainer, FeatureWrapperSelector, HyperparameterTuning
│   ├── evaluation.py           # ModelEvaluator, ReportModel, Visualizer
│   └── ml_manager.py           # AutoMLPipeline (Logic chính)
│
├── 📂 utils/                   # Tiện ích dùng chung (Logger, Splitter)
│   └── common.py
│
├── 📂 logs/                    # Nhật ký vận hành (automl_run.log)
│
└── 📂 results/                 # Kết quả (Model .pkl, biểu đồ, báo cáo)
