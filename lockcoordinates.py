'''
    @date   : 01-01-2024
    @author : Mayand Dangi
'''


import numpy as np
import onnx
import onnxruntime
from skimage.restoration import denoise_wavelet, estimate_sigma


class LockCoordinates:
    def __init__(self, model_path):
        # Initialize variables
        self.ramptime = 0
        self.pddiff = 0
        
        # Load ONNX Model
        self.onnx_model_path = model_path
        self.onnx_model = onnx.load(self.onnx_model_path)
        self.onnx_runtime = onnxruntime.InferenceSession(self.onnx_model_path)
        
    def getLockingPoint(self, pd1, pd2):
        # Pre-processing of data to get feature vector
        
        ## Wavelet Denoising
        pd1_f = denoise_wavelet(pd1, wavelet='db8', wavelet_levels=6, method='VisuShrink', mode='soft', sigma=estimate_sigma(pd1, average_sigmas=True)*4, rescale_sigma=True)
        pd2_f = denoise_wavelet(pd2, wavelet='db8', wavelet_levels=6, method='VisuShrink', mode='soft', sigma=estimate_sigma(pd2, average_sigmas=True)*4, rescale_sigma=True)
        
        ## Normalisation
        pd1_0 = pd1_f/1024
        pd2_0 = pd2_f/1024
        features = pd1_0 - pd2_0 - (np.mean(pd1_0) - np.mean(pd2_0))
        
        # Output prediction
        
        ## prepare input according to input feature vector of model
        inputs = np.reshape(features, (1, 1, 4095))
        onnx_input = {self.onnx_runtime.get_inputs()[0].name: inputs.astype(np.float32)}
        
        ## ouput from onnx model
        onnx_output = self.onnx_runtime.run(None, onnx_input)
        
        ## obtain locking coordinates
        self.ramptime = int(onnx_output[0][0][0]*4095)
        self.pddiff = int((features[self.ramptime] + (np.mean(pd1_0) - np.mean(pd2_0)))*1024)
        
        return self.ramptime, self.pddiff
        