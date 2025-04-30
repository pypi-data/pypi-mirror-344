'''
    YOLO-World Utils
    @Author: Neucrack
    @email: CZD666666@gmail.com
    @Date: 2025-04-27
    @license: AGPL-3.0
'''

import onnxruntime
import os
import numpy as np
from .simple_tokenizer import SimpleTokenizer

class TextFeature:
    def __init__(self, model_path):
        self.session = onnxruntime.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    def infer(self, input_data):
        ort_inputs = {self.input_name: input_data}
        ort_outs = self.session.run([self.output_name], ort_inputs)
        return ort_outs[0]

def gen_input_tokens(labels : list[str], out_dir : str, token_max_length : int = 77, crop : bool = False):
    tokenizer = SimpleTokenizer(os.path.join(os.path.dirname(__file__), "bpe_simple_vocab_16e6.txt"))
    start_idx = tokenizer.encoder["<|startoftext|>"]
    end_idx = tokenizer.encoder["<|endoftext|>"]
    result = np.zeros((len(labels), token_max_length), dtype=np.int32)
    for i, label in enumerate(labels):
        tokens = tokenizer.encode(label)
        print(f"[INFO] label {label} has {len(tokens)} tokens")
        if len(tokens) > token_max_length - 2:
            if crop:
                tokens = tokens[: token_max_length - 2]
            else:
                raise Exception(f"[ERROR] label {label} is too long, max support {token_max_length - 2} tokens, but got {len(tokens)}")
        result[i, : len(tokens) + 2] = [start_idx] + tokens + [end_idx]
    return result

def gen_feature(labels : list[str], out_dir : str, token_max_length : int = 77):
    if token_max_length != 77:
        print("[ERROR] token_max_length now only support 77")
        print("sikp gen_feature")
        return
    tokens = gen_input_tokens(labels, out_dir, token_max_length)
    text_feature_model_path = os.path.join(os.path.dirname(__file__), "yoloworld.vitb.txt.onnx")
    text_feature = TextFeature(text_feature_model_path)
    text_feature_out = text_feature.infer(tokens)
    return text_feature_out



