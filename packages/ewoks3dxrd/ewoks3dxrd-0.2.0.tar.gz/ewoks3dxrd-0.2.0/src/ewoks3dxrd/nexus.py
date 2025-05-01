from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional, Tuple

import h5py
import numpy as np
from ImageD11 import columnfile as PeakColumnFile
from ImageD11 import grain as grainmod
from ImageD11.grain import grain as Grain
from silx.io.utils import DataUrl, h5py_read_dataset


class GroupNotFound(FileNotFoundError):
    def __init__(self, file_path: str, data_path: str | None):
        super().__init__(
            f""" File or Data Group not Found Error,
            Either it is missing nexus file path: {file_path} or
            process data group path: {data_path}.
            """
        )


def group_exists(filename: str | Path, data_group_path: str) -> bool:
    if isinstance(filename, str):
        filename = Path(filename)
    if not filename.exists():
        return False

    with h5py.File(filename, "r") as file:
        if data_group_path in file:
            return True
    return False


def check_throw_write_data_group_url(
    overwrite: bool, filename: str | Path, data_group_path: str
):
    if not overwrite and group_exists(
        filename=filename, data_group_path=data_group_path
    ):
        raise ValueError(
            f"""Data group '{data_group_path}' already exists in {filename},
            Set `overwrite` to True if you wish to overwrite the existing data group.
            """
        )


def get_data_url_paths(data_url_as_str: str) -> Tuple[str, str]:
    data_url = DataUrl(data_url_as_str)
    file_path = data_url.file_path()
    data_path = data_url.data_path()
    if data_path is None or not group_exists(file_path, data_path):
        raise GroupNotFound(file_path, data_path)

    return file_path, data_path


def save_column_file_as_ascii(
    output_file_name: str | Path, cf_file_path: str | Path, cf_group_path: str
):
    """
    Creating an ascii filter file (ImageD11 specific) from the nexus stored process group peaks data.
    """
    peaks_dict = read_peaks_attributes(
        filename=cf_file_path, process_group=cf_group_path
    )
    cf = PeakColumnFile.colfile_from_dict(peaks_dict)

    cf.writefile(output_file_name)


def _save_parameters(
    parent_group: h5py.Group,
    config_settings: dict[str, Any],
    group_name: str = "parameters",
):
    """
    Helper function to place the config_settings in 'param_name' group
    in the given `parent_group`
    """
    parameters_group = parent_group.require_group(group_name)
    parameters_group.attrs["NX_class"] = "NXcollection"

    for key, value in config_settings.items():
        if key in parameters_group:
            del parameters_group[key]
        parameters_group.create_dataset(
            key, data=value if value is not None else "None"
        )


def create_parameters_group(
    group_path: h5py.Group,
    config_settings: dict[str, Any] | dict[str, dict[str, Any]],
):
    if isinstance(config_settings, dict) and all(
        isinstance(value, dict) for value in config_settings.values()
    ):
        parameters_group = group_path.require_group("parameters")
        parameters_group.attrs["NX_class"] = "NXcollection"
        for param_name, param_values in config_settings.items():
            _save_parameters(
                parent_group=parameters_group,
                config_settings=param_values,
                group_name=param_name,
            )
    else:
        _save_parameters(parent_group=group_path, config_settings=config_settings)


def create_nexus_peaks_data_group(
    group_path: h5py.Group,
    peaks_data: dict[str, np.ndarray],
    pks_axes: Tuple[str, str],
    signal_name: str,
    scale: str,
    soft_ln_pks_path: Optional[str] = None,
) -> str:

    peak_data_group = group_path.require_group("peaks")
    peak_data_group.attrs["NX_class"] = "NXdata"
    for key, value in peaks_data.items():
        peak_data_group.create_dataset(key, data=value)

    if soft_ln_pks_path:
        soft_ln_pks_group = group_path.file[soft_ln_pks_path]
        if "peaks" in soft_ln_pks_group:
            soft_link_peaks = soft_ln_pks_group["peaks"]
            for key in soft_link_peaks.keys():
                if key not in peak_data_group:
                    peak_data_group[key] = h5py.SoftLink(soft_link_peaks[key].name)

    peak_data_group.attrs["axes"] = pks_axes
    peak_data_group.attrs["signal"] = signal_name

    if scale not in ["log", "linear"]:
        raise ValueError("scale must be 'log' or 'linear'")

    peak_data_group.attrs["scale"] = scale
    return peak_data_group.name


def create_nexus_grains_data_group(
    group_path: h5py.Group,
    grains: List[Grain],
) -> str:

    grain_data_group = group_path.require_group("grains")
    grain_data_group.attrs["NX_class"] = "NXdata"
    num_grains = len(grains)
    ubi_matrices = np.zeros((num_grains, 3, 3), dtype=grains[0].ubi.dtype)
    translations = np.full((num_grains, 3), fill_value=np.nan)

    ubi_matrices = grain_data_group.create_dataset(
        "UBI", shape=(num_grains, 3, 3), dtype=grains[0].ubi.dtype
    )
    translations = grain_data_group.create_dataset(
        "translation", shape=(num_grains, 3), dtype=grains[0].ubi.dtype
    )
    npks = grain_data_group.create_dataset("npks", shape=(num_grains,), dtype=np.int64)
    nuniq = grain_data_group.create_dataset(
        "nuniq", shape=(num_grains,), dtype=np.int64
    )
    for i, grain in enumerate(grains):
        ubi_matrices[i] = grain.ubi
        if hasattr(grain, "translation"):
            translations[i] = grain.translation
        if hasattr(grain, "npks"):
            npks[i] = grain.npks
        if hasattr(grain, "nuniq"):
            nuniq[i] = grain.nuniq

    return grain_data_group.name


def save_nexus_process(
    filename: str | Path,
    entry_name: str,
    process_name: str,
    peaks_data: dict[str, np.ndarray],
    config_settings: dict[str, Any] | dict[str, dict[str, Any]],
    pks_axes: Tuple[str, str],
    signal_name: str,
    scale: str,
    overwrite: bool = False,
    ln_pks_from_group_name: Optional[str] = None,
) -> str:

    with h5py.File(filename, "a") as h5_file:
        entry = h5_file.require_group(entry_name)
        entry.attrs["NX_class"] = "NXentry"

        if process_name in entry:
            if overwrite:
                del entry[process_name]
            else:
                raise FileExistsError(
                    f"""IN the nexus process file name {filename}, there is already a
                    nexus process group {process_name} exists.
                    To overwrite provide a overwrite permission.
                    """
                )

        process_group = entry.create_group(process_name)
        process_group.attrs["NX_class"] = "NXprocess"
        create_nexus_peaks_data_group(
            group_path=process_group,
            peaks_data=peaks_data,
            soft_ln_pks_path=ln_pks_from_group_name,
            pks_axes=pks_axes,
            signal_name=signal_name,
            scale=scale,
        )
        create_parameters_group(
            group_path=process_group,
            config_settings=config_settings,
        )
        return f"{filename}::{process_group.name}"


def save_nexus_grain_process(
    filename: str | Path,
    entry_name: str,
    process_name: str,
    config_settings: dict[str, Any] | dict[str, dict[str, Any]],
    grains: List[Grain],
    overwrite: bool = False,
) -> str:
    with h5py.File(filename, "a") as h5_file:
        entry = h5_file.require_group(entry_name)
        entry.attrs["NX_class"] = "NXentry"
        if process_name in entry:
            if overwrite:
                del entry[process_name]
            else:
                raise FileExistsError(
                    f"""In the nexus process file name {filename}, there is already a
                    nexus process group {process_name} exists.
                    To overwrite provide a overwrite permission.
                    """
                )

        process_group = entry.create_group(process_name)
        process_group.attrs["NX_class"] = "NXprocess"
        create_nexus_grains_data_group(
            group_path=process_group,
            grains=grains,
        )
        create_parameters_group(
            group_path=process_group,
            config_settings=config_settings,
        )
        return f"{filename}::{process_group.name}"


def read_peaks_attributes(
    filename: str | Path, process_group: str
) -> dict[str, np.ndarray]:
    """
    Extract peaks column data stored in {entry_name}/{process_name}/peaks
    Inputs:
        filename: file path to .h5 file
        entry_name: entry point inside .h5 file
        process_name: group name inside the entry point
    """
    with h5py.File(filename, "r") as f:
        peaks_group = f[f"{process_group}/peaks"]
        return {name: dataset[()] for name, dataset in peaks_group.items()}


def read_grains_attributes(filename: str | Path, process_group: str) -> dict[str, list]:
    with h5py.File(filename, "r") as h5file:
        grain_group = h5file[f"{process_group}/grains"]
        return {name: dataset[()] for name, dataset in grain_group.items()}


def create_nexus_ubi(
    grains: List[Grain],
    entry_name: str,
    grain_file: str | Path,
    grain_settings: dict[str, Any],
    peaks_path: Tuple[str | Path, str],
):
    """
    Create nexus file with entry_name place the grains (list of UBIs)
    and also link the peaks used to generate these UBIS as external link
    """
    with h5py.File(grain_file, "w") as gf:
        entry = gf.create_group(entry_name)
        entry.attrs["NX_class"] = "NXentry"
        grain_group = entry.create_group("indexed_grains")
        grain_group.attrs["NX_class"] = "NXprocess"
        grain_group["peaks"] = h5py.ExternalLink(peaks_path[0], peaks_path[1])
        ubi_group = grain_group.create_group("UBI")
        ubi_group.attrs["NX_class"] = "NXdata"
        ubi_matrices = ubi_group.create_dataset(
            "UBI", shape=(len(grains), 3, 3), dtype=grains[0].ubi.dtype
        )
        for i, grain in enumerate(grains):
            ubi_matrices[i] = grain.ubi
        create_parameters_group(
            parent_group=grain_group, config_settings=grain_settings
        )


def create_nexus_grains(
    grains: List[Grain],
    entry_name: str,
    grain_file: str | Path,
    grain_settings: dict[str, Any],
    grain_group_name: str,
):
    num_grains = len(grains)
    with h5py.File(grain_file, "a") as gf:
        entry = gf[entry_name]
        grp = entry.create_group(grain_group_name)
        grp.attrs["NX_class"] = "NXprocess"
        grains_gr = grp.create_group("grains")
        grains_gr.attrs["NX_class"] = "NXdata"

        ubi_matrices = grains_gr.create_dataset(
            "UBI", shape=(num_grains, 3, 3), dtype=grains[0].ubi.dtype
        )
        translations = grains_gr.create_dataset(
            "translation", shape=(num_grains, 3), dtype=grains[0].ubi.dtype
        )
        npks = grains_gr.create_dataset("npks", shape=(num_grains,), dtype=np.int64)
        nuniq = grains_gr.create_dataset("nuniq", shape=(num_grains,), dtype=np.int64)
        for i, grain in enumerate(grains):
            ubi_matrices[i] = grain.ubi
            translations[i] = grain.translation
            npks[i] = grain.npks
            nuniq[i] = grain.nuniq

        create_parameters_group(parent_group=grp, config_settings=grain_settings)


def save_indexed_grains_as_ascii(
    grain_file_h5: str | Path,
    process_group_path: str,
    grain_file_ascii: str | Path,
):
    """
    Function to extract grains that generated by Indexing function,
    which is simpler, i.e it only has UBI matrices.
    """
    grains_list = []
    with h5py.File(grain_file_h5, "r") as gf:
        ubi_dataset = gf[f"{process_group_path}/grains/UBI"]
        for ubi_matrix in ubi_dataset:
            grains_list.append(Grain(ubi=ubi_matrix))

    grainmod.write_grain_file(grain_file_ascii, grains_list)


def read_grains(
    grain_file_h5: str | Path, entry_name: str, process_group_name: str
) -> List[Grain]:

    grains_list = []
    with h5py.File(grain_file_h5, "r") as gf:
        entry = gf[f"{entry_name}/{process_group_name}/grains"]
        for i in range(entry["translation"][()].shape[0]):
            gr = Grain.grain(ubi=entry["UBI"][i], translation=entry["translation"][i])
            gr.npks = entry["npks"][i]
            gr.nuniq = entry["nuniq"][i]
            grains_list.append(gr)
    return grains_list


def get_omega_array(
    filename: str | Path, entry_name: str, process_group_name: str
) -> np.ndarray:
    with h5py.File(filename, "r") as f:
        entry = f[f"{entry_name}/{process_group_name}"]
        folder_grp = entry["parameters/FolderFileSettings"]
        masterfile = h5py_read_dataset(dset=folder_grp["masterfile"])
        scan_number = h5py_read_dataset(dset=folder_grp["scan_number"])
        omegamotor = h5py_read_dataset(dset=folder_grp["omegamotor"])
        with h5py.File(masterfile, "r") as hin:
            omega_angles = hin[f"{scan_number}.1/measurement"][omegamotor]
            return h5py_read_dataset(dset=omega_angles)


def find_lattice_parameters(data_url_as_str: str) -> Tuple[np.ndarray, int]:
    lattice_params = find_parameter(data_url_as_str, key="lattice_parameters")
    symmetry = find_parameter(data_url_as_str, key="lattice_space_group")

    return lattice_params, int(symmetry)


def find_wavelength(data_url_as_str: str) -> float:
    return np.float64(find_parameter(data_url_as_str, key="wavelength"))


def find_reciprocal_distance_tolerance(data_url_as_str: str) -> float:
    return np.float64(find_parameter(data_url_as_str, key="dstol"))


def get_lattice_parameters(
    filename: str | Path, entry_name: str, process_group_name: str
) -> Tuple[np.ndarray, int]:
    return find_lattice_parameters(f"{filename}::/{entry_name}/{process_group_name}")


def get_wavelength(
    filename: str | Path, entry_name: str, process_group_name: str
) -> float:
    return find_wavelength(f"{filename}::/{entry_name}/{process_group_name}")


def get_parameters(filename: str | Path, process_group_name: str) -> dict[str, str]:
    return get_parameter(f"{filename}::{process_group_name}", key=None)


def get_parameter(data_url_as_str: str, key: str | None):
    file_path, data_path = get_data_url_paths(data_url_as_str)

    with h5py.File(file_path, "r") as h5file:
        parameters: h5py.Group = h5file[f"{data_path}/parameters"]
        if key is None:
            return {k: h5py_read_dataset(dset=v) for k, v in parameters.items()}

        if key not in parameters:
            return None

        return h5py_read_dataset(h5file[f"{data_path}/parameters/{key}"])


def find_parameter(data_url_as_str: str, key: str):
    value = get_parameter(data_url_as_str, key=key)
    if value is not None:
        return value

    data_from = get_parameter(data_url_as_str, key="data_from")
    if data_from is None:
        raise KeyError(f"Could not find {key} nor 'data_from' in {data_url_as_str}")

    data_from_value = find_parameter(data_from, key=key)
    if data_from_value is None:
        raise KeyError(f"Could not find {key} in {data_from}/parameters.")

    return data_from_value


def save_geometry_and_lattice_par_file(
    file_path: str | Path, geom_dict: dict[str, Any], lattice_dict: dict[str, Any]
):
    with open(file_path, "w") as f:
        lattice_params = lattice_dict.get("lattice_parameters", [])
        if len(lattice_params) != 6:
            raise ValueError(
                f"Expected a list of 6 lattice params. Got {lattice_params}"
            )
        f.write(f"cell__a {lattice_params[0]}\n")
        f.write(f"cell__b {lattice_params[1]}\n")
        f.write(f"cell__c {lattice_params[2]}\n")
        f.write(f"cell_alpha {lattice_params[3]}\n")
        f.write(f"cell_beta {lattice_params[4]}\n")
        f.write(f"cell_gamma {lattice_params[5]}\n")

        if "lattice_space_group" in lattice_dict:
            f.write(
                f"cell_lattice_[P,A,B,C,I,F,R] {lattice_dict['lattice_space_group']}\n"
            )

        for key, value in geom_dict.items():
            f.write(f"{key} {value}\n")
