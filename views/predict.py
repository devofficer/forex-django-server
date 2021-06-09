"""
import library
"""
import numpy
import matplotlib.pyplot as plt
import pandas
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import requests
import re
import json

def getPrediction():

    url = "https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=GBP"
    params = {
        'limit': "2000"
    }

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'api_key': "499372a892c79cd63eeb10ff08957a0fb9983c0c8d7170f9f6fb3154c04f1f37"
    }
    response = requests.request("GET", url, params=params, headers=headers)

    apiData = json.loads(response.text)
    dataset = []

    for item in apiData["Data"]["Data"]:
        dataset.append(item["open"])

    dataset = numpy.array(dataset)
    dataset = dataset.reshape(-1, 1) #returns a numpy array

    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)

    # fix random seed for reproducibility
    numpy.random.seed(3)

    """
    A simple method that we can use is to split the ordered dataset into train and test datasets. The code below
    calculates the index of the split point and separates the data into the training datasets with 67% of the
    observations that we can use to train our model, leaving the remaining 33% for testing the model.
    """
    # split into train and test sets
    train_size = int(len(dataset) * 0.67)
    test_size = len(dataset) - train_size
    train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
    print("train_data_size: "+str(len(train)), " test_data_size: "+str(len(test)))

    # convert an array of values into a dataset matrix
    def create_dataset(dataset, look_back=1):
        dataX, dataY = [], []
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
        return numpy.array(dataX), numpy.array(dataY)

    # reshape into X=t and Y=t+1
    look_back = 10
    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)

    # reshape input to be [samples, time steps, features]
    trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

    """ The network has a visible layer with 1 input, a hidden layer with
    4 LSTM blocks or neurons and an output layer that makes a single value
    prediction. The default sigmoid activation function is used for the
    LSTM blocks. The network is trained for 100 epochs and a batch size of
    1 is used."""

    # create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(4, input_dim=look_back))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=20, batch_size=1, verbose=2)

    # make predictions
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)
    # invert predictions
    trainPredict = scaler.inverse_transform(trainPredict)
    trainY = scaler.inverse_transform([trainY])
    testPredict = scaler.inverse_transform(testPredict)
    testY = scaler.inverse_transform([testY])

    # calculate root mean squared error
    # trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
    # print(trainY[0])
    # print(trainPredict[:,0])
    # print('Train Score: %.2f RMSE' % (trainScore))
    # testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
    # print(testY[0])
    # print(testPredict[:,0])
    # print('Test Score: %.2f RMSE' % (testScore))

    # shift train predictions for plotting
    trainPredictPlot = numpy.empty_like(dataset)
    trainPredictPlot[:, :] = numpy.nan
    trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict
    # shift test predictions for plotting
    testPredictPlot = numpy.empty_like(dataset)
    testPredictPlot[:, :] = numpy.nan
    testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict

    return scaler.inverse_transform(dataset).flatten(), trainPredictPlot.flatten(), testPredictPlot.flatten()
    
    # # plot baseline and predictions
    # plt.plot(scaler.inverse_transform(dataset))
    # plt.plot(trainPredictPlot)
    # plt.plot(testPredictPlot)
    # plt.show()
