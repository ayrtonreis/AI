import sys
import numpy as np


def linear_regression(x1, x2, y, learning_rate=0.1, max_iterations=100):
    b0 = 0
    b1 = 0
    b2 = 0
    n = len(x1)
    count = 0
    max_count = max_iterations

    while True:
        f = b0 + b1*x1 + b2*x2  # f is a n-dimensional vector as well as y
        R = 0.5/n * np.sum((f - y)**2)
        #print("Risk: ", R)

        if count == max_count:
            break

        b0 = b0 - learning_rate/n * np.sum((f - y) * 1)
        b1 = b1 - learning_rate/n * np.sum((f - y) * x1)
        b2 = b2 - learning_rate/n * np.sum((f - y) * x2)

        count += 1

        #print("Coefficients: ", [b0, b1, b2])

    return [b0, b1, b2]


def scale_feature(x):
    mean_x = np.mean(x)
    std_x = np.std(x)
    return (x - mean_x)/std_x


def main():
    input_file = str(sys.argv[1])
    output_file = str(sys.argv[2])

    alpha = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
    x1,x2,y = np.loadtxt(input_file, unpack=True, delimiter=',')

    new_x1 = scale_feature(x1)
    new_x2 = scale_feature(x2)

    file = open(output_file, "w")

    for a in alpha:
        result = linear_regression(new_x1, new_x2, y, learning_rate=a, max_iterations = 100)

        string = str(a) + ',' + str(100) + ',' + str(result[0]) + ',' + str(result[1]) + ',' + str(result[2])
        file.write(string + "\n")

        #print("For a = ", a, ":\n", result)
        #print("\n\nFinal betas for a = ", a, ":\n {0:.3f}  {0:.3f}  {0:.3f}".format(result[0], result[1], result[2]))


    my_iterations = 64
    my_learning_rate = 0.6
    my_result = linear_regression(new_x1, new_x2, y, learning_rate=my_learning_rate, max_iterations=my_iterations)

    string = str(my_learning_rate) + ',' + str(my_iterations) + ',' + str(my_result[0]) + ',' + str(my_result[1]) + ',' + str(my_result[2])
    file.write(string + "\n")

    file.close()

    # print(x1)
    #print(new_x1)
    # print(x2)
    #print(new_x2)
    # print(x1-x2)

    #pla(x1, x2, y)

if __name__ == '__main__':
    main()