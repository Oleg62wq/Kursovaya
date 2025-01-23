import math
import numpy as np
import matplotlib.pyplot as plt
from Object import Rectangle
from moving import MovingRectangle
def plot_velocity_distribution(rect, times):
    # Построение распределения скоростей для разных моментов времени
    fig, axs = plt.subplots(1, len(times), figsize=(15, 5))
    fig.canvas.manager.set_window_title("Распределение скоростей")

    x = np.linspace(-20, 20, 30)
    y = np.linspace(-20, 20, 30)
    X, Y = np.meshgrid(x, y)

    for idx, t in enumerate(times):
        U = np.zeros_like(X)
        V = np.zeros_like(Y)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                U[i, j], V[i, j] = rect.get_velocity(t, X[i, j], Y[i, j])
        axs[idx].quiver(X, Y, U, V, scale=50, color='green')
        axs[idx].set_title(f"Распределение скоростей при t = {t}")
        axs[idx].set_xlim(-20, 20)
        axs[idx].set_ylim(-20, 20)
        axs[idx].axhline(0, color='black', linewidth=0.5)
        axs[idx].axvline(0, color='black', linewidth=0.5)
        axs[idx].grid(color='gray', linestyle='--', linewidth=0.5)

    plt.tight_layout()
    plt.show()


def plot_streamlines(rect, times):
    # Построение линий тока для разных моментов времени
    fig, axs = plt.subplots(1, len(times), figsize=(15, 5))
    fig.canvas.manager.set_window_title("Линии тока")

    x = np.linspace(-20, 20, 30)
    y = np.linspace(-20, 20, 30)
    X, Y = np.meshgrid(x, y)

    for idx, t in enumerate(times):
        U = np.zeros_like(X)
        V = np.zeros_like(Y)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                U[i, j], V[i, j] = rect.get_velocity(t, X[i, j], Y[i, j])

        axs[idx].streamplot(X, Y, U, V, color='blue', density=2, arrowstyle='->', arrowsize=1.5)
        axs[idx].set_title(f"Линии тока при t = {t}")
        axs[idx].set_xlim(-20, 20)
        axs[idx].set_ylim(-20, 20)
        axs[idx].axhline(0, color='black', linewidth=0.5)
        axs[idx].axvline(0, color='black', linewidth=0.5)
        axs[idx].grid(color='gray', linestyle='--', linewidth=0.5)

    plt.tight_layout()
    plt.show()

    def plot_trajectory(rect):
    # Построение траектории
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.canvas.manager.set_window_title("Траектория движения прямоугольника")

    # Начальное положение
    initial_corners = rect.trajectory[0]
    x_init, y_init = zip(*initial_corners)
    ax.plot(x_init + (x_init[0],), y_init + (y_init[0],), 'bo-', label="Начальное положение")

    # Конечное положение
    final_corners = rect.trajectory[-1]
    x_final, y_final = zip(*final_corners)
    ax.plot(x_final + (x_final[0],), y_final + (y_final[0],), 'ro-', label="Конечное положение")

    # Траектория движения углов
    for i in range(4):
        x_traj = [step[i][0] for step in rect.trajectory]
        y_traj = [step[i][1] for step in rect.trajectory]
        ax.plot(x_traj, y_traj, 'g--', label=f"Траектория угла {i+1}" if i == 0 else "")

    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    ax.legend()
    plt.show()
if __name__ == "__main__":
    try:
        center_x = float(input("Введите X координату центра прямоугольника: "))
        center_y = float(input("Введите Y координату центра прямоугольника: "))
        angle = float(input("Введите угол наклона прямоугольника в градусах: "))

        rect = MovingRectangle(center_x, center_y, angle=angle)

        print(rect)
        print("Координаты углов прямоугольника:", rect.get_corners())

        # Двигаем прямоугольник до t = 4
        delta_t = 0.1
        while rect.t <= 4:
            rect.move(delta_t)

        # Построение графиков
        plot_velocity_distribution(rect, [1, 2, 3])  
        plot_streamlines(rect, [1, 2, 3])           
        plot_trajectory(rect)                       

    except ValueError:
        print("Пожалуйста, вводите только числовые значения.")
