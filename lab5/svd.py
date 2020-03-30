"""
@author Filip Twardy
"""
import numpy as np
from PIL import Image
import os
import sys
from matplotlib import image
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation


"Set float formatter for numpy"
float_format = np.set_printoptions(
    formatter={'float_kind' : lambda x : "%.3f" % x})

echo_formatter = lambda x, y: f"echo \'{x}\' >> {y}"

assert os.path.isfile("./sammy-kernane-qiyana.jpg")
IMG = Image.open("./image.jpg")
I = np.array(IMG)

FILE = "svd.txt"
SIZE = I.shape[0]
RANK = SIZE
APPROX_IMG = np.zeros((SIZE,SIZE,3), dtype='int')

#matplot
FIG, (AX1, AX2) = plt.subplots(1, 2)
FIG.suptitle("Difference between ORIGINAL and APROXIMATED image")

AX1.axis("off")
AX1.set_title("Original")

AX2.axis("off")
AX2.set_title("Approximated")

"Show difference between images"
def plot_diff(image=IMG, aprox_image=IMG):
    AX1.imshow(image)

    AX2.imshow(aprox_image)

    plt.show()
    plt.close()

"SVD decomposition"
def svd(matrix):
    A = matrix
    
    U, S, V = np.linalg.svd(A, full_matrices=True)
    E = np.diag(S)

    os.system(
        echo_formatter("SVD decomposition A = U E V", FILE))
    os.system(
        echo_formatter(f"U MATRIX: \n{U}", FILE ))
    os.system(
        echo_formatter(f"E MATRIX: \n{E}", FILE ))
    os.system(
        echo_formatter(f"V MATRIX: \n{V}", FILE ))

"low rank approximation !rank < matrix.shape[0]"
def low_rank_approximation(matrix, rank):
    assert rank <= matrix.shape[0]
    U, S, V = np.linalg.svd(matrix)

    os.system(
        echo_formatter(f"RANK {rank}", FILE ))

    return U[:, :rank] @ np.diag(S[:rank]) @ V[:rank, :]

if __name__ == "__main__":

    ims = []
    os.system("echo \' \' > " + FILE)
    
    for rank in [x for x in range(0, SIZE + 1) if x < 10 or x % 32 == 0 or x == SIZE]:
    
        colors = [
            ("RED", 0),
            ("GREEN", 1),
            ("BLUE", 2)
        ]
    
        for color, idx in colors:
            os.system(
                echo_formatter(color, FILE))
    
            IMG_color = I[:, :, idx].copy()
            svd(IMG_color)
            approx_image_color = low_rank_approximation(IMG_color, rank)
            
            APPROX_IMG[..., idx] = approx_image_color

        ims.append([plt.imshow(APPROX_IMG.astype('uint8'), animated=True)])

    
    ani = ArtistAnimation(FIG, ims, interval=300, blit=True,
                          repeat_delay=2000)

    AX1.imshow(I.astype('uint8'))
    
    plt.show()
    

    
