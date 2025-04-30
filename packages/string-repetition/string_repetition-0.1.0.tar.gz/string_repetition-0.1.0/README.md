# String Repetition Detector

一个高效的Python包，用于检测字符串中的重复模式。使用前缀哈希和二分查找算法实现，支持并行处理。

## 特点

- 高效的前缀哈希算法
- 二分查找优化
- 支持并行处理大型文本
- 支持Python 3.7-3.13
- 提供详细的重复信息（起始位置、终止位置、重复次数等）

## 安装

```bash
pip install string-repetition
```

## 使用示例

### 基本使用

```python
from string_repetition import StringRepetitionDetector

# 创建检测器实例
detector = StringRepetitionDetector(
    min_length=20,     # 最小重复长度
    min_repeats=5      # 最小重复次数
)

# 检测单个字符串
text = "your_text_here" * 10
result = detector.detect_single(text)

if result.has_repetition:
    print(f"找到重复模式！")
    print(f"重复子串: {result.substring}")
    print(f"起始位置: {result.start_pos}")
    print(f"终止位置: {result.end_pos}")
    print(f"重复次数: {result.repetition_count}")
    print(f"序列长度: {result.sequence_length}")
```

### 批量处理

```python
# 批量检测多个字符串
texts = ["text1", "text2", "text3"]
results = detector.detect_batch(texts)

for result in results:
    if result.has_repetition:
        print(f"重复子串: {result.substring}")
```

### 大文本并行处理

```python
# 对大型文本使用并行处理
long_text = "very_long_text_here"
result = detector.detect_string(text, parallel=True)
```

## 参数配置

- `base`: 哈希算法的基数（默认: 256）
- `mod`: 哈希算法的模数（默认: 10^18 + 3）
- `min_length`: 最小重复子串长度（默认: 20）
- `min_repeats`: 最小重复次数（默认: 5）
- `num_processes`: 并行处理时使用的进程数（默认: CPU核心数）

## 性能优化建议

1. 对于短文本（<1MB），使用单进程模式即可
2. 对于大型文本，建议开启并行处理模式
3. 可以根据实际需求调整min_length和min_repeats参数

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！