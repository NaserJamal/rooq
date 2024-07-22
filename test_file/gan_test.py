import torch
import torch.nn as nn
import torch.optim as optim

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class Generator(nn.Module):
    def __init__(self, latent_dim, state_dim):
        super(Generator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(latent_dim + 4, 128),
            nn.LeakyReLU(0.2),
            nn.Linear(128, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, state_dim),
            nn.Tanh()
        )

    def forward(self, z, action):
        x = torch.cat([z, action], dim=1)
        return self.model(x)


class Discriminator(nn.Module):
    def __init__(self, state_dim):
        super(Discriminator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(state_dim + 4, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, state, action):
        x = torch.cat([state, action], dim=1)
        return self.model(x)


class SnakeGAN:
    def __init__(self, state_dim, latent_dim=100, lr=0.0002, beta1=0.5):
        self.state_dim = state_dim
        self.latent_dim = latent_dim

        self.generator = Generator(latent_dim, state_dim).to(device)
        self.discriminator = Discriminator(state_dim).to(device)

        self.g_optimizer = optim.Adam(
            self.generator.parameters(), lr=lr, betas=(beta1, 0.999)
        )
        self.d_optimizer = optim.Adam(
            self.discriminator.parameters(), lr=lr, betas=(beta1, 0.999)
        )

        self.criterion = nn.BCELoss()

    def train_step(self, real_states, actions):
        batch_size = real_states.size(0)
        real_labels = torch.ones(batch_size, 1).to(device)
        fake_labels = torch.zeros(batch_size, 1).to(device)

        # Train Discriminator
        self.d_optimizer.zero_grad()

        # Real samples
        real_outputs = self.discriminator(real_states, actions)
        d_loss_real = self.criterion(real_outputs, real_labels)

        # Fake samples
        z = torch.randn(batch_size, self.latent_dim).to(device)
        fake_states = self.generator(z, actions)
        fake_outputs = self.discriminator(fake_states.detach(), actions)
        d_loss_fake = self.criterion(fake_outputs, fake_labels)

        d_loss = d_loss_real + d_loss_fake
        d_loss.backward()
        self.d_optimizer.step()

        # Train Generator
        self.g_optimizer.zero_grad()
        fake_outputs = self.discriminator(fake_states, actions)
        g_loss = self.criterion(fake_outputs, real_labels)
        g_loss.backward()
        self.g_optimizer.step()

        return d_loss.item(), g_loss.item()

    def generate_state(self, action):
        z = torch.randn(1, self.latent_dim).to(device)
        action_tensor = torch.zeros(1, 4).to(device)
        action_tensor[0, action] = 1
        with torch.no_grad():
            generated_state = self.generator(z, action_tensor)
        return generated_state.squeeze().cpu().numpy()