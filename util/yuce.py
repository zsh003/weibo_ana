import pymysql
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from pmdarima.arima import auto_arima
from statsmodels.tsa.arima_model import ARIMA

connection = pymysql.connect(host='localhost', user='mysql', password='123456', db='weibo_ana',
                                 charset='utf8mb4')
query = "select like_count,created_at FROM comment WHERE keyword = '%" + '考研调剂' + "%' ORDER BY STR_TO_DATE(created_at, '%Y-%m-%d %H:%i:%s') ASC;"
# 从MySQL数据库读取数据
df = pd.read_sql_query(query, connection)
# 将字符型的时间转换为时间格式
df['created_at'] = df['created_at'].astype(str)
df['created_at'] = pd.to_datetime(df['created_at'])
# 计算热度指标
df['hotness'] = df['post_count'] + df['comment_count'] * df['like_count']
df = df[['hotness']]
# 可视化时间序列
df.plot()
plt.show()


# 将时间列设为索引，并按照时间排序
df = df.set_index('created_at')
df = df.sort_index()
# 进行差分处理
df_diff = df.diff().dropna()
# 确定ARIMA模型的p、d、q参数
# 自动寻找最优参数
p_values = range(0, 3)
d_values = range(0, 2)
q_values = range(0, 3)

best_score, best_cfg = float('inf'), None

for p in p_values:
    for d in d_values:
        for q in q_values:
            order = (p, d, q)
            try:
                model = ARIMA(df, order=order)
                model_fit = model.fit()
                mse = model_fit.mse
                if mse < best_score:
                    best_score, best_cfg = mse, order
                print('ARIMA%s MSE=%.3f' % (order, mse))
            except:
                continue
print('Best ARIMA%s MSE=%.3f' % (best_cfg, best_score))


# 训练ARIMA模型并进行预测
# 训练模型并进行预测
model = ARIMA(df, order=best_cfg)
model_fit = model.fit()
forecast = model_fit.forecast(steps=36)

# 绘制预测结果的折线图
plt.plot(df, label='Actual')
plt.plot(forecast, label='Predicted')
plt.legend()
plt.show()


train_data = df_diff[:len(df_diff) - 7]
test_data = df_diff[len(df_diff) - 7:]
arima_model = ARIMA(train_data, order=auto_model.order)
arima_result = arima_model.fit()
pred = arima_result.predict(start=len(train_data), end=len(train_data) + len(test_data) - 1, typ='levels')
# 将预测结果反差分
diff_recover = df_diff.shift(1)
diff_recover.iloc[0] = df.iloc[0]
predictions = diff_recover.add(pred, fill_value=0)
# 可视化预测结果
plt.figure(figsize=(15, 6))
plt.plot(df.index, df, label='Original')
plt.plot(predictions.index, predictions, label='Predictions')
plt.legend(loc='best')
plt.title('ARIMA Time Series Forecasting')
plt.show()
plt.savefig('myplot.png')