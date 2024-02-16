import pandas as pd
import matplotlib
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

matplotlib.use('TkAgg')  # Set the backend to TkAgg


def read_sensor_data(file_path, threshold=1.0):
    df = pd.read_csv(file_path)
    df = df[(abs(df['accel_x']) > threshold) &
            (abs(df['accel_y']) > threshold) &
            (abs(df['accel_z']) > threshold)]
    return df


def visualize_motion(ax, data, label):
    accel_x = data['accel_x']
    accel_y = data['accel_y']
    accel_z = data['accel_z']
    gyro_x = data['gyro_x']
    gyro_y = data['gyro_y']
    gyro_z = data['gyro_z']

    ax.set_xlabel('X Acceleration')
    ax.set_ylabel('Y Acceleration')
    ax.set_zlabel('Z Acceleration')
    ax.plot(accel_x, accel_y, accel_z, marker='o', linestyle='-', markersize=2, label='Acceleration')
    ax.plot(gyro_x, gyro_y, gyro_z, marker='o', linestyle='-', markersize=2, label='Gyroscope')
    ax.legend()
    ax.set_title(label)


if __name__ == "__main__":
    # Specify the path to your sensor data file
    folder_name = 'experiments/helicopter'
    files = [
        "/device_red_B0A104.csv",
        "/device_red_B1A105.csv",
        "/device_red_B1A104.csv",
        "/device_red_B0A105.csv",
    ]
    files = [folder_name + file for file in files]

    data_list = [read_sensor_data(file, threshold=0.07) for file in files]

    show_final = 1
    if show_final:
        fig, axs = plt.subplots(2, 2, figsize=(12, 8), subplot_kw={'projection': '3d'})
        axs[0, 0].set_title('Sensor 1')
        axs[0, 1].set_title('Sensor 2')
        axs[1, 0].set_title('Sensor 3')
        axs[1, 1].set_title('Sensor 4')

        visualize_motion(axs[0, 0], data_list[0], "Sensor 1")
        visualize_motion(axs[0, 1], data_list[1], "Sensor 2")
        visualize_motion(axs[1, 0], data_list[2], "Sensor 3")
        visualize_motion(axs[1, 1], data_list[3], "Sensor 4")

        plt.show()
    else:
        fig, axs = plt.subplots(2, 2, figsize=(10, 10), subplot_kw={'projection': '3d'})
        axs_flat = axs.flatten()


        def update(frame):
            for i, (ax, data) in enumerate(zip(axs_flat, data_list)):
                ax.clear()
                if frame < len(data):
                    visualize_motion(ax, data[:frame], f"Sensor {i + 1}")


        min_length = min(len(data) for data in data_list)
        ani = FuncAnimation(fig, update, frames=min_length, interval=200, repeat=False)
        plt.show()
