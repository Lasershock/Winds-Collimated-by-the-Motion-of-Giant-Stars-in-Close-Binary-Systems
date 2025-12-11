# main.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# === Configuration ===
red_radius = 1.2
blue_radius = 3.0
orbit_period = 120  # number of frames in one orbit
red_circ = 2 * np.pi * red_radius  # circumference
red_speed = red_circ / orbit_period  # speed per frame (unused directly but kept)
center = np.array([0.0, 0.0, 0.0])

particles_frame = 400  # particles emitted per frame
wind_speed = red_speed
particle_life = 1000
period = 4.8
frame_time = period / orbit_period

# theta array used for circular motion (length = orbit_period)
theta = np.linspace(0, 2 * np.pi, orbit_period, endpoint=False)

absorption_radius = 2.5
absorption_speed = 0.05

# === Figure / Axes setup ===
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-10, 10)
ax.view_init(elev=90, azim=180)  # try other values if desired

# particle storage: pos (N x 3), vel (N x 3), age (N,)
particles = {
    'pos': np.empty((0, 3)),
    'vel': np.empty((0, 3)),
    'age': np.empty((0,))
}


def setup_cords():
    """Reset view/limits and return a 2D text object for simulation time display."""
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-10, 10)
    ax.view_init(elev=90, azim=180)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.grid(False)
    return ax.text2D(0.05, 0.95, "", transform=ax.transAxes)


def emit_particles(x, y, z, n, radius):
    """Emit n particles from a spherical shell centered at (x,y,z) with given radius.
    Particles get initial velocities based on random directions scaled by wind_speed.
    """
    if n <= 0:
        return

    azimuthal_angles = np.random.uniform(0, 2 * np.pi, n)
    polar_angles = np.arccos(np.random.uniform(-1, 1, n))

    vx = np.cos(azimuthal_angles) * np.sin(polar_angles) * wind_speed
    vy = np.sin(azimuthal_angles) * np.sin(polar_angles) * wind_speed
    vz = np.cos(polar_angles) * wind_speed

    new_pos_x = x + radius * np.cos(azimuthal_angles) * np.sin(polar_angles)
    new_pos_y = y + radius * np.sin(azimuthal_angles) * np.sin(polar_angles)
    new_pos_z = z + radius * np.cos(polar_angles)

    new_pos = np.stack([new_pos_x, new_pos_y, new_pos_z], axis=1)
    new_vel = np.stack([vx, vy, vz], axis=1)
    new_age = np.zeros(n)

    particles['pos'] = np.vstack([particles['pos'], new_pos])
    particles['vel'] = np.vstack([particles['vel'], new_vel])
    particles['age'] = np.concatenate([particles['age'], new_age])


def update_particles(blue_pos):
    """Advance particle positions, apply absorption force towards blue_pos, and remove absorbed particles."""
    if particles['pos'].shape[0] == 0:
        return

    # Move and age
    particles['pos'] = particles['pos'] + particles['vel']
    particles['age'] = particles['age'] + 1

    # Distances to blue object
    distances = np.linalg.norm(particles['pos'] - blue_pos, axis=1)

    # Find particles within absorption radius
    close_mask = distances < absorption_radius
    if np.any(close_mask):
        direction_to_blue = blue_pos - particles['pos'][close_mask]
        norms = np.linalg.norm(direction_to_blue, axis=1)
        # avoid division by zero
        norms[norms == 0] = 1.0
        normalized_direction = direction_to_blue / norms[:, np.newaxis]
        absorption_force = absorption_speed * normalized_direction
        particles['vel'][close_mask] = absorption_force

    # Remove particles that are effectively absorbed (very close)
    absorbed_mask = distances < 0.1
    alive_mask = ~absorbed_mask
    particles['pos'] = particles['pos'][alive_mask]
    particles['vel'] = particles['vel'][alive_mask]
    particles['age'] = particles['age'][alive_mask]


def update_frames(frame):
    """Animation update for a single frame index."""
    ax.clear()
    time_text = setup_cords()

    frame_idx = int(frame) % orbit_period

    # red position (emitter)
    x_red = center[0] + red_radius * np.cos(theta[frame_idx])
    y_red = center[1] + red_radius * np.sin(theta[frame_idx])
    z_red = center[2]

    # blue position (absorber) opposite phase
    x_blue = center[0] + blue_radius * np.cos(theta[frame_idx] + np.pi)
    y_blue = center[1] + blue_radius * np.sin(theta[frame_idx] + np.pi)
    z_blue = center[2]
    blue_pos = np.array([x_blue, y_blue, z_blue])

    # emit and update particles
    emit_particles(x_red, y_red, z_red, particles_frame, red_radius)
    update_particles(blue_pos)

    # draw red and blue points
    ax.scatter(x_red, y_red, z_red, color='red', s=80, alpha=1.0, zorder=5)
    ax.scatter(x_blue, y_blue, z_blue, color='blue', s=20, alpha=1.0, zorder=5)

    # draw particles (if any)
    if particles['pos'].shape[0] > 0:
        ax.scatter(
            particles['pos'][:, 0],
            particles['pos'][:, 1],
            particles['pos'][:, 2],
            s=0.05,
            color='C0',
            alpha=0.3,
            zorder=2
        )

    sim_time = frame_idx * frame_time
    time_text.set_text('Simulation Time: {:.2f} hours'.format(sim_time))

    # Return a sequence of artists to be re-drawn (FuncAnimation can accept None as well)
    return ax,


def main():
    ani = FuncAnimation(
        fig,
        update_frames,
        frames=np.arange(orbit_period),
        blit=False,
        repeat=True,
        interval=80
    )
    plt.show()


if __name__ == '__main__':
    main()
