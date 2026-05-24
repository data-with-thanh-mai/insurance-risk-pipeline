import logging
import os
from utils.common import DataSplitter
from etl_pipeline.extract import DataLoader
from ml_pipeline.modeling import FeatureWrapperSelector, ModelTrainer, HyperparameterTuning
from ml_pipeline.evaluation import ModelEvaluator, ReportModel, Visualizer

class AutoMLPipeline:
    def __init__(self, train_file, test_file, tuning_method="random_search", feature_method="rfe", n_features=15):
        self.train_file = train_file
        self.test_file = test_file
        self.tuning_method = tuning_method
        self.feature_method = feature_method
        self.n_features = n_features
        self.logger = logging.getLogger("AutoML Pipeline")
        self.all_results_metrics = {}
        
        # Tự động tạo thư mục results nếu chưa có
        self.results_dir = "results"
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

    def run(self):
        self.logger.info("=== BẮT ĐẦU CHẠY AUTOML PIPELINE ===")
        # 1. Load Data đã sạch từ ETL
        df_train = DataLoader(self.train_file).data
        df_test = DataLoader(self.test_file).data

        target_col = "OUTCOME"
        cols_drop = [c for c in ["ID"] if c in df_train.columns]

        X_train = df_train.drop(columns=cols_drop + [target_col], errors='ignore')
        y_train = df_train[target_col]
        X_test = df_test.drop(columns=cols_drop + [target_col], errors='ignore')
        y_test = df_test[target_col]

        # 2. Feature Selection
        selector = FeatureWrapperSelector(method=self.feature_method, n_features_to_select=self.n_features)
        X_train_selected = selector.fit_transform(X_train, y_train)
        X_test_selected = X_test[selector.selected_columns]

        # 3. Loop Models
        supported_models = ModelTrainer.get_supported_models()
        for model_name in supported_models:
            self.logger.info(f"PROCESSING MODEL: {model_name.upper()}")
            try:
                X_tune = X_train_selected.reset_index(drop=True)
                y_tune = y_train.reset_index(drop=True)
                
                splitter = DataSplitter(X_tune)
                folds = splitter.kfold_split_data(n_splits=3) 

                tuner = HyperparameterTuning(tuning_method=self.tuning_method, scoring="f1")
                tuning_res = tuner.tune_hyperparameters(X_tune, y_tune, folds, model_name)
                best_params = tuning_res["best_params"] if tuning_res else {}

                trainer = ModelTrainer(model_name, **best_params)
                trainer.train_model(X_train_selected, y_train)
                # Lưu model vào thư mục results
                trainer.save_model(self.results_dir) 

                y_pred = trainer.predict_y(X_test_selected)
                result_pack = [(trainer.model, X_test_selected, y_test, y_pred)]

                evaluator = ModelEvaluator(result_pack)
                self.all_results_metrics[model_name] = evaluator.metrics

                # Lưu ảnh vào thư mục results
                viz = Visualizer(result_pack, model_name_prefix=model_name, save_dir=self.results_dir)
                viz.plot_all()

            except Exception as e:
                self.logger.error(f"Lỗi: {e}")
                continue
            
        # 4. Final Report
        report_path = os.path.join(self.results_dir, "evaluation_report.txt")
        reporter = ReportModel(report_path)
        reporter.save_comparision(self.all_results_metrics)
        self.logger.info("=== HOÀN TẤT AUTOML PIPELINE ===")
