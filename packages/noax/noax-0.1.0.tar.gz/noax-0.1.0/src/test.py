from layers.spectral_conv import SpectralConvND
import jax.numpy as jnp
import jax

in_channels = 1
out_channels = 1
h = 64
w = 64
n_modes = [16, 16]
use_bias = False

x = jnp.zeros((in_channels, h, w))

conv = SpectralConvND(in_channels, out_channels, n_modes, use_bias,
                      jax.random.PRNGKey(0))

y = conv(x)

print(y.shape)

in_channels = 1
out_channels = 1
h = 64
w = 64
n_modes = [16]
use_bias = False

x = jnp.zeros((in_channels, h))

conv = SpectralConvND(in_channels, out_channels, n_modes, use_bias,
                      jax.random.PRNGKey(0))

y = conv(x)

print(y.shape)
