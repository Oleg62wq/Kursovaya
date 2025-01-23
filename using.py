from Object import Rectangle
from moving import MovingRectangle
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
