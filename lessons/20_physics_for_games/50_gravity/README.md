# Gravity

Our prior programs have the player moving around the screen, which means there
is a change of position. 

Gravity is a constant force, so it will cause an acelleration; if your drop a
ball it will fall toward the earth, propelled by gravity, moving faster and
faster. 

$$
F = m a
$$

* $F$ is the force on the object
* $a$ is the aceleration
* $m$ is the mass of the object. 

We will also need to use our equations of motion:

$$
\begin{aligned}
v &= a t \\
x &= v t 
\end{aligned}
$$

Since we update our program multiple times a second, at the FPS framerate, our
$t$ is really a timestep, a slice of the total time. In mathematics we will
refer to this as "Delta t", or $\Delta t$, but in code we will write `d_t`

Here is what the important part of the physics looks like in code

```python 

t = 0
v = 0
x = 0
a_x = 10 # Our acceleration or gravity

while True:

    t += d_t
    v_x += a_x * d_t
    x += v_x * d_t

```

# Assignment

* Add X velocity X acceleration using the left and right keys. Each key will
  provide a small change in the velocity
* Add additional upward thrust with the up arrow. 
* Make the player bounce off the left and right walls. Hint: after the bounce,
  the X velocity will be the opposite of what it was before the bounce. 
