import os

onnx_path = os.path.join(os.path.dirname(__file__), "yoloworld.vitb.txt.onnx")
if not os.path.exists(onnx_path):
    print(f"now downloading {os.path.basename(onnx_path)} file, please wait")
    print(f"you can mannually download it (https://github.com/Neutree/yolo-world-utils/releases) and put it in {onnx_path}")
    msg = f"Download {os.path.basename(onnx_path)} failed, you can mannually download from https://github.com/Neutree/yolo-world-utils/releases"
    msg += f"And save to {onnx_path}"
    try:
        import requests
        url = "https://github.com/Neutree/yolo-world-utils/releases/download/v1.0.0/yoloworld.vitb.txt.onnx"

        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(onnx_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        else:
            print("Downlaod faield:", response.status_code)
            raise Exception(msg)
    except Exception as e:
        print(e)
        raise Exception(msg)


