
def fill_empty_array(arr, generator):
    """
    """
    cdef int idx
    for idx, row in enumerate(generator):
        arr[idx] = row
