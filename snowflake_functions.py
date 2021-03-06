from numpy import *

def checkerboard(side_len, boolean, num):
    '''Creates a "cubic checkerboard" of sorts.
        side_len: choose an even-valued integer for side length
        boolean: set to True if wanting Boolean True/False states
                 set to False if wanting numeric 1/0 states
        num: allows for choice of checkerboard startpoint
             set to 0 if wanting False/0 value at (0,0,0)
             set to 1 if wanting True/1 value at (0,0,0)
    '''
    halflen = side_len/2
    if boolean == True:
        even_row = r_[halflen*[False,True]]
        odd_row = r_[halflen*[True,False]]
        even_plane = vstack(halflen*(even_row,odd_row))
        odd_plane = vstack(halflen*(odd_row,even_row))
        if num == 0:
            cube = dstack(halflen*(even_plane,odd_plane))
        elif num == 1:
            cube = dstack(halflen*(odd_plane,even_plane))
        else:
            print "Argument for checkerboard startpoint (num) not recognized."
        return cube
    elif boolean == False:
        even_row = r_[halflen*[0,1]]
        odd_row = r_[halflen*[1,0]]
        even_plane = vstack(halflen*(even_row,odd_row))
        odd_plane = vstack(halflen*(odd_row,even_row))
        if num == 0:
            cube = dstack(halflen*(even_plane,odd_plane))
        elif num == 1:
            cube = dstack(halflen*(odd_plane,even_plane))
        else:
            print "Argument for checkerboard startpoint (num) not recognized."
        return cube
    else:
        print "Argument for Boolean variable not recognized."



def receptive_ind(arr, z, side_len):
    ''' Function to find indices of all receptive cells              
        arr: recombined matrix
        z: define outside loop as z = zeros(side_len, side_len,dtype=bool)
    '''

    # get indices of ice cells
    i_I = arr >= 1.0
    
    # get indices of neighbouring cells in same plane
        # from left column
    i_LEFT = hstack((z.reshape(side_len,1,side_len), i_I[:,:-1,:]))
        # from adjacent rows
    i_TOP = vstack((z.reshape(1,side_len,side_len), i_I[:-1,:,:]))
    i_BOTTOM = vstack((i_I[1:,:,:],z.reshape(1,side_len,side_len)))

    # get indices of neighbouring cells in adjacent planes
        # (adding indices down from neighbouring cells in the plane above)
    iA = checkerboard(side_len, True, 0)*i_I
    i_ABOVE = dstack((z.reshape(side_len,side_len,1),iA[:,:,:-1]))
        # (adding indices up from neighbouring cells in the plane below)
    iB = checkerboard(side_len, True, 1)*i_I
    i_BELOW = dstack((iB[:,:,1:],z.reshape(side_len,side_len,1)))
    
    # return indices of all receptive cells
    IND = i_I + i_LEFT + i_TOP + i_BOTTOM + i_ABOVE + i_BELOW
    # (also return indices of ice cells)
    return IND, i_I


def pad_beta(arr,beta):
    '''Function to pad an cubic array (arr) with the value of beta on all sides.'''
    sh = shape(arr)
    one_sm = ones(sh)
    # cube, so all side lengths the same
    s = sh[0] + 2
    sh2 = (s,s,s)
    one_lg = ones(sh2)
    lg_int = one_lg[1:-1,1:-1,1:-1]
    lg_int -= one_sm
    one_lg *= beta
    lg_int += arr
    return one_lg

def average_nearest(arr, alpha, beta, side_len):
    '''Function to average value of cell over itself and its
        four nearest neighbours.
        Three nearest neighbours are found in the same plane;
        one is found in an adjacent plane. The weight of the
        ratios of these planar neighbours to vertical neighbours
        is dependent on the 'alpha' variable.
        Boundary cells are not averaged: the saturation of these cells
        is fixed by the boundary condition set by the 'beta' variable.
    '''
    
    # sum of nearest neighbours in same plane
    u1 = arr[:-2,1:-1,1:-1]
    u2 = arr[2:,1:-1,1:-1]
    u3 = arr[1:-1,:-2,1:-1]
    u = u1 + u2 + u3
    # sum of adjacent planes
    c1 = checkerboard(side_len, False, 0)*arr
    c2 = checkerboard(side_len, False, 1)*arr
    v = c2[1:-1,1:-1,2:] + c1[1:-1,1:-1,:-2]
    # state value at cell itself
    w = arr[1:-1,1:-1,1:-1]
    # sum over all 5 cells
    k = u + alpha*v + w
    # get average state value
    avg_inside = k/(4.+alpha)
    avg = pad_beta(avg_inside,beta)
    return avg 
