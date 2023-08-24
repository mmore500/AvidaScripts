import typing

import pandas as pd
import opytional as opyt


def load_grid_task_dataframe(
    path: str,
    num_tasks: typing.Optional[int] = None,
) -> pd.DataFrame:

    grid_df = pd.read_csv(
        path,
        sep=" ",
        header=None,
    ).dropna(axis=1)
    max_val = max(int(grid_df.max().max()), 0)
    max_bitlength = max_val.bit_length()
    num_tasks = opyt.or_value(
        num_tasks,
        max_bitlength - max_bitlength % -16,
    )
    # rounding up to powers of 16 makes greater chance for
    # cross-file consistency without num_tasks specified
    records = []
    for index, row in grid_df.iterrows():
        for col in grid_df.columns:
            entry = row[col]
            site_data = {
                "Alive": int(entry >= 0),
                "Empty": int(entry == -1),
                "Raw Tasks Bitfield": int((entry > 0) * entry),
                "Num Tasks": (entry > 0) * int(entry).bit_count(),
                "Row": index,
                "Col": col,
                "Site": len(records),
            }
            task_data = {
                f"Trait {task}": int((entry > 0) and bool(entry & (1 << task)))
                for task in range(num_tasks)
            }
            records.append(
                {
                    **site_data,
                    **task_data,
                },
            )

    return pd.DataFrame.from_records(records)
