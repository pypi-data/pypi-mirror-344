import argparse
from yoloprep.core import YoloImagePreparator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="Path to input images")
    parser.add_argument("--size", type=int, default=640, help="Resize to this size")
    parser.add_argument("--video", help="Path to video to extract frames from")
    parser.add_argument(
        "--frameskip", type=int, default=10, help="Extract every Nth frame"
    )
    parser.add_argument(
        "--yaml", nargs="+", help="Generate data.yaml with given class names"
    )
    args = parser.parse_args()

    prep = YoloImagePreparator(args.source or ".", image_size=args.size)

    if args.video:
        prep.extract_frames(args.video, every_n_frames=args.frameskip)
    elif args.yaml:
        prep.generate_yaml(args.yaml)
    else:
        prep.prepare()
