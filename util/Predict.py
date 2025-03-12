import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from pmdarima.arima import auto_arima

data = pd.read_csv('数据2.csv', parse_dates=True)
# 将字符型的时间转换为时间格式
data['date'] = pd.to_datetime(data['date'])
# 将时间列设为索引，并按照时间排序
df = data.set_index('date').sort_index()
# 进行差分处理
df_diff = df.diff().dropna()
df.index.freq = 'D'
# 确定ARIMA模型的p、d、q参数
auto_model = auto_arima(df_diff, start_p=0, start_q=0, max_p=10, max_q=10, d=None, trace=True, error_action='ignore',
                        suppress_warnings=True, stepwise=True)
print(auto_model.summary())
# 训练ARIMA模型并进行预测
train_data = df_diff[:len(df_diff) - 30]
test_data = df_diff[len(df_diff) - 30:]
arima_model = sm.tsa.ARIMA(train_data, order=(2,1,2))
arima_result = arima_model.fit()
pred = arima_result.predict(start=len(train_data), end=len(train_data) + len(test_data) - 1, typ='levels')
# 将预测结果反差分
diff_recover = df_diff.shift(1)
diff_recover.iloc[0] = df.iloc[0]
predictions = diff_recover.add(pred, fill_value=None)
# 可视化预测结果
plt.plot(train_data.index[1:], arima_result.fittedvalues, label='Fitted', color='blue')
plt.plot(train_data.index, train_data, label='Train', color='green')
plt.plot(test_data.index, predictions, label='Predict', color='red')
plt.figure(figsize=(15, 6))
plt.plot(df.index, df, label='Original', color='black')

plt.plot(predictions.index, predictions, label='Predictions', color='red')
plt.legend(loc='best')
plt.title('ARIMA Time Series Forecasting')
plt.show()