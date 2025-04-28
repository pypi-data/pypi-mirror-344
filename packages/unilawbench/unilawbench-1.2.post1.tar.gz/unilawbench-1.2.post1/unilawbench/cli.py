import argparse
from pathlib import Path
from typing import List

import evalscope

def main():
    parser = argparse.ArgumentParser(description='UniLawBench 法律评估工具')
    
    # 核心参数
    parser.add_argument('-set', nargs='+', help='指定评估数据集ID，例如1-1 2-3')
    parser.add_argument('-form', choices=['qa', 'mcq'], required=True, 
                      help='评估形式: qa-问答题 mcq-选择题')
    parser.add_argument('-model', type=Path, required=True,
                      help='本地模型路径（包含模型文件和配置文件）')
    
    # 批量运行功能
    parser.add_argument('--run-all', action='store_true',
                      help='自动运行当前form类型的所有数据集')

    args = parser.parse_args()

    # 构建任务配置
    task_cfg = evalscope.TaskConfig(
        model_path=args.model,
        form_type=args.form,
        datasets=resolve_datasets(args),
    )
    evalscope.run_task(task_cfg)

def resolve_datasets(args) -> List[str]:
    """解析数据集参数，支持--run-all时自动加载对应类型的所有数据集"""
    if args.run_all:
        data_dir = Path(__file__).parent / 'dataset' / args.form
        return [f.stem for f in data_dir.glob('*.*') if f.suffix in ('.csv', '.jsonl')]
    return args.set if args.set else []

if __name__ == '__main__':
    main()