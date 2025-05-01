from ewokscore import Task
from pathlib import Path
import shutil
import posixpath

from ImageD11 import columnfile as PeakColumnFile
from silx.io.utils import DataUrl
from ..nexus import read_peaks_attributes, save_nexus_process, group_exists


class GeometryTransformation(
    Task,
    input_names=[
        "spatial_corrected_data_url",
        "geometry_par_file",
    ],
    optional_input_names=["overwrite"],
    output_names=["geometry_updated_data_url"],
):
    """
    Does the geometry Transformation on the detector spatial corrected 3d peaks
    and geometry parameter (.par) file,
    Inputs:
        'spatial_corrected_data_url'
        a detector spatial corrected 3d peaks nexus data group path and
        geometry file path a .par file
    This task performs the following operations:
    1. Gathers geometry information from the `geometry_tdxrd.par` file.
    2. Copy the geometry file in the directory structure:
            `analysis_folder / dset_name / (dset_name + sample_name)`.
            i.e the parent folder of 'detector_spatial_corrected_3d_peaks_file'
    3. Applies the geometry correction to the 3D peaks column file using
        the `ImageD11` dataset class.
    4. Save the geometry corrected 3d peaks columnfile (output: `geometry_updated_3d_peaks_file`)
    """

    def run(self):
        data_url = DataUrl(self.inputs.spatial_corrected_data_url)
        nexus_file_path = data_url.file_path()
        spatial_corrected_data_group_path = data_url.data_path()

        if not group_exists(nexus_file_path, spatial_corrected_data_group_path):
            raise FileNotFoundError(
                f""" File or Data Group not Found Error,
                Either it is missing nexus file path: {nexus_file_path} or
                spatial corrected data group path: {spatial_corrected_data_group_path}.
                """
            )

        geometry_par_file = self.inputs.geometry_par_file

        error_message = []
        if not Path(geometry_par_file).exists():
            error_message.append(f"Geometry file '{geometry_par_file}' not found.")

        if not geometry_par_file.endswith(".par"):
            error_message.append(
                f"Invalid geometry file '{geometry_par_file}'. Expected a '.par' file."
            )

        if error_message:
            raise ValueError("\n".join(error_message))

        overwrite = self.get_input_value("overwrite", False)
        geo_updated_data_group = f"{posixpath.dirname(spatial_corrected_data_group_path)}/geometry_updated_peaks"
        if not overwrite and group_exists(
            filename=nexus_file_path, data_group_path=geo_updated_data_group
        ):
            raise ValueError(
                f"""Data group '{geo_updated_data_group}' already exists in {nexus_file_path},
                Set `overwrite` to True if you wish to overwrite the existing data group.
                """
            )

        work_folder = Path(nexus_file_path).parent
        par_folder = work_folder / "par_folder"
        par_folder.mkdir(exist_ok=True)
        new_geometry_par_file = par_folder / "geometry_tdxrd.par"
        shutil.copy2(geometry_par_file, new_geometry_par_file)

        # following code is derived by refering:
        # https://github.com/FABLE-3DXRD/ImageD11/blob/master/ImageD11/sinograms/dataset.py
        # refer at function  update_colfile_pars()
        # https://github.com/FABLE-3DXRD/ImageD11/blob/master/ImageD11/parameters.py
        # refer at function loadparameters() in the class 'parameters' (yes it is a class not function)
        # https://github.com/FABLE-3DXRD/ImageD11/blob/master/ImageD11/columnfile.py
        # refer at function updateGeometry() in the class 'columnfile' (yes it is a class not function)
        # as for as my investigation, it does not do any computation,
        # but with the style of imageD11 library, it adds various geometry parameter from
        # geometry_tdxrd.par file into the column file,

        sp_corrected_3d_peaks = read_peaks_attributes(
            filename=nexus_file_path,
            process_group=spatial_corrected_data_group_path,
        )
        columnfile_3d = PeakColumnFile.colfile_from_dict(sp_corrected_3d_peaks)
        columnfile_3d.parameters.loadparameters(filename=str(new_geometry_par_file))
        columnfile_3d.updateGeometry()
        peaks_data = {}
        for key in ["ds", "eta", "gx", "gy", "gz", "tth", "xl", "yl", "zl"]:
            peaks_data[key] = columnfile_3d[key]

        nxprocess_url = save_nexus_process(
            filename=nexus_file_path,
            entry_name=posixpath.dirname(spatial_corrected_data_group_path),
            process_name="geometry_updated_peaks",
            peaks_data=peaks_data,
            config_settings=columnfile_3d.parameters.parameters,
            pks_axes=("ds", "eta"),
            signal_name="Number_of_pixels",
            scale="log",
            overwrite=overwrite,
            ln_pks_from_group_name=spatial_corrected_data_group_path,
        )
        self.outputs.geometry_updated_data_url = nxprocess_url
