import os

onnx_path = os.path.join(os.path.dirname(__file__), "yoloworld.vitb.txt.onnx")
if not os.path.exists(onnx_path):
    print(f"now downloading {os.path.basename(onnx_path)} file, please wait")
    print(f"you can mannually download it (https://github.com/Neutree/yolo-world-utils/releases) and put it in {onnx_path}")
    try:
        from huggingface_hub import hf_hub_download
        import shutil
        file_path = hf_hub_download(
            repo_id="neucrack/yolo-world-utils",
            filename="yolo_world_utils/yoloworld.vitb.txt.onnx",
            revision="main"
        )
        shutil.move(file_path, onnx_path)
        del hf_hub_download, file_path
    except Exception as e:
        print(e)
        print(f"Download {os.path.basename(onnx_path)} failed, you can mannually download from https://github.com/Neutree/yolo-world-utils/releases")
        print(f"And save to {onnx_path}")


