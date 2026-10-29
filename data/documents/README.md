# Document images: CV or not?

A small image dataset for tasks 1.4 and 1.5: scanned documents in 4 classes that can come with a job application.

| Class | Meaning | train | val | test |
|---|---|---|---|---|
| `resume` | CV / resume | 700 | 150 | 150 |
| `letter` | letter (e.g. cover letter) | 700 | 150 | 150 |
| `email` | printed email | 700 | 150 | 150 |
| `form` | filled form | 700 | 150 | 150 |

Images are 128×128 greyscale JPEG files: `{train,val,test}/{class}/{class}_NNNN.jpg`.

**Source:** RVL-CDIP (A. W. Harley, A. Ufkes, K. G. Derpanis, *Evaluation of Deep Convolutional Nets for Document Image Classification and Retrieval*, ICDAR 2015),
Hugging Face copy [`chainyo/rvl-cdip`](https://huggingface.co/datasets/chainyo/rvl-cdip), split `val`.
RVL-CDIP is a subset of the IIT-CDIP Test Collection, which is made of public documents from the Legacy Tobacco Documents Library.
Used here only for a university assignment.

The folder was made with [`scripts/prepare_documents_dataset.py`](../../scripts/prepare_documents_dataset.py)
(the first 1,000 scans of each class, shrunk to 128×128).
