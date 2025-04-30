
print("""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


HouseDF = pd.read_csv('USA_Housing.csv')


HouseDF.head()


HouseDF.info()

HouseDF.columns

sns.pairplot(HouseDF, diag_kind='kde')
plt.show()

## Exploratory Data Analysis for House Price Prediction

sns.histplot(HouseDF['Price'], kde=True)
plt.show()

corr = HouseDF.select_dtypes(include='number').corr()['Price'].drop('Price')
corr.sort_values().plot(kind='barh', figsize=(8, 5), title='Correlation with Price')
plt.show()

## Training a Linear Regression Model

### X and y List


X = HouseDF[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
               'Avg. Area Number of Bedrooms', 'Area Population']]

y = HouseDF['Price']

### Split Data into Train, Test

from sklearn.model_selection import train_test_split


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)

## Creating and Training the LinearRegression Model


from sklearn.linear_model import LinearRegression

lm = LinearRegression()

lm.fit(X_train,y_train)

## LinearRegression Model Evaluation

print(lm.intercept_)


coeff_df = pd.DataFrame(lm.coef_,X.columns,columns=['Coefficient'])
coeff_df

## Predictions from our Linear Regression Model


predictions = lm.predict(X_test)

plt.scatter(y_test,predictions)
plt.show()

sns.distplot((y_test-predictions),bins=50);
plt.show()

## Regression Evaluation Metrics

from sklearn import metrics

print('MAE:', metrics.mean_absolute_error(y_test, predictions))
print('MSE:', metrics.mean_squared_error(y_test, predictions))
print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))

"""


)








