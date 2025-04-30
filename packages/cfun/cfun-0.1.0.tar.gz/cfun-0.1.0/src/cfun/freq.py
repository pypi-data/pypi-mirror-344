import pandas as pd

# 所有的词频（只有中文)
all_frequency_path = "src/cfun/data/all_frequency.parquet"
# 常见的4字和5字词
frequency_path = "src/cfun/data/frequency.parquet"


ALL_FREQUENCY = pd.read_parquet(all_frequency_path)
FREQUENCY = pd.read_parquet(frequency_path)

__all__ = [
    "ALL_FREQUENCY",
    "FREQUENCY",
]
