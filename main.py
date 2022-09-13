from ctypes import *
from numpy.ctypeslib import ndpointer
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


#################### READ PARAMS.TXT #################### 

def p_read(var, vartype = float):
    params = open('params.txt', 'r')
    for row in params:
        if row.startswith(f'{var} ') or row.startswith(f'{var}='):
            _, rval = row.split('=')
            params.close()
            if vartype == int:
                return int(rval.strip())
            elif vartype == bool:
                if rval.strip() == 'True' or rval.strip() == '1':
                    return True
                else:
                    return False
            else:
                return float(rval.strip())


#################### GENERATION POS ARRAYS ####################

def TBP_calculate():
    # Shared C-Python-libraries
    os.system('cc -fPIC -shared -o numint.so numint.c')
    so_numint = "./numint.so"
    numint = CDLL(so_numint)

    numint.thethreebodyproblem.restype = ndpointer(dtype = c_double, shape=(3, 3, p_read('i_steps', int) +1))
    numint.thethreebodyproblem.argtypes = [
        c_double, c_double, c_double, c_double, c_double, c_double, c_double, 
        c_double, c_double, c_double, c_double, c_double, c_double, c_double,
        c_double, c_double, c_double, c_double, c_double, c_double, c_double,
        c_int, c_double
    ]

    # Initialize and copy Array to Python as TBP using numint.so
    TBP_array = numint.thethreebodyproblem(
        p_read('m1'), p_read('x1'), p_read('y1'), p_read('z1'), p_read('v_x1'), p_read('v_y1'), p_read('v_z1'), 
        p_read('m2'), p_read('x2'), p_read('y2'), p_read('z2'), p_read('v_x2'), p_read('v_y2'), p_read('v_z2'), 
        p_read('m3'), p_read('x3'), p_read('y3'), p_read('z3'), p_read('v_x3'), p_read('v_y3'), p_read('v_z3'),  
        p_read('i_steps', int), p_read('T')
    )
    TBP = TBP_array.copy()

    # Free memory of original Array
    TBP_ptr = TBP_array.ctypes.data_as(POINTER(c_double))
    numint.freemem(TBP_ptr)
    return TBP


#################### PARAMETER CHECK ####################

def param_check(run_time, framerate, sun_speed, i_steps):
    if run_time * framerate * sun_speed >= i_steps + 1:
        #raise IndexError('Your positions array does not have enough entries! Please fix.')
        print(f'ERROR! You have {i_steps + 1} array entries but need {run_time * framerate * sun_speed}. Type -p to modify parameters and -c to rerun the calculation.')
        return 0
    else:
        print(f'Parameters valid: {run_time * framerate * sun_speed} of {i_steps + 1} array entries will be used.')
        return 1


#################### MATPLOTLIB ANIMATION PREVIEW ####################

def anim_preview(TBP, run_time, framerate, sun_speed):
    fig, ax = plt.subplots(figsize = (16,9))
    used_frames = framerate * run_time * sun_speed

    # Positional matrices of each sun
    r1 = TBP[0]
    r2 = TBP[1]
    r3 = TBP[2]

    ax.plot(r1[0,:used_frames], r1[1,:used_frames], color = 'red', alpha = 0.5)
    ax.plot(r2[0,:used_frames], r2[1,:used_frames], color = 'blue', alpha = 0.5)
    ax.plot(r3[0,:used_frames], r3[1,:used_frames], color = 'black', alpha = 0.5)

    ax.plot(r1[0,used_frames:], r1[1,used_frames:], color = 'red', alpha = 0.25, linestyle = '--')
    ax.plot(r2[0,used_frames:], r2[1,used_frames:], color = 'blue', alpha = 0.25, linestyle = '--')
    ax.plot(r3[0,used_frames:], r3[1,used_frames:], color = 'black', alpha = 0.25, linestyle = '--')

    ax.add_patch(Rectangle((-7.111, -4), 14.222, 8, edgecolor = 'black', facecolor = 'none', lw = 0.75))

    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')

    plt.grid()
    #plt.savefig('../TBP_extra/TBP_preview_L.png', facecolor = 'white', bbox_inches='tight')
    plt.show()