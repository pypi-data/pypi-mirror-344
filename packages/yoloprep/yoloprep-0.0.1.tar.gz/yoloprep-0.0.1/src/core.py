import cv2
import yaml
from pathlib import Path
from tqdm import tqdm


class YoloImagePreparator:
    def __init__(
        self,
        source_dir,
        image_out_dir="images/train",
        label_out_dir="labels/train",
        image_size=640,
    ):
        self.source_dir = Path(source_dir)
        self.image_out_dir = Path(image_out_dir)
        self.label_out_dir = Path(label_out_dir)
        self.image_size = image_size

        self.image_out_dir.mkdir(parents=True, exist_ok=True)
        self.label_out_dir.mkdir(parents=True, exist_ok=True)

    def prepare(self):
        image_paths = list(self.source_dir.glob("*.*"))
        for img_path in tqdm(image_paths, desc="Preparing images"):
            self._process(img_path)

    def _process(self, img_path: Path):
        try:
            img = cv2.imread(str(img_path))
            if img is None or img.shape[0] < 50 or img.shape[1] < 50:
                print(f"Skipped: {img_path.name}")
                return

            resized = cv2.resize(img, (self.image_size, self.image_size))
            out_img = self.image_out_dir / (img_path.stem + ".jpg")
            out_txt = self.label_out_dir / (img_path.stem + ".txt")

            cv2.imwrite(str(out_img), resized)
            out_txt.write_text("")  # empty YOLO label
        except Exception as e:
            print(f"Error processing {img_path.name}: {e}")

    def extract_frames(self, video_path, every_n_frames=10):
        video_path = Path(video_path)
        cap = cv2.VideoCapture(str(video_path))
        count = 0
        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % every_n_frames == 0:
                out_path = self.image_out_dir / f"{video_path.stem}_frame_{count}.jpg"
                resized = cv2.resize(frame, (self.image_size, self.image_size))
                cv2.imwrite(str(out_path), resized)
                txt_path = self.label_out_dir / f"{video_path.stem}_frame_{count}.txt"
                txt_path.write_text("")
                count += 1
            frame_idx += 1
        cap.release()

    def generate_yaml(self, class_names, output_path="data.yaml"):
        yaml_data = {
            "path": ".",
            "train": str(self.image_out_dir),
            "val": str(self.image_out_dir).replace("train", "val"),
            "names": {i: name for i, name in enumerate(class_names)},
        }
        with open(output_path, "w") as f:
            yaml.dump(yaml_data, f)
