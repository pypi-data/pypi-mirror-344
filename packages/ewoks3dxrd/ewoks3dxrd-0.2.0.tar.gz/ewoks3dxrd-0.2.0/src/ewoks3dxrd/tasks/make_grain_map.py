from __future__ import annotations

from pathlib import Path
import posixpath
from ewokscore import Task
from ImageD11 import grain as grainMod
from ..models import SampleConfig
from ..utils import (
    extract_sample_info,
    get_omega_slope,
    refine_grains,
    tmp_grain_processing_files,
)
from ..nexus import (
    get_data_url_paths,
    save_column_file_as_ascii,
    get_parameters,
    save_nexus_grain_process,
    check_throw_write_data_group_url,
)


class MakeGrainMap(
    Task,
    input_names=[
        "folder_file_config",
        "indexed_grain_data_url",
        "intensity_filtered_data_url",
        "hkl_tols",
        "minpks",
    ],
    optional_input_names=[
        "intensity_fine_filtered_data_url",
        "intensity_two_theta_range",
        "symmetry",
        "analyse_folder",
        "overwrite",
    ],
    output_names=["make_map_data_url"],
):
    """
    Does an iterative refinement based on `hkl_tols` followed by a fine refinement on the indexed grains

    Inputs:

    - `folder_file_config`: Output from Init Folder File Config Task as input here.
    - `indexed_grain_ubi_file`: indexed Grains ascii file path.
    - `intensity_filtered_data_url`: Filtered peaks data group path that were used for the indexing
    - `hkl_tols`: Decreasing sequence of hkl tolerances. Will be used for iterative refinement (one after the other).
    - `minpks`: To filter grains that are not associated with at least #minpks peaks after iterative refinement.
    - `lattice_name`: Use lattice parameter value from lattice par file referred by 'lattice_name'.par.

    Optional Inputs:

    - `intensity_fine_filtered_data_url`: Peaks used to refine the grains finely at the end of the iterative refinement.
        Default: `intensity_filtered_data_url`.
    - `intensity_two_theta_range`: tuple of two floats, giving two theta min and max when refining. Default: (0., 180.).
    - `symmetry` (str): Lattice symmetry used to further refine grains. Default: `cubic`.

    Outputs:
    - `ascii_grain_map_file`: file where the refined grains are saved
    """

    def run(self):
        nexus_file_path, intensity_filtered_data_group_path = get_data_url_paths(
            self.inputs.intensity_filtered_data_url
        )
        analyse_folder = self.get_input_value(
            "analyse_folder", Path(nexus_file_path).parent
        )
        flt_pks_file = Path(analyse_folder) / "flt_3d_peaks.flt"
        save_column_file_as_ascii(
            output_file_name=flt_pks_file,
            cf_file_path=nexus_file_path,
            cf_group_path=intensity_filtered_data_group_path,
        )

        intensity_fine_filtered_data_url = self.get_input_value(
            "intensity_fine_filtered_data_url", None
        )

        fine_filtered_data_url = (
            intensity_fine_filtered_data_url
            if intensity_fine_filtered_data_url
            else self.inputs.intensity_filtered_data_url
        )

        if fine_filtered_data_url == self.inputs.intensity_filtered_data_url:
            fine_flt_pks_file = flt_pks_file
        else:
            fine_nexus_file_path, fine_filtered_data_group_path = get_data_url_paths(
                fine_filtered_data_url
            )
            fine_flt_pks_file = Path(analyse_folder) / "fine_flt_3d_peaks.flt"
            save_column_file_as_ascii(
                output_file_name=fine_flt_pks_file,
                cf_file_path=fine_nexus_file_path,
                cf_group_path=fine_filtered_data_group_path,
            )

        overwrite = self.get_input_value("overwrite", False)

        make_map_ubi_data_group = (
            f"{posixpath.dirname(intensity_filtered_data_group_path)}/make_map_grains"
        )
        check_throw_write_data_group_url(
            overwrite=overwrite,
            filename=nexus_file_path,
            data_group_path=make_map_ubi_data_group,
        )

        cfg = SampleConfig(**self.inputs.folder_file_config)
        omega_motor = cfg.omega_motor
        scan_folder = cfg.scan_folder
        _, sample_name, dset_name, scan_number = extract_sample_info(
            path_str=scan_folder
        )
        master_file = Path(scan_folder).parent / f"{sample_name}_{dset_name}.h5"
        if not master_file.exists():
            raise FileNotFoundError(
                f"""Could not find HDF5 master file at {master_file}.
                    Check `scan_folder`, `sample_name` and `dset_name` in the `folder_file_config` input.
                """
            )

        minpks = self.inputs.minpks
        if minpks <= 0:
            raise ValueError("Input: 'minpks' should be a positive number")

        intensity_parameter = get_parameters(
            filename=nexus_file_path,
            process_group_name=intensity_filtered_data_group_path,
        )
        geo_par_url = f"{nexus_file_path}::{posixpath.dirname(intensity_filtered_data_group_path)}/geometry_updated_peaks"
        lat_par_url = intensity_parameter["data_from"]

        omega_slope = get_omega_slope(
            filepath=master_file, scan_number=scan_number, omega_motor=omega_motor
        )
        with tmp_grain_processing_files(
            ubi_data_url=self.inputs.indexed_grain_data_url,
            geo_par_data_url=geo_par_url,
            lat_par_data_url=lat_par_url,
        ) as (ubi_file, par_file):
            hkl_tols = self.inputs.hkl_tols
            intensity_tth_range = self.get_input_value(
                "intensity_two_theta_range", (0.0, 180.0)
            )
            symmetry = self.get_input_value("symmetry", "cubic")
            for tol in hkl_tols:
                iterative_refined_grains = refine_grains(
                    tolerance=tol,
                    intensity_tth_range=intensity_tth_range,
                    omega_slope=omega_slope,
                    parameter_file=par_file,
                    filtered_peaks_file=flt_pks_file,
                    ubi_file=ubi_file,
                    symmetry=symmetry,
                )
                iterative_refined_grains.savegrains(ubi_file, sort_npks=True)

            refined_grains = grainMod.read_grain_file(ubi_file)
            grains_filtered = [
                grain for grain in refined_grains if float(grain.npks) > minpks
            ]
            grainMod.write_grain_file(filename=ubi_file, list_of_grains=grains_filtered)

            # fine refinement
            fine_refined_grains = refine_grains(
                tolerance=hkl_tols[-1],
                intensity_tth_range=intensity_tth_range,
                omega_slope=omega_slope,
                parameter_file=par_file,
                filtered_peaks_file=fine_flt_pks_file,
                ubi_file=ubi_file,
                symmetry=symmetry,
            )

        ubi_grain_file = Path(analyse_folder) / "refined_grains_map_file.flt"
        fine_refined_grains.savegrains(str(ubi_grain_file), sort_npks=True)
        grains_list = grainMod.read_grain_file(filename=str(ubi_grain_file))

        refined_config = {
            "intensity_tth_range": intensity_tth_range,
            "symmetry": symmetry,
            "omega_slop": omega_slope,
            "hkl_tol": hkl_tols,
            "grains_came_from": self.inputs.indexed_grain_data_url,
            "peaks_came_from": self.inputs.intensity_filtered_data_url,
            "fine_peaks_came_from": fine_filtered_data_url,
            "minpks": minpks,
            "hkl_tol_seq": hkl_tols[-1],
            "symmetry": symmetry,
        }

        makemap_grains_group_name = save_nexus_grain_process(
            filename=nexus_file_path,
            entry_name=posixpath.dirname(intensity_filtered_data_group_path),
            process_name="make_map_grains",
            config_settings=refined_config,
            grains=grains_list,
            overwrite=True,
        )
        self.outputs.make_map_data_url = makemap_grains_group_name
