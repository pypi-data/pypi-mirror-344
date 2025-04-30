from typing import Optional, Tuple, Dict
from dataclasses import dataclass
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

@dataclass
class RepetitionResult:
    """重复子串检测结果"""
    has_repetition: bool
    start_pos: int = -1
    end_pos: int = -1
    substring: str = ""
    repetition_count: int = 0
    sequence_length: int = 0

class StringRepetitionDetector:
    def __init__(self, 
                base: int = 256, 
                mod: int = 10**18 + 3,
                min_length: int = 20,
                min_repeats: int = 5,
                num_processes: Optional[int] = None):
        """
        初始化字符串重复检测器
        
        Args:
            base: 哈希算法的基数
            mod: 哈希算法的模数
            min_length: 最小重复子串长度
            min_repeats: 最小重复次数
            num_processes: 并行处理时使用的进程数，None表示使用CPU核心数
        """
        self.base = base
        self.mod = mod
        self.min_length = min_length
        self.min_repeats = min_repeats
        self.num_processes = num_processes or multiprocessing.cpu_count()

    def _compute_prefix_hash(self, text: str) -> Tuple[list, list]:
        """计算字符串的前缀哈希数组和幂次数组"""
        n = len(text)
        prefix_hash = [0] * (n + 1)
        power = [1] * (n + 1)
        
        for i in range(n):
            prefix_hash[i+1] = (prefix_hash[i] * self.base + ord(text[i])) % self.mod
            power[i+1] = (power[i] * self.base) % self.mod
            
        return prefix_hash, power

    def _get_substring_hash(self, prefix_hash: list, power: list, l: int, r: int) -> int:
        """获取子串的哈希值"""
        hash_val = (prefix_hash[r] - prefix_hash[l] * power[r - l]) % self.mod
        return hash_val + self.mod if hash_val < 0 else hash_val

    def detect_single(self, text: str) -> RepetitionResult:
        """
        检测单个字符串中的重复子串
        
        Args:
            text: 输入字符串
            
        Returns:
            RepetitionResult: 检测结果
        """
        n = len(text)
        min_total_len = self.min_length * self.min_repeats
        
        if n < min_total_len:
            return RepetitionResult(has_repetition=False)

        prefix_hash, power = self._compute_prefix_hash(text)

        # 遍历所有可能的起始位置
        for i in range(n - min_total_len + 1):
            max_L = (n - i) // self.min_repeats
            if max_L < self.min_length:
                continue

            # 二分查找最长的重复子串
            low, high = self.min_length, max_L
            best_result = None

            while low <= high:
                mid_L = (low + high) // 2
                end_pos = i + mid_L * self.min_repeats

                if end_pos > n:
                    high = mid_L - 1
                    continue

                base_hash = self._get_substring_hash(prefix_hash, power, i, i + mid_L)
                valid = True
                actual_repeats = self.min_repeats

                # 验证连续重复
                for k in range(1, self.min_repeats):
                    start = i + k * mid_L
                    end = start + mid_L
                    if end > n:
                        valid = False
                        break
                    curr_hash = self._get_substring_hash(prefix_hash, power, start, end)
                    if curr_hash != base_hash:
                        if text[i:i+mid_L] != text[start:end]:
                            valid = False
                            break

                # 如果找到有效重复，继续寻找更多重复
                if valid:
                    while True:
                        next_start = i + actual_repeats * mid_L
                        next_end = next_start + mid_L
                        if next_end > n:
                            break
                        next_hash = self._get_substring_hash(prefix_hash, power, next_start, next_end)
                        if next_hash == base_hash and text[i:i+mid_L] == text[next_start:next_end]:
                            actual_repeats += 1
                        else:
                            break

                    if actual_repeats >= self.min_repeats:
                        best_result = RepetitionResult(
                            has_repetition=True,
                            start_pos=i,
                            end_pos=i + mid_L * actual_repeats,
                            substring=text[i:i+mid_L],
                            repetition_count=actual_repeats,
                            sequence_length=mid_L
                        )
                        high = mid_L - 1  # 尝试找更短的重复
                    else:
                        low = mid_L + 1
                else:
                    low = mid_L + 1

            if best_result:
                return best_result

        return RepetitionResult(has_repetition=False)

    def detect_batch(self, texts: list[str]) -> list[RepetitionResult]:
        """
        并行检测多个字符串中的重复子串
        
        Args:
            texts: 字符串列表
            
        Returns:
            list[RepetitionResult]: 检测结果列表
        """
        with ProcessPoolExecutor(max_workers=self.num_processes) as executor:
            results = list(executor.map(self.detect_single, texts))
        return results

    def detect_string(self, text: str, parallel: bool = False) -> RepetitionResult:
        """
        检测字符串中的重复子串（便捷方法）
        
        Args:
            text: 输入字符串
            parallel: 是否使用并行处理（当输入是很长的字符串时）
            
        Returns:
            RepetitionResult: 检测结果
        """
        if not parallel or len(text) < 1000000:  # 对于较短的字符串直接处理
            return self.detect_single(text)
            
        # 对于很长的字符串，将其分割成块并行处理
        chunk_size = 1000000
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        results = self.detect_batch(chunks)
        
        # 返回找到的第一个重复或无重复结果
        for i, result in enumerate(results):
            if result.has_repetition:
                # 调整起始位置以匹配原始字符串
                result.start_pos += i * chunk_size
                result.end_pos += i * chunk_size
                return result
                
        return RepetitionResult(has_repetition=False)