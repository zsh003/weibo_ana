import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pmdarima.arima import auto_arima


db = pymysql.connect(
    host="localhost",
    user="root",
    password="123456",
    database="database"
)
cursor = db.cursor()
query = "SELECT created_at, like_count FROM comment WHERE keyword='薛之谦演唱会'"
cursor.execute(query)
rows = cursor.fetchall()
columns = [col[0] for col in cursor.description]  # 获取列名
data = pd.DataFrame(rows, columns=columns)
data['created_at'] = pd.to_datetime(data['created_at'])
data.set_index('created_at', inplace=True)
data = data.resample('D').sum()
diff_data = data.diff().dropna()
plt.plot(diff_data)
plt.show()
stepwise_model = auto_arima(diff_data, start_p=0, start_q=0,
                            max_p=5, max_q=5, m=12,
                            start_P=0, seasonal=True,
                            d=None, D=1, trace=True,
                            error_action='ignore',
                            suppress_warnings=True,
                            stepwise=True)
print(stepwise_model.aic())
model = ARIMA(data, order=stepwise_model.order).fit()

forecast_data = model.forecast(steps=30)

plt.plot(forecast_data)
plt.show()