import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.widgets as widgets
from scipy.ndimage import convolve
import json

class GameOfLife:
    def __init__(self, size=50, birth_rule=[3], survival_rule=[2, 3]):
        self.size = size
        self.grid = np.random.choice([0, 1], size=(size, size), p=[0.8, 0.2])
        self.birth_rule = birth_rule
        self.survival_rule = survival_rule
        self.kernel = np.array([[2, 0, 1],
                                [1, 0, 5],
                                [2, 0, 0]])

    def update(self):
        neighbor_count = convolve(self.grid, self.kernel, mode='wrap')
        birth = (neighbor_count == self.birth_rule[0]) & (self.grid == 0)
        survive = np.isin(neighbor_count, self.survival_rule) & (self.grid == 1)
        self.grid = np.where(birth | survive, 1, 0)

    def reset(self):
        self.grid = np.random.choice([0, 1], size=(self.size, self.size), p=[0.8, 0.2])

    def resize(self, new_size):
        self.size = new_size
        self.reset()

class GameOfLifeVisualization:
    def __init__(self):
        self.game = GameOfLife()
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.img = self.ax.imshow(self.game.grid, interpolation='nearest', cmap='binary')
        self.setup_ui()

    def setup_ui(self):
        self.ax_reset = plt.axes([0.81, 0.05, 0.1, 0.04])
        self.btn_reset = widgets.Button(self.ax_reset, 'Reset')
        self.btn_reset.on_clicked(self.reset)

        self.ax_birth = plt.axes([0.25, 0.09, 0.5, 0.03])
        self.slider_birth = widgets.RangeSlider(self.ax_birth, 'Birth Rule', 0, 8, valinit=(3, 3))

        self.ax_survival = plt.axes([0.25, 0.05, 0.5, 0.03])
        self.slider_survival = widgets.RangeSlider(self.ax_survival, 'Survival Rule', 0, 8, valinit=(2, 3))

        self.ax_size = plt.axes([0.25, 0.01, 0.5, 0.03])
        self.slider_size = widgets.Slider(self.ax_size, 'Grid Size', 10, 10000, valinit=50, valstep=1)
        self.slider_size.on_changed(self.resize)

        # Add a button for saving settings
        self.ax_save = plt.axes([0.81, 0.10, 0.1, 0.04])
        self.btn_save = widgets.Button(self.ax_save, 'Save Settings')
        self.btn_save.on_clicked(self.save_settings)

    def update(self, frame):
        self.game.birth_rule = list(range(int(self.slider_birth.val[0]), int(self.slider_birth.val[1])+1))
        self.game.survival_rule = list(range(int(self.slider_survival.val[0]), int(self.slider_survival.val[1])+1))
        self.game.update()
        self.img.set_array(self.game.grid)
        return [self.img]

    def reset(self, event):
        self.game.reset()
        self.img.set_array(self.game.grid)

    def resize(self, val):
        new_size = int(val)
        self.game.resize(new_size)
        self.img.set_array(self.game.grid)

    def animate(self):
        self.anim = FuncAnimation(self.fig, self.update, frames=200, interval=50, blit=True)
        plt.show()

    def save_settings(self, event):
        settings = {
            'birth_rule': [int(self.slider_birth.val[0]), int(self.slider_birth.val[1])],
            'survival_rule': [int(self.slider_survival.val[0]), int(self.slider_survival.val[1])],
            'grid_size': int(self.slider_size.val)
        }
        try:
            with open('settings.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(settings)

        with open('settings.json', 'w') as file:
            json.dump(data, file, indent=4)

if __name__ == "__main__":
    viz = GameOfLifeVisualization()
    viz.animate()
