import shutil

from ewoks3dxrd.tasks.make_grain_map import MakeGrainMap

from .conftest import assert_grain_map_results


def test_map_grains(tmp_path):
    new_filename = tmp_path / "nexus_segment.h5"
    shutil.copy2(
        "/data/projects/id03_3dxrd/ewoks_test_data/indexing/nexus_segment.h5",
        new_filename,
    )

    inputs = {
        "hkl_tols": (0.05, 0.025, 0.01),
        "minpks": 120,
        "folder_file_config": {
            "omega_motor": "diffrz",
            "scan_folder": "/data/projects/id03_3dxrd/expt/RAW_DATA/FeAu_0p5_tR/FeAu_0p5_tR_ff1/scan0001",
        },
        "intensity_fine_filtered_data_url": f"{new_filename}::/1.1/intensity_filtered_inner_peaks",
        "indexed_grain_data_url": f"{new_filename}::/1.1/indexed_ubi",
        "intensity_filtered_data_url": f"{new_filename}::/1.1/intensity_filtered_all_peaks",
        "analyse_folder": tmp_path,
        "overwrite": True,
    }

    task = MakeGrainMap(inputs=inputs)
    task.execute()

    assert_grain_map_results(task.outputs)
