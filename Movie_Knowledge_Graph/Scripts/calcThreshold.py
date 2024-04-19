# определение пороговой оценки (рейтинга),
# при которой можно считать, что пользователю понравился фильм

import pandas as pd

filePath_ratings = '../../Datasets/ratings.csv'
ratings_df = pd.read_csv(filePath_ratings)

total_ratings = ratings_df['rating'].count()
print(f'Общее количество оценок: {total_ratings}')

mean_rating = ratings_df['rating'].mean()
print(f'Среднее значение: {round(mean_rating, 4)}')

std_deviation = ratings_df['rating'].std()
print(f'Стандартное отклонение: {round(std_deviation, 4)}')

'''Пороговую оценку можно определить как значение, 
которое находится на определенное количество стандартных отклонений выше среднего значения. '''
threshold = mean_rating + std_deviation
print("Пороговая оценка, начиная с которой можно считать, что пользователю понравился фильм:", round(threshold, 4))