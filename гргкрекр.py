import math
import numpy as np
import matplotlib.pyplot as plt

class Rectangle:
    def __init__(self, center_x, center_y, width=3, height=2, angle=0):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.angle = angle

    def get_corners(self):
        half_width = self.width / 2
        half_height = self.height / 2

        corners = [
            (-half_width, half_height),   # Верхний левый
            (half_width, half_height),    # Верхний правый
            (half_width, -half_height),   # Нижний правый
            (-half_width, -half_height)   # Нижний левый
        ]

        angle_rad = math.radians(self.angle)

        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        rotated_corners = []
        for x, y in corners:
            rotated_x = self.center_x + (x * cos_a - y * sin_a)
            rotated_y = self.center_y + (x * sin_a + y * cos_a)
            rotated_corners.append((rotated_x, rotated_y))

        return rotated_corners

    def __repr__(self):
        return f"Rectangle(center=({self.center_x}, {self.center_y}), width={self.width}, height={self.height}, angle={self.angle})"

class MovingRectangle(Rectangle):
    def __init__(self, center_x, center_y, width=3, height=2, angle=0):
        super().__init__(center_x, center_y, width, height, angle)
        self.t = 0
        self.corner_velocities = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.trajectory = []  # Для хранения траектории движения углов

    def get_velocity(self, t, x, y):
        vx = -0.1 * t * x  
        vy = 0.1 * t * y
        return vx, vy

    def runge_kutta_step(self, t, dt):
        def acceleration(t):
            return self.get_velocity(t, self.center_x, self.center_y)

        accelerations = [self.get_velocity(t, x, y) for x, y in self.get_corners()]

        new_corners = []
        for i, (x, y) in enumerate(self.get_corners()):
            ax1, ay1 = accelerations[i]
            k1_vx = ax1
            k1_vy = ay1
            k1_x = self.corner_velocities[i][0]
            k1_y = self.corner_velocities[i][1]

            ax2, ay2 = accelerations[i]
            k2_vx = ax2
            k2_vy = ay2
            k2_x = self.corner_velocities[i][0] + k1_vx * dt
            k2_y = self.corner_velocities[i][1] + k1_vy * dt

            new_vx = self.corner_velocities[i][0] + (k1_vx + k2_vx) * dt / 2
            new_vy = self.corner_velocities[i][1] + (k1_vy + k2_vy) * dt / 2

            new_x = x + (k1_x + k2_x) * dt / 2
            new_y = y + (k1_y + k2_y) * dt / 2

            new_corners.append((new_x, new_y))
            self.corner_velocities[i] = (new_vx, new_vy)

        self.update_corners(new_corners)
        self.trajectory.append(new_corners)  # Сохраняем траекторию

    def update_corners(self, new_corners):
        self.center_x = sum(x for x, y in new_corners) / 4
        self.center_y = sum(y for x, y in new_corners) / 4

        self.width = math.sqrt((new_corners[1][0] - new_corners[0][0])**2 + (new_corners[1][1] - new_corners[0][1])**2)
        self.height = math.sqrt((new_corners[2][0] - new_corners[1][0])**2 + (new_corners[2][1] - new_corners[1][1])**2)

    def move(self, delta_t):
        self.t += delta_t
        self.runge_kutta_step(self.t, delta_t)

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