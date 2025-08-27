"""
Planetary data classes and functions for orbital simulation.
"""

# Get planetary data from Skyfield and create PlanetData objects
from dataclasses import dataclass
from typing import Tuple
from skyfield.api import load
from skyfield.framelib import ecliptic_frame

@dataclass
class PlanetData:
    """Data class to store planetary position, velocity, and mass"""
    name: str
    pos2: Tuple[float, float]  # (x, y) coordinates in meters
    vel2: Tuple[float, float]  # (v_x, v_y) velocities in m/s
    pos3: Tuple[float, float, float]  # (x, y, z) coordinates in meters
    vel3: Tuple[float, float, float]  # (v_x, v_y, v_z) velocities in m/s
    mass: float  # Mass in kg

# Hardcoded planetary masses in kg
planetary_masses = {
    'mercury': 3.301e23,
    'venus': 4.867e24,
    'earth': 5.972e24,
    'mars': 6.417e23,
    'jupiter barycenter': 1.898e27,
    'sun': 1.989e30
}

# Suppress the nutation warnings from Skyfield
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="skyfield.nutationlib")

def build_planet_data():
    """Build and return a dictionary of PlanetData objects 
    with data about the position, velocity and mass for the planets."""

    # Load JPL ephemeris and get planet objects
    planets = load('de421.bsp')

    names = ['sun', 'mercury', 'venus', 'earth', 'mars', 'jupiter barycenter']

    sun = planets['sun']

    # Get current time
    ts = load.timescale()
    t = ts.now()

    # Create PlanetData objects directly
    planet_data = {}

    for name in names:
        # Get position relative to Sun in ecliptic coordinates
        pos = sun.at(t).observe(planets[name])
        x, y, z = pos.frame_xyz(ecliptic_frame).au
        
        # Convert AU to km (1 AU = 149,597,870.7 km), then km to meters
        au_to_km = 149597870.7
        km_to_m = 1000
        x_m = x * au_to_km * km_to_m
        y_m = y * au_to_km * km_to_m
        z_m = z * au_to_km * km_to_m
        
        # Get velocity components and convert km/s to m/s
        planet_at_t = planets[name].at(t)
        vx, vy, vz = planet_at_t.velocity.km_per_s
        vx_m = vx * km_to_m
        vy_m = vy * km_to_m
        vz_m = vz * km_to_m
        
        # Create PlanetData object (convert numpy values to Python floats)

        pname = (name.split(' ', 1)[0])

        planet_data[pname] = PlanetData(
            name=pname,
            pos2=(float(x_m), float(y_m)),
            vel2=(float(vx_m), float(vy_m)),
            pos3=(float(x_m), float(y_m), float(z_m)),
            vel3=(float(vx_m), float(vy_m), float(vz_m)),
            mass=float(planetary_masses[name])
        )

    return planet_data
