#pip install --quiet "git+https://github.com/opendatalab/DocLayout-YOLO"
#pip install --quiet matplotlib

# 2. Upload your image
image_path = r"C:\Users\feder\Programmazione\LaTeX\gptpdf_LaTeX\Screenshot.png"

# 3. Load DocLayout-YOLO pre-trained on DocStructBench (figures, tables, text, etc.)
from doclayout_yolo import YOLOv10
import matplotlib.pyplot as plt

# Download model weights from huggingface
from huggingface_hub import hf_hub_download
#weights = hf_hub_download(repo_id="juliozhao/DocLayout-YOLO-DocStructBench", filename="doclayout_yolo_docstructbench_imgsz1024.pt")
weights = hf_hub_download(repo_id="juliozhao/DocLayout-YOLO-DocLayNet-Docsynth300K_pretrained",
                          filename="doclayout_yolo_doclaynet_imgsz1120_docsynth_pretrain.pt")

model = YOLOv10(weights)

# 4. Predict (set to detect images/figures)
result = model.predict(
    image_path,
    imgsz=1024,
    conf=0.2,
    device='cuda:0'# if torch.cuda.is_available() else 'cpu'
)

# 5. Draw and display all detected regions
annotated = result[0].plot(pil=True, line_width=5, font_size=20)
plt.figure(figsize=(12, 12))
plt.imshow(annotated)
plt.axis('off')
plt.show()

# 6. Print and crop "figure" regions
# Get numpy array of bounding boxes and class indices
boxes = result[0].boxes.xyxy.cpu().numpy()  # (N,4)
classes = result[0].boxes.cls.cpu().numpy().astype(int)
names = result[0].names  # dict(int: str), class names

for i, (xyxy, cls) in enumerate(zip(boxes, classes)):
    label = names[cls]
    if label.lower() == 'figure':  # or adjust for your diagram/image class
        x1, y1, x2, y2 = map(int, xyxy)
        print(f"Detected Figure {i+1} at: {x1}, {y1}, {x2}, {y2}")
        from PIL import Image
        with Image.open(image_path) as im:
            crop = im.crop((x1, y1, x2, y2))
            plt.figure()
            plt.imshow(crop)
            plt.title(f'Figure {i+1}')
            plt.axis('off')
            plt.show()
    if label.lower() == 'picture':  # or adjust for your diagram/image class
        x1, y1, x2, y2 = map(int, xyxy)
        print(f"Detected Figure {i+1} at: {x1}, {y1}, {x2}, {y2}")
        from PIL import Image
        with Image.open(image_path) as im:
            crop = im.crop((x1, y1, x2, y2))
            plt.figure()
            plt.imshow(crop)
            plt.title(f'Figure {i+1}')
            plt.axis('off')
            plt.show()