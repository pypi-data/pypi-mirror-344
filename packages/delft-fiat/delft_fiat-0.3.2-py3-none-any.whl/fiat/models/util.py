"""The FIAT model workers."""

from concurrent.futures import ProcessPoolExecutor, wait
from itertools import product
from multiprocessing.context import SpawnContext
from pathlib import Path
from typing import Callable, Generator

from osgeo import ogr

from fiat.cfg import Configurations
from fiat.fio import TableLazy
from fiat.util import NEWLINE_CHAR, generic_path_check, replace_empty

GEOM_DEFAULT_CHUNK = 50000
GRID_PREFER = {
    False: "hazard",
    True: "exposure",
}


def check_file_for_read(
    cfg: Configurations,
    entry: str,
    path: Path | str,
):
    """Quick check on the input for reading."""
    if path is not None:
        path = generic_path_check(path, cfg.path)
    else:
        path = cfg.get(entry)
    return path


def exposure_from_geom(
    ft: ogr.Feature,
    exp: TableLazy,
    oid: int,
    mid: int,
    idxs_haz: list | tuple,
    pattern: object,
):
    """Get exposure info from feature."""
    method = ft.GetField(mid)
    haz = [ft.GetField(idx) for idx in idxs_haz]
    return ft, [ft.GetField(oid)], method, haz


def exposure_from_csv(
    ft: ogr.Feature,
    exp: TableLazy,
    oid: int,
    mid: int,
    idxs_haz: list | tuple,
    pattern: object,
):
    """Get exposure info from csv file."""
    ft_info_raw = exp[ft.GetField(oid)]
    if ft_info_raw is None:
        return None, None, None, None

    ft_info = replace_empty(pattern.split(ft_info_raw))
    ft_info = [x(y) for x, y in zip(exp.dtypes, ft_info)]
    method = ft_info[exp._columns["extract_method"]].lower()
    haz = [ft_info[idx] for idx in idxs_haz]
    return ft_info, ft_info, method, haz


EXPOSURE_FIELDS = {
    True: exposure_from_geom,
    False: exposure_from_csv,
}


def csv_def_file(
    p: Path | str,
    columns: tuple | list,
):
    """_summary_Set up the outgoing csv file.

    Parameters
    ----------
    p : Path | str
        Path to the file.
    columns : tuple | list
        Headers to be added to the file.
    """
    header = b""
    header += ",".join(columns).encode()
    header += NEWLINE_CHAR.encode()

    with open(p, "wb") as _dw:
        _dw.write(header)


def generate_jobs(
    d: dict,
    tied: tuple | list = None,
) -> dict:  # type: ignore
    """Generate jobs.

    Parameters
    ----------
    d : dict
        Dictionary of elements, either containing single values or iterables.
    tied : tuple | list, optional
        Values in the dictionary that depend on each other.

    Returns
    -------
    dict
        Dictionary containing the job.
    """
    arg_list = []
    single_var = None
    if tied is not None:
        single_var = "_".join(tied)
        d[single_var] = list(zip(*[d[var] for var in tied]))
        for var in tied:
            del d[var]
    for arg in d.values():
        if not isinstance(arg, (tuple, list, range, zip)):
            arg = [
                arg,
            ]
        arg_list.append(arg)
    for element in product(*arg_list):
        kwargs = dict(zip(d.keys(), element))
        if single_var is not None:
            values = kwargs[single_var]
            for var, value in zip(tied, values):
                kwargs[var] = value
            del kwargs[single_var]
        yield kwargs


def execute_pool(
    ctx: SpawnContext,
    func: Callable,
    jobs: Generator,
    threads: int,
):
    """Execute a python process pool.

    Parameters
    ----------
    ctx : SpawnContext
        Context of the current process.
    func : Callable
        To be executed function.
    jobs : Generator
        A job generator. Returns single dictionaries.
    threads : int
        Number of threads.
    """
    # If there is only one thread needed, execute in the main process
    if threads == 1:
        for job in jobs:
            func(**job)
        return

    # If there are more threads needed however
    processes = []
    # Setup the multiprocessing pool
    pool = ProcessPoolExecutor(
        max_workers=threads,
        mp_context=ctx,
    )

    # Go through all the jobs
    for job in jobs:
        pr = pool.submit(
            func,
            **job,
        )
        processes.append(pr)

    # wait for all jobs to conclude
    wait(processes)

    pool.shutdown(wait=False)
