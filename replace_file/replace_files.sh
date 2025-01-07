#!/bin/bash

# 定义需要替换的文件和目标目录的对应关系
declare -A files_to_replace=(
    ["./replace_file/tasks.py"]="/home/ma-user/anaconda3/envs/MindSpore/lib/python3.9/site-packages/ultralytics/nn/tasks.py"
    ["./replace_file/torch_utils.py"]="/home/ma-user/anaconda3/envs/MindSpore/lib/python3.9/site-packages/ultralytics/utils/torch_utils.py"
    ["./replace_file/tal.py"]="/home/ma-user/anaconda3/envs/MindSpore/lib/python3.9/site-packages/ultralytics/utils/tal.py"
    ["./replace_file/ops.py"]="/home/ma-user/anaconda3/envs/MindSpore/lib/python3.9/site-packages/ultralytics/utils/ops.py"
    ["./replace_file/results.py"]="/home/ma-user/anaconda3/envs/MindSpore/lib/python3.9/site-packages/ultralytics/engine/results.py"
)

# 遍历每个文件并执行替换操作
for source_file in "${!files_to_replace[@]}"; do
    target_file="${files_to_replace[$source_file]}"

    # 检查源文件是否存在
    if [ ! -f "$source_file" ]; then
        echo "源文件不存在: $source_file"
        continue
    fi

    # 创建目标文件的目录，如果不存在则创建
    target_dir=$(dirname "$target_file")
    if [ ! -d "$target_dir" ]; then
        echo "目标目录不存在，正在创建: $target_dir"
        mkdir -p "$target_dir"
    fi

    # 移动文件并替换目标位置的文件
    echo "正在替换 $target_file..."
    cp "$source_file" "$target_file"

    # 如果需要删除源文件（如果你只想替换，不需要保留源文件）
    # rm "$source_file"
done

echo "文件替换完成！"