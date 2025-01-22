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
