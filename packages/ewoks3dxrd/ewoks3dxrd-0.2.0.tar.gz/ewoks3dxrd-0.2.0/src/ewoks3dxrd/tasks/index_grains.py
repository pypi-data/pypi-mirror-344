from __future__ import annotations

import posixpath
from ewokscore import Task
from ImageD11 import columnfile as PeakColumnFile
from ImageD11 import indexing
from ImageD11.unitcell import unitcell
from ..nexus import (
    read_peaks_attributes,
    get_data_url_paths,
    find_lattice_parameters,
    find_wavelength,
    save_nexus_grain_process,
    check_throw_write_data_group_url,
)


class IndexGrains(
    Task,
    input_names=[
        "intensity_filtered_data_url",
        "gen_rings_from_idx",
        "score_rings_from_idx",
    ],
    optional_input_names=[
        "max_grains",
        "reciprocal_dist_tol",
        "hkl_tols",
        "min_pks_frac",
        "cosine_tol",
        "overwrite",
    ],
    output_names=["indexed_grain_data_url"],
):
    """
    From 3D peaks, finds grains' UBI  matrices and stores them in both ASCII format and NeXus (.h5) format.

    Inputs:

    - `intensity_filtered_data_url` (str): Data path to the intensity filtered 'NxProcess group data' peaks
    - `gen_rings_from_idx` (Tuple): Indices of rings used for generating UBI. Two are usually enough, three in some rare cases.
    - `score_rings_from_idx` (Tuple): Indices of the rings used for scoring. These must contain the indices used for indexing.

    Optional Inputs:

    - `max_grains` (int): To limit the maximum number of grains (UBI matrices).
    - `reciprocal_dist_tol` (float): reciprocal distance tolerance value.
    - `hkl_tols` (Tuple): hkl tolerance, (hkl are integers, while doing convergence, had to do discretization on processed values)
    - `min_pks_frac` (Tuple): min peaks fraction to iterate over
    - `cosine_tol` (float): a tolerance value used in the Indexer convergence scheme
        for finding pairs of peaks to make an orientation

    Outputs:

    - `indexed_grain_data_url` (str): Data path to 'NxProcess group data' Grains that stores generated UBI
    """

    def run(self):
        nexus_file_path, intensity_filtered_data_group_path = get_data_url_paths(
            self.inputs.intensity_filtered_data_url
        )

        gen_rings_idx = self.inputs.gen_rings_from_idx
        score_rings_idx = self.inputs.score_rings_from_idx

        indexing_params = {}
        if self.get_input_value("max_grains", None):
            indexing_params["max_grains"] = self.inputs.max_grains
        if self.get_input_value("reciprocal_dist_tol", None):
            indexing_params["dstol"] = self.inputs.reciprocal_dist_tol
        if self.get_input_value("hkl_tols", None):
            indexing_params["hkl_tols"] = self.inputs.hkl_tols
        if self.get_input_value("min_pks_frac", None):
            indexing_params["fracs"] = self.inputs.min_pks_frac
        if self.get_input_value("cosine_tol", None):
            indexing_params["cosine_tol"] = self.inputs.cosine_tol

        if len(gen_rings_idx) < 2:
            raise ValueError(
                f"UBI needs at least two ring indices in `gen_rings_idx`. Got {gen_rings_idx}"
            )

        overwrite = self.get_input_value("overwrite", False)
        indexed_ubi_data_group = (
            f"{posixpath.dirname(intensity_filtered_data_group_path)}/indexed_grains"
        )
        check_throw_write_data_group_url(
            overwrite=overwrite,
            filename=nexus_file_path,
            data_group_path=indexed_ubi_data_group,
        )

        intensity_filtered_peaks = read_peaks_attributes(
            filename=nexus_file_path, process_group=intensity_filtered_data_group_path
        )
        filtered_cf = PeakColumnFile.colfile_from_dict(intensity_filtered_peaks)

        lattice_parameters, space_group = find_lattice_parameters(
            self.inputs.intensity_filtered_data_url
        )
        unit_cell = unitcell(
            lattice_parameters=lattice_parameters,
            symmetry=space_group,
        )
        unit_cell.makerings(limit=filtered_cf.ds.max())
        wavelength = find_wavelength(self.inputs.intensity_filtered_data_url)
        indexing_params["wavelength"] = wavelength
        grains, _ = indexing.do_index(
            cf=filtered_cf,
            forgen=gen_rings_idx,
            foridx=score_rings_idx,
            unitcell=unit_cell,
            **indexing_params,
        )

        config_settings = {
            **indexing_params,
            "data_from": self.inputs.intensity_filtered_data_url,
            "lattice_parameters": lattice_parameters,
            "lattice_space_group": space_group,
            "idx_for_gen": gen_rings_idx,
            "idx_for_score": score_rings_idx,
        }
        ubi_grains_group_name = save_nexus_grain_process(
            filename=nexus_file_path,
            entry_name=posixpath.dirname(intensity_filtered_data_group_path),
            process_name="indexed_grains",
            config_settings=config_settings,
            grains=grains,
            overwrite=overwrite,
        )
        self.outputs.indexed_grain_data_url = ubi_grains_group_name
