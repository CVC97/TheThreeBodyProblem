from ctypes import *
from numpy.ctypeslib import ndpointer
import os
from manim import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from params import m1, x1, y1, z1, v_x1, v_y1, v_z1, m2, x2, y2, z2, v_x2, v_y2, v_z2, m3, x3, y3, z3, v_x3, v_y3, v_z3 
from params import i_steps, T, framerate, run_time, sun_speed, fade_lenght, rays, tail


#################### GENERATION POS ARRAYS ####################

# Shared C-Python-libraries
os.system('cc -fPIC -shared -o numint.so numint.c')
so_numint = "./numint.so"
numint = CDLL(so_numint)

numint.thethreebodyproblem.restype = ndpointer(dtype = c_double, shape=(3, 3, i_steps+1))
numint.thethreebodyproblem.argtypes = [
    c_double, c_double, c_double, c_double, c_double, c_double, c_double, 
    c_double, c_double, c_double, c_double, c_double, c_double, c_double,
    c_double, c_double, c_double, c_double, c_double, c_double, c_double,
    c_int, c_double
    ]

# Initialize and copy Array to Python as TBP using numint.so
TBP_array = numint.thethreebodyproblem(m1, x1, y1, z1, v_x1, v_y1, v_z1, m2, x2, y2, z2, v_x2, v_y2, v_z2, m3, x3, y3, z3, v_x3, v_y3, v_z3, i_steps, T)
TBP = TBP_array.copy()

# Positional matrices of each sun
r1 = TBP[0]
r2 = TBP[1]
r3 = TBP[2]

# Free memory of original Array
TBP_ptr = TBP_array.ctypes.data_as(POINTER(c_double))
numint.freemem(TBP_ptr)


#################### PARAMETER CHECK ####################

def param_check(framerate, run_time, sun_speed, i_steps):
    if run_time * framerate * sun_speed >= i_steps + 1:
        raise IndexError('Your positions array does not have enough entries! Please fix.')
    else:
        print(f'Parameters valid: {run_time * framerate * sun_speed} of {i_steps + 1} array entries will be used.')


#################### MATPLOTLIB ANIMATION PREVIEW ####################

def anim_preview():
    fig, ax = plt.subplots(figsize = (16,9))
    used_frames = framerate * run_time * sun_speed

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


#################### MAIN #################### 

print('\nNumerical Integration of the Three-Body-Problem animated using manim created by Carlo von Carnap\n')
print('\t-p\tpreview animation in matplotlib\n')
print('\t-a\trender manim animation.\n')
print('\t-q\tquit\n')

while True:
    command = input()
    if command == '-q' or command == 'quit' or command == 'q':
        break
    elif command == '-p' or command == 'preview' or command == 'p':
        anim_preview()
    elif command == '--help' or command == '-h' or command == 'h':
        print('\t-p\tpreview animation in matplotlib\n')
        print('\t-a\trender manim animation.\n')
        print('\t-q\tquit\n')
    else:
        print('Unknown command. Type \'--help\' for help')

#print(TBP)