import matplotlib.pyplot as plt

if __name__ == '__main__':
    inp = list(input().split("|"))
    X = [float(x.split(" ")[0]) for x in inp[:-1]]
    Y = [float(x.split(" ")[1]) for x in inp[:-1]]
    plt.scatter(X, Y, s=1, color="black")
    plt.savefig("bif2.jpg")
    plt.show()
