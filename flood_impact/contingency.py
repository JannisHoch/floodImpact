import numpy as np

def hit_rate(array1, array2):
    """
    calculate the hit rate based upon 2 boolean maps. (i.e. where are both 1)
    """
    # count the number of cells that are flooded in both array1 and 2
    idx_both = np.sum(np.logical_and(array1, array2))
    idx_1 = np.sum(array1)
    
    return float(idx_both)/float(idx_1)

def false_alarm_rate(array1, array2):
    """
    calculate the false alarm rate based upon 2 boolean maps. (i.e. amount of cells where array2 is True but array1 False)
    """
    # count the number of cells that are flooded in both array1 and 2
    idx_2_only = np.sum(np.logical_and(array2, array1!=1))
    idx_2_total = np.sum(array2)
    
    return float(idx_2_only)/float(idx_2_total)

def critical_success(array1, array2):
    """
    calculate the critical success rate based upon 2 boolean maps. 
    """
    idx_both = np.sum(np.logical_and(array1, array2))
    idx_either = np.sum(np.logical_or(array1, array2))

    return float(idx_both)/float(idx_either)

def contingency_map(array1, array2, threshold1=0., threshold2=0.):
    """
    Establish the contingency between array1 and array2.
    Returns an array where 
    1 means only array2 gives a value > threshold1, 
    2 means only array1 gives a values > threshold2,
    3 means array1 gives a value > threshold1, and array2 a value > threshold2
    0 means both arrays do not give a value > threshold1, 2 respectively
    
    function returns the threshold exceedance (0-1) of array 1 and 2, as well as the contingency map
    """
    array1_thres = array1 > threshold1
    array2_thres = array2 > threshold2
    contingency = np.zeros(array1.shape)
    contingency += np.int16(array2_thres)
    contingency += np.int16(array1_thres)*2

    return array1_thres, array2_thres, contingency

def calc_contingency(bench_d, model_d, bench_thres, model_thres):
    """
    determines hit rate, false alarm ratio, critical success index, and contingency map for a given combination of simulated and observed flood extent.
    """
    
    x_bench = bench_d.width
    y_bench = bench_d.height
    bench_data = bench_d.read(1)
    fill_bench = bench_d.nodata
    extent_bench = bench_d.bounds
    
    x_model = model_d.width
    y_model = model_d.height
    model_data = model_d.read(1)
    fill_model = model_d.nodata
    
    bench_data[bench_data==fill_bench] = 0.
    model_data[model_data==fill_model] = 0.
        
    flood1, flood2, cont_arr = contingency_map(bench_data, model_data, threshold1=bench_thres, threshold2=model_thres)
    
    hr = hit_rate(flood1, flood2)
    far = false_alarm_rate(flood1, flood2)
    csi = critical_success(flood1, flood2)

    return hr, far, csi, cont_arr