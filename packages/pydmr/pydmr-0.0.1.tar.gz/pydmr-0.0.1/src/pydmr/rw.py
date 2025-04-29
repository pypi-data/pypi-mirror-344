import os
import shutil
import zipfile
import csv
from io import TextIOWrapper

import numpy as np



def write(path:str, dmr:dict, format='flat'):
    """Write data to disk in .dmr format.

    Args:
        path (str): path to .dmr file. If the extension .dmr is not 
          included, it is added automatically.
        dmr (dict): A dictionary with one required key 'data' 
          and optional keys 'rois', 'pars', 'sdev', 'columns'. 
          dmr['data'] is a dictionary with one item for each 
          parameter; the key is the parameter and the value is a list 
          of containing description, unit and python data type. 
          dmr['rois'] is a dictionary with one item per ROI; each 
          ROI is a dictionary on itself which has keys 
          (subject, study, parameter) and a list or array as value.
          dmr['pars'] is a dictionary with parameters 
          such as sequence parameters or subject characteristics. 
          dmr['sdev'] is a dictionary with standard deviations 
          of parameters listed in pars.csv. This can include only a 
          subset of parameters but all parameters in sdev.csv must 
          also be in pars.csv. Defaults to None.
          dmr['columns'] is a list of headers for optional 
          columns in the data dictionary. Required if the data 
          dictionary contains extra columns above the required three 
          (description, unit, type). 
        format (str, optional): Formatting of the arguments. 
          The default ('flat') is a dictionary with a 
          multi-index, meaning values (rois, pars, sdev) are 
          flat dictionaries with a multi-index consisting of 
          (subject, study, parameter). If format='nest', these values 
          are nested dictionaries with 3 levels. If 
          format='table', the values are a list of lists. 
          Defaults to 'flat'.
        
 
    Raises:
        ValueError: if the data are not dmr-compliant formatted.
    """

    #
    # Check dmr compliance
    #

    if not 'data' in dmr:
        raise ValueError("data key is required in dmr dictionary")
    data = dmr['data']

    # Convert to dictionary
    if format=='table':
        if not isinstance(data, list):
            raise ValueError("dmr['data'] must be a list")
        data = {dat[0]: dat[1:] for dat in data}
    elif not isinstance(data, dict):
        raise ValueError("dmr['data'] must be a dictionary")
    
    for key, values in data.items():
        if not isinstance(values, list):
            raise ValueError(
                f"Each dmr['data'] value must be a list"
            )     
        length = 3
        if 'columns' in dmr:
            length += len(dmr['columns'])    
        if len(values) < length:
            raise ValueError(
                f"Each dmr['data'] value must have at least {length} elements. "
                f"The required 'description', 'unit', 'type' and the "
                f"optional columns {columns}."
            )
        
    if 'rois' in dmr:
        rois = dmr['rois']

        # convert to flat dictionary
        if format=='flat':
            if not isinstance(rois, dict):
                raise ValueError("dmr['rois'] must be a dictionary")
        elif format=='nest':
            if not isinstance(rois, dict):
                raise ValueError("dmr['rois'] must be a dictionary")
            rois = _nested_dict_to_multi_index(rois)
        elif format=='table':
            if not isinstance(rois, list):
                raise ValueError("dmr['rois'] must be a list")
            rois = {tuple(roi[:3]): roi[4] for roi in rois}

        for roi in rois.keys():
            if len(roi) != 3:
                raise ValueError("Each rois key must be a 3-element tuple")
            if roi[-1] not in list(data.keys()):
                raise ValueError(
                    f"rois parameter {roi[-1]} not in dmr['data']. "
                    "Please add it to the dictionary."
                )
        for key, values in rois.items():
            if key[-1] not in data:
                raise ValueError(
                    f"rois parameter {key[-1]} not in data. "
                    "Please add it to the dictionary."
                )
            data_type = np.dtype(data[key[-1]][2])
            write_values = np.asarray(values).astype(data_type) # is this ovewriting values?
            if not np.array_equal(write_values, values):
                raise ValueError(
                    f"rois parameter {key[-1]} has wrong data type. "
                    "Please correct the data in rois.csv "
                    "or correct the data type in data.csv"
                )
            
    if 'pars' in dmr:
        pars = dmr['pars']

        # Convert to flat dictionary
        if format=='flat':
            if not isinstance(pars, dict):
                raise ValueError("dmr['pars'] must be a dictionary")
        elif format=='nest':
            if not isinstance(pars, dict):
                raise ValueError("dmr['pars'] must be a dictionary")
            pars = _nested_dict_to_multi_index(pars)
        elif format=='table':
            if not isinstance(pars, list):
                raise ValueError("dmr['pars'] must be a list")
            pars = {tuple(par[:3]): par[4] for par in pars}

        for par in pars.keys():
            if len(par) != 3:
                raise ValueError("Each pars key must be a 3-element tuple")
            if par[-1] not in list(data.keys()):
                raise ValueError(
                    f"pars parameter {par[-1]} not in dmr['data']. "
                    "Please add it to the dictionary."
                )
        for key, value in pars.items():
            if key[-1] not in data:
                raise ValueError(
                    f"pars parameter {key[-1]} not in data. "
                    "Please add it to the dictionary."
                )
            data_type = data[key[-1]][2]
            if data_type == 'str':
                if not isinstance(value, str):
                    raise ValueError(
                        f"pars parameter {key[-1]} must be a string. "
                        "Please correct the data in pars.csv "
                        "or correct the data type in data.csv"
                    )
            elif data_type == 'float':
                if not isinstance(value, (float, int)):
                    raise ValueError(
                        f"pars parameter {key[-1]} must be a float. "
                        "Please correct the data in pars.csv "
                        "or correct the data type in data.csv"
                    )
            elif data_type == 'bool':
                if not isinstance(value, bool):
                    raise ValueError(
                        f"pars parameter {key[-1]} must be a boolean. "
                        "Please correct the data in pars.csv "
                        "or correct the data type in data.csv"
                    )
            elif data_type == 'int':
                if not isinstance(value, int):
                    raise ValueError(
                        f"pars parameter {key[-1]} must be an integer. "
                        "Please correct the data in pars.csv "
                        "or correct the data type in data.csv"
                    )
            elif data_type == 'complex':
                if not isinstance(value, complex):
                    raise ValueError(
                        f"pars parameter {key[-1]} must be a complex number. "
                        "Please correct the data in pars.csv"
                        "or correct the data type in data.csv"
                    )
    
    if 'sdev' in dmr:
        if 'pars' not in dmr:
            raise ValueError(
                "dmr['sdev'] should only be provided if dmr['pars'] are also "
                "provided."
            )
        sdev = dmr['sdev']

        # Convert to flat dictionary
        if format=='flat':
            if not isinstance(sdev, dict):
                raise ValueError("dmr['sdev'] must be a dictionary")
        elif format=='nest':
            if not isinstance(sdev, dict):
                raise ValueError("dmr['sdev'] must be a dictionary")
            sdev = _nested_dict_to_multi_index(sdev)
        elif format=='table':
            if not isinstance(sdev, list):
                raise ValueError("dmr['sdev'] must be a list")
            sdev = {tuple(sd[:3]): sd[4] for sd in sdev}

        if not (sdev.keys() <= pars.keys()):
            raise ValueError(
                'keys in the sdev dictionary must also be in pars.'
            )
        for key, value in sdev.items():
            try:
                float(value)
            except:
                raise ValueError("sdev values must be float.")
            

    # make folder 
    if path[-4:] == ".dmr":
        path = path[:-4]

    if not os.path.exists(path):
        os.makedirs(path)


    #
    # Write data dictionary
    #

    # Build rows
    header = ['parameter', 'description', 'unit', 'type']
    if 'columns' in dmr:
        header += dmr['columns']
    rows = [header]
    for key, values in data.items():
        row = [key] + values
        rows.append(row)

    # Write rows to dict.csv
    file = os.path.join(path, "data.csv")
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    #
    # Write ROI curves
    #

    if 'rois' in dmr:
        
        # Find the longest array length
        max_len = max(len(arr) for arr in rois.values())

        # Prepare CSV data (convert dictionary to column format)
        columns = []

        # First 3 rows: keys (tuple elements)
        for key, values in rois.items():
            data_type = np.dtype(data[key[-1]][2])
            write_values = np.asarray(values).astype(data_type)
            if data_type=='bool':
                write_values = write_values.astype(str)
                write_values[write_values=='True'] = '1'
                write_values[write_values=='False'] = '0'
            col = list(key) + list(write_values) + [""] * (max_len - len(values))  # Pad shorter columns
            columns.append(col)

        # Transpose to get row-wise structure
        rows = list(map(list, zip(*columns)))

        # Write to CSV
        file = os.path.join(path, "rois.csv")
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    #
    # Write parameters
    # 

    if 'pars' in dmr:
        rows = [
            ['subject', 'study', 'parameter', 'value'],
        ]
        for key, value in pars.items():
            data_type = data[key[-1]][2]
            if data_type == 'str':
                write_value = value
            elif data_type == 'float':
                write_value = value
            elif data_type == 'bool':
                write_value = '1' if value else '0'
            elif data_type == 'int':
                write_value = value
            elif data_type == 'complex':
                write_value = value
            row = list(key) + [write_value]
            rows.append(row)
        file = os.path.join(path, "pars.csv")
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    if 'sdev' in dmr:
        rows = [
            ['subject', 'study', 'parameter', 'value'],
        ]
        for key, value in sdev.items():
            row = list(key) + [value]
            rows.append(row)
        file = os.path.join(path, "sdev.csv")
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    # Zip and delete original
    shutil.make_archive(path + ".dmr", "zip", path)
    shutil.rmtree(path)



def read(path:str, format='flat'):
    """Read .dmr data from disk.

    Args:
        path (str): Path to .dmr file where the data are 
        saved. The extensions do not need to be included.
        format (str, optional): Formatting of the returned results. 
          The default ('flat') returns a dictionary with a 
          multi-index, meaning values (rois, pars, sdev) are returned 
          as flat dictionaries with a multi-index consisting of 
          (subject, study, parameter). If format='nest', these values 
          are returned as nested dictionaries with 3 levels. If 
          format='table', the values are returned as a list of lists. 
          Defaults to 'flat'.

    Raises:
        ValueError: If the data on disk are not correctly formatted.

    Returns:
        dict: A dictionary with one item for each of the csv files 
          in the dmr file - keys are either 'data', 'rois', 'pars', 
          'sdev'. The optional key 'columns' is returned as well if
          the data dictionary has optional columns, in which case it 
          lists the names of those extra columns.
    """
    
    if path[-8:] == ".dmr.zip":
        read_path = path
    
    # If the filename is provided with the .dmr extension alone, add the .zip
    elif path[-4:] == ".dmr":
        read_path = path + ".zip"

    # If filename is provided without extensions, add them both
    else:
        read_path = path + ".dmr.zip"


    with zipfile.ZipFile(read_path, "r") as z:
        
        # Check files
        csv_files = [f for f in z.namelist() if f.endswith(".csv")]  
        if 'data.csv' not in csv_files:
            raise ValueError("A .dmr file must contain a data.csv file.")    
        if ('pars.csv' not in csv_files) and ('rois.csv' not in csv_files):
            raise ValueError("A .dmr file must contain a pars.csv, a rois.csv file, or both.") 
        
        
        # Read data dictionary
        data = {}
        with z.open('data.csv') as file:
            text = TextIOWrapper(file, encoding="utf-8")
            reader = csv.reader(text)
            dict_list = list(reader)
            data_headers = dict_list[0]
            for d in dict_list[1:]: 
                if len(d) != len(data_headers):
                    raise ValueError(
                        f"Each data_dict row must have {len(data_headers)} "
                        f"elements {data_headers}. "
                        f"Correct the data dictionary in data.csv"
                    )
                if d[3] not in ['str', 'float', 'bool', 'int', 'complex']:
                    raise ValueError(
                        f"data type {d[3]} is not allowed. Correct "
                        f"the data dictionary in data.csv"
                    )
                data[d[0]] = d[1:]


        if 'pars.csv' in csv_files: 
            pars = {}
            with z.open('pars.csv') as file:
                text = TextIOWrapper(file, encoding="utf-8")
                reader = csv.reader(text)
                pars_list = list(reader)
                pars_list = pars_list[1:] # do not return headers
                for p in pars_list:
                    if len(p) != 4:
                        raise ValueError(
                            f"Each pars row must have 4 elements: "
                            f"subject, study, parameter, value. "
                            f"Correct the data in pars.csv"
                        )
                    if p[2] not in data:
                        raise ValueError(
                            f"parameter {p[2]} is not listed in the "
                            f"data dictionary in data.csv"
                        )
                    data_type = data[p[2]][2]
                    if data_type=='str':
                        value = p[3]
                    elif data_type=='float':
                        value = float(p[3])
                    elif data_type=='bool':
                        if p[3]=='1':
                            value = True
                        elif p[3]=='0':
                            value = False
                        else:
                            raise ValueError(
                                f"Boolean value {p[3]} is not allowed. "
                                "Possible values are 1 or 0. "
                                "Correct the data in pars.csv"
                            )
                    elif data_type=='int':
                        value = int(p[3])
                    elif data_type=='complex':
                        value = complex(p[3])
                    pars[tuple(p[:3])] = value

        if 'rois.csv' in csv_files: 
            rois = {}
            with z.open('rois.csv') as file:
                text = TextIOWrapper(file, encoding="utf-8")
                reader = csv.reader(text)
                rois_list = list(reader)
                if len(rois_list)!=0:
                    # Extract headers (first 3 rows)
                    # Transpose first 3 rows to get column-wise headers
                    headers = list(zip(*rois_list[:3]))  
                    # Extract data (from row 3 onward) and convert to NumPy arrays
                    rois = {}
                    for header, col in zip(headers, zip(*rois_list[3:])):
                        if header[2] not in data:
                            raise ValueError(
                                f"roi parameter {header[2]} is not listed in the "
                                f"data dictionary in data.csv. Please update the dictionary."
                            )
                        values = np.array([val for val in col if val])
                        data_type = data[header[2]][2]
                        if data_type == 'bool':
                            rois[header] = values.astype(int).astype(bool)
                        else:
                            rois[header] = values.astype(np.dtype(data_type))

        if 'sdev.csv' in csv_files: 
            if 'pars.csv' not in csv_files:
                raise ValueError(
                    "A file sdev.csv is included in the .dmr file "
                    "without a corresponding pars.csv file. "
                    "Please remove the sdev.csv file or add a "
                    "pars.csv file."
                )
            sdev = {}
            with z.open('sdev.csv') as file:
                text = TextIOWrapper(file, encoding="utf-8")
                reader = csv.reader(text)
                sdev_list = list(reader)
                sdev_list = sdev_list[1:] # do not return headers
                for p in sdev_list:
                    if len(p) != 4:
                        raise ValueError(
                            f"Each sdev row must have 4 elements: "
                            f"subject, study, parameter, sdev. "
                            f"Correct the data in sdev.csv"
                        )
                    if tuple(p[:3]) not in pars:
                        raise ValueError(
                            f"parameter {tuple(p[:3])} has a sdev but "
                            f"no corresponding value in pars.csv."
                        ) 
                    sdev[tuple(p[:3])] = float(p[3])

        # Convert to required return format
        dmr = {}
        if format == 'table':
            data = [[key] + value for key, value in data.items()]
        dmr['data'] = data
        if len(data_headers) > 4:
            dmr['columns'] = data_headers[4:]
        if 'pars.csv' in csv_files:
            if format == 'nest':
                pars = _multi_index_to_nested_dict(pars)
            elif format == 'table':
                pars = [list(key) + [value] for key, value in pars.items()]
            dmr['pars'] = pars
        if 'rois.csv' in csv_files: 
            if format == 'nest':
                rois = _multi_index_to_nested_dict(rois)
            elif format == 'table':
                rois = [list(key) + [value] for key, value in rois.items()]
            dmr['rois'] = rois
        if 'sdev.csv' in csv_files:
            if format == 'nest':
                sdev = _multi_index_to_nested_dict(sdev)
            elif format == 'table':
                sdev = [list(key) + [value] for key, value in sdev.items()]
            dmr['sdev'] = sdev

    return dmr


def _multi_index_to_nested_dict(multi_index_dict):
    """
    Converts a dictionary with tuple keys (multi-index) into a nested dictionary.
    
    Parameters:
        multi_index_dict (dict): A dictionary where keys are tuples of indices.

    Returns:
        dict: A nested dictionary where each level corresponds to an index in the tuple.
    """
    nested_dict = {}

    for key_tuple, value in multi_index_dict.items():
        current_level = nested_dict  # Start at the root level
        for key in key_tuple[:-1]:  # Iterate through all but the last key
            current_level = current_level.setdefault(key, {})  # Go deeper/create dict
        current_level[key_tuple[-1]] = value  # Assign the final value

    return nested_dict


def _nested_dict_to_multi_index(nested_dict, parent_keys=()):
    """
    Converts a nested dictionary into a dictionary with tuple keys (multi-index).

    Parameters:
        nested_dict (dict): A nested dictionary.
        parent_keys (tuple): Used for recursion to keep track of the current key path.

    Returns:
        dict: A dictionary where keys are tuples representing the hierarchy.
    """
    flat_dict = {}

    for key, value in nested_dict.items():
        new_keys = parent_keys + (key,)  # Append the current key to the path

        if isinstance(value, dict):  # If the value is a dict, recurse
            flat_dict.update(_nested_dict_to_multi_index(value, new_keys))
        else:  # If it's a final value, store it with the multi-index key
            flat_dict[new_keys] = value

    return flat_dict

