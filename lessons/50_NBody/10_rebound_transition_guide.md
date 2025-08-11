# Orbital Mechanics Simulation: From Custom Physics to Rebound

This document explains the transition from custom gravitational physics simulation to using the Rebound library for accurate N-body orbital mechanics.

## Overview

We've evolved our orbital mechanics simulation in several stages:

1. **Custom Physics (Original)**: Manual implementation of gravitational forces and Euler integration
2. **Rebound Integration (Current)**: Using the professional-grade Rebound library for accurate orbital mechanics

## Key Improvements with Rebound

### 1. Accurate Integration
- **Before**: Simple Euler integration with poor energy conservation
- **After**: WHFAST integrator designed specifically for orbital mechanics
- **Benefit**: Maintains orbital stability over long time periods

### 2. Real Astronomical Parameters
- **Before**: Arbitrary units and masses
- **After**: SI units with actual solar system masses and distances
- **Benefit**: Educational value and realistic orbital periods

### 3. Automatic Center-of-Mass Handling
- **Before**: Manual positioning around a fixed star
- **After**: Rebound automatically handles center-of-mass reference frame
- **Benefit**: More accurate multi-body dynamics

## Code Comparison

### Original Custom Physics Approach
```python
def force_vec_due_to(self, other):
    r2 = self.pos.distance_squared_to(other.pos)
    f_g = (G * self.mass * other.mass) / r2
    f = (other.pos - self.pos).normalize() * f_g
    return f

def update(self):
    f = self.force_vec_due_to(self.sun)
    a = f / self.mass
    self.vel += a * d_T  # Euler integration
    self.pos += self.vel * d_T
```

### Rebound Approach
```python
# Set up simulation
sim = rebound.Simulation()
sim.G = G_SI
sim.units = ('m', 'kg', 's')

# Add bodies with real parameters
sim.add(m=M_SUN, x=0, y=0, z=0, vx=0, vy=0, vz=0)
sim.add(m=M_EARTH, x=AU, y=0, z=0, vx=0, vy=earth_orbital_velocity, vz=0)

# Let Rebound handle the physics
sim.integrate(sim.t + sim.dt)
```

## Real Astronomical Parameters Used

### Solar System Constants
- **AU**: 1.496 × 10¹¹ meters (Astronomical Unit)
- **M_SUN**: 1.989 × 10³⁰ kg (Solar mass)
- **M_EARTH**: 5.972 × 10²⁴ kg (Earth mass)
- **M_MOON**: 7.342 × 10²² kg (Moon mass)
- **G_SI**: 6.674 × 10⁻¹¹ m³ kg⁻¹ s⁻² (Gravitational constant)

### Orbital Parameters
- **Earth orbital velocity**: √(GM_SUN/AU) ≈ 29.8 km/s
- **Moon orbital velocity**: 1.022 km/s (relative to Earth)
- **Earth-Moon distance**: 384,400 km

## Visualization Enhancements

### Trail Visualization
- Orbital paths are drawn with fading trails
- Trail length is limited to prevent memory issues
- Different colors for different bodies

### Interactive Controls
- **SPACE**: Pause/Resume simulation
- **R**: Reset simulation
- **↑/↓**: Zoom in/out
- **WASD**: Pan view
- **+/-**: Speed up/slow down time

### Real-time Information Display
- Current simulation time (days/years)
- Earth's distance from Sun (AU)
- Earth's orbital speed (km/s)
- Moon's distance from Earth (when included)
- Current zoom level and time multiplier

## Educational Benefits

### 1. Numerical Integration Accuracy
Students can observe how different integration methods affect orbital stability:
- Euler method: Orbits spiral outward due to energy non-conservation
- WHFAST: Maintains stable orbits over thousands of years

### 2. Real-world Scale
Using actual astronomical parameters helps students understand:
- The vast scale of the solar system
- Realistic orbital velocities and periods
- The relationship between distance and orbital speed

### 3. Multi-body Dynamics
The extended version demonstrates:
- How the Moon's gravity affects Earth's orbit
- Three-body problem complexity
- Center-of-mass motion

## Running the Simulations

### Basic Version (stage3.py)
```bash
python lessons/stage3.py
```
Features:
- Sun and Earth only
- Basic controls and visualization
- Good for understanding fundamental concepts

### Extended Version (stage3_extended.py)
```bash
python lessons/stage3_extended.py
```
Features:
- Sun, Earth, and Moon
- Advanced controls (zoom, pan, time control)
- More detailed information display
- Better for exploring complex orbital mechanics

## Key Learning Outcomes

1. **Integration Methods Matter**: Different numerical methods have different stability properties
2. **Real Parameters**: Using actual astronomical data makes simulations educational and meaningful
3. **Professional Tools**: Libraries like Rebound provide tested, accurate implementations
4. **Visualization**: Interactive graphics help build intuition about orbital mechanics
5. **Scale Appreciation**: Understanding the vast scales involved in astronomy

## Next Steps

This foundation can be extended to explore:
- More complex solar system configurations
- Asteroid and comet trajectories
- Spacecraft trajectory planning
- Tidal effects and precession
- Relativistic corrections

The transition from custom physics to Rebound demonstrates how professional scientific software can make complex simulations both more accurate and more accessible for educational purposes.
