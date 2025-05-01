import shutil

from ewoks3dxrd.tasks.index_grains import IndexGrains

from .conftest import assert_indexing_results


def test_indexing(tmp_path):
    new_filename = tmp_path / "nexus_segment.h5"
    shutil.copy2(
        "/data/projects/id03_3dxrd/ewoks_test_data/indexing/nexus_segment.h5",
        new_filename,
    )
    filepath = f"{new_filename}::/1.1/intensity_filtered_inner_peaks"

    inputs = {
        "intensity_filtered_data_url": filepath,
        "reciprocal_dist_tol": 0.05,
        "gen_rings_from_idx": (0, 1),
        "score_rings_from_idx": (0, 1, 2, 3),
        "hkl_tols": (0.01, 0.02, 0.03, 0.04),
        "min_pks_frac": (0.9, 0.75),
        "overwrite": True,
    }

    task = IndexGrains(inputs=inputs)
    task.execute()

    assert_indexing_results(task.outputs)
