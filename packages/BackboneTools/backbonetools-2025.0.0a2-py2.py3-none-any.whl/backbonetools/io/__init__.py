import platform
import subprocess as sp
from pathlib import Path

import pandas as pd
from gams import SV_EPS, GamsWorkspace

from backbonetools.io.inputs import BackboneInput as BackboneInput
from backbonetools.io.outputs import BackboneResult as BackboneResult
from backbonetools.io.outputs import \
    BackboneScenarioAnalysis as BackboneScenarioAnalysis


def excel_to_frame_dict(xl_path):
    # read the excel file
    frame_dict = {}
    with pd.ExcelFile(xl_path) as xl:
        # iterate over sheets and write them as csv into csv_dir
        for name in xl.sheet_names:
            df = pd.read_excel(xl, name)
            frame_dict[name] = df

    return frame_dict


def excel_to_csvs(xl_path, csv_dir_parent="backbone_input/versioned", overwrite=False):
    """converts an excel file to a directory of .csv files where each .csv filename corresponds to a sheet of the excel file

    Args:
        xl_path (str): Path to the excel file
        csv_dir (str, optional): Path to the directory in which the csv directory will be created. Name of the csv_dir will be derived from exel file name.
        overwrite (bool, optional): Wether or not to overwrite existing files. Defaults to False.
    """
    # if no specific directory was passed, create directory name from filename
    csv_dir_name = Path(xl_path).stem
    csv_dir = Path(csv_dir_parent).joinpath(csv_dir_name).resolve()

    # create directory
    csv_dir.mkdir(exist_ok=overwrite, parents=True)

    # read excel contents
    frame_dict = excel_to_frame_dict(xl_path)

    # write contents to csvs
    frame_dict_to_csvs(frame_dict, csv_dir)


def excel_to_gdx(xl_path, gdx_path=None):
    """converts an excel file to a gdx file (both could be used as backbone inputs)

    Args:
        xl_path (str): path to excel file
        gdx_path (str): path to gdx file
    """
    if gdx_path is None:
        gdx_path = Path(xl_path).as_posix().replace(".xlsx", ".gdx")

    if platform.system() == "Windows":
        sp_output = sp.run(
            ["gdxxrw", xl_path, f"output={gdx_path}", "index=index!"], stdout=sp.PIPE
        )
        assert sp_output.returncode == 0, AssertionError(
            f"gdxxrw returned {sp_output.returncode}. Output was:\n{sp_output.stdout.decode()}"
        )
    else:
        frames = excel_to_frame_dict(xl_path)
        frame_dict_to_gdx(frames, gdx_path)
    if gdx_path is None:
        gdx_path = Path(xl_path).as_posix().replace(".xlsx", ".gdx")

    if platform.system() == "Windows":
        sp_output = sp.run(
            ["gdxxrw", xl_path, f"output={gdx_path}", "index=index!"], stdout=sp.PIPE
        )
        assert sp_output.returncode == 0, AssertionError(
            f"gdxxrw returned {sp_output.returncode}. Output was:\n{sp_output.stdout.decode()}"
        )
    else:
        frames = excel_to_frame_dict(xl_path)
        frame_dict_to_gdx(frames, gdx_path)

    return gdx_path

    return gdx_path


def csvs_to_frame_dict(csv_dir):
    dir_path = Path(csv_dir)
    files = [f for f in dir_path.iterdir() if f.name.endswith(".csv")]

    frame_dict = {}
    for file in files:
        try:
            df = pd.read_csv(file)
            # if a column contains non-numeric values e.g. "eps", it is parsed as str
            # strings are written to excel with preceding ' which results in a backbone error
            for col in df.columns:
                # find indices of eps
                if "eps" in df[col].values:
                    soon_zeros = df[col] == "eps"
                    # set others to be floats
                    df[col] = df[col][~soon_zeros].astype(float)

        except pd.io.parsers.EmptyDataError:
            print(f"{file} is empty.")
            df = pd.DataFrame()
        except Exception as e:
            e.args = (f"error occured with {file}:", *e.args)
            raise e  # Exception(f"error occured with {file}:", e.with_traceback())
        frame_dict[file.stem] = df

    return frame_dict


def csvs_to_excel(csv_dir, xl_path=None, overwrite=False):
    dir_path = Path(csv_dir)

    frame_dict = csvs_to_frame_dict(csv_dir)

    if not xl_path:
        xl_path = Path("results").joinpath(f"{dir_path.name}.xlsx")

    frame_dict_to_excel(frame_dict, xl_path)


def frame_dict_to_excel(frame_dict, xl_path):
    with pd.ExcelWriter(xl_path) as writer:
        for key in frame_dict:
            frame_dict[key].to_excel(writer, sheet_name=key, index=False)


def frame_dict_to_csvs(
    frames_dict, csv_dir="backbone_input/versioned/default", overwrite=True
):

    csv_dir = Path(csv_dir).resolve()
    csv_dir.mkdir(exist_ok=overwrite, parents=True)

    for key in frames_dict.keys():
        frames_dict[key].to_csv(f"{csv_dir}/{key}.csv", index=False)
    print("written frames as csvs to ", csv_dir)


def frame_dict_to_gdx(frames_dict, gdx_path, ws_dir=Path(__file__).parent.parent):
    """Writes the dict of pandas.DataFrames to a gdx file.

    Args:
        frames_dict (dict): dict of pd.DataFrames
        gdx_path (str):

    """
    # GamsWorkspace needs to be initialized so that relative paths supplied by snakemake workout
    ws = GamsWorkspace(ws_dir)
    db = ws.add_database()
    lookup_df = frames_dict["index"].set_index("Symbol")

    sheet_diff = set(frames_dict.keys()).difference(frames_dict["index"]["Symbol"])
    assert sheet_diff == {"index"}, AssertionError(
        f"Expected to find only a missing index sheet, but got {sheet_diff}"
    )

    for sheet_key in lookup_df.index:
        gams_type = lookup_df.loc[sheet_key, "Type"]

        if gams_type.lower() == "par":
            # print(sheet_key)
            add_param_to_gdx_db(sheet_key, frames_dict, db)
        else:
            # print(sheet_key)
            add_set_to_gdx_db(sheet_key, frames_dict, db)

    db.export(gdx_path)


def add_param_to_gdx_db(sheet_name, frames_dict, gams_db, debug=False):
    """
    in backbone, the sheet_name of the excel file (= the file name of the csv)
    corresponds to the parameter/set name.
    """
    lookup_df = frames_dict["index"].set_index("Symbol")

    r_dim = lookup_df.loc[sheet_name, ["Rdim", "Cdim"]].sum().astype(int)
    r_dim = int(r_dim)  # gams doesn't like numpy.int32 from above
    # add 1 to dimension for values
    if sheet_name in [
        "p_groupPolicyUnit",
        "p_s_discountFactor",
        "p_groupPolicyEmission",
    ]:
        # theres something funky going on with these two parameters
        slice_mod = 1
    else:
        slice_mod = 0
    param = gams_db.add_parameter(sheet_name, r_dim)
    for index, row in frames_dict[sheet_name].iterrows():
        # index should correspond to dimensionality
        # e.g. for p_gnn -> this is grid,node,node (3 dimensions)
        # any entries with index higher than dimension are corresponding values e.g. "transfercap"
        dim_index = tuple(row[: r_dim - 1 + slice_mod].values)
        for column_key, val in row[r_dim - 1 + slice_mod :].items():
            try:
                value_index = dim_index + (column_key,)
                if debug:
                    print(
                        sheet_name, dim_index, column_key, val, f"dim={r_dim}", sep=", "
                    )

                if slice_mod:
                    # switch up index for weird params
                    value_index = dim_index
                if val == "inf":
                    param.add_record(value_index).value = float("inf")
                elif val == "eps":
                    param.add_record(value_index).value = SV_EPS
                elif pd.isna(val):
                    # ignore nans
                    continue
                elif not pd.isna(val) and isinstance(val, str):
                    # only set value if it is neither nan nor str
                    param.add_record(value_index).value = val
                elif val != "":
                    # some unhandled value
                    raise ValueError(
                        f"Value of type {type(val)} with value {val} not supported"
                    )
                else:
                    # ignore empty strings
                    pass
            except Exception as e:
                print(sheet_name, dim_index, column_key, val, f"dim={r_dim}", sep=", ")
                raise e


def add_set_to_gdx_db(sheet_name, frames_dict, gams_db, debug=False):
    lookup_df = frames_dict["index"].set_index("Symbol")

    r_dim = lookup_df.loc[
        sheet_name, "Rdim"
    ]  # lookup_df.loc[sheet_name,["Rdim","Cdim"]].sum().astype(int)
    r_dim = int(r_dim)  # gams doesn't like numpy.int32 from above
    gams_set = gams_db.add_set(
        sheet_name,
        r_dim,
    )
    for index, row in frames_dict[sheet_name].iterrows():
        dim_index = tuple(row[:r_dim].values)
        if debug:
            print(sheet_name, dim_index)
        try:
            gams_set.add_record(dim_index)
        except Exception as e:
            print(sheet_name, dim_index)
            raise e
