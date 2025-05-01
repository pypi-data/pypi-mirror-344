import os
import shutil
import argparse
import numpy as np
from .feature_generate import gen_feature, gen_input_tokens

def main():
    parser = argparse.ArgumentParser(description="Generate text feature for YOLO-World.")
    subparsers = parser.add_subparsers(help='command help', dest="cmd", required=True)
    # cmd gen_text_feature
    parser_gen_text_feature = subparsers.add_parser("gen_text_feature", help="Generate text feature for YOLO-World.")
    parser_gen_text_feature.add_argument(
        "--labels_path", type=str, required=True, help="Path to the labels file (txt format), one label per line."
    )
    parser_gen_text_feature.add_argument(
        "--out_dir", type=str, default="out", help="Output directory to save the generated text feature. Default is 'out'."
    )
    parser_gen_text_feature.add_argument(
        "--out_feature_path", type=str, default="", help="Output path to save the generated text feature, default sanme with labels_path file name. can be .bin or .npy fromat"
    )
    parser_gen_text_feature.add_argument(
        "--token_max_length", type=int, default=77, help="Maximum length of the tokenized input, default 77."
    )
    # cmd gen_input_tokens
    parser_gen_input_token = subparsers.add_parser("gen_input_tokens", help="Generate input token for YOLO-World.")
    parser_gen_input_token.add_argument(
        "--labels_path", type=str, required=True, help="Path to the labels file (txt format), one label per line."
    )
    parser_gen_input_token.add_argument(
        "--out_dir", type=str, default="out", help="Output directory to save the generated text feature. Default is 'out'."
    )
    parser_gen_input_token.add_argument(
        "--out_feature_path", type=str, default="", help="Output path to save the generated text feature, default sanme with labels_path file name. can be .bin or .npy fromat"
    )
    parser_gen_input_token.add_argument(
        "--token_max_length", type=int, default=77, help="Maximum length of the tokenized input, default 77."
    )

    args = parser.parse_args()
    labels_path = args.labels_path
    out_dir = args.out_dir
    token_max_length = args.token_max_length
    out_feature_path = args.out_feature_path
    if not os.path.exists(labels_path):
        print(f"File {labels_path} does not exist.")
        exit(1)
    os.makedirs(out_dir, exist_ok=True)
    with open(labels_path, "r") as f:
        labels = f.readlines()
    labels = [label.strip() for label in labels]
    labels_file_name = os.path.splitext(os.path.basename(labels_path))[0]
    if args.cmd == "gen_input_tokens":
        print("Generating input token...")
        tokens = gen_input_tokens(labels, out_dir, token_max_length)
        if tokens is None:
            print("Error: Failed to generate input tokens.")
            exit(1)
        final_path = os.path.join(out_dir, f"{labels_file_name}.npy")
        print(f"Saving input tokens to {final_path}")
        np.save(final_path, tokens)
        print("Save input tokens Done.\n")
    if args.cmd == "gen_text_feature":
        print("Generating text feature...")
        feature = gen_feature(labels, out_dir, token_max_length)
        if not out_feature_path:
            out_feature_path = f"{labels_file_name}_text_feature.bin"
        final_path = os.path.join(out_dir, out_feature_path)
        print(f"Saving text feature to {final_path}")
        if final_path.endswith(".npy"):
            np.save(final_path, feature)
        else:
            feature.tofile(final_path)
        print("Copy labels file to out dir")
        shutil.copy(labels_path, os.path.join(out_dir, os.path.basename(labels_path)))
        print("Save text feature Done.\n")
    print("Done.")

if __name__ == "__main__":
    main()
