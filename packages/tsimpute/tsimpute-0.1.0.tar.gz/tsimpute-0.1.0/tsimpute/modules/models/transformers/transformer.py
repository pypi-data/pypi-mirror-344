import torch
import torch.nn as nn
from torch.optim import Adam
from tsimpute.core.logger import log
from tsimpute.modules.models.base import BaseBiDirectionalModel


class Transformer(nn.Module):
    def __init__(self, n_features: int, **kwargs):
        super(Transformer, self).__init__()

        self.n_features = n_features

        self.num_encoder_layers = kwargs.get('num_encoder_layers', 4)
        self.num_decoder_layers = kwargs.get('num_decoder_layers', 4)
        self.dim_feedforward = kwargs.get('dim_feedforward', 256)

        self.transformer = nn.Transformer(
            d_model=n_features,
            nhead=n_features,
            num_encoder_layers=self.num_encoder_layers,
            num_decoder_layers=self.num_decoder_layers,
            dim_feedforward=self.dim_feedforward,
            batch_first=True
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        tgt = torch.ones((x.shape[0], 1, self.n_features)).to(x.device)
        return self.transformer(x, tgt)


class TransformerModel(BaseBiDirectionalModel):
    '''
    Transformer model
    '''
    use_generator = True
    use_tensor_cast = True
    name = 'Transformer'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.epochs = kwargs.get('epochs', 100)
        self.patience = kwargs.get('patience', 5)
        self.learning_rate = kwargs.get('lr', 1e-4)
        self.weight_decay = kwargs.get('weight_decay', 1e-5)
        self.n_features = self.get_property('Data.n_features', self.kwargs)
        self.window_size = self.get_property('Data.window_size', self.kwargs)

        self.model = Transformer(
            n_features=self.n_features,
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
        self.model = Transformer(
            n_features=self.n_features,
            **self.kwargs
        ).to(self.device)

    def summary(self):
        return str(self.model)

    def get_history(self) -> list[float]:
        return self.losses
