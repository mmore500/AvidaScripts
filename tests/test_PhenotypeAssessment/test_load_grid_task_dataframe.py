import os

import pandas as pd

from AvidaScripts.GenericScripts.PhenotypeAssessment import (
    get_named_environment_content,
    load_grid_task_dataframe,
)


def test_load_grid_task_dataframe():
    data_path = f"{os.path.dirname(__file__)}/assets/grid_task.dat"
    task_grid_df = load_grid_task_dataframe(data_path, 4)
    assert len(task_grid_df) == 8

    expected_df = pd.DataFrame(
        {
            "alive": [1, 0, 1, 1, 1, 0, 1, 1],
            "empty": [0, 1, 0, 0, 0, 1, 0, 0],
            "task bitfield": [0, 0, 3, 1, 5, 0, 0, 2],
            "num tasks": [0, 0, 2, 1, 2, 0, 0, 1],
            "row": [0, 0, 0, 0, 1, 1, 1, 1],
            "col": [0, 1, 2, 3, 0, 1, 2, 3],
            "task 0": [0, 0, 1, 1, 1, 0, 0, 0],
            "task 1": [0, 0, 1, 0, 0, 0, 0, 1],
            "task 2": [0, 0, 0, 0, 1, 0, 0, 0],
            "task 3": [0, 0, 0, 0, 0, 0, 0, 0],
        }
    )
    assert expected_df.equals(task_grid_df)


def test_load_grid_task_dataframe_infer_ntasks():
    data_path = f"{os.path.dirname(__file__)}/assets/grid_task.dat"
    task_grid_df = load_grid_task_dataframe(data_path)
    assert len(task_grid_df) == 8

    expected_df = pd.DataFrame(
        {
            "alive": [1, 0, 1, 1, 1, 0, 1, 1],
            "empty": [0, 1, 0, 0, 0, 1, 0, 0],
            "task bitfield": [0, 0, 3, 1, 5, 0, 0, 2],
            "num tasks": [0, 0, 2, 1, 2, 0, 0, 1],
            "row": [0, 0, 0, 0, 1, 1, 1, 1],
            "col": [0, 1, 2, 3, 0, 1, 2, 3],
            "task 0": [0, 0, 1, 1, 1, 0, 0, 0],
            "task 1": [0, 0, 1, 0, 0, 0, 0, 1],
            "task 2": [0, 0, 0, 0, 1, 0, 0, 0],
            "task 3": [0, 0, 0, 0, 0, 0, 0, 0],
            "task 4": [0, 0, 0, 0, 0, 0, 0, 0],
            "task 5": [0, 0, 0, 0, 0, 0, 0, 0],
            "task 6": [0, 0, 0, 0, 0, 0, 0, 0],
            "task 7": [0, 0, 0, 0, 0, 0, 0, 0],
            "task 8": [0, 0, 0, 0, 0, 0, 0, 0],
            "task 9": [0, 0, 0, 0, 0, 0, 0, 0],
            "task 10": [0, 0, 0, 0, 0, 0, 0, 0],
            "task 11": [0, 0, 0, 0, 0, 0, 0, 0],
            "task 12": [0, 0, 0, 0, 0, 0, 0, 0],
            "task 13": [0, 0, 0, 0, 0, 0, 0, 0],
            "task 14": [0, 0, 0, 0, 0, 0, 0, 0],
            "task 15": [0, 0, 0, 0, 0, 0, 0, 0],
        }
    )
    assert expected_df.equals(task_grid_df)
