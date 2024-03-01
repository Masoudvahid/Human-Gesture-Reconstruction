import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

folder_name = r'experiments/1minwalk'
files = [
    "/device_red_B0A104.csv",
    "/device_red_B1A105.csv",
    "/device_red_B1A104.csv",
    "/device_red_B0A105.csv",
]
file_names = [folder_name + file for file in files]

fig, axs = plt.subplots(2, 2, subplot_kw={'projection': '3d'})

for i, file_name in enumerate(file_names):
    data = np.genfromtxt(file_name, delimiter=',')

    accel_x = data[1:, 0]
    accel_y = data[1:, 1]
    accel_z = data[1:, 2]

    # Time array (assuming data is sampled at a constant rate)
    time = np.arange(0, len(accel_x))  # Adjust the time scale if needed
    dt = time[1] - time[0]
    dt = 0.01

    # Integrate accelerometer data to get velocity
    vel_x = np.cumsum(accel_x) * dt
    vel_y = np.cumsum(accel_y) * dt
    vel_z = np.cumsum(accel_z) * dt

    # Integrate velocity to get displacement
    disp_x = np.cumsum(vel_x) * dt
    disp_y = np.cumsum(vel_y) * dt
    disp_z = np.cumsum(vel_z) * dt

    ax = axs[i // 2, i % 2]
    # ax.plot3D(position_x, position_y, position_z)
    ax.plot3D(disp_x, disp_y, disp_z)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Trajectory {}'.format(i + 1))

plt.tight_layout()
plt.show()
