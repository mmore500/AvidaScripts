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
            "Alive": [1, 0, 1, 1, 1, 0, 1, 1],
            "Empty": [0, 1, 0, 0, 0, 1, 0, 0],
            "Traits Bitfield": [0, 0, 3, 1, 5, 0, 0, 2],
            "Num Traits": [0, 0, 2, 1, 2, 0, 0, 1],
            "Row": [0, 0, 0, 0, 1, 1, 1, 1],
            "Col": [0, 1, 2, 3, 0, 1, 2, 3],
            "Site": [0, 1, 2, 3, 4, 5, 6, 7],
            "Trait 0": [0, 0, 1, 1, 1, 0, 0, 0],
            "Trait 1": [0, 0, 1, 0, 0, 0, 0, 1],
            "Trait 2": [0, 0, 0, 0, 1, 0, 0, 0],
            "Trait 3": [0, 0, 0, 0, 0, 0, 0, 0],
        }
    )
    assert expected_df.equals(task_grid_df)


def test_load_grid_task_dataframe_infer_ntasks():
    data_path = f"{os.path.dirname(__file__)}/assets/grid_task.dat"
    task_grid_df = load_grid_task_dataframe(data_path)
    assert len(task_grid_df) == 8

    expected_df = pd.DataFrame(
        {
            "Alive": [1, 0, 1, 1, 1, 0, 1, 1],
            "Empty": [0, 1, 0, 0, 0, 1, 0, 0],
            "Traits Bitfield": [0, 0, 3, 1, 5, 0, 0, 2],
            "Num Traits": [0, 0, 2, 1, 2, 0, 0, 1],
            "Row": [0, 0, 0, 0, 1, 1, 1, 1],
            "Col": [0, 1, 2, 3, 0, 1, 2, 3],
            "Site": [0, 1, 2, 3, 4, 5, 6, 7],
            "Trait 0": [0, 0, 1, 1, 1, 0, 0, 0],
            "Trait 1": [0, 0, 1, 0, 0, 0, 0, 1],
            "Trait 2": [0, 0, 0, 0, 1, 0, 0, 0],
            "Trait 3": [0, 0, 0, 0, 0, 0, 0, 0],
            "Trait 4": [0, 0, 0, 0, 0, 0, 0, 0],
            "Trait 5": [0, 0, 0, 0, 0, 0, 0, 0],
            "Trait 6": [0, 0, 0, 0, 0, 0, 0, 0],
            "Trait 7": [0, 0, 0, 0, 0, 0, 0, 0],
            "Trait 8": [0, 0, 0, 0, 0, 0, 0, 0],
            "Trait 9": [0, 0, 0, 0, 0, 0, 0, 0],
            "Trait 10": [0, 0, 0, 0, 0, 0, 0, 0],
            "Trait 11": [0, 0, 0, 0, 0, 0, 0, 0],
            "Trait 12": [0, 0, 0, 0, 0, 0, 0, 0],
            "Trait 13": [0, 0, 0, 0, 0, 0, 0, 0],
            "Trait 14": [0, 0, 0, 0, 0, 0, 0, 0],
            "Trait 15": [0, 0, 0, 0, 0, 0, 0, 0],
        }
    )
    assert expected_df.equals(task_grid_df)
