import torch
import torch.nn as nn
from torch.optim import Adam
from tsimpute.core.logger import log
from tsimpute.modules.models.base import BaseBiDirectionalModel


class Attention(nn.Module):
    def __init__(self, window_size, n_features, **kwargs):
        super(Attention, self).__init__()
        self.window_size = window_size
        self.n_features = n_features

        self.hidden1_features = 256
        self.hidden2_features = 128

        self.dropout = 0.3

        self.attention = nn.MultiheadAttention(
            embed_dim=self.window_size, num_heads=1, batch_first=True)
        self.flatten = nn.Flatten()

        self.fc1 = nn.Linear(self.window_size, self.hidden1_features)
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
            if isinstance(m, (nn.Linear)):
                nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

    def forward(self, x):
        # Shape: (batch_size, window_size, n_features) -> (batch_size, n_features, window_size)
        x = x.permute(0, 2, 1)

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


class AttentionModel(BaseBiDirectionalModel):
    '''
    Attention model.
    '''
    use_generator = True
    use_tensor_cast = True
    name = 'Attention'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.epochs = kwargs.get('epochs', 100)
        self.patience = kwargs.get('patience', 5)
        self.learning_rate = kwargs.get('lr', 1e-4)
        self.weight_decay = kwargs.get('weight_decay', 1e-5)
        self.n_features = self.get_property('Data.n_features', self.kwargs)
        self.window_size = self.get_property('Data.window_size', self.kwargs)

        self.model = Attention(
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
        self.model = Attention(
            n_features=self.n_features,
            window_size=self.window_size,
            **self.kwargs
        ).to(self.device)

    def summary(self):
        return str(self.model)

    def get_history(self) -> list[float]:
        return self.losses
