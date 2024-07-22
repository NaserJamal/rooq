import pygame
from game.snake_game import SnakeGame
from data.data_collector import DataCollector

def main():
    
    pass
    game = SnakeGame()
data_collector = DataCollector()
    running = True
    
    while running:
        action = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    action = 0
                elif event.key == pygame.K_DOWN:
                    action = 1
                elif event.key == pygame.K_LEFT:
                    action = 2
                elif event.key == pygame.K_RIGHT:
                    action = 3

if action is not None:
            game.change_direction(action)
        
        # Step the game
state, reward, done = game.step()
        game.render()
        
        # Collect data
if action is not None:
            data_collector.add_sample(state, action)
        
        if game.game_over:
print(f"Game Over! Score: {game.score}")
            game.reset()
        
# Control the game speed
        game.clock.tick(game.fps)
def example_function():
    print("Hello, World!")  
     
def another_function():
def some_function():
return True


class SomeClass:
    pass
    game.close()
    
    # Save collected data
    data_collector.save_data("gameplay_data.npz")

if __name__ == "__main__":
    main()