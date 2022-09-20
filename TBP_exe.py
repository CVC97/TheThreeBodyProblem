import os
from main import anim_preview, anim_preview_3D, param_check, TBP_calculate, p_read

#################### MAIN #################### 

TBP = TBP_calculate()
run_time = p_read('run_time', int)
framerate = p_read('framerate', int)
sun_speed = p_read('sun_speed', int)
i_steps = p_read('i_steps', int)

print('Numerical Integration of the Three-Body-Problem animated using manim created by Carlo von Carnap\n')
print('\t-p\t(params) open params.py in gedit for parameter manipulation')
print('\t-c\t(calculate) process calculation for set parameters')
print('\t-v\t(view) preview animation in matplotlib')
print('\t-a\t(animate) render manim animation.')
print('\t-m\t(merge) merge starting and main animation.')
print('\t-q\tquit\n')

while True:
    print('TBP>', end = '')
    command = input()
    if command == '-q' or command == 'quit' or command == 'q':
        break
    elif command == '-c' or command == 'calculate' or command == 'c':
        if param_check(p_read('run_time', int), p_read('framerate', int), p_read('sun_speed', int), i_steps = p_read('i_steps', int)):      
            TBP = TBP_calculate()
            run_time = p_read('run_time', int)
            framerate = p_read('framerate', int)
            sun_speed = p_read('sun_speed', int)
            i_steps = p_read('i_steps', int)
    elif command == '-p' or command == 'params' or command == 'p':
        os.system('gedit params.txt')
    elif command == '-v' or command == 'view' or command == 'v':
        if param_check(run_time, framerate, sun_speed, i_steps):
            anim_preview(TBP, run_time, framerate, sun_speed)
    elif command == 'view -3D' or command == 'v -3D':
        if param_check(run_time, framerate, sun_speed, i_steps):
            anim_preview_3D(TBP, run_time, framerate, sun_speed)
    elif command == '-a' or command == 'animate' or command == 'a':
        if param_check(run_time, framerate, sun_speed, i_steps):
            os.system(f'manim -pql --fps {framerate} animations.py TBP_main_scene')
    elif command == 'animate -3D' or command == 'a -3D':
        if param_check(run_time, framerate, sun_speed, i_steps):
            os.system(f'manim -pqh --fps {framerate} animations.py TBP_main_3D')
    elif command[:5] == 'merge':
        if command == 'merge':
            print('ERROR. \'merge\' requires resolution (\'1080p60\') and name of output.mp4 as additional argument.') 
        else:
            res, name = command[6:].split(' ')
            os.system(f'ffmpeg -f concat -i media/videos/animations/{res}/input.txt -c copy media/videos/animations/{res}/{name}')
    elif command[:8] == 'animate ':
        if param_check(run_time, framerate, sun_speed, i_steps):
            if command[8:] == '-start':
                os.system(f'manim -pql --fps {framerate} animations.py TBP_starting_scene')
            elif command[8:17] == '-start ':
                os.system(f'manim {command[10:]} animations.py TBP_starting_scene')
            elif command[8:12] == '-all':
                if command[8:13] == '-all ':
                    os.system(f'manim {command[13:]} animations.py TBP_starting_scene')
                    os.system(f'manim {command[13:]} animations.py TBP_main_scene')
                else:
                    os.system(f'manim -pql --fps {framerate} animations.py TBP_starting_scene')
                    os.system(f'manim -pql --fps {framerate} animations.py TBP_main_scene')
            else:
                os.system(f'manim {command[10:]} animations.py TBP_main_scene')
    elif command == '--help' or command == '-h' or command == 'h':
        print('\t-params\t(params) open params.py in gedit for parameter manipulation')
        print('\t-v\t(view) show animation in matplotlib')
        print('\t-a\t(animate) render manim animation.')
        print('\t-q\tquit')
    else:
        print(f'Unknown command \'{command}\'. Type \'--help\' for help')