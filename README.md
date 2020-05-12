# A-Star-Pathfinding-Visualizer
A visualization tool for the A* pathfinding algorithm using the Arcade library for visualization.

The A* algorithm was taught in my graduate course "AI for Robotics", so I used that code with minor changes to accompany the Arcade library used for visualization.  The algorithm uses a heuristic to understand where to create the path in the grid, and I calculated the heuristic using euclidean distance to the goal point.

You can add diagonal pathing by replacing 'delta' and 'delta_name' with the below:  

- delta = [[-1, 0],  # go up  
         [0, -1],  # go left  
         [1, 0],  # go down  
         [0, 1], # go right  
         [-1, 1], # up, right diag  
         [-1, -1], # up, left diag  
         [1, 1], # down, right diag  
         [1, -1]] # down, left diag

- delta_name = ['^', '<', 'v', '>', '^>', '^<', 'v>', 'v<']    

### REQUIRED LIBRARIES:
- arcade  
- pyautogui
- numpy  
  
### Demo  
![](/a_star_visualizer_gif.gif)  
