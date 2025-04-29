import pyshtools

def sh_smooth_xr(F, trunc=None,):
    '''
    Parameters
    ----------
    F : xarray
        global field, has the shape of N*N or N*2N, do not need data on 90S and 360W.
    trunc : int
        truncation

    Returns
    -------
    F_sm : xarray
        smoothed F
    l_max : int
        largest truncation number
    '''
    
    grid = pyshtools.SHGrid.from_xarray(F, grid='DH')
    coef = grid.expand()
    l_max = coef.lmax 
    
    if trunc==None:
        coef_adj = coef.copy()
    else:        
        coef_temp = coef.pad(lmax=trunc)
        coef_adj  = coef_temp.pad(lmax=l_max)
    
    grid_adj = coef_adj.expand() 
    F_sm = grid_adj.to_xarray()
     
    return F_sm, l_max 