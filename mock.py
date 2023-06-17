import random as rd
import sys

def mock_func(size):
    return [rd.randint(0, 10) for _ in range(size)]

def main(size):
    print(mock_func(size))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        size = int(sys.argv[1])
    else: 
        size = 10
    
    main(size)