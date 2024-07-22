import torch
import numpy as np
from data.data_collector import DataCollector
from model.gan import SnakeGAN
from game.snake_game import SnakeGame

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

def preprocess_data(states, actions):
    # Normalize states
    states = states.astype(np.float32) / 255.0
    states = states.reshape(states.shape[0], -1)  # Flatten the states

    # One-hot encode actions
    actions_one_hot = np.zeros((actions.shape[0], 4), dtype=np.float32)
    actions_one_hot[np.arange(actions.shape[0]), actions] = 1

    return torch.tensor(states).to(device), torch.tensor(actions_one_hot).to(device)

def train(gan, states, actions, num_epochs=100, batch_size=64):
    for epoch in range(num_epochs):
        permutation = np.random.permutation(states.shape[0])
        states, actions = states[permutation], actions[permutation]

        for i in range(0, states.shape[0], batch_size):
            batch_states = states[i:i+batch_size]
            batch_actions = actions[i:i+batch_size]

            d_loss, g_loss = gan.train_step(batch_states, batch_actions)

        print(f"Epoch [{epoch+1}/{num_epochs}], D Loss: {d_loss:.4f}, G Loss: {g_loss:.4f}")

def main():
    # Load data
    states, actions = DataCollector.load_data("gameplay_data.npz")
    states, actions = preprocess_data(states, actions)

    # Initialize GAN
    state_dim = states.shape[1]
    gan = SnakeGAN(state_dim)

    # Train GAN
    train(gan, states, actions)

    # Save the trained model
    torch.save(gan.generator.state_dict(), "generator.pth")
    torch.save(gan.discriminator.state_dict(), "discriminator.pth")

if __name__ == "__main__":
    main()