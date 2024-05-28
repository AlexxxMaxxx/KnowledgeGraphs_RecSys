import matplotlib.pyplot as plt

# Данные для content
x1 = [250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000]
y1 = [0.7122, 0.7183, 0.7223, 0.7243, 0.7296, 0.7290, 0.7303, 0.7311, 0.7310, 0.7318, 0.7326, 0.7330]

# Данные для user base
x2 = [250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000]
y2 = [0.7754, 0.7875, 0.7955, 0.8020, 0.8054, 0.8093, 0.8121, 0.8156, 0.8187, 0.8200, 0.8210, 0.8218]

# Данные для item base
x3 = [250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000]
y3 = [0.7595, 0.7745, 0.7866, 0.7943, 0.8018, 0.8058, 0.8088, 0.8113, 0.8141, 0.8160, 0.8176, 0.8195]

# Построение первого графика
plt.plot(x1, y1, label='Content RS', color='blue')

# Построение второго графика
plt.plot(x2, y2, label='User-based RS', color='red')

# Построение второго графика
plt.plot(x3, y3, label='Item-based RS', color='green')
# Добавление легенды к графику
plt.legend()

# Настройка осей и заголовка графика
plt.xlabel('New movies')
plt.ylabel('MAE')
plt.title('Холодный старт объектов')

# Отображение графика
plt.show()