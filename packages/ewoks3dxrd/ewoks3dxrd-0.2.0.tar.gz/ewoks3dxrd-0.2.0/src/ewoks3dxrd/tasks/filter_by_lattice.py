from ewokscore import Task
from pathlib import Path
import posixpath
import shutil
from ImageD11 import columnfile as PeakColumnFile
from ..utils import read_lattice_cell_data
from ImageD11.unitcell import unitcell
from ImageD11.peakselect import filter_peaks_by_phase
from silx.io.utils import DataUrl
from ..nexus import read_peaks_attributes, save_nexus_process, group_exists


class FilterByLattice(
    Task,
    input_names=[
        "geometry_updated_data_url",
        "lattice_par_file",
        "reciprocal_dist_tol",
    ],
    optional_input_names=["reciprocal_dist_max", "process_group_name", "overwrite"],
    output_names=["lattice_filtered_data_url", "copied_lattice_par_file"],
):
    """
    Performs Lattice/Phase-based filtering on a geometry-transformed 3D peaks file.

    This process applies filtering based on 'reciprocal distance' and 'lattice' rings ds criteria
    to extract relevant peaks.

    ### Steps:
    1. **Initial Filtering:**
        - Copies the input geometry-transformed 3D peaks file.
        - Reads the `ds` column and removes rows where `ds` exceeds the specified `reciprocal_dist_max` value.

    2. **Lattice-Based Filtering:**
        - Computes ideal lattice ring `ds` values (reciprocal distances from the origin).
        - Further filters peaks based on these values, using the tolerance defined by `reciprocal_dist_tol`.

    3. **File Storage:**
        - Saves the lattice-filtered 3D peaks file as
            `{Lattice_name}_{reciprocal_dist_max_tag}_filtered_3d_peaks.h5,flt`
            in the parent directory of the input file ('geometry_trans_3d_peaks_file').

    Additionally, if the specified `lattice_par_file` is not present in the sample analysis path,
    it is copied to `"par_folder/{lattice_par_file}"`.

    ### Inputs
    - `geometry_updated_data_url` (str): Data Path to the geometry-transformed `NxProcess group data` peaks.
    - `lattice_par_file` (str): Path to the `.par` file containing lattice parameters and space group information.
    - `reciprocal_dist_max` (float): Maximum reciprocal distance for filtering (an Optional Value)
        If it is not provided, then maximum value in the `ds` column from input file will be used.
    - `reciprocal_dist_tol` (float): Tolerance for peak inclusion near lattice rings.
    - `process_group_name` (str): Optional Nexus process group name. Default: "phase_filtered_peaks."
    ### Outputs
    - `lattice_filtered_data_url` (str): Data path to the lattice filtered 'NxProcess group data' peaks
    - `copied_lattice_par_file` (str): Path to the copied lattice parameter file stored within the analysis folder.
    """

    def run(self):
        data_url = DataUrl(self.inputs.geometry_updated_data_url)
        nexus_file_path = data_url.file_path()
        geometry_updated_data_group_path = data_url.data_path()
        if not group_exists(nexus_file_path, geometry_updated_data_group_path):
            raise FileNotFoundError(
                f""" File or Data Group not Found Error,
                Either it is missing nexus file path: {nexus_file_path} or
                geometry updated data group path: {geometry_updated_data_group_path}.
                """
            )

        overwrite = self.get_input_value("overwrite", False)
        process_group_name = self.get_input_value(
            "process_group_name", "phase_filtered_peaks"
        )
        phase_filtered_data_group = f"{posixpath.dirname(geometry_updated_data_group_path)}/{process_group_name}"
        if not overwrite and group_exists(
            filename=nexus_file_path, data_group_path=phase_filtered_data_group
        ):
            raise ValueError(
                f"""Data group '{phase_filtered_data_group}' already exists in {nexus_file_path},
                Set `overwrite` to True if you wish to overwrite the existing data group.
                Or provide a (new) data group name to optional input 'process_group_name'.
                """
            )

        lattice_par_file = Path(self.inputs.lattice_par_file)
        dstar_tol = self.inputs.reciprocal_dist_tol
        error_message = []
        if not lattice_par_file.exists():
            error_message.append(
                f"Provided Lattice file '{lattice_par_file}' does not exist."
            )
        if lattice_par_file.suffix != ".par":
            error_message.append(
                f"Provided Lattice file '{lattice_par_file}' is not a .par file"
            )
        if error_message:
            raise ValueError("\n".join(error_message))

        lattice_file_in_par_folder = (
            Path(nexus_file_path).parent / "par_folder" / lattice_par_file.name
        )

        lattice_file_in_par_folder.parent.mkdir(exist_ok=True)
        shutil.copy2(lattice_par_file, lattice_file_in_par_folder)

        geo_updated_peaks = read_peaks_attributes(
            filename=nexus_file_path,
            process_group=geometry_updated_data_group_path,
        )
        g_trans_peaks_3d = PeakColumnFile.colfile_from_dict(geo_updated_peaks)
        unit_cell_parameters = read_lattice_cell_data(lattice_par_file)

        lattice_name = lattice_par_file.stem
        reciprocal_dist_max: float | None = self.get_input_value(
            "reciprocal_dist_max", None
        )
        dstar_max = (
            reciprocal_dist_max if reciprocal_dist_max else g_trans_peaks_3d.ds.max()
        )
        cf = g_trans_peaks_3d.copyrows(g_trans_peaks_3d.ds <= dstar_max)
        ucell = unitcell(
            lattice_parameters=unit_cell_parameters.lattice_parameters,
            symmetry=unit_cell_parameters.space_group,
        )
        ucell.makerings(limit=g_trans_peaks_3d.ds.max())

        filtered_peaks_cf = filter_peaks_by_phase(
            cf=cf, dstol=dstar_tol, dsmax=dstar_max, cell=ucell
        )

        lattice_phase_filt_config = {
            "lattice_name": lattice_name,
            "lattice_parameters": unit_cell_parameters.lattice_parameters,
            "lattice_space_group": unit_cell_parameters.space_group,
            "dsmax": dstar_max,
            "dstol": dstar_tol,
            "data_from": f"{nexus_file_path}::{geometry_updated_data_group_path}",
        }

        filtered_3d_peaks_dict = {}
        for key in filtered_peaks_cf.keys():
            filtered_3d_peaks_dict[key] = filtered_peaks_cf[key]

        nxprocess_url = save_nexus_process(
            filename=nexus_file_path,
            entry_name=posixpath.dirname(geometry_updated_data_group_path),
            process_name=process_group_name,
            peaks_data=filtered_3d_peaks_dict,
            config_settings=lattice_phase_filt_config,
            pks_axes=("ds", "eta"),
            signal_name="Number_of_pixels",
            scale="log",
            overwrite=overwrite,
        )

        self.outputs.lattice_filtered_data_url = nxprocess_url
        self.outputs.copied_lattice_par_file = str(lattice_file_in_par_folder)
