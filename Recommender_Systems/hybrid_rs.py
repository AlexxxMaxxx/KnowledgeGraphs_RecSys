import additionalFunctions as af
import matplotlib.pyplot as plt
from math import sqrt
import pandas as pd
import numpy as np
import pickle


def modified_mae(predictions_RS, predictions_hybrid):
    errors = []
    for pred_hybrid, pred_RS in zip(predictions_hybrid, predictions_RS):
        errors.append(abs(pred_hybrid - pred_RS.r_ui))
    return sum(errors) / len(predictions_hybrid)


def modified_rmse(predictions_RS, predictions_hybrid):
    squared_errors = []
    for pred_hybrid, pred_RS in zip(predictions_hybrid, predictions_RS):
        squared_errors.append((pred_hybrid - pred_RS.r_ui) ** 2)
    mean_squared_error = sum(squared_errors) / len(predictions_hybrid)
    return sqrt(mean_squared_error)


def getPlot(chart_val, label, color, text):
    chart_val_np = np.array(chart_val)
    x = chart_val_np[:, 0]
    y = chart_val_np[:, 1]

    fig, ax = plt.subplots()
    ax.plot(x, y, label='hybrid', color=color)
    ax.legend()
    plt.title(text)
    plt.xlabel('w')
    plt.ylabel(label)
    plt.show()


def hybridPrediction(predictions_RS, predictions_EMB, type):
    chart_rmseVal = []
    chart_maeVal = []
    weight = np.linspace(0, 1, 21)

    for w in weight:
        predictions_hybrid = []
        for pred_RS, pred_EMB in zip(predictions_RS, predictions_EMB):
            predictions_hybrid.append(pred_RS.est * w + pred_EMB * (1 - w))

        rmse_value = modified_rmse(predictions_RS, predictions_hybrid)
        chart_rmseVal.append([w, rmse_value])

        mae_value = modified_mae(predictions_RS, predictions_hybrid)
        chart_maeVal.append([w, mae_value])

    getPlot(chart_rmseVal, 'RMSE', 'red', type + ' + Content KG')
    getPlot(chart_maeVal, 'MAE', 'blue', type + ' + Content KG')


comb = 'comb1'
df = 'df1'

# collaborative RS
RS_type = 'KNNBasic_Item'

# content RS
combination = '32_50_30_8'

filePath_clbrRS = '../Datasets/experiments/collaborative_rs/' + RS_type + '/' + df + '_' + comb
filePath_model = filePath_clbrRS + '/models/' + RS_type + '.pkl'

# Загрузка сохраненной модели из файла
with open(filePath_model, 'rb') as file:
    KNNBasic_User_model = pickle.load(file)

test_data_path = filePath_clbrRS + '/test_data_' + df + '.pkl'
test_data = af.pikcle_load(test_data_path)

predictions_RS = KNNBasic_User_model.test(test_data)

# content RS
combination = '32_50_30_8'
filePath_predictions_CRS = '../Datasets/experiments/content_rs/combsEmb/' + \
                           df + '_' + comb + '/predictions/predict_' + combination + '.csv'
predictions_CRS = pd.read_csv(filePath_predictions_CRS, header=None)
column_names = ['est']  # замените на нужные названия столбцов
predictions_CRS.columns = column_names
predictions_CRS = predictions_CRS['est'].tolist()


print(predictions_CRS)

hybridPrediction(predictions_RS, predictions_CRS, RS_type)

# другие способы гибридизации