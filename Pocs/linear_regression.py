# ref : https://pt.wikipedia.org/wiki/M%C3%A9todo_dos_m%C3%ADnimos_quadrados

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression


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
        numerator = np.sum((self.X - self.__x_mean) * (self.y - self.__y_mean))
        denominator = np.sum(np.power((self.X - self.__x_mean), 2))

        beta = numerator / denominator
        return beta

    def angular_coefficient(self, linear_coefficient: float):
        return np.mean(self.y) - (linear_coefficient * self.__x_mean)
    
    
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

    modelo = SimpleLinearRegression(X_subset, y)
    ypred = modelo.predict()
    show_results(X_subset, y, ypred, modelo.coeficients, 'Regressão Linear - Implementada')

    model = LinearRegression()
    model.fit(X_subset, y)
    coeficients = {'alpha': np.round(model.coef_[0], 2), 'beta': np.round(model.intercept_, 2)}
    show_results(X_subset, y, model.predict(X_subset), coeficients, 'Regressão Linear - sklearn')
        
if __name__ == '__main__':
    main()