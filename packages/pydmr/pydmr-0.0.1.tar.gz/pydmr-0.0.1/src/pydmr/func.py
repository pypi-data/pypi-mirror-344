import os
import pydmr.rw


def concat(
        files:list, 
        result:str,
        cleanup=False,
    ):
    """Concatenate a list of dmr files into a single dmr file

    Args:
        files (list): dmr files to concatenate
        result (str): file path to the resulting dmr file
        cleanup (bool, optional): If set to True, the original files 
          are deleted after concatenating.
    Raises:
        ValueError: if duplicate indices exist in the file set.
    """

    # combine dmr files
    dmr = {'data': {}}

    for i, file in enumerate(files):

        dmr_file = pydmr.rw.read(file)

        dmr['data'] = dmr['data'] | dmr_file['data']

        # Check dat all data dictionaries have the same columns
        if 'columns' in dmr_file:
            if i==0:
                dmr['columns'] = dmr_file['columns']
            elif 'columns' not in dmr:
                raise ValueError(
                    'Cannot concatenate: all data.csv files must have '
                    'the same optional variables (columns).'
                )
            elif dmr['columns'] != dmr_file['columns']:
                raise ValueError(
                    'Cannot concatenate: all data.csv files must have '
                    'the same optional variables (columns).'
                )

        for var in ['rois', 'pars', 'sdev']:
            if var in dmr_file:
                if i==0:
                    dmr[var] = dmr_file[var]
                elif set(dmr_file[var].keys()) <= set(dmr[var].keys()):
                    raise ValueError(
                        f"Cannot concatenate: duplicate indices "
                        f"in {var}.csv of {dmr_file}."
                    )
                else:
                    dmr[var] = dmr[var] | dmr_file[var]

    pydmr.rw.write(result, dmr)

    if cleanup:
        for file in files:
            if file[-4:] == ".dmr":
                os.remove(file+'.zip')
            else:
                os.remove(file+'.dmr.zip')