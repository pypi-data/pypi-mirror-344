from ewokscore import Task
import posixpath
from ImageD11 import columnfile as PeakColumnFile
from ImageD11.peakselect import sorted_peak_intensity_mask_and_cumsum
from ..nexus import (
    read_peaks_attributes,
    save_nexus_process,
    group_exists,
    get_data_url_paths,
)


class FilterByIntensity(
    Task,
    input_names=[
        "lattice_filtered_data_url",
        "intensity_frac",
    ],
    optional_input_names=["process_group_name", "overwrite"],
    output_names=["intensity_filtered_data_url"],
):
    """
    Does the Intensity based peaks filter,
        computes intensity metric based on sum_intensity, ds (reciprocal distance) columns from the input file
        normalize with the maximum value of intensity metric,
        only keeps the rows whose value is above the given input 'intensity_frac'
        and save them in ascii (.flt) and .h5 format.

    Inputs:

    - `lattice_filtered_data_url`: a 3d peaks data group, it is must be corrected for geometry and detector
    - `intensity_frac`: float value to remove the peaks row whose intensity metric below than this value.

    Outputs:

    - `intensity_filtered_data_url` (str): Data path to the intensity filtered 'NxProcess group data' peaks
    """

    def run(self):
        nexus_file_path, lattice_filtered_data_group_path = get_data_url_paths(
            self.inputs.lattice_filtered_data_url
        )

        intensity_frac = self.inputs.intensity_frac
        lattice_filtered_peaks = read_peaks_attributes(
            filename=nexus_file_path, process_group=lattice_filtered_data_group_path
        )
        cf = PeakColumnFile.colfile_from_dict(lattice_filtered_peaks)
        mask, _ = sorted_peak_intensity_mask_and_cumsum(colf=cf, frac=intensity_frac)
        cf.filter(mask)
        process_group_name = self.get_input_value(
            "process_group_name", "intensity_filtered_peaks"
        )
        overwrite = self.get_input_value("overwrite", False)
        intensity_filtered_data_group = f"{posixpath.dirname(lattice_filtered_data_group_path)}/{process_group_name}"
        if not overwrite and group_exists(
            filename=nexus_file_path, data_group_path=intensity_filtered_data_group
        ):
            raise ValueError(
                f"""Data group '{intensity_filtered_data_group}' already exists in {nexus_file_path},
                Set `overwrite` to True if you wish to overwrite the existing data group.
                Or provide a (new) data group name to optional input 'process_group_name'.
                """
            )

        intensity_config = {
            "intensity_frac": intensity_frac,
            "data_from": f"{nexus_file_path}::{lattice_filtered_data_group_path}",
        }
        filtered_3d_peaks_dict = {}
        for key in cf.keys():
            filtered_3d_peaks_dict[key] = cf[key]

        nxprocess_url = save_nexus_process(
            filename=nexus_file_path,
            entry_name=posixpath.dirname(lattice_filtered_data_group_path),
            process_name=process_group_name,
            peaks_data=filtered_3d_peaks_dict,
            config_settings=intensity_config,
            pks_axes=("ds", "eta"),
            signal_name="Number_of_pixels",
            scale="log",
            overwrite=overwrite,
        )
        self.outputs.intensity_filtered_data_url = nxprocess_url
