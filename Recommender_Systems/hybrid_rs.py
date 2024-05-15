import matplotlib.pyplot as plt
from math import sqrt
import numpy as np


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

    min_rmse = 99999
    min_mae = 99999
    w_min = -1

    for w in weight:
        predictions_hybrid = []
        for pred_RS, pred_EMB in zip(predictions_RS, predictions_EMB):
            predictions_hybrid.append(pred_RS.est * w + pred_EMB * (1 - w))

        rmse_value = modified_rmse(predictions_RS, predictions_hybrid)
        chart_rmseVal.append([w, rmse_value])

        mae_value = modified_mae(predictions_RS, predictions_hybrid)
        chart_maeVal.append([w, mae_value])

        if mae_value < min_mae:
            min_mae = mae_value
            min_rmse = rmse_value
            w_min = w

    getPlot(chart_rmseVal, 'RMSE', 'red', type + ' + Content KG')
    getPlot(chart_maeVal, 'MAE', 'blue', type + ' + Content KG')
    print(f'min_mae = {min_mae}')
    print(f'min_rmse = {min_rmse}')
    print(f'w_clbr = {w_min}, w_content = {1-w_min}\n')