'''
Peri-midFormer model
'''
import numpy as np
import torch
from torch import nn
from .enc_dec import Encoder
from .embed import PositionEmbedding, TemporalEmbedding
from .utils import SeriesDecomp
from tsimpute.modules.models.base import BaseBiDirectionalModel


def FFT4Period(x, k: int = 2):
    # [B, T, C]
    xf = torch.fft.rfft(x, dim=1)
    # find period by amplitudes
    frequency_list = abs(xf).mean(0).mean(-1)
    frequency_list[0] = 0
    _, top_list = torch.topk(frequency_list, k)

    top_list = torch.sort(top_list, descending=False).values

    # Make sure the first level is the original time series itself
    if top_list[0] != 1:
        top_list = torch.cat(
            [torch.tensor([1]).to(top_list.device), top_list[:-1]])

    top_list = top_list.detach().cpu().numpy()
    top_list = top_list[top_list != 0]
    top_list = np.unique(top_list)
    if len(top_list) == 1:
        top_list = np.append(top_list, top_list[0] * 2)
    period = x.shape[1] // top_list

    unique_period, _ = np.unique(period, return_index=True)
    unique_period = np.sort(unique_period)[::-1]

    return unique_period


class PeriMidConst(nn.Module):
    def __init__(self, **kwargs):
        super(PeriMidConst, self).__init__()
        self.k = kwargs.get("top_k", 3)
        self.seq_len = kwargs.get("seq_len", 100)
        self.d_model = kwargs.get("d_model", 768)
        self.projection = nn.Linear(self.seq_len, self.d_model)

    def forward(self, x):
        B, L, C = x.size()
        period_list = FFT4Period(x, self.k)

        levels = []
        components_per_level = []
        for i in range(len(period_list)):
            period = period_list[i]

            if L % period != 0:
                remainder = L % period
                length = L - remainder
                x = x[:, :-remainder, :]
            else:
                length = L

            # split into components
            components_num = int(length / period)
            components_per_level.append(components_num)
            components_size = int(length // components_num)
            components = [
                x[:, i * components_size:(i + 1) * components_size, :] for i in range(components_num)]

            components_uniform_size = []
            for component in components:
                component = component.permute(0, 2, 1)
                component_length = component.shape[-1]
                original_length = L

                # padding to original length
                if component_length < original_length:
                    padding_size = original_length - component_length
                    padding = torch.zeros(
                        (component.shape[:-1] + (padding_size,)), device=component.device)
                    component = torch.cat((component, padding), dim=-1)

                component = self.projection(component)
                component = component.permute(0, 2, 1)
                components_uniform_size.append(component)

            levels = levels + components_uniform_size

        peri_mid = torch.stack(levels, dim=-1)
        peri_mid = peri_mid.permute(0, 3, 1, 2)
        return peri_mid, components_per_level


class PerimidFormer(nn.Module):
    def __init__(self, **kwargs):
        super(PerimidFormer, self).__init__()

        # Model params
        self.top_k = kwargs.get("top_k", 3)
        self.d_model = kwargs.get("d_model", 768)
        self.n_heads = kwargs.get("n_heads", 8)
        self.layers = kwargs.get("layers", 2)
        self.dropout_rate = kwargs.get("dropout", 0.1)
        self.moving_avg = kwargs.get("moving_avg", 25)
        self.feature_flows_dim = self.d_model * self.top_k * 1 * 3
        self.chan_in = 1

        # Data params
        self.seq_len = kwargs.get("seq_len", 100)
        self.label_len = kwargs.get("label_len", 1)
        self.pred_len = kwargs.get("pred_len", 1)
        self.features = kwargs.get("features", 'S')
        self.target = kwargs.get("target", 'values')
        self.embed = kwargs.get("embed", 'timeF')
        self.freq = kwargs.get("freq", 'h')

        # Model components
        self.peri_mid_const = PeriMidConst(**kwargs)
        self.feature_flows_dim = self.d_model * self.top_k * 1 * 3
        self.peri_midformer = Encoder(**kwargs)
        self.position_embedding = PositionEmbedding(**kwargs)
        self.temporal_embedding = TemporalEmbedding(**kwargs)
        self.decompsition = SeriesDecomp(kernel_size=self.moving_avg)
        self.projection_trend = nn.Linear(
            self.seq_len, self.label_len + self.pred_len)
        self.dropout = nn.Dropout(p=self.dropout_rate)
        self.projection = nn.Linear(
            self.d_model * self.top_k, self.label_len + self.pred_len, bias=True)

    def forward(self, x_enc: torch.Tensor, x_mark_enc: torch.Tensor = None):
        # Normalization from Non-stationary Transformer
        means = x_enc.mean(1, keepdim=True).detach()
        x_enc = x_enc - means
        stdev = torch.sqrt(
            torch.var(x_enc, dim=1, keepdim=True, unbiased=False) + 1e-5)
        x_enc /= stdev

        # time series decompsition
        seasonal_part, trend_part = self.decompsition(x_enc)
        enc_in = seasonal_part

        # temporal embedding
        if x_mark_enc is not None:
            enc_in = self.temporal_embedding(enc_in, x_mark_enc)

        # Mapping trend part to target length
        trend_part = trend_part.permute(0, 2, 1)
        trend_part = self.projection_trend(trend_part)
        trend_part = trend_part.permute(0, 2, 1)

        enc_in, components_per_level = self.peri_mid_const(enc_in)

        enc_in = self.position_embedding(enc_in)

        enc_out = self.peri_midformer(
            enc_in, components_per_level, self.configs.task_name)

        enc_out_dim = enc_out.shape[-1]
        target_dim = self.d_model * self.top_k
        if enc_out_dim < target_dim:
            padding_size = target_dim - enc_out_dim
            padding = torch.zeros(
                (enc_out.shape[:-1] + (padding_size,)), device=enc_out.device)
            enc_out = torch.cat((enc_out, padding), dim=-1)

        periodic_feature_flows = self.projection(enc_out)
        periodic_feature_flows_aggration = torch.mean(
            periodic_feature_flows, dim=-2)
        dec_out = periodic_feature_flows_aggration.permute(0, 2, 1)

        # add trend part
        dec_out = dec_out + trend_part

        # De-Normalization from Non-stationary Transformer
        dec_out = dec_out * \
            (stdev[:, 0, :].unsqueeze(1).repeat(
                1, self.configs.label_len + self.pred_len, 1))
        dec_out = dec_out + \
            (means[:, 0, :].unsqueeze(1).repeat(
                1, self.configs.label_len + self.pred_len, 1))

        return dec_out


class PerimidFormerModel(BaseBiDirectionalModel):
    '''
    Peri-midFormer model.
    Implements from paper: https://arxiv.org/abs/2411.04554
    '''
    use_generator = True
    name = "Peri-midFormer"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Model params
        self.top_k = kwargs.get("top_k", 3)
        self.d_model = kwargs.get("d_model", 768)
        self.n_heads = kwargs.get("n_heads", 8)
        self.layers = kwargs.get("layers", 2)
        self.dropout = kwargs.get("dropout", 0.1)
        self.moving_avg = kwargs.get("moving_avg", 25)
        self.feature_flows_dim = self.d_model * self.top_k * 1 * 3
        self.chan_in = 1
