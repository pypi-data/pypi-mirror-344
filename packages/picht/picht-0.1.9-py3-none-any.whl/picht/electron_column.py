import numpy as np
import matplotlib.pyplot as plt
from core import IonOpticsSystem

system = IonOpticsSystem(nr=100.0, nz=500.0, physical_size=0.4)

system.add_einzel_lens(
    position=20.0,
    width=6.0,
    aperture_center=50.0,
    aperture_width=10.0,
    outer_diameter=30.0,
    focus_voltage=2000.0
)

system.add_einzel_lens(
    position=70.0,
    width=6.0,
    aperture_center=50.0,
    aperture_width=10.0,
    outer_diameter=30.0,
    focus_voltage=4000.0
)

system.add_einzel_lens(
    position=110.0,
    width=6.0,
    aperture_center=50.0,
    aperture_width=10.0,
    outer_diameter=30.0,
    focus_voltage=4750.0
)

system.solve_fields()
trajectories = system.simulate_beam(
    energy_eV=10000.0,
    start_z=0.0,
    r_range=(0.1999925, 0.2000075),
    angle_range=(0.0, 0.0),
    num_particles=10.0,
    simulation_time=3e-9
)

system.visualize_system(trajectories=trajectories)
plt.show()