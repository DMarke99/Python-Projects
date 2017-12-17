#Letter Classification Problem
#imports libraries
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense

#imports dataset
dataset = pd.read_csv('letter-recognition.csv')

#separates into dependent and independent variables
X = dataset.iloc[:,1:].values
y = dataset.iloc[:,0].values

#encodes letter categories into numbers
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_y = LabelEncoder()
y = labelencoder_y.fit_transform(y.reshape(-1,1))
y = y.reshape(-1,1)

#encodes numerical categories into separate columns
onehotencoder_y = OneHotEncoder(categorical_features = [0])
y = onehotencoder_y.fit_transform(y).toarray()

#Feature scaling of dependent variables
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X = sc.fit_transform(X)

#splits data into training set and test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

#initialise the neural network
classifier = Sequential()

#adds the input Layer and the first hidden layer
classifier.add(Dense(input_dim = 16,units = 50,kernel_initializer = 'uniform',activation = 'relu'))

#adds a second layer
classifier.add(Dense(units = 50,kernel_initializer = 'uniform',activation = 'relu'))

#adds the output layer
classifier.add(Dense(units = 26,kernel_initializer = 'uniform',activation = 'sigmoid'))

#compiles the neural network
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

#fitting neural net to training set
classifier.fit(X_train, y_train, batch_size = 100, epochs = 200)

#tests predictions on test set
y_pred = classifier.predict(X_test)

#compares predicted classification with actual classification
y_class_pred = y_pred.argmax(axis=-1)
y_class = y_test.argmax(axis=-1)
y_accuracy = (y_class == y_class_pred)

#draws conclusions
accuracy = y_accuracy.mean()
print('the neural network classifies letters in the test set with an accuracy of ' + str(100*accuracy) + '%')

#with batch_size of 500 and 1000 epochs, testing the model on the test set gave 95.68% accuracy
#with batch_size of 250 and 500 epochs, testing the model on the test set gave 95.4% accuracy
#with batch_size of 200 and 400 epochs, testing the model on the test set gave 95.34% accuracy
#with batch_size of 100 and 200 epochs, testing the model on the test set gave 95.54% accuracy