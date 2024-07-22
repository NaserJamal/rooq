import pygame
import torch
import numpy as np
from game.snake_game import SnakeGame
from model.gan import Generator

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def main():
    # Initialize game and GAN
    game = SnakeGame()
    state_dim = game.width * game.height * 3  # RGB state
    latent_dim = 100

    generator = Generator(latent_dim, state_dim).to(device)
    generator.load_state_dict(torch.load("generator.pth", map_location=device))
    generator.eval()

    running = True
    action = None

    while running:
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
            # Generate new state using GAN
            z = torch.randn(1, latent_dim).to(device)
            action_tensor = torch.zeros(1, 4).to(device)
            action_tensor[0, action] = 1
            with torch.no_grad():
                generated_state = generator(z, action_tensor).squeeze().cpu().numpy()

            # Reshape and denormalize the generated state
            generated_state = (generated_state * 255).reshape(game.height, game.width, 3).astype(np.uint8)

            # Update game state (this is a simplified version, you might need to adapt it)
            game.snake = [(x, y) for y in range(game.height) for x in range(game.width) if np.any(generated_state[y, x] > 128)]
            food_positions = [(x, y) for y in range(game.height) for x in range(game.width) if np.all(generated_state[y, x] > 200)]
            if food_positions:
                game.food = food_positions[0]

            # Render the generated state
            game.screen.blit(pygame.surfarray.make_surface(generated_state), (0, 0))
            pygame.display.flip()

        game.clock.tick(game.fps)

    game.close()

if __name__ == "__main__":
    main()