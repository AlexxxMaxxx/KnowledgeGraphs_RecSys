import matplotlib.pyplot as plt

# Данные для content
x1 = [6250, 12500, 25000, 50000, 100000]
y1 = [0.6997, 0.7030, 0.7015, 0.7111, 0.7120]

# Данные для user base
x2 = [6250, 12500, 25000, 50000, 100000]
y2 = [0.8093, 0.7627, 0.7407,  0.7096, 0.6991]

# Данные для item base
x3 = [6250, 12500, 25000, 50000, 100000]
y3 = [0.7236, 0.7216, 0.7072,  0.6999, 0.6894]

# Построение первого графика
plt.plot(x1, y1, label='Content RS', color='blue')

# Построение второго графика
plt.plot(x2, y2, label='User-based RS', color='red')

# Построение второго графика
plt.plot(x3, y3, label='Item-based RS', color='green')
# Добавление легенды к графику
plt.legend()

# Настройка осей и заголовка графика
plt.xlabel('ratings')
plt.ylabel('MAE')
plt.title('Ограниченное количество данных')

# Отображение графика
plt.show()