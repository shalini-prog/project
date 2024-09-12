import mne
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# Step 1: Load EEG data (example with a .edf file)
# Replace 'your_eeg_file.edf' with the path to your EEG file
eeg_file = 'your_eeg_file.edf'
raw_eeg = mne.io.read_raw_edf(eeg_file, preload=True)

# Step 2: Filter Design (Band-pass filter to isolate Alpha wave: 8-12 Hz)
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Step 3: Extract Data and Sampling Frequency
eeg_data = raw_eeg.get_data()  # EEG data as numpy array
sfreq = raw_eeg.info['sfreq']  # Sampling frequency

# Step 4: Preprocessing - Filter the EEG signal (Alpha band: 8-12 Hz)
lowcut = 8.0
highcut = 12.0
filtered_eeg = bandpass_filter(eeg_data[0], lowcut, highcut, sfreq)

# Step 5: Visualize the Original vs Filtered EEG Data
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(eeg_data[0][:1000], color='blue')
plt.title('Original EEG Signal')
plt.xlabel('Samples')
plt.ylabel('Amplitude')

plt.subplot(2, 1, 2)
plt.plot(filtered_eeg[:1000], color='red')
plt.title('Filtered EEG Signal (8-12 Hz Alpha Band)')
plt.xlabel('Samples')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()