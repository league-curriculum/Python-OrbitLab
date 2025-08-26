# Physics for Games Programming Style Guide

This style guide defines the consistent structure, naming conventions, and patterns used in physics-based game programming for the Python-OrbitLab curriculum. It covers both component-based and vector-based programming styles.

## 1. Overall File Structure

### Import Order
```python
import pygame
from dataclasses import dataclass
```

### Class Declaration Order
1. `Settings` dataclass
2. `Body` class (if applicable)
3. `Simulation` class
4. `main()` function
5. Main guard

## 2. Settings Dataclass

### Structure
```python
@dataclass
class Settings:
    """Class to hold all game settings and constants."""
    
    # Screen settings
    SCREEN_WIDTH: int = 600
    SCREEN_HEIGHT: int = 600
    
    # Object settings (Square/Player/etc)
    OBJECT_SIZE: int = 50
    OBJECT_COLOR = (255, 0, 0)  # Red
    
    # Physics settings
    GRAVITY: float = 60.0
    MASS: float = 2.0
    
    # Display settings
    BACKGROUND_COLOR = (0, 0, 0)  # Black
    FPS: int = 60
    TIMESCALE: int = 1
    
    def __post_init__(self):
        """Calculate derived values after initialization."""
        self.d_t = self.TIMESCALE / self.FPS  # Time step for physics calculations
```

### Naming Conventions for Settings
- **Screen dimensions**: `SCREEN_WIDTH`, `SCREEN_HEIGHT`
- **Frame rate**: `FPS`
- **Time step**: `d_t` (calculated in `__post_init__`)
- **Colors**: `BACKGROUND_COLOR`, `OBJECT_COLOR`, `SQUARE_COLOR`, `PLAYER_COLOR`
- **Sizes**: `SQUARE_SIZE`, `PLAYER_SIZE`, `OBJECT_SIZE`
- **Physics constants**: `GRAVITY`, `MASS`, `K` (spring constant)
- **Velocities**: `JUMP_VELOCITY`, `JUMP_VELOCITY_X`, `JUMP_VELOCITY_Y`, `SQUARE_SPEED`

### Type Annotations
- All settings fields must have type annotations except colors
- Colors: No type annotation required (e.g., `BACKGROUND_COLOR = (0, 0, 0)`)
- Numeric values: `int` or `float` as appropriate
- Constants should be UPPERCASE

## 3. Body or Player Class (Component-Based Style)

### Structure
```python
class Body:
    """Class representing a physical body with position, velocity, and acceleration."""
    
    def __init__(self, x: float, y: float, mass: float, settings: Settings, v_x: float = 0.0, v_y: float = 0.0):
        """Initialize the body with position, physics properties, and optional initial velocity."""
        # Position components
        self.x = x
        self.y = y
        
        # Velocity components  
        self.v_x = v_x
        self.v_y = v_y
        
        # Acceleration components
        self.a_x = 0.0
        self.a_y = 0.0
        
        # Physics properties
        self.mass = mass
        self.settings = settings
        
        # Object properties
        self.size = settings.OBJECT_SIZE  # or SQUARE_SIZE, PLAYER_SIZE
    
    def update(self):
        """Update the body's position and velocity based on acceleration."""
        # Update velocity with acceleration
        self.v_x += self.a_x * self.settings.d_t
        self.v_y += self.a_y * self.settings.d_t
        
        # Update position with velocity
        self.x += self.v_x * self.settings.d_t
        self.y += self.v_y * self.settings.d_t
        
        # Reset acceleration (forces need to be applied each frame)
        self.a_x = 0.0
        self.a_y = 0.0
    
    def draw(self, screen: pygame.Surface):
        """Draw the body on the screen."""
        pygame.draw.rect(
            screen,
            self.settings.OBJECT_COLOR,
            (self.x, self.y, self.size, self.size)
        )
```

### Component-Based Variable Naming
- **Position**: `x`, `y`
- **Velocity**: `v_x`, `v_y`
- **Acceleration**: `a_x`, `a_y`
- **Force**: `f_x`, `f_y`
- **Displacement**: `d_x`, `d_y`
- **Target**: `t_x`, `t_y`
- **Change in position**: `d_x`, `d_y` (context-dependent)

### Physics Methods
Common physics methods should follow these patterns:
- `apply_gravity(gravity: float)` - Sets `self.a_y = gravity`
- `apply_spring_force(t_x: float, t_y: float, k: float)` - Calculates and sets acceleration
- `jump(jump_velocity: float)` - Sets initial velocity
- `check_ground_collision(ground_y: float) -> bool` - Collision detection with position correction

## 4. Vector-Based Style (Future Extension)

### Variable Naming Convention
When using vector-based physics, follow this naming pattern:
- **Vector name**: Single letter (e.g., `r`, `v`, `a`, `f`)
- **Component names**: Vector name + underscore + component (e.g., `r_x`, `r_y`)

Examples for vector-based style:
```python
# Position vector 'r'
self.r_x = x  # x-component of position
self.r_y = y  # y-component of position

# Velocity vector 'v'  
self.v_x = 0.0  # x-component of velocity
self.v_y = 0.0  # y-component of velocity

# Acceleration vector 'a'
self.a_x = 0.0  # x-component of acceleration
self.a_y = 0.0  # y-component of acceleration

# Force vector 'f'
self.f_x = 0.0  # x-component of force
self.f_y = 0.0  # y-component of force
```

**Note**: The current programs use component-based style (shown in Section 3) where components are named directly (e.g., `v_x`, `v_y`) without reference to a vector name. Vector-based implementations will be defined more completely when vector-based programs are available for analysis.

## 5. Simulation Class

### Structure
```python
class Simulation:
    """Class to handle the main simulation loop and coordinate the physics simulation."""
    
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Create settings object
        self.settings = Settings()
        
        # Initialize the screen
        self.screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Window Title")
        
        # Clock to control the frame rate
        self.clock = pygame.time.Clock()
        
        # Initialize game objects
        # ... create bodies, set initial state
    
    def update(self):
        """Update the physics simulation."""
        # Apply forces to bodies
        # Call body.update() for each body
        # Handle collisions
        pass
    
    def draw(self):
        """Draw everything on the screen."""
        # Clear screen
        self.screen.fill(self.settings.BACKGROUND_COLOR)
        
        # Draw all bodies
        # body.draw(self.screen) for each body
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main simulation loop."""
        running = True
        
        while running:
            # Event handling - REQUIRED
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Update physics
            self.update()
            
            # Draw everything
            self.draw()
            
            # Frame rate control - REQUIRED
            self.clock.tick(self.settings.FPS)
        
        # Quit Pygame
        pygame.quit()
```

### Method Requirements

- **`update()`**: Must call `body.update()` for each body
- **`draw()`**: Must call `body.draw(screen)` for each body
- **`run()`**: Must contain main loop with event handling and clock tick

## 6. Main Function and Guard

### Required Structure
```python
def main():
    """Main function to start the simulation."""
    simulation = Simulation()
    simulation.run()


if __name__ == "__main__":
    main()
```

## 7. Main Loop Requirements

### Event Handling (REQUIRED)
```python
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
```

### Frame Rate Control (REQUIRED)
```python
self.clock.tick(self.settings.FPS)
```

### Loop Structure
```python
while running:
    # 1. Event handling (required)
    # 2. Update physics
    # 3. Draw everything  
    # 4. Frame rate control (required)
```

## 8. Documentation Standards

### Class Docstrings
- Settings: `"Class to hold all game settings and constants."`
- Body: `"Class representing a physical body with position, velocity, and acceleration."`
- Simulation: `"Class to handle the main simulation loop and coordinate the physics simulation."`

### Method Docstrings
- Always include purpose of the method
- Document parameters and return values when applicable
- Use consistent language patterns

### File Header
```python
"""

Program Title - Object Oriented Version

Brief description of what the program demonstrates.

This version uses Object Oriented Programming with a Settings dataclass to hold
all constants, a Body class for physics objects, and a Simulation class 
to handle the main loop and game logic.

"""
```

## 9. Physics Integration Patterns

### Force Application
1. Calculate forces
2. Apply forces to set acceleration
3. Call `body.update()` to integrate motion
4. Reset acceleration in `update()` method

### Standard Physics Loop
```python
def update(self):
    # Apply forces (sets acceleration)
    body.apply_gravity(self.settings.GRAVITY)
    
    # Integrate motion (velocity and position)
    body.update()
    
    # Handle collisions
    body.check_collisions(...)
```

## 10. Common Patterns

### Position Updates
```python
# In Body.update()
self.v_x += self.a_x * self.settings.d_t
self.v_y += self.a_y * self.settings.d_t
self.x += self.v_x * self.settings.d_t  
self.y += self.v_y * self.settings.d_t
```

### Collision Detection
- Return boolean indicating collision occurred
- Correct position to valid location
- Update velocity as appropriate for collision type

### Screen Clearing and Drawing
```python
# In Simulation.draw()
self.screen.fill(self.settings.BACKGROUND_COLOR)
# ... draw objects ...
pygame.display.flip()
```

This style guide ensures consistent, readable, and maintainable physics simulation code across all programs in the curriculum.
