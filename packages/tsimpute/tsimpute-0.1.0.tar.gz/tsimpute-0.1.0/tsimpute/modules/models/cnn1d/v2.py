import torch
import torch.nn as nn
from torch.optim import Adam
from tsimpute.core.logger import log
from tsimpute.modules.models.base import BaseBiDirectionalModel


class CNN1D(nn.Module):
    def __init__(self, n_features: int, window_size: int, **kwargs):
        super(CNN1D, self).__init__()

        self.n_features = n_features
        self.window_size = window_size

        self.conv0_features = kwargs.get('conv0_features', 128)
        self.conv0_kernel_size = kwargs.get('conv0_kernel_size', 5)

        self.conv1_features = kwargs.get('conv1_features', 128)
        self.conv1_kernel_size = kwargs.get('conv1_kernel_size', 5)

        self.conv2_features = kwargs.get('conv2_features', 256)
        self.conv2_kernel_size = kwargs.get('conv2_kernel_size', 5)

        self.hidden1_features = kwargs.get('hidden1_features', 256)
        self.hidden2_features = kwargs.get('hidden2_features', 128)

        self.dropout = kwargs.get('dropout', 0.5)

        self.initialize_method = kwargs.get(
            'initialize_method', "he")  # glorot or he
        if self.initialize_method not in ['glorot', 'he']:
            log.warning(
                'Invalid initialize method. Use default Glorot initialization.')
            self.initialize_method = 'glorot'

        # Define the layers
        self.layers = [
            # Shape: (batch_size, n_features, window_size) -> (batch_size, conv1_features, window_size)
            nn.Conv1d(in_channels=n_features, out_channels=self.conv0_features,
                      kernel_size=self.conv0_kernel_size, padding=(self.conv0_kernel_size // 2)),
            nn.ReLU(),


            # Shape: (batch_size, conv1_features, window_size) -> (batch_size, conv2_features, window_size)
            nn.Conv1d(in_channels=self.conv0_features, out_channels=self.conv1_features,
                      kernel_size=self.conv1_kernel_size, padding=(self.conv1_kernel_size // 2)),
            nn.ReLU(),

            # Reduce the window size by half
            # Shape: (batch_size, conv1_features, window_size) -> (batch_size, conv1_features, window_size // 2)
            nn.AvgPool1d(kernel_size=2, stride=2),

            # Shape: (batch_size, conv1_features, window_size) -> (batch_size, conv2_features, window_size)
            nn.Conv1d(in_channels=self.conv1_features, out_channels=self.conv2_features,
                      kernel_size=self.conv2_kernel_size, padding=(self.conv2_kernel_size // 2)),
            nn.ReLU(),
            # Shape: (batch_size, conv2_features, window_size) -> (batch_size, conv2_features * window_size)
            nn.Flatten(),

            # Shape: (batch_size, conv2_features * window_size) -> (batch_size, hidden1_features)
            nn.Linear(self.conv2_features * (window_size // 2),
                      self.hidden1_features),
            nn.LayerNorm(self.hidden1_features),
            nn.ReLU(),
            nn.Dropout(self.dropout),

            # Shape: (batch_size, hidden1_features) -> (batch_size, hidden2_features)
            nn.Linear(self.hidden1_features, self.hidden2_features),
            nn.LayerNorm(self.hidden2_features),
            nn.ReLU(),
            # Shape: (batch_size, hidden2_features) -> (batch_size, n_features)
            nn.Linear(self.hidden2_features, n_features)
        ]
        self.model = nn.Sequential(*self.layers)

        # Apply Glorot initialization to all layers
        if self.initialize_method == 'glorot':
            for layer in self.layers:
                if isinstance(layer, (nn.Conv1d, nn.Linear)):
                    nn.init.xavier_normal_(layer.weight)
                    if layer.bias is not None:
                        nn.init.constant_(layer.bias, 0)

        # Apply He initialization to all layers
        if self.initialize_method == 'he':
            for layer in self.layers:
                if isinstance(layer, (nn.Conv1d, nn.Linear)):
                    nn.init.kaiming_normal_(layer.weight)
                    if layer.bias is not None:
                        nn.init.constant_(layer.bias, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Change the shape to (batch_size, n_features, window_size)
        x = x.permute(0, 2, 1)
        return self.model(x)


class CNN1DModel(BaseBiDirectionalModel):
    '''
    CNN1D version 2 model.
    '''
    use_generator = True
    use_tensor_cast = True
    name = 'CNN1d-v2'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.epochs = kwargs.get('epochs', 100)
        self.patience = kwargs.get('patience', 5)
        self.learning_rate = kwargs.get('lr', 1e-4)
        self.weight_decay = kwargs.get('weight_decay', 1e-5)
        self.n_features = self.get_property('Data.n_features', self.kwargs)
        self.window_size = self.get_property('Data.window_size', self.kwargs)

        self.model = CNN1D(
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
        self.model = CNN1D(
            n_features=self.n_features,
            window_size=self.window_size,
            **self.kwargs
        ).to(self.device)

    def summary(self):
        return str(self.model)

    def get_history(self) -> list[float]:
        return self.losses
