#!/bin/bash

# 定义要测试的模型列表
MODELS=("google/flan-t5-small" "google/flan-t5-base" "facebook/bart-base")
DATA_FILE="data/single_goal/6x6/test_iid.jsonl"
OUT_DIR="outputs"

mkdir -p $OUT_DIR

echo "🚀 开始执行 Baseline 批量测试..."

for MODEL in "${MODELS[@]}"; do
    # 提取模型名称作为文件名缩写 (例如 google/flan-t5-small -> flan-t5-small)
    MODEL_NAME=$(basename $MODEL)
    PRED_FILE="${OUT_DIR}/${MODEL_NAME}_preds.jsonl"
    METRIC_FILE="${OUT_DIR}/${MODEL_NAME}_metrics.json"

    echo "=================================================="
    echo "🤖 正在处理模型: $MODEL"
    echo "=================================================="

    # 1. 运行模型推理 (调用你之前写的 run_baseline.py)
    echo "➤ 正在生成路径预测..."
    python scripts/run_baseline.py \
        --model $MODEL \
        --data_file $DATA_FILE \
        --out_file $PRED_FILE

    # 2. 运行评估执行器
    echo "➤ 正在计算评估指标..."
    python scripts/evaluate_executor.py \
        --data_file $DATA_FILE \
        --pred_file $PRED_FILE \
        --out_file $METRIC_FILE

    echo "✅ $MODEL 测试完成！指标已保存至 $METRIC_FILE"
done

echo "🎉 所有 Baseline 模型运行完毕！"