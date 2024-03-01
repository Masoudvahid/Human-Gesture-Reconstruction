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

refresh_rate = 0.01

fig, axs = plt.subplots(2, 2, subplot_kw={'projection': '3d'})

for i, file_name in enumerate(file_names):
    data = np.genfromtxt(file_name, delimiter=',')

    accel_x = data[:, 0]
    accel_y = data[:, 1]
    accel_z = data[:, 2]

    position_x = np.zeros_like(accel_x)
    position_y = np.zeros_like(accel_x)
    position_z = np.zeros_like(accel_x)

    for j in range(1, len(accel_x)):
        position_x[j] = position_x[j - 1] + (accel_x[j] * refresh_rate ** 2)
        position_y[j] = position_y[j - 1] + (accel_y[j] * refresh_rate ** 2)
        position_z[j] = position_z[j - 1] + (accel_z[j] * refresh_rate ** 2)

    trajectory_data = np.column_stack((position_x, position_y, position_z))
    output_file_name = '{}/trajectory{}.csv'.format(folder_name, i + 1)
    np.savetxt(output_file_name, trajectory_data, delimiter=',')

    ax = axs[i // 2, i % 2]
    ax.plot3D(position_x, position_y, position_z)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Trajectory {}'.format(i + 1))

plt.tight_layout()
plt.show()
