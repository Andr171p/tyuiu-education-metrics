import numpy as np
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional

from src.config import BASE_DIR


def load_csv_data(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def group_by_feature(data: pd.DataFrame, feature: str) -> List[pd.DataFrame]:
    '''values: Dict[str, np.int64] = dict(data.value_counts(feature))
    dfs: Optional[List[pd.DataFrame]] = []
    for value in values:
        df: pd.DataFrame = data.loc[data[feature] == value]
        dfs.append(df)
    return dfs'''
    return [group for _, group in data.groupby(feature)]


df = load_csv_data(path=BASE_DIR / "data" / "data 2019-2024.csv")
a = df.value_counts("Законченное образ. учреждение")
g = group_by_feature(df, "Законченное образ. учреждение")
print(len(g))

