

from pathlib import Path
from typing import Generator
from graphmaker.model.extract._dataprovider import DataProvider
import pandas as pd
import os

class Pandas(DataProvider):
    def __init__(self, df, batch_size=1000):
        self._df = df
        self.batch_size = batch_size

    def is_connected(self):
        return True

    def connect(self):
        return self

    def close(self):
        self._df = None

    def total_rows(self):
        return self._df.shape[0]

    def columns(self):
        return self._df.columns.tolist()

    def unique(self, column):
        return self._df[column].unique()

    def df(self, rows=None, columns=None) -> pd.DataFrame:
        if columns is None:
            columns = self._df.columns
        if rows is not None:
            return self._df[columns].sample(n=rows)
        return self._df[columns]

    def unique_multiple(self, columns, drop_na=False):
        df = self.df(columns=columns)
        for col in columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(str)
        ret = df.drop_duplicates(subset=columns)
        if drop_na:
            return ret.dropna()
        return ret

    def value_counts_multiple(self, columns):
        df = self.df(columns=columns)
        for col in columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(str)
        return df.groupby(columns).size().reset_index(name="count")

    def next(self) -> Generator[list[str | int | float], None, None]:
        for idx in range(0, len(self._df), self.batch_size):
            yield self._df.iloc[idx: idx + self.batch_size].values.tolist()

    def to_parquet_file(self, output_file:Path|str, batch_size=500, verbose=False):
        import pyarrow as pa
        import pyarrow.parquet as pq
        
        if isinstance(output_file, str):
            output_file = Path(output_file)
            
        output_file.parent.mkdir(parents=True, exist_ok=True)

        table = pa.Table.from_pandas(self._df)
        pq.write_table(table, output_file, row_group_size=batch_size)
        if verbose:
            print(f"Data written to {output_file} in Parquet format.")
        return output_file
