## YoloPrep

**YoloPrep** is a lightweight Python toolkit to prepare your object detection dataset for training with YOLOv5, YOLOv8, or other YOLO-based frameworks.

#### Output Structure

```
images/
└── train/
    ├── image_001.jpg
    ├── image_002.jpg
labels/
└── train/
    ├── image_001.txt    ← empty YOLO annotation
    ├── image_002.txt
```

### Installation

```bash
pip install yoloprep
```

#### Example

```python
from yoloprep.core import YoloImagePreparator

prep = YoloImagePreparator(
    source_dir="raw_images",
    image_out_dir="images/train",
    label_out_dir="labels/train",
    image_size=640
)
prep.extract_frames("video.mp4", every_n_frames=10)
prep.prepare()
```

#### Command Line

```bash
yoloprep --source raw_images --size 640
```

#### License

MIT License
