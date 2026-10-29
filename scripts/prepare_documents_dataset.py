"""Build the small document image dataset used in tasks 1.4 and 1.5.

Takes 4 document types from RVL-CDIP (Hugging Face `chainyo/rvl-cdip`, split `val`),
shrinks them to 128x128 greyscale and saves them as JPEG files:

    data/documents/{train,val,test}/{resume,letter,email,form}/*.jpg

Only the parquet row groups that contain the needed labels are downloaded.

Run:  python scripts/prepare_documents_dataset.py
"""
import io
import os

import fsspec
import pyarrow.parquet as pq
from PIL import Image

CLASSES = {12: "resume", 7: "letter", 2: "email", 4: "form"}   # RVL-CDIP label id -> folder name
PER_CLASS = 1000
SPLITS = [("train", 700), ("val", 150), ("test", 150)]
SIZE = (128, 128)
SHARDS = [f"https://huggingface.co/api/datasets/chainyo/rvl-cdip/parquet/default/val/{i}.parquet" for i in range(7)]
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "documents")

fs = fsspec.filesystem("https")
counts = {name: 0 for name in CLASSES.values()}


def save(name, image_bytes):
    i = counts[name]
    offset = 0
    for split, n in SPLITS:
        if i < offset + n:
            break
        offset += n
    folder = os.path.join(OUT, split, name)
    os.makedirs(folder, exist_ok=True)
    img = Image.open(io.BytesIO(image_bytes)).convert("L").resize(SIZE, Image.LANCZOS)
    img.save(os.path.join(folder, f"{name}_{i:04d}.jpg"), quality=90)
    counts[name] += 1


for url in SHARDS:
    if all(c >= PER_CLASS for c in counts.values()):
        break
    with fs.open(url, block_size=8 * 2**20) as f:
        pf = pq.ParquetFile(f)
        for rg in range(pf.num_row_groups):
            # read only the small label column first, the images only if this row group has a label we need
            labels = set(pf.read_row_group(rg, columns=["label"]).column("label").to_pylist())
            if not any(lab in labels and counts[CLASSES[lab]] < PER_CLASS for lab in CLASSES):
                continue
            for row in pf.read_row_group(rg).to_pylist():
                name = CLASSES.get(row["label"])
                if name and counts[name] < PER_CLASS:
                    try:
                        save(name, row["image"]["bytes"])
                    except Exception as e:   # a few RVL-CDIP files are broken
                        print("skipped one image:", e)
            print(url.rsplit("/", 1)[-1], "row group", rg, counts)

print("done:", counts)
