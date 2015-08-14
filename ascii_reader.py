import numpy as np 

def file_len(fname):
    """ Function computes the total number of lines in an ascii file.

    Parameters 
    -----------
    fname : string 

    Returns 
    --------
    file length : int 
    """
    for i, line in enumerate(open(fname)):
        pass
    return i+1

def column_cut_chunk_gen(chunk_size, columns_to_keep, f):
    """ Generator used to produce a sequence of length ``chunk_size`` 
    storing the desired columns data stored in open file object ``f``.

    Parameters 
    ----------
    chunks_size : int 
        Number of rows defining the chunk. 

    columns_to_keep : list 
        List of integers of the indices of the column numbers 
        to store from the input tabular data. 

    f : open file object 
    """

    cur = 0
    while cur < chunk_size:
        line = f.readline()    
        parsed_line = line.strip().split()
        yield tuple(parsed_line[i] for i in columns_to_keep)
        cur += 1 

def rowcut(arr):
    """ Example function used to apply a cut 
    to a structured numpy array or Astropy Table.

    Parameters 
    -----------
    arr : numpy array or astropy table 

    Returns 
    --------
    mask : boolean array 

    Notes 
    ------
    Input array ``arr`` contains tabular input data. The returned boolean 
    result is True for the rows of ``arr`` passing the desired cut. 
    """
    mask = np.where(arr['z'] > -300, True, False)
    return mask

def read_rowcut_file(fname, cut_func, dt):
    """ Read an ascii file ``fname``, apply the ``cut_func`` function object to each row 
    to determine if the row passes the cut, and store the result as a 
    numpy structured array with dtype ``dt``.

    Parameters 
    -----------
    fname : string 

    cut_func : function 
        Function used to apply cuts to the tabular data 

    dt : numpy dtype 
        dtype of the array after applying column cuts
    """
    num_total_rows = file_len(fname)
    chunksize = int(num_total_rows / 10.)
    num_full_chunks = num_total_rows/chunksize
    chunksize_remainder = num_total_rows % chunksize

    with open(fname) as f:
        for ichunk in xrange(num_full_chunks):
            chunk_array = np.array(list(column_cut_chunk_gen(chunksize, [0, 2], f)), dtype=dt)
            mask = cut_func(chunk_array)
            try:
                full_array = np.append(full_array, chunk_array[mask])
            except NameError:
                full_array = chunk_array[mask]
        chunk_array = np.array(list(column_cut_chunk_gen(chunksize_remainder, [0, 2], f)), dtype=dt)
        full_array = np.append(full_array, chunk_array)
    return full_array