from ewokscore import Task
import posixpath
from ImageD11.unitcell import unitcell
from ..nexus import (
    read_peaks_attributes,
    save_nexus_process,
    get_data_url_paths,
    find_reciprocal_distance_tolerance,
    find_lattice_parameters,
    check_throw_write_data_group_url,
    find_wavelength,
)
from ..utils import do_filter_using_indexer


class FilterByIndexer(
    Task,
    input_names=[
        "intensity_filtered_data_url",
        "use_rings_for_index_filter",
    ],
    optional_input_names=["process_group_name", "overwrite"],
    output_names=["indexer_filtered_data_url"],
):
    """
    Filter the 3D merged peaks using Indexer, to be used only to grid indexer for producing grains.
    Inputs:

    - `intensity_filtered_data_url` (str): Data path to the intensity filtered 'NxProcess group data' peaks
    - `use_rings_for_index_filter` (tuple[int,...]): Tuple of int indicating the index of the ring, ex: (0,1,2)

    Optional Inputs:

    - `overwrite` (Bool): OverWrite permission if output nexus process group already exists.
    - `process_group_name` (str): 'Nexus group data name' to save the index filtered peaks, default: indexer_filtered_peaks

    Outputs:

    - `indexer_filtered_data_url` (str): Data path to 'NxProcess group data' Grains that stores generated UBI

    """

    def run(self):
        nexus_file_path, intensity_filtered_data_group_path = get_data_url_paths(
            self.inputs.intensity_filtered_data_url
        )
        process_group_name = self.get_input_value(
            "process_group_name", "indexer_filtered_peaks"
        )
        overwrite = self.get_input_value("overwrite", False)
        indexer_filtered_data_group = f"{posixpath.dirname(intensity_filtered_data_group_path)}/{process_group_name}"
        check_throw_write_data_group_url(
            overwrite=overwrite,
            filename=nexus_file_path,
            data_group_path=indexer_filtered_data_group,
        )

        intensity_filtered_peaks = read_peaks_attributes(
            filename=nexus_file_path, process_group=intensity_filtered_data_group_path
        )
        use_rings_for_index_filter = self.inputs.use_rings_for_index_filter
        phase_ds_tolerance = find_reciprocal_distance_tolerance(
            data_url_as_str=self.inputs.intensity_filtered_data_url
        )
        lattice_parameters, space_group = find_lattice_parameters(
            self.inputs.intensity_filtered_data_url
        )
        unit_cell = unitcell(
            lattice_parameters=lattice_parameters,
            symmetry=space_group,
        )
        wavelength = find_wavelength(self.inputs.intensity_filtered_data_url)
        index_filtered_peaks = do_filter_using_indexer(
            peak_3d_dict=intensity_filtered_peaks,
            unit_cell=unit_cell,
            wavelength=wavelength,
            phase_ds_tolerance=phase_ds_tolerance,
            use_rings_for_index_filter=use_rings_for_index_filter,
        )
        indexer_filter_config = {
            "dstol": phase_ds_tolerance,
            "rings_used": use_rings_for_index_filter,
            "data_from": self.inputs.intensity_filtered_data_url,
        }
        filtered_3d_peaks_dict = {}
        for key in index_filtered_peaks.keys():
            filtered_3d_peaks_dict[key] = index_filtered_peaks[key]

        nxprocess_url = save_nexus_process(
            filename=nexus_file_path,
            entry_name=posixpath.dirname(intensity_filtered_data_group_path),
            process_name=process_group_name,
            peaks_data=filtered_3d_peaks_dict,
            config_settings=indexer_filter_config,
            pks_axes=("ds", "eta"),
            signal_name="Number_of_pixels",
            scale="log",
            overwrite=overwrite,
        )
        self.outputs.indexer_filtered_data_url = nxprocess_url
