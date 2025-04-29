# When testing, do not run this file directly. Run try_curvesim.py (in the parent directory) instead.
from .cs_animation import CurveSimAnimation
from .cs_bodies import CurveSimBodies
from .cs_parameters import CurveSimParameters


def curvesim(config_file=""):
    parameters = CurveSimParameters(config_file)  # Read program parameters from config file.
    bodies = CurveSimBodies(parameters)  # Read physical bodies from config file and initialize them, calculate their state vectors and generate their patches for the animation
    results, lightcurve = bodies.calc_physics(parameters)  # Calculate all body positions and the resulting lightcurve
    CurveSimAnimation(parameters, bodies, results, lightcurve)  # Create the video
    results.save_results(parameters, bodies, lightcurve)
    return parameters, bodies, results, lightcurve


# import math
# def debug_print_points(config_file=""):
#     # Just for debugging purposes, because something in the initial state vector is wrong.
#     parameters = CurveSimParameters(config_file)  # Read program parameters from config file.
#     for _L in parameters.debug_L:
#         bodies = CurveSimBodies(parameters, debug_L=_L)  # Initialize the physical bodies, calculate their state vectors and generate their patches for the animation
#         bodies[1].positions[0] /= 2273900000.0  # bodies[0] is the sun, bodies[1] is the test planet
#         bodies[1].a /= 2273900000.0  # normalize to a=100
#         myfile = "debug_file.txt"
#         with open(myfile, "a", encoding='utf-8') as file:  # encoding is important, otherwise symbols like Ω get destroyed
#             if bodies[1].L == 0:  # write headline with parameters, e.g. "a=100 e=0.90 i=90 Ω=0 ϖ=0"
#                 file.write(f'a={bodies[1].a:.0f} e={bodies[1].e:.2f} i={bodies[1].i / math.pi * 180:.0f} Ω={bodies[1].Ω / math.pi * 180:.0f} ϖ={bodies[1].ϖ / math.pi * 180:.0f}\n')
#             file.write(f'L{bodies[1].L / math.pi * 180:.0f},{bodies[1].positions[0][0]:.2f},{bodies[1].positions[0][1]:.2f},{bodies[1].positions[0][2]:.2f}\n')  # write coordinates of starting position for this value of L
#     return parameters, bodies
