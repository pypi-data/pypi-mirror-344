
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

HouseDF = pd.read_csv('USA_Housing.csv')

sns.pairplot(HouseDF, diag_kind='kde')
plt.show()

sns.histplot(HouseDF['Price'], kde=True)
plt.show()

# Correlation plot
corr = HouseDF.select_dtypes(include='number').corr()['Price'].drop('Price')
corr.sort_values().plot(kind='barh', figsize=(8, 5), title='Correlation with Price')
plt.show()

# Features and Target
X = HouseDF[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
             'Avg. Area Number of Bedrooms', 'Area Population']]
y = HouseDF['Price']

# Train Test Split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)

# Model
from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(X_train, y_train)

# Predictions
predictions = lm.predict(X_test)

# Scatter Plot of True vs Predictions
plt.scatter(y_test, predictions)
plt.xlabel('True Prices')
plt.ylabel('Predicted Prices')
plt.show()

# Residuals
sns.histplot((y_test - predictions), bins=50, kde=True)
plt.show()

# Evaluation
from sklearn import metrics
print('MAE:', metrics.mean_absolute_error(y_test, predictions))
print('MSE:', metrics.mean_squared_error(y_test, predictions))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))

