import sys
import pandas as pd

import torch
from torch.utils.data import DataLoader

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

sys.path.append("/home/self_supervised_learning_gr/self_supervised_learning/dev/ProjetCassiopee/")
from src.dataset import MocaplabDatasetFC
from src.setup import setup_python, setup_pytorch
from src.dataset import MocaplabDatasetFC
from src.models.mocaplab import MocaplabFC
from fc.train import *


def plot_animation(i, data, label, prediction, nom):

    print(f"i={i}")
    print(f"data={data}")
    print(f"label={label}")
    print(f"prediction={prediction}")
    print(f"nom={nom}")

    # List of points that should appear in different color each frame (list of 100 lists of len 10) 
    points_color_indices = [
        [231, 220, 230,  24, 232, 221,  23, 219, 222,  25],
        [ 24,  23, 220, 231, 221,  25, 222, 230,  22, 223],
        [ 24,  23,  25, 227,  22, 226, 225,  26, 224, 228],
        [ 24,  25,  23,  26,  27,  22,  28, 227, 228, 226],
        [ 24,  25,  26,  23,  27,  28, 227,  22, 228, 226],
        [ 24,  25,  26,  23,  27, 227, 228, 226,  28,  22],
        [ 24,  25,  26, 227,  27,  23, 228, 226,  28, 229],
        [ 24,  25, 227,  26,  27,  23, 228, 226, 229,  28],
        [ 24, 227,  25,  26,  27,  23, 228, 226, 229,  28],
        [ 24, 227,  25,  26,  27,  23, 228, 226, 229, 116],
        [ 24, 227,  25,  26,  23,  27, 228, 226, 109,  94],
        [ 24, 227,  25,  26,  23,  27, 228, 109, 226,  94],
        [ 24, 227,  25,  26,  23,  27, 228, 109, 226,  94],
        [ 24, 227,  25,  26, 109, 228,  27,  23,  61, 226],
        [ 24, 227,  25, 109,  26,  61,  27, 228,  23,  60],
        [ 24, 227,  61,  25, 109,  26,  27, 228,  60,  23],
        [ 61, 227,  24,  25, 109,  26,  27,  60, 228,  23],
        [227, 109,  24,  61,  25,  26,  27, 228, 108,  60],
        [109, 227,  24,  61,  25,  26,  27, 108, 228,  60],
        [109, 227,  24,  61,  25,  26,  27, 108, 228,  60],
        [109, 227,  24,  25,  61,  26,  27, 108, 228,  60],
        [227, 109,  24,  25,  26,  61,  27, 108, 228,  60],
        [227,  24, 109,  25,  26,  27,  61, 228, 108,  23],
        [227,  24,  25,  26, 109,  27,  61, 228, 108,  23],
        [227,  24,  25,  26,  27, 109,  61, 228,  23, 108],
        [227,  24,  25,  26,  27, 109,  61, 228,  23, 108],
        [227,  24,  25,  26,  27, 109,  61, 228,  23, 108],
        [227,  24,  25,  26,  27, 109,  61, 228,  23, 108],
        [227,  24,  25,  26, 109,  27,  61, 228,  23, 108],
        [227,  24,  25,  26, 109,  27,  61, 228,  23, 108],
        [227,  24,  25,  26, 109,  27,  61, 228,  23,  60],
        [227,  24,  25,  26, 109,  61,  27, 228,  23,  60],
        [227,  24,  25,  26,  61, 109,  27, 228,  23,  60],
        [227,  24,  25,  26,  61, 109,  27, 228,  23,  60],
        [227,  24,  25,  26,  61, 109,  27, 228,  23,  60],
        [227,  24,  25,  26,  61,  27, 109, 228,  23,  60],
        [227,  24,  25,  26,  61,  27, 109, 228,  23,  60],
        [227,  24,  25,  26,  61,  27, 109, 228,  23,  60],
        [227,  24,  25,  26,  61,  27, 109, 228,  23,  60],
        [227,  24,  25,  26,  61,  27, 109, 228,  60,  23],
        [227,  24,  25,  61,  26,  27, 109, 228,  60,  23],
        [227,  24,  25,  61,  26,  27, 228, 109,  60,  23],
        [227,  24,  61,  25,  26,  27, 228, 109,  60,  23],
        [227,  61,  24,  25,  26,  27,  60, 109, 228,  23],
        [ 61, 227,  24,  25,  26, 109,  60,  27, 228,  23],
        [ 61, 227, 109,  24,  60,  25,  26,  27, 108, 228],
        [ 61, 109, 227,  60,  24,  25, 108,  26,  27, 110],
        [ 61, 109,  60, 108, 227,  24, 110,  25,  26,  27],
        [ 61, 109,  60, 108, 227, 110,  24,  25,  26,  27],
        [ 61, 109,  60, 108, 227,  24, 110,  25,  26,  27],
        [ 61, 109,  60, 227,  24,  25, 108,  26, 110,  27],
        [ 61, 109, 227,  60,  24,  25,  26,  27, 108, 228],
        [ 61, 227,  60,  24, 109,  25,  26,  27, 228,  23],
        [ 61, 227,  60,  24,  25,  26, 109,  27, 228,  23],
        [ 61, 227,  60,  24,  25,  26,  27, 109, 228,  23],
        [ 61,  60, 227,  24,  25,  26,  27, 109, 228,  23],
        [ 61,  60, 227, 109,  24,  25,  26,  27, 228, 108],
        [ 61,  60, 109, 227,  24, 108,  25, 110,  26,  27],
        [ 61, 109,  60, 108, 227, 110,  24,  25,  26,  62],
        [ 61, 109,  60, 108, 110, 227,  24,  25,  26, 107],
        [109,  61, 108,  60, 110, 227,  24,  25,  26,  27],
        [109,  61, 227, 108,  24,  25,  60,  26, 110,  27],
        [227, 109,  24,  25,  26,  61,  27, 228, 108,  60],
        [227,  24,  25,  26,  27, 228, 109,  23, 226,  61],
        [227,  24,  25,  26,  27, 228,  23, 226, 109, 229],
        [227,  24,  25,  26,  27, 228, 226,  23, 229, 225],
        [227,  24,  25,  26,  27, 228, 226,  23, 229, 225],
        [227,  24,  25,  26,  27, 228,  23, 226, 229, 225],
        [227,  24,  25,  26, 228,  27,  23, 226, 229, 225],
        [227,  24,  25,  26, 228,  27,  23, 226, 229,  28],
        [227,  24,  25,  26, 228,  27,  23, 226, 229,  28],
        [227,  24,  25,  26, 228,  27,  23, 226, 229,  28],
        [227,  24,  25,  26, 228,  27,  23, 226, 229,  28],
        [227,  24,  25,  26, 228,  27,  23, 226, 229,  28],
        [ 24, 227,  25,  26, 228,  27,  23, 226, 229,  28],
        [ 24, 227,  25,  26, 228,  27,  23, 226, 229,  28],
        [ 24, 227,  25,  26,  27, 228,  23, 226,  28, 229],
        [ 24,  25,  26, 227,  27,  23, 228, 226,  28, 229],
        [227,  24,  25,  26,  27, 228,  23, 226,  28, 229],
        [227,  24,  25, 228,  26,  27,  23, 226, 229,  28],
        [227,  24,  25, 228,  23,  26, 226,  27, 229, 225],
        [ 24,  25,  23,  26,  27,  22, 227, 228, 116,  28],
        [ 24,  23,  25,  26,  22,  27, 116,  76,  16,  15],
        [ 24,  23,  25,  22,  26,  21, 198,  27,  76, 197],
        [236, 235,  24, 234,  23,  25, 233,  26,  22,  27],
        [236, 235, 234, 233,  24,  23,  25,  35,  26,  75],
        [235, 236, 234,  20,  21, 183,  75,  74,  73,  19],
        [ 20,  21, 236, 235,  22,  19,  72,  23,  73,  74],
        [231, 230, 229, 228, 227, 232,  23,  24,  22,  21],
        [231, 232,  23,  24, 230, 233,  22, 229, 234, 236],
        [236, 235, 234, 233, 232, 231,  23,  24, 230,  22],
        [236, 235, 234, 233, 232, 231, 213, 212, 230, 214],
        [236, 235, 234, 233, 232, 231, 230, 229, 228, 227],
        [235, 236, 234, 233, 232, 231, 230, 229, 228, 227],
        [236, 235, 234, 233, 232, 231, 230, 229, 228, 227],
        [236, 235, 234, 233, 232, 231, 230, 229, 228, 227],
        [236, 235, 234, 233, 232, 231, 230, 229, 228, 227],
        [235, 236, 234, 233, 232, 231, 230, 229, 228, 227],
        [236, 235, 234, 233, 232, 231, 230, 229, 228, 227],
        [236, 235, 234, 233, 232, 231, 230, 229, 228, 227]
    ]

    # Transform the list into a list of lists of joints that should be in different color in each frame
    joints_color = []
    for i in range(100):
        joints_color_frame = []
        for j in range(10):
            joints_color_frame.append(points_color_indices[i][j] // 3)
        joints_color.append(joints_color_frame)

    model = "CNN"

    data = data.numpy()
    
    x_data = data[:, 0::3]
    y_data = data[:, 1::3]
    z_data = data[:, 2::3]

    fig = plt.figure()

    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlim(min([min(x_data[i]) for i in range(len(x_data))]),
                max([max(x_data[i]) for i in range(len(x_data))]))
    ax.set_ylim(min([min(y_data[i]) for i in range(len(y_data))]),
                max([max(y_data[i]) for i in range(len(y_data))]))
    ax.set_zlim(min([min(z_data[i]) for i in range(len(z_data))]),
                max([max(z_data[i]) for i in range(len(z_data))]))

    ax.set_xlabel("X")
    ax.set_ylabel("Z")
    ax.set_zlabel("Y")

    # Initialize an empty scatter plot (to be updated in the animation)
    scatter = ax.scatter([], [], [])

    # Initialize lines
    line_points_indices = [
        (0, 1), (0, 2), (3, 4), (4, 5), (5, 6), (5, 7), (6, 8), (7, 9), (8, 9), (1, 70),     # Chest and head
        (3, 10), (2, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15),                  # Right arm (without hand)
        (2, 40), (3, 40), (40, 41), (41, 42), (42, 43), (43, 44), (44, 45),                  # Left arm (without hand)
        (70, 71), (71, 72), (72, 73), (73, 74),                                              # Right leg
        (70, 75), (75, 76), (76, 77), (77, 78),                                              # Left leg
        (15, 16), (16, 17), (17, 18), (18, 19), (19, 20),                                    # Right hand, pinky
        (15, 21), (21, 22), (22, 23), (23, 24), (24, 25),                                    # Right hand, ring
        (15, 26), (26, 27), (27, 28), (28, 29), (29, 30),                                    # Right hand, mid
        (15, 31), (31, 32), (32, 33), (33, 34), (34, 35),                                    # Right hand, index
        (15, 36), (36, 37), (37, 38), (38, 39),                                              # Right hand, thumb
        (45, 46), (46, 47), (47, 48), (48, 49), (49, 50),                                    # Left hand, pinky
        (45, 51), (51, 52), (52, 53), (53, 54), (54, 55),                                    # Left hand, ring
        (45, 56), (56, 57), (57, 58), (58, 59), (59, 60),                                    # Left hand, mid
        (45, 61), (61, 62), (62, 63), (63, 64), (64, 65),                                    # Left hand, index
        (45, 66), (66, 67), (67, 68), (68, 69)                                               # Left hand, thumb                
    ]

    # Plus qu'à faire les mains 

    num_lines = len(line_points_indices)
    lines = [ax.plot([], [], [], "-", color="red")[0] for _ in range(num_lines)]

    # Function to update the scatter plot
    def update(frame):    

        # Get the coordinates for the current frame
        frame_coordinates = (x_data[frame], z_data[frame], y_data[frame])

        # Update the scatter plot with new point positions
        scatter._offsets3d = frame_coordinates

        # Set the title to display the current data, label and frame
        ax.set_title(f"Data {i}, Label : {label}, Prediction : {prediction} with model {model} \nFrame: {frame}")

        # Adding lines between the joints
        for line, (start, end) in zip(lines, line_points_indices):
            line.set_data_3d([x_data[frame][start], x_data[frame][end]],
                             [z_data[frame][start], z_data[frame][end]],
                             [y_data[frame][start], y_data[frame][end]])

        # Update the colors of the points based on the joints_color list
        colors = ["red" if idx in joints_color[frame] else "blue" for idx in range(len(x_data[frame]))]
        sizes = [200 if idx in joints_color[frame] else 50 for idx in range(len(x_data[frame]))] # Set larger size for points with red color
        scatter.set_edgecolors(colors)
        scatter.set_facecolors(colors)
        scatter.set_sizes(sizes)

        print(f"scatter={scatter}")
        print(f"lines={lines}")

        return scatter, *lines

    # Create the animation
    print(f"data={data}")
    animation = FuncAnimation(fig, update, frames=len(data), blit=True)
    
    # Save the animation as a GIF
    animation.save(f"/home/self_supervised_learning_gr/self_supervised_learning/dev/ProjetCassiopee/src/visualisation/mocaplab_points_color/{nom}.gif",
                   writer='pillow')
    plt.close()


if __name__ == "__main__":
    
    # Begin set-up
    print("#### Set-Up ####")

    # Set-up Python
    setup_python()

    # Set-up PyTorch
    DEVICE = setup_pytorch(gpu=False)

    print("#### Dataset ####")
    dataset = MocaplabDatasetFC(path=("/home/self_supervised_learning_gr/self_supervised_learning/dev/"
                                      "ProjetCassiopee/data/mocaplab/Cassiopée_Allbones"),
                                padding=True, 
                                train_test_ratio=8,
                                validation_percentage=0.01)
    
    print("#### Data Loader ####")
    data_loader = DataLoader(dataset,
                             batch_size=1,
                             shuffle=False)
    
    print("#### Model ####")
    model = MocaplabFC(dataset.max_length * 237).to(DEVICE)
    model.load_state_dict(torch.load(("/home/self_supervised_learning_gr/self_supervised_learning/dev/"
                                      "ProjetCassiopee/src/models/mocaplab/fc/saved_models/model_20240325_141951.ckpt"),
                                     map_location=torch.device("cpu")))
    model = model.to(DEVICE)
    model = model.double()
    
    print("#### Plot ####")
    for i, batch in enumerate(data_loader) :
        
        print(f"## Batch {i:4} / {len(data_loader)} ##")
        data, label = batch
        data = data.to(DEVICE)
        label = label.to(DEVICE)
    
        data_flattened = data.view(data.size(0), -1)
        output = model(data_flattened.double())
    
        _, predicted = torch.max(output.data, dim=1)

        label = int(label[0])
        predicted = int(predicted[0])
        
        data = data.squeeze(0)
        
        nom = f"{i}_{label}_{predicted}"
        
        n0 = 0
        n1 = 0
        ndiff = 0

        if ndiff < 2 and predicted != label :
            ndiff += 1
            plot_animation(i, data, label, predicted, nom)

        elif n0 < 2 and label == 0 :
            n0 += 1
            plot_animation(i, data, label, predicted, nom)

        elif n1 < 2 and label == 1 :
            n1 += 1
            plot_animation(i, data, label, predicted, nom)

    print("#### DONE ####")