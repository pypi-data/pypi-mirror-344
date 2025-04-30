import numpy as np
from VuVoPy.data.containers.prepocessing import Preprocessed as pp
from VuVoPy.data.containers.sample import VoiceSample as vs
from VuVoPy.data.containers.segmentation import Segmented as sg
from VuVoPy.data.utils.vuvs_detection import Vuvs as vuvs

def durmad(folder_path, winlen = 512, winover = 496 , wintype = 'hamm'):
    """
    Computes the absolute median deviation of silence durations from a voice sample.
    This function processes a voice sample from a given folder path, segments it
    using specified window parameters, and calculates the silence durations. It
    then returns the absolute median deviation of these silence durations.
    
    Parameters:
        folder_path (str): The path to the folder containing the voice sample in WAV format.
        winlen (int, optional): The length of the analysis window. Default is 512.
        winover (int, optional): The overlap between consecutive windows. Default is 496.
        wintype (str, optional): The type of window function to apply (e.g., 'hamm' for Hamming window). Default is 'hamm'.
    
    Returns:
        float: The absolute median deviation of silence durations in the voice sample, in seconds.
    """
    
    preprocessed_sample = pp.from_voice_sample(vs.from_wav(folder_path))
    segment = sg.from_voice_sample(preprocessed_sample, winlen, wintype, winover)
    fs = segment.get_sampling_rate()
    labels = vuvs(segment, fs=fs, winlen =segment.get_window_length(), winover = segment.get_window_overlap(), wintype=segment.get_window_type(), smoothing_window=5)
    silence_dur = labels.get_silence_durations()
    return np.mean(np.abs(silence_dur - np.median(silence_dur)))
