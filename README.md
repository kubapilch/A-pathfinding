This is my implementation of A* pathfinding algorithm in pygame. You can download it and try it by yourself, all you need to do is install pygame.

### There are 4 stages in game: 

* Placing starting cell
* Placing end cell
* Placing walls
* Game

To go to the next stage all you have to do is press SPACE.
When the game is over you can press SPACE one more time to restart the game or exit by closing the game.

### You can modify:
* Speed of the AI game by passing diffrent argument when creating instance of Game class

* If you want to play by yourself or you want to watch AI

* If you want to see G and H costs labels that indicate cost to move from starting node and cost to move to end node

* If you want to see F cost label that is added up h and g costs