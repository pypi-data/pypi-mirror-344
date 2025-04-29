import json
from pathlib import Path
from typing import Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
from ..constants import DataCollection

class ResultAnalyzer:
    def __init__(self, results_dir: str):
        self.results_dir = Path(results_dir)
        self.metadata = self._load_dataset_metadata()

    def _load_results(self) -> Dict[str, Any]:
        result_files = list(self.results_dir.glob('*.json'))
        combined = {}
        for f in result_files:
            with open(f) as fp:
                data = json.load(fp)
                combined.update(data)
        return combined

    def generate_report(self) -> Dict[str, Any]:
        results = self._load_results()
        stats = {
            'dataset_versions': self._get_dataset_versions(),
            'metric_summary': self._calculate_metric_stats(results),
            'performance_trends': self._analyze_trends(results)
        }
        self._generate_visualizations(stats)
        return stats

    def _get_dataset_metadata(self, dataset_name: str) -> Dict[str, str]:
        return DataCollection.get_metadata(dataset_name)

    def _calculate_metric_stats(self, results: Dict) -> Dict[str, float]:
        df = pd.DataFrame(results.items(), columns=['metric', 'value'])
        return {
            'mean': df['value'].mean(),
            'std': df['value'].std(),
            'max': df['value'].max(),
            'min': df['value'].min()
        }

    def _analyze_trends(self, results: Dict) -> Dict:
        # 实现跨数据集性能趋势分析
        return {}

    def _generate_visualizations(self, stats: Dict):
        plt.figure(figsize=(10, 6))
        pd.Series(stats['metric_summary']).plot(kind='bar')
        plt.savefig(self.results_dir / 'metric_summary.png')
        plt.close()

    def _load_dataset_metadata(self) -> Dict:
        """加载所有数据集的元数据信息"""
        return {
            dataset: self._get_dataset_metadata(dataset)
            for dataset in DataCollection.get_available_datasets()
        }


def add_dataset_metadata(dataset_name: str, metadata: Dict):
    """为数据集添加版本控制和来源信息"""
    DataCollection.update_metadata(dataset_name, metadata)