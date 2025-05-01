import torch
import torch.nn as nn
from torch.optim import Adam
from tsimpute.core.logger import log
from tsimpute.modules.models.base import BaseBiDirectionalModel


class CNN1DAttention(nn.Module):
    def __init__(self, window_size, n_features, **kwargs):
        super(CNN1DAttention, self).__init__()
        self.window_size = window_size
        self.n_features = n_features

        self.conv1_features = 128
        self.conv1_kernel_size = 5

        self.conv2_features = 128
        self.conv2_kernel_size = 5

        self.conv3_features = 256
        self.conv3_kernel_size = 5

        self.conv4_features = 256
        self.conv4_kernel_size = 5

        self.hidden1_features = 256
        self.hidden2_features = 128

        self.dropout = 0.5

        self.conv1 = nn.Conv1d(in_channels=self.n_features, out_channels=self.conv1_features,
                               kernel_size=self.conv1_kernel_size, padding="same")
        self.relu1 = nn.ReLU()

        self.conv2 = nn.Conv1d(in_channels=self.conv1_features, out_channels=self.conv2_features,
                               kernel_size=self.conv2_kernel_size, padding="same")
        self.relu2 = nn.ReLU()

        self.conv3 = nn.Conv1d(in_channels=self.conv2_features, out_channels=self.conv3_features,
                               kernel_size=self.conv3_kernel_size, padding="same")
        self.relu3 = nn.ReLU()

        self.conv4 = nn.Conv1d(in_channels=self.conv3_features, out_channels=self.conv4_features,
                               kernel_size=self.conv4_kernel_size, padding="same")
        self.relu4 = nn.ReLU()

        self.attention = nn.MultiheadAttention(
            embed_dim=self.window_size, num_heads=self.window_size, batch_first=True)
        self.flatten = nn.Flatten()

        self.fc1 = nn.Linear(self.conv4_features *
                             self.window_size, self.hidden1_features)
        self.relu3 = nn.ReLU()
        self.ln3 = nn.LayerNorm(self.hidden1_features)
        self.dropout = nn.Dropout(self.dropout)

        self.fc2 = nn.Linear(self.hidden1_features, self.hidden2_features)
        self.relu4 = nn.ReLU()
        self.ln4 = nn.LayerNorm(self.hidden2_features)

        self.fc3 = nn.Linear(self.hidden2_features, self.n_features)
        self._init_weights()

    def _init_weights(self):
        # Apply Glorot initialization (Xavier initialization)
        for m in self.modules():
            if isinstance(m, (nn.Conv1d, nn.Linear)):
                nn.init.xavier_normal_(m.weight)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

    def forward(self, x):
        # Shape: (batch_size, window_size, n_features) -> (batch_size, n_features, window_size)
        x = x.permute(0, 2, 1)
        x = self.conv1(x)
        x = self.relu1(x)

        x = self.conv2(x)
        x = self.relu2(x)

        x = self.conv3(x)
        x = self.relu3(x)

        x = self.conv4(x)
        x = self.relu4(x)

        x, _ = self.attention(x, x, x)

        x = self.flatten(x)
        x = self.fc1(x)
        x = self.relu3(x)
        x = self.ln3(x)
        x = self.dropout(x)

        x = self.fc2(x)
        x = self.relu4(x)
        x = self.ln4(x)

        x = self.fc3(x)
        return x


class CNN1DAttentionModel(BaseBiDirectionalModel):
    '''
    CNN1D Attention model.
    '''
    use_generator = True
    use_tensor_cast = True
    name = 'CNN1d-Attention'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.epochs = kwargs.get('epochs', 100)
        self.patience = kwargs.get('patience', 5)
        self.learning_rate = kwargs.get('lr', 1e-4)
        self.weight_decay = kwargs.get('weight_decay', 1e-5)
        self.n_features = self.get_property('Data.n_features', self.kwargs)
        self.window_size = self.get_property('Data.window_size', self.kwargs)

        self.model = CNN1DAttention(
            n_features=self.n_features,
            window_size=self.window_size,
            **self.kwargs
        ).to(self.device)
        self.criterion = nn.MSELoss()
        self.optimizer = Adam(
            self.model.parameters(),
            lr=self.learning_rate,
            weight_decay=self.weight_decay
        )
        self.losses = []

    def train(self, x, y):
        self.model.train()

        # Training loop on epochs
        for epoch in range(self.epochs):
            _datagen = log.progress(x, desc=f'Epoch {epoch+1}/{self.epochs}')

            batch_count = 0
            total_loss = 0
            for data, target in _datagen:
                # Forward pass
                self.optimizer.zero_grad()

                output = self.model(data)
                loss = self.criterion(output, target)

                # Backward pass
                loss.backward()
                self.optimizer.step()

                # Show the loss
                _datagen.set_postfix(loss=loss.item())

                # Track batch metrics
                batch_count += 1
                total_loss += loss.item()

            # Calculate epoch loss
            epoch_loss = total_loss / \
                batch_count if batch_count > 0 else float('inf')

            # Save the loss
            self.losses.append(epoch_loss)

            # Early stopping
            if epoch > self.patience and max(self.losses[-self.patience:]) == self.losses[-1]:
                log.info('⛔ Early stopping')
                break
        self.model.eval()

    @torch.no_grad()
    def forecast(self, x):
        x = x.unsqueeze(0)
        return self.model(x)[0]

    def reset(self):
        self.model = CNN1DAttention(
            n_features=self.n_features,
            window_size=self.window_size,
            **self.kwargs
        ).to(self.device)

    def summary(self):
        return str(self.model)

    def get_history(self) -> list[float]:
        return self.losses
