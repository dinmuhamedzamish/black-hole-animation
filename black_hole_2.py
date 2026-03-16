

import numpy as np

import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

from matplotlib.patches import Circle

import matplotlib.cm as cm



# ========================

# PARAMETERS - FIXED

# ========================

BLACK_HOLE_MASS = 1_000_000.0

BLACK_HOLE_RADIUS = 2.0

TIDAL_RADIUS = 48.0

STAR_RADIUS = 2.0

STAR_DISTANCE = 70.0

NUM_PARTICLES = 1800

G = 1.0

DT = 0.03  # smaller for accuracy

FRICTION = 0.010 # higher for faster spiral in



# ========================

# INITIALIZE STAR

# ========================

def create_star():

    """Create a spherical star made of particles"""

    particles = []

   

    for i in range(NUM_PARTICLES):

        # Random position in sphere

        theta = np.random.uniform(0, 2 * np.pi)

        phi = np.random.uniform(0, np.pi)

        r = STAR_RADIUS * (np.random.random() ** (1/3))

       

        # Convert to Cartesian

        x = STAR_DISTANCE + r * np.sin(phi) * np.cos(theta)

        y = r * np.sin(phi) * np.sin(theta)

       

        # Orbital velocity - fixed for proper TDE orbit

        dist = np.sqrt(x**2 + y**2)

        v_tangential = np.sqrt(G * BLACK_HOLE_MASS / dist) * 0.9

       

        vx = -v_tangential * y / dist  # no extra factor

        vy = v_tangential * x / dist   # no extra factor

       

        particles.append({

            'x': x, 'y': y,

            'vx': vx, 'vy': vy,

            'alive': True,

            'disk': False,

            'color': r / STAR_RADIUS

        })

   

    return particles



# ========================

# PHYSICS UPDATE

# ========================

def update_physics(particles):

    """Update all particles - fixed to actually work!"""

    for p in particles:

        if not p['alive']:

            continue

       

        # Distance from black hole

        r = np.sqrt(p['x']**2 + p['y']**2)

       

        # Consumed by black hole

        if r < BLACK_HOLE_RADIUS * 2.5:

            p['alive'] = False

            continue

       

        # Enter accretion disk at tidal radius

        if r < TIDAL_RADIUS and not p['disk']:

            p['disk'] = True

       

        # Gravitational force

        if r > 0.01:

            a = G * BLACK_HOLE_MASS / (r * r)

            ax = -a * p['x'] / r

            ay = -a * p['y'] / r

        else:

            ax = ay = 0

       

        # Accretion disk behavior

        if p['disk']:

            # Tangential velocity boost (creates swirling)

            L = p['x'] * p['vy'] - p['y'] * p['vx']

            factor = L / (r * r + 0.1) * 0.08

           

            perp_x = -p['y'] / r

            perp_y = p['x'] / r

           

            p['vx'] += perp_x * factor

            p['vy'] += perp_y * factor

           

            # Friction causes inward spiral

            p['vx'] *= (1 - FRICTION)

            p['vy'] *= (1 - FRICTION)

           

            # Stronger pull in disk

            ax *= 1.05

            ay *= 1.05

       

        # Update velocity and position

        p['vx'] += ax * DT

        p['vy'] += ay * DT

        p['x'] += p['vx'] * DT

        p['y'] += p['vy'] * DT



# ========================

# VISUALIZATION

# ========================

particles = create_star()



fig = plt.figure(figsize=(12, 9), facecolor='black')

ax = fig.add_subplot(111, facecolor='black')

ax.set_xlim(-80, 80)  # widened to see full approach

ax.set_ylim(-80, 80)  # widened

ax.set_aspect('equal')

ax.axis('off')



# Create scatter plot

scat = ax.scatter([], [], s=[], c=[], cmap='hot', alpha=0.8, edgecolors='none')



# Black hole visualization

bh_circle = Circle((0, 0), BLACK_HOLE_RADIUS, color='black', zorder=100)

ax.add_patch(bh_circle)



# Event horizon glow

glow1 = Circle((0, 0), BLACK_HOLE_RADIUS + 0.5, color='red', alpha=0.3, zorder=99)

glow2 = Circle((0, 0), BLACK_HOLE_RADIUS + 1.0, color='orange', alpha=0.15, zorder=98)

glow3 = Circle((0, 0), BLACK_HOLE_RADIUS + 2.0, color='yellow', alpha=0.08, zorder=97)

ax.add_patch(glow1)

ax.add_patch(glow2)

ax.add_patch(glow3)



# Tidal radius

tidal = Circle((0, 0), TIDAL_RADIUS, fill=False,

               edgecolor='cyan', linestyle='--', linewidth=2, alpha=0.4, zorder=1)

ax.add_patch(tidal)



# Text

title = ax.text(0, 75, 'Tidal Disruption Event',

               fontsize=20, color='white', ha='center', weight='bold')

time_text = ax.text(-75, 70, '', fontsize=11, color='white')

stats_text = ax.text(-75, 65, '', fontsize=10, color='cyan')

phase_text = ax.text(-75, 60, '', fontsize=11, color='yellow', weight='bold')



# Info

ax.text(-75, -75, '━ Cyan dashed = Tidal disruption radius',

        fontsize=8, color='cyan')

ax.text(-75, -78, '● Red/Orange = Black hole event horizon',

        fontsize=8, color='orange')



frame_counter = [0]



def animate(frame):

    """Animation function"""

    frame_counter[0] += 1

   

    # Reset simulation if mostly consumed (for repetitions)

    alive_particles = [p for p in particles if p['alive']]

    if len(alive_particles) < NUM_PARTICLES * 0.1:

        frame_counter[0] = 0

        particles[:] = create_star()

   

    # Update physics

    update_physics(particles)

   

    # Separate particles by state

    alive = [p for p in particles if p['alive']]

    intact = [p for p in alive if not p['disk']]

    disk = [p for p in alive if p['disk']]

    consumed = len([p for p in particles if not p['alive']])

   

    # Prepare data for plotting

    if alive:

        x_coords = [p['x'] for p in alive]

        y_coords = [p['y'] for p in alive]

       

        # Size based on distance (closer = hotter = bigger)

        sizes = []

        colors = []

        for p in alive:

            r = np.sqrt(p['x']**2 + p['y']**2)

            if p['disk']:

                # Hot accretion disk - size by distance

                heat = max(0, 1 - r / (TIDAL_RADIUS * 1.5))

                sizes.append(10 + heat * 40)

                colors.append(0.3 + heat * 0.7)  # Hotter = brighter

            else:

                # Intact star

                sizes.append(15)

                colors.append(p['color'] * 0.5)

       

        scat.set_offsets(np.c_[x_coords, y_coords])

        scat.set_sizes(sizes)

        scat.set_array(np.array(colors))

    else:

        scat.set_offsets(np.empty((0, 2)))

   

    # Update text

    hours = frame_counter[0] * DT * 0.25

    time_text.set_text(f'Time: {hours:.1f} hours')

    stats_text.set_text(

        f'Intact: {len(intact)}  |  Disk: {len(disk)}  |  Consumed: {consumed}'

    )

   

    # Phase

    if len(intact) > NUM_PARTICLES * 0.6:

        phase = "PHASE 1: Approach"

    elif len(intact) > NUM_PARTICLES * 0.2:

        phase = "PHASE 2: Spaghettification!"

    elif len(disk) > NUM_PARTICLES * 0.3:

        phase = "PHASE 3: Accretion Disk"

    else:

        phase = "PHASE 4: Consumption"

    phase_text.set_text(phase)

   

    return scat, time_text, stats_text, phase_text



# ========================

# RUN

# ========================

print("\n" + "="*70)

print("  🌟  TIDAL DISRUPTION EVENT SIMULATOR  🕳️")

print("="*70)

print(f"\n  Simulating {NUM_PARTICLES} particles")

print("  Watch as the star is torn apart and consumed!\n")

print("  Starting animation...")

print("="*70 + "\n")



anim = FuncAnimation(fig, animate, interval=40, blit=True)  # infinite, slower visual



plt.tight_layout()

plt.show(block=True)  # ensures window stays open



print("\n" + "="*70)

print("SIMULATION COMPLETE")

print("="*70)

print("\nWhat you saw:")

print("  • Yellow/dim particles = Intact star")

print("  • Bright white/yellow = Hot accretion disk")

print("  • Disappearing particles = Consumed by black hole")

print("\nReal timescales:")

print("  • Disruption: 1-12 hours")

print("  • Disk formation: Days-weeks")

print("  • Full consumption: Months-years")

print("="*70 + "\n")