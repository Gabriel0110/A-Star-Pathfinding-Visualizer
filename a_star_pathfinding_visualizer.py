import arcade
from arcade.gui import *
import random
import numpy
import time
import pyautogui as pag

# Set how many rows and columns we will have based on screen size
ROW_COUNT = round(pag.size()[0]*0.6) // 50 #25
COLUMN_COUNT = round(pag.size()[0]*0.6) // 50 #25

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell
MARGIN = 5

SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "A* Path Finding Visualization"

delta = [[-1, 0],  # go up
        [0, -1],  # go left
        [1, 0],  # go down
        [0, 1]] # go right

delta_name = ['^', '<', 'v', '>']

start = []
goal = []
path = []
failed = False

window = None

def getButtonThemes():
    theme = Theme()
    theme.set_font(24, arcade.color.BLACK)
    normal = "images/Normal.png"
    hover = "images/Hover.png"
    clicked = "images/Clicked.png"
    locked = "images/Locked.png"
    theme.add_button_textures(normal, hover, clicked, locked)
    return theme

class ResetButton(TextButton):
    def __init__(self, view, x=0, y=0, width=250, height=40, text="Reset", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)

    def on_press(self):
        pass

class ExitButton(TextButton):
    def __init__(self, view, x=0, y=0, width=250, height=40, text="Exit", theme=None):
        super().__init__(x, y, width, height, text, theme=theme)

    def on_press(self):
        pass

class Visualizer(arcade.Window):

    def __init__(self, width, height, title):
        global start, goal
        super().__init__(width, height, title)

        self.grid = [[0 for col in range(COLUMN_COUNT)] for row in range(ROW_COUNT)]

        for i in range(175):
            rand_row = random.randint(0,ROW_COUNT-1)
            rand_col = random.randint(0, COLUMN_COUNT-1)
            while self.grid[rand_row][rand_col] == -1:
                rand_row = random.randint(0,ROW_COUNT-1)
                rand_col = random.randint(0, COLUMN_COUNT-1)
            self.grid[random.randint(0,ROW_COUNT-1)][random.randint(0, COLUMN_COUNT-1)] = -1
        
        # Random starting point at bottom row
        start = [0, random.randint(0, COLUMN_COUNT-1)]
        self.grid[start[0]][start[1]] = 8

        # Random goal point at top row
        goal = [ROW_COUNT-1, random.randint(0, COLUMN_COUNT-1)]
        self.grid[goal[0]][goal[1]] = 9

        arcade.set_background_color(arcade.color.BLACK)

        self.grid_sprite_list = arcade.SpriteList()

        for row in range(COLUMN_COUNT):
            for column in range(ROW_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                if self.grid[row][column] == -1:
                    sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.BLACK)
                elif self.grid[row][column] == 9:
                    sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.GOLD)
                elif self.grid[row][column] == 8:
                    sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.BLUE_SAPPHIRE)
                else:
                    sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)

        # self.theme = getButtonThemes()
        # self.button_list.append(ResetButton(self, SCREEN_WIDTH*0.25, SCREEN_HEIGHT*0.075, 300, 40, "New Bars", theme=self.theme))
        # self.button_list.append(ExitButton(self, SCREEN_WIDTH*0.75, SCREEN_HEIGHT*0.075, 300, 40, "Reset Bars", theme=self.theme))

    def setup(self):
        global start, goal
        self.grid = [[0 for col in range(COLUMN_COUNT)] for row in range(ROW_COUNT)]

        for i in range(175):
            rand_row = random.randint(0,ROW_COUNT-1)
            rand_col = random.randint(0, COLUMN_COUNT-1)
            while self.grid[rand_row][rand_col] == -1:
                rand_row = random.randint(0,ROW_COUNT-1)
                rand_col = random.randint(0, COLUMN_COUNT-1)
            self.grid[random.randint(0,ROW_COUNT-1)][random.randint(0, COLUMN_COUNT-1)] = -1
        
        # Random starting point at bottom row
        start = [0, random.randint(0, COLUMN_COUNT-1)]
        self.grid[start[0]][start[1]] = 8

        # Random goal point at top row
        goal = [ROW_COUNT-1, random.randint(0, COLUMN_COUNT-1)]
        self.grid[goal[0]][goal[1]] = 9

        arcade.set_background_color(arcade.color.BLACK)

        self.grid_sprite_list = arcade.SpriteList()

        for row in range(COLUMN_COUNT):
            for column in range(ROW_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                if self.grid[row][column] == -1:
                    sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.BLACK)
                elif self.grid[row][column] == 9:
                    sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.GOLD)
                elif self.grid[row][column] == 8:
                    sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.BLUE_SAPPHIRE)
                else:
                    sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)

    def on_draw(self):
        global path

        arcade.start_render()

        if failed:
            pag.alert("NO PATH AVAILABLE", "Impossible", "OK")
            window.setup()
            # for button in self.button_list:
            #     button.draw()

        self.grid_sprite_list.draw()

    def on_mouse_press(self, x, y, button, modifier5s):
        global path, failed

        try:
            path = self.getGridAndSearch()
        except:
            print("ERROR")
            return

        if path != "Fail":
            arcade.schedule(self.colorPath, 0.15)
        else:
            failed = True
            return

    def colorPath(self, delta_time: float):
        global path, window

        if len(path) == 0:
            arcade.unschedule(self.colorPath)
            pag.alert("Path found!", "Path found!", "OK")
            window.setup()
            # ans = pag.confirm("Path found! Would you like to run it again?", "Path found!", ["Yes", "No"])
            # if ans == "Yes":
            #     window.setup()
            # else:
            #     exit()
        else:
            pos = path[0][0] * COLUMN_COUNT + path[0][1]
            self.grid_sprite_list[pos].color = arcade.color.GREEN
            del path[0]

    def search(self, grid, init, goal, cost, heuristic):
        closed = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]
        closed[init[0]][init[1]] = 1

        expand = [[-1 for col in range(len(grid[0]))] for row in range(len(grid))]
        action = [[-1 for col in range(len(grid[0]))] for row in range(len(grid))]

        x = init[0]
        y = init[1]
        g = 0
        h = heuristic[x][y]
        f = g + h

        open = [[f, g, h, x, y]]

        found = False  # flag that is set when search is complete
        resign = False  # flag set if we can't find expand
        count = 0

        while not found and not resign:
            if len(open) == 0:
                resign = True
                return "Fail"
            else:
                open.sort()
                open.reverse()
                next = open.pop()
                x = next[3]
                y = next[4]
                g = next[1]
                expand[x][y] = count
                count += 1

                if x == goal[0] and y == goal[1]:
                    found = True
                else:
                    # expand the winning element and add to new open list
                    for i in range(len(delta)):
                        x2 = x + delta[i][0]
                        y2 = y + delta[i][1]
                        if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]):
                            if closed[x2][y2] == 0 and (grid[x2][y2] == 0 or (grid[x2][y2] == 9)):
                                g2 = g + cost
                                h2 = heuristic[x2][y2]
                                f2 = g2 + h2
                                open.append([f2, g2, h2, x2, y2])
                                closed[x2][y2] = 1
                                action[x2][y2] = i

        policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
        x = goal[0]
        y = goal[1]
        policy[x][y] = '*'
        path_coords = []
        while x != init[0] or y != init[1]:
            x2 = x - delta[action[x][y]][0]
            y2 = y - delta[action[x][y]][1]
            policy[x2][y2] = delta_name[action[x][y]]
            path_coords.append([x2, y2])
            x = x2
            y = y2

        for i in range(len(policy)):
            print(policy[i])

        print("FOUND")
        print("Cost:", g2)
        return path_coords

    def getGridAndSearch(self):
        global start, goal
        grid = self.grid

        init = [start[0], start[1]]
        goals = [9] # [[len(grid) - 1, len(grid[0]) - 1], [len(grid) - 3, len(grid[0]) - 1]]
        goal_locs = {}
        cost = 2

        heuristics = {}
        h = None
        for g in goals:
            gpos = np.argwhere(np.array(grid) == g)
            goal_locs[g] = [gpos.tolist()[0][0], gpos.tolist()[0][1]]
            h = [[0.0 for col in range(len(grid[0]))] for row in range(len(grid))]
            for x in range(len(grid)):
                for y in range(len(grid[0])):
                    if g is grid[x][y]:
                        h[x][y] = 0.0
                    else:
                        h[x][y] = float("%.2f" % (np.linalg.norm(np.array([x, y]) - np.array(gpos))))

            heuristics[g] = h
            for row in h:
                print(row)
            print()

        print(heuristics)

        result = None
        for g in goals:
            heuristic = heuristics[g]
            result = self.search(grid, init, goal_locs[g], cost, heuristic)
            for row in result[::-1]:
                print(row)
            print("\n")

        return result[::-1] if result != "Fail" else "Fail"

def main():
    global window
    window = Visualizer(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()
