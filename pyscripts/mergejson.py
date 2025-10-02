#!/usr/bin/env python3
import os
import json
import sys
import glob

def deep_merge_no_overwrite(target, source):
    """
    递归合并 source 到 target，但不覆盖已有键（除非双方都是 dict，则递归合并）。
    - 如果 key 不存在于 target，则添加
    - 如果 key 存在，且 target[key] 和 source[key] 都是 dict，则递归合并
    - 否则，保留 target[key]（不覆盖）
    """
    for key, value in source.items():
        if key not in target:
            # 全新键，直接赋值（深拷贝非必需，因后续不再修改 source）
            target[key] = value
        else:
            # 键已存在
            if isinstance(target[key], dict) and isinstance(value, dict):
                # 双方都是 dict，递归合并
                deep_merge_no_overwrite(target[key], value)
            # 否则：不覆盖，保留 target[key]（包括数组、字符串、数字等）

def merge_json_files_recursive(directory):
    pattern = os.path.join(directory, "**", "*.json")
    json_files = glob.glob(pattern, recursive=True)

    if not json_files:
        print(f"警告: 在目录 '{directory}' 及其子目录中未找到任何 .json 文件。", file=sys.stderr)
        return {}

    merged = {}
    for file_path in sorted(json_files):  # 排序保证顺序一致
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    print(f"警告: 文件 '{file_path}' 不是 JSON 对象（dict），跳过。", file=sys.stderr)
                    continue
                deep_merge_no_overwrite(merged, data)
        except json.JSONDecodeError as e:
            print(f"错误: 无法解析 JSON 文件 '{file_path}': {e}", file=sys.stderr)
        except Exception as e:
            print(f"错误: 读取文件 '{file_path}' 时出错: {e}", file=sys.stderr)

    return merged

def main():
    if len(sys.argv) != 2:
        print("用法: python mergejson.py [dir]", file=sys.stderr)
        sys.exit(1)

    input_dir = sys.argv[1]

    if not os.path.isdir(input_dir):
        print(f"错误: 目录 '{input_dir}' 不存在。", file=sys.stderr)
        sys.exit(1)

    merged_data = merge_json_files_recursive(input_dir)

    # 生成输出文件名：取目录 basename + ".json"
    base_name = os.path.basename(os.path.abspath(input_dir))
    output_filename = base_name + ".json"

    try:
        with open(output_filename, 'w', encoding='utf-8') as out_file:
            json.dump(merged_data, out_file, ensure_ascii=False, indent=2)
        print(f"递归合并完成，结果已保存到 '{output_filename}'")
    except Exception as e:
        print(f"错误: 无法写入输出文件 '{output_filename}': {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()