from ewokscore import Task

import posixpath

from ..utils import do_spatial_correction
from ..nexus import read_peaks_attributes, save_nexus_process, group_exists
from silx.io.utils import DataUrl


class DetectorSpatialCorrection(
    Task,
    input_names=["segmented_peaks_url", "correction_files"],
    optional_input_names=["overwrite"],
    output_names=[
        "spatial_corrected_data_url",
    ],
):
    """
    Does the detector spatial correction on the segmented 3d peaks and saves the corrected 3D column peak file

    Inputs:

    - `segmented_peaks_url`: a segmented 3d peaks data group data url
    - `correction_files`: two corrections are possible:
        - Spline correction: `correction_files` should be a string containing the path to the spline file
        - e2dx,e2dy correction: `correction_files` should be a tuple of 2 strings, the first one being the path to e2dx file, the second the path to the e2dy file
        - any other type will be treated as invalid input

    Outputs:
    - `spatial_corrected_data_url`: A Nexus file path along with data entry point to `spatial_corrected_peaks` data group
    """

    def run(self):
        data_url = DataUrl(self.inputs.segmented_peaks_url)
        nexus_file_path = data_url.file_path()
        segmented_data_group_path = data_url.data_path()

        if not group_exists(nexus_file_path, segmented_data_group_path):
            raise FileNotFoundError(
                f""" File or Data Group not Found Error,
                Either it is missing nexus file path: {nexus_file_path} or
                segmented data group path: {segmented_data_group_path}.
                """
            )

        overwrite = self.get_input_value("overwrite", False)
        sp_corrected_data_group = (
            f"{posixpath.dirname(segmented_data_group_path)}/spatial_corrected_peaks"
        )
        if not overwrite and group_exists(
            filename=nexus_file_path, data_group_path=sp_corrected_data_group
        ):
            raise ValueError(
                f"""Data group '{sp_corrected_data_group}' already exists in {nexus_file_path},
                Set `overwrite` to True if you wish to overwrite the existing data group.
                """
            )

        segmented_3d_peaks = read_peaks_attributes(
            filename=nexus_file_path,
            process_group=segmented_data_group_path,
        )
        detector_spatial_correction_file_lists = self.inputs.correction_files
        columnfile_3d = do_spatial_correction(
            segmented_3d_peaks, detector_spatial_correction_file_lists
        )
        peaks_data = {"sc": columnfile_3d["sc"], "fc": columnfile_3d["fc"]}
        spatial_correction_config = {
            "correction_files": detector_spatial_correction_file_lists,
            "in_peaks_data_from": data_url.path(),
        }

        nxprocess_url = save_nexus_process(
            filename=nexus_file_path,
            entry_name=posixpath.dirname(segmented_data_group_path),
            process_name="spatial_corrected_peaks",
            peaks_data=peaks_data,
            config_settings=spatial_correction_config,
            pks_axes=("fc", "sc"),
            signal_name="Number_of_pixels",
            scale="log",
            overwrite=overwrite,
            ln_pks_from_group_name=segmented_data_group_path,
        )
        self.outputs.spatial_corrected_data_url = nxprocess_url
