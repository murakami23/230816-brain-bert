import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, stats

original_sf = 9600  # 9600
re_sf = 2048  # 2048

# ダウンサンプリング（input_dataだけ指定すれば良い）
def downsampling(input_data, original_sf=original_sf, re_sf=re_sf, lowpass_order=6):
    # Calculate the downsample factor
    downsample_factor = original_sf // re_sf

    # Design a low-pass filter for anti-aliasing
    nyquist_freq = 0.5 * original_sf
    lowpass_cutoff = 0.5 * re_sf
    lowpass_b, lowpass_a = signal.butter(lowpass_order, lowpass_cutoff / nyquist_freq, btype='low')

    # Apply the low-pass filter and downsample
    downsampled_data = signal.filtfilt(lowpass_b, lowpass_a, input_data, axis=0)[::downsample_factor]
    return downsampled_data

def get_stft(x, fs, clip_fs=-1, normalizing=None, **kwargs):
    f, t, Zxx = signal.stft(x, fs, **kwargs)
   
    Zxx = Zxx[:clip_fs]
    f = f[:clip_fs]

    Zxx = np.abs(Zxx)
    clip = 5 #To handle boundary effects
    if normalizing=="zscore":
        Zxx = Zxx[:,clip:-clip]
        Zxx = stats.zscore(Zxx, axis=-1)
        t = t[clip:-clip]
    elif normalizing=="baselined":
        Zxx = baseline(Zxx[:,clip:-clip])
        t = t[clip:-clip]
    elif normalizing=="db":
        Zxx = np.log2(Zxx[:,clip:-clip])
        t = t[clip:-clip]

    if np.isnan(Zxx).any():
        import pdb; pdb.set_trace()

    return f, t, Zxx

# downsamplingを追加
# chを選択
def plot_stft(ecog, ch):
    f,t,linear = get_stft(ecog[:, ch], 2048, clip_fs=40, nperseg=400, noverlap=350, normalizing="zscore", return_onesided=True) #TODO hardcode sampling rate
    plt.figure(figsize=(15,3))
    f[-1]=200
    g1 = plt.pcolormesh(t,f,linear, shading="gouraud", vmin=-3, vmax=5)

    cbar = plt.colorbar(g1)
    tick_font_size = 15
    cbar.ax.tick_params(labelsize=tick_font_size)
    cbar.ax.set_ylabel("Power (Arbitrary units)", fontsize=15)
    plt.xticks(fontsize=20)
    plt.ylabel("")
    plt.yticks(fontsize=20)
    plt.xlabel("Time (s)", fontsize=20)
    plt.ylabel("Frequency (Hz)", fontsize=20)

    plt.show()