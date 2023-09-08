# ref : https://pt.wikipedia.org/wiki/M%C3%A9todo_dos_m%C3%ADnimos_quadrados

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Regressão simples
class SimpleLinearRegression():
    def __init__(self, X: np.ndarray, y: np.ndarray):
        self.X = X.reshape(-1)
        self.y = y
        self.coeficients = dict()
        self.__x_mean = np.mean(self.X)
        self.__y_mean = np.mean(self.y)

    # minimos quadrados (y = alpha + (beta * x) + error)
    def predict(self): 
        alpha = self.linear_coefficient()
        beta = self.angular_coefficient(alpha)
        self.coeficients = {'alpha': np.round(alpha, 2), 'beta': np.round(beta, 2)}

        ypred = (alpha * self.X) + beta 

        return ypred
        
    def linear_coefficient(self): 
        '''
        numerator = 0
        denominator = 0
        total_points = len(self.X)
        for i in range(total_points):
            numerator += (self.X[i] - self.__x_mean) * (self.y[i] - self.__y_mean)
            denominator += np.power((self.X[i] - self.__x_mean), 2)
        '''
        # forma mais eficiente
        numerator = np.sum(self.X * (self.y - self.__y_mean))
        denominator = np.sum(self.X * (self.X - self.__x_mean))

        beta = numerator / denominator
        return beta

    def angular_coefficient(self, linear_coefficient: float):
        return np.mean(self.y) - (linear_coefficient * self.__x_mean)
    

class MultipleLinearRegression():
    def __init__(self, X: np.ndarray, y: np.ndarray):
        self.X = self.add_intercept(X)
        self.y = y.reshape(-1,1)
        self.coeficients = dict()

    # minimos quadrados (B = (X^T * X)^-1 * X^T Y)
    def predict(self): 
        matrix = self.coeficient_matrix()
        self.coeficients = {'alpha': np.round(matrix[1][0], 2), 'beta': np.round(matrix[0][0], 2)}

        return self.X.dot(matrix)

    def coeficient_matrix(self):
        x_transposed = self.X.T
        return self.inverse(x_transposed.dot(self.X)).dot(x_transposed).dot(self.y)
        
    def inverse(self, M: np.ndarray):
        if M.ndim != 2 or M.shape[0] != M.shape[1]:
            raise Exception('A matriz precisa ser quadrada para ser inversível')
        return np.linalg.inv(M)
    
    def add_intercept(self, X):
        ones_column = np.ones((X.shape[0], 1))
        return np.hstack((ones_column, X))
        
    
    
def mse(y: np.ndarray, ypred: np.ndarray):
    if y.shape != ypred.shape:
        raise Exception('y e ypred devem ter o mesmo tamanho!')
    return np.sum(np.power(y - ypred, 2)) / len(y)


def show_results(X: np.ndarray, y: np.ndarray, ypred : np.ndarray, coeficients: dict = None, legend : str = ''):
    plt.scatter(X, y)
    plt.plot(X, ypred, 'r')
    plt.title(legend)
    if coeficients is not None:
        alpha, beta = coeficients.get('alpha'), coeficients.get('beta')
        plt.text(0.1, 0.9, f'alpha = {alpha}', transform=plt.gca().transAxes)
        plt.text(0.1, 0.8, f'beta = {beta}', transform=plt.gca().transAxes)

    plt.show()
    

def main():
    data = load_diabetes()
    X, y = data['data'], data['target']
    X_subset = X[:, 2:3]

    # Regressão simples
    simpleModel = SimpleLinearRegression(X_subset, y)
    ypred = simpleModel.predict()
    show_results(X_subset, y, ypred, simpleModel.coeficients, 'Regressão Linear - Implementada')
    error = mse(y, ypred)
    print(f'MSE - Implementado: {error}')

    # SkLearn
    model = LinearRegression()
    model.fit(X_subset, y)
    coeficients = {'alpha': np.round(model.coef_[0], 2), 'beta': np.round(model.intercept_, 2)}
    ypredict = model.predict(X_subset)
    show_results(X_subset, y, ypredict, coeficients, 'Regressão Linear - sklearn')
    error = mean_squared_error(y, ypredict)
    print(f'MSE - sklearn: {error}')

    # Regressão multipla
    generalModel = MultipleLinearRegression(X_subset, y)
    ypred = generalModel.predict()
    show_results(X_subset, y, ypred, generalModel.coeficients, 'Regressão Linear - Multipla')
    error = mean_squared_error(y, ypredict)
    print(f'MSE - Multipla: {error}')
        
if __name__ == '__main__':
    main()