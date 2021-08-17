import os
import sys
from glob import glob
import torchaudio
import torch
import zipfile
from omegaconf import OmegaConf

from utils import init_jit_model, read_batch, split_into_batches,  prepare_model_input

def recognizeAudio(path):
    filename, file_extension = os.path.splitext(path)
    assert(file_extension == '.wav')

    device = torch.device('cpu')
    
    jit_model = "ua_v1_jit.model"
    model, decoder = init_jit_model(jit_model, device=device)
    test_file = glob(path)
    batches = split_into_batches(test_file, batch_size=10)
    input = prepare_model_input(read_batch(batches[0]), device=device) # Вхідний шар в нейронній мережі
    output = model(input)

    return decoder(output[0].cpu())
    
