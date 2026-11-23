#!/usr/bin/env python3
"""Scaffold the top30-papers monorepo (standard library only).

Creates anything that is missing and NEVER overwrites an existing file, so it is
safe to re-run after you have started working in the notebooks.

Usage (from the repo root):
    python tools/scaffold.py                 # build / repair the whole skeleton
    python tools/scaffold.py add --num 31 --slug my_paper --track trackA_classical \
        --short "My Paper" --title "Full title" --authors "A, B" --year 2024 \
        --venue "CVPR 2024" --link https://arxiv.org/abs/xxxx --depth Standard

Placeholders used in templates/paper_template.ipynb:
    {{NUM}} {{SHORT}} {{TITLE}} {{AUTHORS}} {{YEAR}} {{VENUE}} {{LINK}}
    {{TRACK}} {{DEPTH}} {{FOLDER}} {{SLUG}} {{GITHUB_USER}}
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GITHUB_USER = "anwarmirza"
AUTHOR_NAME = "Anwar M. Mirza"
YEAR_NOW = 2026

# --------------------------------------------------------------------------- #
# Tracks and papers
# --------------------------------------------------------------------------- #
TRACKS = {
    "trackA_classical": ("A", "Classical ML & CV", "A-classical.md"),
    "trackB_foundations": ("B", "Neural-net foundations & training", "B-foundations.md"),
    "trackC_cnn_rl": ("C", "CNN architectures & deep RL", "C-cnn-rl.md"),
    "trackD_detection_segmentation": ("D", "Detection & segmentation", "D-detection-segmentation.md"),
    "trackE_sequences_language": ("E", "Sequences, embeddings & language models", "E-sequences-language.md"),
    "trackF_vit_multimodal": ("F", "Vision Transformers & multimodal", "F-vit-multimodal.md"),
    "trackG_generative": ("G", "Generative models", "G-generative.md"),
}

# num, slug, short name, title, authors, year, venue, link, track, depth
PAPERS = [
    (1, "lstm", "LSTM", "Long Short-Term Memory",
     "Sepp Hochreiter, Jürgen Schmidhuber", 1997, "Neural Computation 9(8), 1997",
     "https://www.bioinf.jku.at/publications/older/2604.pdf", "trackE_sequences_language", "Standard"),
    (2, "lenet5", "LeNet-5", "Gradient-Based Learning Applied to Document Recognition",
     "Yann LeCun, Léon Bottou, Yoshua Bengio, Patrick Haffner", 1998, "Proceedings of the IEEE, 1998",
     "http://yann.lecun.com/exdb/publis/pdf/lecun-98.pdf", "trackB_foundations", "Deep"),
    (3, "random_forests", "Random Forests", "Random Forests",
     "Leo Breiman", 2001, "Machine Learning 45(1), 2001",
     "https://www.stat.berkeley.edu/~breiman/randomforest2001.pdf", "trackA_classical", "Deep"),
    (4, "viola_jones", "Viola–Jones", "Rapid Object Detection using a Boosted Cascade of Simple Features",
     "Paul Viola, Michael Jones", 2001, "CVPR 2001",
     "https://www.cs.cmu.edu/~efros/courses/LBMR/papers/viola-cvpr-01.pdf", "trackA_classical", "Standard"),
    (5, "sift", "SIFT", "Distinctive Image Features from Scale-Invariant Keypoints",
     "David G. Lowe", 2004, "IJCV 60(2), 2004",
     "https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf", "trackA_classical", "Standard"),
    (6, "hog", "HOG", "Histograms of Oriented Gradients for Human Detection",
     "Navneet Dalal, Bill Triggs", 2005, "CVPR 2005",
     "https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf", "trackA_classical", "Deep"),
    (7, "deep_belief_nets", "Deep Belief Nets", "A Fast Learning Algorithm for Deep Belief Nets",
     "Geoffrey E. Hinton, Simon Osindero, Yee-Whye Teh", 2006, "Neural Computation 18(7), 2006",
     "https://www.cs.toronto.edu/~hinton/absps/fastnc.pdf", "trackB_foundations", "Standard"),
    (8, "imagenet", "ImageNet", "ImageNet: A Large-Scale Hierarchical Image Database",
     "Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li, Li Fei-Fei", 2009, "CVPR 2009",
     "https://www.image-net.org/static_files/papers/imagenet_cvpr09.pdf", "trackC_cnn_rl", "Standard"),
    (9, "alexnet", "AlexNet", "ImageNet Classification with Deep Convolutional Neural Networks",
     "Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton", 2012, "NeurIPS 2012",
     "https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html",
     "trackC_cnn_rl", "Standard"),
    (10, "word2vec", "word2vec", "Efficient Estimation of Word Representations in Vector Space",
     "Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean", 2013, "ICLR Workshop 2013",
     "https://arxiv.org/abs/1301.3781", "trackE_sequences_language", "Standard"),
    (11, "vae", "VAE", "Auto-Encoding Variational Bayes",
     "Diederik P. Kingma, Max Welling", 2013, "ICLR 2014 (arXiv 2013)",
     "https://arxiv.org/abs/1312.6114", "trackG_generative", "Deep"),
    (12, "gan", "GAN", "Generative Adversarial Nets",
     "Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, "
     "Aaron Courville, Yoshua Bengio", 2014, "NeurIPS 2014",
     "https://arxiv.org/abs/1406.2661", "trackG_generative", "Standard"),
    (13, "dropout", "Dropout", "Dropout: A Simple Way to Prevent Neural Networks from Overfitting",
     "Nitish Srivastava, Geoffrey Hinton, Alex Krizhevsky, Ilya Sutskever, Ruslan Salakhutdinov", 2014,
     "JMLR 15, 2014", "https://jmlr.org/papers/v15/srivastava14a.html", "trackB_foundations",
     "Deep (with BatchNorm, one ablation)"),
    (14, "adam", "Adam", "Adam: A Method for Stochastic Optimization",
     "Diederik P. Kingma, Jimmy Ba", 2014, "ICLR 2015 (arXiv 2014)",
     "https://arxiv.org/abs/1412.6980", "trackB_foundations", "Standard"),
    (15, "vgg", "VGG", "Very Deep Convolutional Networks for Large-Scale Image Recognition",
     "Karen Simonyan, Andrew Zisserman", 2014, "ICLR 2015 (arXiv 2014)",
     "https://arxiv.org/abs/1409.1556", "trackC_cnn_rl", "Standard"),
    (16, "batch_norm", "Batch Normalization",
     "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift",
     "Sergey Ioffe, Christian Szegedy", 2015, "ICML 2015",
     "https://arxiv.org/abs/1502.03167", "trackB_foundations", "Deep (with Dropout, one ablation)"),
    (17, "unet", "U-Net", "U-Net: Convolutional Networks for Biomedical Image Segmentation",
     "Olaf Ronneberger, Philipp Fischer, Thomas Brox", 2015, "MICCAI 2015",
     "https://arxiv.org/abs/1505.04597", "trackD_detection_segmentation", "Deep"),
    (18, "faster_rcnn", "Faster R-CNN",
     "Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks",
     "Shaoqing Ren, Kaiming He, Ross Girshick, Jian Sun", 2015, "NeurIPS 2015",
     "https://arxiv.org/abs/1506.01497", "trackD_detection_segmentation", "Deep (with Mask R-CNN, one fine-tune)"),
    (19, "yolo", "YOLO", "You Only Look Once: Unified, Real-Time Object Detection",
     "Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi", 2015, "CVPR 2016 (arXiv 2015)",
     "https://arxiv.org/abs/1506.02640", "trackD_detection_segmentation", "Standard"),
    (20, "dqn", "DQN", "Human-level control through deep reinforcement learning "
     "(preprint: Playing Atari with Deep Reinforcement Learning, 2013)",
     "Volodymyr Mnih, Koray Kavukcuoglu, David Silver, et al.", 2015, "Nature 518, 2015 (arXiv 2013)",
     "https://arxiv.org/abs/1312.5602", "trackC_cnn_rl", "Standard"),
    (21, "resnet", "ResNet", "Deep Residual Learning for Image Recognition",
     "Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun", 2015, "CVPR 2016 (arXiv 2015)",
     "https://arxiv.org/abs/1512.03385", "trackC_cnn_rl", "Deep"),
    (22, "xgboost", "XGBoost", "XGBoost: A Scalable Tree Boosting System",
     "Tianqi Chen, Carlos Guestrin", 2016, "KDD 2016",
     "https://arxiv.org/abs/1603.02754", "trackA_classical", "Standard"),
    (23, "transformer", "Transformer", "Attention Is All You Need",
     "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, "
     "Łukasz Kaiser, Illia Polosukhin", 2017, "NeurIPS 2017",
     "https://arxiv.org/abs/1706.03762", "trackE_sequences_language", "Deep"),
    (24, "mask_rcnn", "Mask R-CNN", "Mask R-CNN",
     "Kaiming He, Georgia Gkioxari, Piotr Dollár, Ross Girshick", 2017, "ICCV 2017",
     "https://arxiv.org/abs/1703.06870", "trackD_detection_segmentation", "Deep (with Faster R-CNN, one fine-tune)"),
    (25, "bert", "BERT", "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
     "Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova", 2018, "NAACL 2019 (arXiv 2018)",
     "https://arxiv.org/abs/1810.04805", "trackE_sequences_language", "Standard"),
    (26, "gpt3", "GPT-3", "Language Models are Few-Shot Learners",
     "Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, et al.", 2020, "NeurIPS 2020",
     "https://arxiv.org/abs/2005.14165", "trackE_sequences_language", "Standard"),
    (27, "ddpm", "DDPM", "Denoising Diffusion Probabilistic Models",
     "Jonathan Ho, Ajay Jain, Pieter Abbeel", 2020, "NeurIPS 2020",
     "https://arxiv.org/abs/2006.11239", "trackG_generative", "Deep"),
    (28, "vit", "ViT", "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale",
     "Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, et al.", 2020, "ICLR 2021 (arXiv 2020)",
     "https://arxiv.org/abs/2010.11929", "trackF_vit_multimodal", "Deep"),
    (29, "clip", "CLIP", "Learning Transferable Visual Models From Natural Language Supervision",
     "Alec Radford, Jong Wook Kim, Chris Hallacy, et al.", 2021, "ICML 2021",
     "https://arxiv.org/abs/2103.00020", "trackF_vit_multimodal", "Standard"),
    (30, "latent_diffusion", "Latent Diffusion (Stable Diffusion)",
     "High-Resolution Image Synthesis with Latent Diffusion Models",
     "Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, Björn Ommer", 2021,
     "CVPR 2022 (arXiv 2021)", "https://arxiv.org/abs/2112.10752", "trackG_generative", "Standard"),
]


def paper_fields(p) -> dict:
    num, slug, short, title, authors, year, venue, link, track, depth = p
    folder = f"{track}/{num:02d}_{slug}"
    return {
        "NUM": f"{num:02d}", "SLUG": slug, "SHORT": short, "TITLE": title, "AUTHORS": authors,
        "YEAR": str(year), "VENUE": venue, "LINK": link,
        "TRACK": f"{TRACKS[track][0]}. {TRACKS[track][1]}", "TRACK_DIR": track,
        "DEPTH": depth, "FOLDER": folder, "GITHUB_USER": GITHUB_USER,
    }


def fill(text: str, fields: dict) -> str:
    for k, v in fields.items():
        text = text.replace("{{" + k + "}}", v)
    return text


# --------------------------------------------------------------------------- #
# Notebook template
# --------------------------------------------------------------------------- #
# Each cell: (cell_type, source, tags)
TEMPLATE_CELLS = [
    ("markdown", r"""# {{NUM}} · {{SHORT}} ({{YEAR}})

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/{{GITHUB_USER}}/top30-papers/blob/main/{{FOLDER}}/notebook.ipynb)

| | |
|---|---|
| **Paper** | *{{TITLE}}* |
| **Authors** | {{AUTHORS}} |
| **Venue / year** | {{VENUE}} |
| **Link** | {{LINK}} |
| **Track** | {{TRACK}} |
| **Depth** | {{DEPTH}} |
| **Status** | Not started |

> **How to use this notebook.** Work top to bottom. Markdown cells are written for a learner, so the
> notebook doubles as lecture/lab material. Cells tagged `solution` are removed by
> `tools/make_student_version.py` when you build the student copy.""", []),

    ("markdown", r"""## 1. Title & reproduction target

*Before reading:* open the paper's main results table and copy the **one number** you will try to reproduce.

| Target metric | Paper value | Paper setting (data, model, epochs) | My scaled-down setting |
|---|---|---|---|
| e.g. Test error (%) on … | | | |

**Session log**

| Date | Hours | What I did |
|---|---|---|
| | | |""", []),

    ("markdown", "## 0. Setup\nEnvironment detection (Colab / Kaggle / local Mac), paths and seeds. Run this first.", []),

    ("code", r'''import os, sys, random, subprocess
from pathlib import Path

PAPER_DIR_NAME = "{{FOLDER}}"
GITHUB_REPO = "https://github.com/{{GITHUB_USER}}/top30-papers.git"
SEED = 42

IN_COLAB = "google.colab" in sys.modules
IN_KAGGLE = "KAGGLE_KERNEL_RUN_TYPE" in os.environ


def find_repo_root(start: Path):
    """Walk up from `start` until we find the repo (it has common/ and tools/)."""
    for p in [start, *start.parents]:
        if (p / "common").is_dir() and (p / "tools").is_dir():
            return p
    return None


REPO_ROOT = find_repo_root(Path.cwd())
if REPO_ROOT is None and (IN_COLAB or IN_KAGGLE):
    target = Path("/content/top30-papers" if IN_COLAB else "/kaggle/working/top30-papers")
    if not target.exists():
        subprocess.run(["git", "clone", "--depth", "1", GITHUB_REPO, str(target)], check=True)
    REPO_ROOT = target

if REPO_ROOT is not None:
    sys.path.insert(0, str(REPO_ROOT))
    PAPER_DIR = REPO_ROOT / PAPER_DIR_NAME
else:
    print("Repo not found: shared helpers in common/ will be unavailable.")
    PAPER_DIR = Path.cwd()

RESULTS_DIR = PAPER_DIR / "results"          # committed: figures, CSV metrics
CHECKPOINT_DIR = PAPER_DIR / "checkpoints"   # git-ignored: model weights
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

print("Platform   :", "Colab" if IN_COLAB else "Kaggle" if IN_KAGGLE else "local")
print("Repo root  :", REPO_ROOT)
print("Results dir:", RESULTS_DIR)''', []),

    ("code", r'''# Core imports. Delete the ones a paper does not need.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tensorflow as tf
import keras
# Classical papers (Track A):
# from sklearn import datasets, model_selection, metrics
# import cv2

try:
    from common.env import setup_env
    ENV = setup_env(seed=SEED)   # seeds Python/NumPy/TF and prints library versions + GPU
except ImportError:
    random.seed(SEED); np.random.seed(SEED); tf.random.set_seed(SEED)
    print("TensorFlow", tf.__version__, "| GPUs:", tf.config.list_physical_devices("GPU"))''', []),

    ("markdown", r"""## 2. Literature notes

- **Problem.** What task, and why was it hard at the time?
- **Key idea (one sentence).**
- **What it improved over.** The previous best method and by how much.
- **Why it mattered.** What later work it enabled.

| Related paper | Year | Relation (predecessor / competitor / follow-up) |
|---|---|---|
| | | |
| | | |
| | | |""", []),

    ("markdown", r"""## 3. Mathematical formulation

Write the core equations in LaTeX and define every symbol. Example layout:

**Notation.** $\mathbf{x}\in\mathbb{R}^d$ input, $y$ label, $\theta$ parameters.

**Model.**
$$
\hat{y} = f_\theta(\mathbf{x})
$$

**Objective.**
$$
\mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^{N} \ell\big(f_\theta(\mathbf{x}_i),\, y_i\big)
$$

**Key result / bound / update rule** (the equation that makes this paper this paper):
$$
\text{TODO}
$$""", []),

    ("markdown", r"""## 4. Algorithm

Pseudocode in the paper's own notation.

```text
Algorithm: {{SHORT}}
Input : ...
Output: ...
1. ...
2. for ... do
3.     ...
4. end for
5. return ...
```""", []),

    ("markdown", r"""## 5. Implementation

TensorFlow/Keras by default (scikit-learn / OpenCV for classical papers). Record every place where your
setting differs from the paper. That record is what makes the comparison in Section 6 honest.""", []),

    ("markdown", "### 5.1 Data", []),
    ("code", r'''DATA_CONFIG = {
    "dataset": "TODO",          # what you actually use, e.g. "CIFAR-10"
    "paper_dataset": "TODO",    # what the paper used, e.g. "ImageNet (ILSVRC-2012)"
    "train_size": None,
    "test_size": None,
    "preprocessing": "TODO",
}

# Example:
# (x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
# x_train, x_test = x_train / 255.0, x_test / 255.0''', []),

    ("markdown", "### 5.2 Model", []),
    ("code", r'''def build_model(input_shape, num_classes):
    """Build the model as the paper describes it (layers, sizes, activations, init)."""
    inputs = keras.Input(shape=input_shape)
    x = inputs
    # TODO: the paper's architecture
    x = keras.layers.Flatten()(x)
    outputs = keras.layers.Dense(num_classes, activation="softmax")(x)
    return keras.Model(inputs, outputs, name="{{SLUG}}")

# Classical papers: replace with an sklearn / OpenCV pipeline, e.g.
# from sklearn.ensemble import RandomForestClassifier
# model = RandomForestClassifier(n_estimators=100, random_state=SEED)

# model = build_model(input_shape=(32, 32, 3), num_classes=10)
# model.summary()''', []),

    ("markdown", "### 5.3 Training\n*Tip:* on 2–3 h days, start this cell first and read the paper while it trains.", []),
    ("code", r'''TRAIN_CONFIG = {
    "epochs": None,          "paper_epochs": None,
    "batch_size": None,      "paper_batch_size": None,
    "optimizer": "TODO",     "learning_rate": None,
    "lr_schedule": "TODO",   "augmentation": "TODO",
}

callbacks = [
    keras.callbacks.ModelCheckpoint(str(CHECKPOINT_DIR / "best.keras"), save_best_only=True),
    keras.callbacks.CSVLogger(str(RESULTS_DIR / "training_log.csv")),
]

# model.compile(optimizer=keras.optimizers.Adam(TRAIN_CONFIG["learning_rate"]),
#               loss="sparse_categorical_crossentropy", metrics=["accuracy"])
# history = model.fit(x_train, y_train, validation_split=0.1,
#                     epochs=TRAIN_CONFIG["epochs"], batch_size=TRAIN_CONFIG["batch_size"],
#                     callbacks=callbacks)''', []),

    ("markdown", "### 5.4 Evaluation", []),
    ("code", r'''# test_metrics = model.evaluate(x_test, y_test, return_dict=True)
# print(test_metrics)

# Learning curves (saved to results/):
# from common.plotting import plot_history
# plot_history(history, save_to=RESULTS_DIR / "learning_curves.png")''', []),

    ("markdown", "## 6. Results vs paper", []),
    ("code", r'''comparison = pd.DataFrame([
    {"Metric": "TODO", "Dataset": "TODO", "Paper": None, "Mine": None,
     "Setting differences": "TODO (scale, data, epochs, augmentation)"},
])
comparison["Gap"] = (pd.to_numeric(comparison["Mine"], errors="coerce")
                     - pd.to_numeric(comparison["Paper"], errors="coerce"))
comparison.to_csv(RESULTS_DIR / "results_vs_paper.csv", index=False)
comparison''', []),

    ("markdown", r"""## 7. Analysis

Why do the numbers differ? Go through each cause and say how much it plausibly explains:

- **Scale** (dataset size, model size):
- **Data** (different dataset, preprocessing):
- **Training budget** (epochs, batch size, schedule):
- **Augmentation / regularization:**
- **Implementation details** not stated in the paper:""", []),

    ("markdown", r"""## 8. Improvements

- **Limitations the authors state:**
- **Later fixes** (which papers addressed them):
- **My idea(s)** (standard papers: list them only; deep papers: run one below):

| Idea | Hypothesis | Result |
|---|---|---|
| | | |""", []),
    ("code", "# Improvement experiment (deep papers only)\n", []),

    ("markdown", r"""## 9. Port (later): PyTorch / MATLAB

*Left empty on purpose.* Come back once the PyTorch primer is done.

### 9.1 PyTorch""", []),
    ("code", "# PyTorch port (later)\n", []),
    ("markdown", "### 9.2 MATLAB\n\nKeep the `.m` file next to this notebook (e.g. `port_matlab/main.m`) and link it here.", []),

    ("markdown", r"""## 10. Learning outcomes

- [ ] LO1:
- [ ] LO2:
- [ ] LO3:

Anything you can't tick goes into the buffer week.""", []),

    ("markdown", r"""## 11. Exercises for students

**Exercise 1.** Change one hyperparameter (e.g. …) and explain its effect on the result.""", []),
    ("code", "# Solution 1 (removed from the student version)\n", ["solution"]),
    ("markdown", "**Exercise 2.** …", []),
    ("code", "# Solution 2 (removed from the student version)\n", ["solution"]),
    ("markdown", "**Exercise 3 (stretch).** …", []),
    ("code", "# Solution 3 (removed from the student version)\n", ["solution"]),

    ("markdown", r"""## 12. References

1. {{AUTHORS}} ({{YEAR}}). *{{TITLE}}*. {{VENUE}}. {{LINK}}
2.
3. """, []),
]


def to_lines(src: str) -> list[str]:
    lines = src.split("\n")
    return [l + "\n" for l in lines[:-1]] + [lines[-1]]


def build_notebook(fields: dict | None) -> dict:
    cells = []
    for i, (ctype, src, tags) in enumerate(TEMPLATE_CELLS):
        text = fill(src, fields) if fields else src
        cell = {"cell_type": ctype, "id": f"cell-{i:02d}", "metadata": {}, "source": to_lines(text)}
        if tags:
            cell["metadata"]["tags"] = list(tags)
        if ctype == "code":
            cell["execution_count"] = None
            cell["outputs"] = []
        cells.append(cell)
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
            "colab": {"provenance": [], "toc_visible": True},
            "accelerator": "GPU",
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


# --------------------------------------------------------------------------- #
# Static files
# --------------------------------------------------------------------------- #
GITIGNORE = """# Python
__pycache__/
*.py[cod]
.venv/
venv/
env/
.env

# Jupyter
.ipynb_checkpoints/
.virtual_documents/

# macOS
.DS_Store

# Data and weights (keep the repo small; results/ CSVs and figures ARE committed)
data/
datasets/
checkpoints/
*.keras
*.h5
*.ckpt
*.pt
*.pth
*.safetensors
wandb/
mlruns/
lightning_logs/

# MkDocs build output
site/
"""

REQUIREMENTS = """# Core
numpy
pandas
matplotlib
scipy
jupyter

# Classical ML / CV (Track A)
scikit-learn
scikit-image
opencv-python
xgboost

# Deep learning (TensorFlow/Keras now; PyTorch is added in the "Port" phase)
tensorflow
tensorflow-metal; sys_platform == "darwin" and platform_machine == "arm64"
keras-hub
gymnasium[atari]
gensim

# Publishing
mkdocs
huggingface_hub
gradio

# Later (Port phase): torch torchvision ultralytics diffusers
"""

LICENSE_MIT = f"""MIT License

Copyright (c) {YEAR_NOW} {AUTHOR_NAME}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

LICENSE_DOCS = f"""Documentation and teaching material license
============================================

Copyright (c) {YEAR_NOW} {AUTHOR_NAME}

The code in this repository is licensed under the MIT License (see LICENSE).

All documentation and teaching material — the docs/ and teaching/ folders,
README.md files, and the Markdown text in the notebooks — is licensed under
the Creative Commons Attribution 4.0 International License (CC BY 4.0).

You may share and adapt the material for any purpose, including commercially,
as long as you give appropriate credit, link to the license, and indicate if
changes were made.

Full legal text: https://creativecommons.org/licenses/by/4.0/legalcode
"""

COMMON_INIT = '"""Shared utilities for the top30-papers notebooks."""\n'

COMMON_ENV = '''"""Environment setup: seeds, platform detection, library versions, GPU info."""
from __future__ import annotations

import importlib
import os
import platform
import random
import sys


def _version(module_name: str):
    try:
        return importlib.import_module(module_name).__version__
    except Exception:
        return None


def setup_env(seed: int = 42, deterministic: bool = False, verbose: bool = True) -> dict:
    """Seed every RNG we use and report the environment.

    Returns a dict you can paste into the notebook's Implementation notes.
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass

    gpus = []
    try:
        import tensorflow as tf
        tf.random.set_seed(seed)
        if deterministic:
            tf.config.experimental.enable_op_determinism()
        gpus = [d.name for d in tf.config.list_physical_devices("GPU")]
    except ImportError:
        pass
    try:
        import torch  # only once the PyTorch port phase starts
        torch.manual_seed(seed)
    except ImportError:
        pass

    info = {
        "platform": "colab" if "google.colab" in sys.modules
        else "kaggle" if "KAGGLE_KERNEL_RUN_TYPE" in os.environ else "local",
        "python": platform.python_version(),
        "machine": f"{platform.system()} {platform.machine()}",
        "seed": seed,
        "gpus": gpus,
    }
    for name in ["numpy", "pandas", "sklearn", "tensorflow", "keras", "cv2", "xgboost", "torch"]:
        v = _version(name)
        if v:
            info[name] = v
    if verbose:
        for k, v in info.items():
            print(f"{k:>11}: {v}")
    return info
'''

COMMON_RESULTS = '''"""Helpers for logging runs and comparing with the paper."""
from __future__ import annotations

import csv
import datetime as _dt
from pathlib import Path


def log_run(results_dir, **fields) -> Path:
    """Append one row (with a timestamp) to results/runs.csv."""
    path = Path(results_dir) / "runs.csv"
    row = {"timestamp": _dt.datetime.now().isoformat(timespec="seconds"), **fields}
    new = not path.exists()
    with path.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row))
        if new:
            writer.writeheader()
        writer.writerow(row)
    return path


def compare_with_paper(rows, save_to=None):
    """rows: list of dicts with Metric, Paper, Mine (+ any extra columns).

    Returns a pandas DataFrame with a Gap column; optionally saves it as CSV.
    """
    import pandas as pd

    df = pd.DataFrame(rows)
    df["Gap"] = pd.to_numeric(df.get("Mine"), errors="coerce") - pd.to_numeric(df.get("Paper"), errors="coerce")
    if save_to is not None:
        df.to_csv(save_to, index=False)
    return df
'''

COMMON_PLOTTING = '''"""Plotting helpers shared by the notebooks."""
from __future__ import annotations

from pathlib import Path


def plot_history(history, metrics=("loss", "accuracy"), save_to=None):
    """Plot train/validation curves from a Keras History (or a dict of lists)."""
    import matplotlib.pyplot as plt

    hist = history.history if hasattr(history, "history") else history
    metrics = [m for m in metrics if m in hist]
    fig, axes = plt.subplots(1, len(metrics), figsize=(5 * len(metrics), 3.5), squeeze=False)
    for ax, m in zip(axes[0], metrics):
        ax.plot(hist[m], label=f"train {m}")
        if f"val_{m}" in hist:
            ax.plot(hist[f"val_{m}"], label=f"val {m}")
        ax.set_xlabel("epoch")
        ax.set_title(m)
        ax.legend()
    fig.tight_layout()
    if save_to is not None:
        savefig(fig, save_to)
    return fig


def savefig(fig, path, dpi: int = 150):
    """Save a figure, creating the folder if needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    return path
'''

MAKE_STUDENT = '''#!/usr/bin/env python3
"""Build the student version of a paper notebook.

Removes every cell tagged `solution` and clears all outputs.

Usage (from the repo root):
    python tools/make_student_version.py trackA_classical/03_random_forests/notebook.ipynb
Writes: teaching/student_notebooks/03_random_forests.ipynb
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(src: str) -> None:
    src_path = Path(src)
    nb = json.loads(src_path.read_text(encoding="utf-8"))
    kept = []
    for cell in nb["cells"]:
        if "solution" in cell.get("metadata", {}).get("tags", []):
            continue
        if cell["cell_type"] == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
        kept.append(cell)
    nb["cells"] = kept
    out = ROOT / "teaching" / "student_notebooks" / f"{src_path.resolve().parent.name}.ipynb"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\\n", encoding="utf-8")
    print("Wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
'''

PAPER_README = """# {{NUM}} · {{SHORT}} ({{YEAR}})

**{{TITLE}}**
{{AUTHORS}}. *{{VENUE}}*. [Paper]({{LINK}})

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/{{GITHUB_USER}}/top30-papers/blob/main/{{FOLDER}}/notebook.ipynb)

**Track:** {{TRACK}} · **Depth:** {{DEPTH}} · **Status:** Not started

## Summary

## Key math

## Results vs paper

| Metric | Paper | Mine | Setting differences |
|---|---|---|---|
| | | | |

## Improvements

## Files

- `notebook.ipynb`: full study and reproduction (literature notes, math, algorithm, code, results)
- `results/`: figures and CSV metrics
"""

TRACK_DOC = """# Track {letter}: {name}

## Papers

{paper_list}

## Literature review

How these papers connect: the problem they share, what each one changed, and what came next.

## Math summary

The key equation from each paper, side by side.

## Results vs papers

| Paper | Metric | Paper | Mine | Setting differences |
|---|---|---|---|---|
{result_rows}
"""


def root_readme() -> str:
    rows = []
    for p in PAPERS:
        f = paper_fields(p)
        rows.append(
            f"| {f['NUM']} | [{f['SHORT']}]({f['LINK']}) | {f['YEAR']} | {TRACKS[f['TRACK_DIR']][0]} | "
            f"{f['DEPTH'].split(' ')[0]} | Not started | [notebook]({f['FOLDER']}/notebook.ipynb) | | |"
        )
    tracks = "\n".join(f"- **{v[0]}.** {v[1]} (`{k}/`)" for k, v in TRACKS.items())
    return f"""# Top 30 Papers: Reproducing three decades of ML, DL and CV

Reproductions of 30 landmark papers in machine learning, deep learning and computer vision
(1997–2021). Each paper gets one notebook with literature notes, the math, the algorithm, an
implementation, an honest results-vs-paper comparison, improvement ideas and exercises for students.

**Docs site:** https://{GITHUB_USER}.github.io/top30-papers/ · **Hugging Face:** https://huggingface.co/{GITHUB_USER}

## Index

| # | Paper | Year | Track | Depth | Status | Notebook | HF | Result vs paper |
|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## Tracks

{tracks}

## Repository layout

```
top30-papers/
├── README.md            # this index
├── docs/                # GitHub Pages site (MkDocs): one page per track
├── common/              # shared helpers: env/seeds, results logging, plotting
├── templates/           # paper_template.ipynb: the blank notebook template
├── tools/               # scaffold.py (add papers), make_student_version.py
├── trackA_classical/ … trackG_generative/
│   └── NN_slug/
│       ├── notebook.ipynb
│       ├── README.md    # summary, math, results table, improvements
│       └── results/     # figures, CSV metrics
├── huggingface/         # model cards and Gradio Space apps
├── teaching/            # slides, student notebooks, video scripts
├── LICENSE              # MIT (code)
├── LICENSE-docs         # CC BY 4.0 (docs and teaching material)
└── requirements.txt
```

## Getting started

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt     # installs tensorflow-metal automatically on Apple Silicon
jupyter lab
```

On Colab or Kaggle, use the "Open in Colab" badge in a paper's README; the notebook's setup cell
clones this repo so the shared helpers in `common/` are available.

## Workflow per paper

1. Open `<track>/NN_slug/notebook.ipynb` and fill in the reproduction target first.
2. Work through sections 2–11 (the notebook is the documentation draft).
3. Update the paper's `README.md` and this index table; push.
4. Build the student copy: `python tools/make_student_version.py <path/to/notebook.ipynb>`.

To add a paper beyond the 30: `python tools/scaffold.py add --help`.

## License

Code: MIT (`LICENSE`). Documentation and teaching material: CC BY 4.0 (`LICENSE-docs`).
"""


def mkdocs_yml() -> str:
    nav = "\n".join(f"      - \"{v[0]}. {v[1]}\": tracks/{v[2]}" for v in TRACKS.values())
    return f"""site_name: Top 30 Papers
site_url: https://{GITHUB_USER}.github.io/top30-papers/
repo_url: https://github.com/{GITHUB_USER}/top30-papers
docs_dir: docs
nav:
  - Home: index.md
  - Tracks:
{nav}
markdown_extensions:
  - tables
  - toc:
      permalink: true
"""


DOCS_INDEX = """# Top 30 Papers

Literature reviews, math summaries and results-vs-paper tables for 30 landmark papers in
ML, DL and CV, grouped into seven tracks. Code and notebooks live in the
[GitHub repository](https://github.com/{user}/top30-papers).
""".format(user=GITHUB_USER)

HF_README = """# Hugging Face

- `model_cards/`: one model card per trained deep-paper model (copy `model_card_template.md`).
- `spaces/`: one Gradio Space app per track.
"""

MODEL_CARD = """---
license: mit
library_name: keras
tags: [paper-reproduction, top30-papers]
---

# <Model name>: reproduction of <Paper> (<Year>)

## Model description
## Training data (and how it differs from the paper)
## Training procedure
## Results vs paper
| Metric | Paper | This model | Setting differences |
|---|---|---|---|
## Limitations
## Citation
"""

TEACHING_README = """# Teaching kit

- `student_notebooks/`: generated by `tools/make_student_version.py` (solutions removed).
- `slides/`: 8–12 slides per track, drawn from the notebooks' figures and equations.
- `video_scripts/`: one 10–15 minute walkthrough script per track.
"""


# --------------------------------------------------------------------------- #
# Writers
# --------------------------------------------------------------------------- #
created: list[str] = []


def write(rel: str, content: str) -> None:
    path = ROOT / rel
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    created.append(rel)


def write_json(rel: str, obj: dict) -> None:
    write(rel, json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def scaffold_paper(p) -> None:
    f = paper_fields(p)
    write_json(f"{f['FOLDER']}/notebook.ipynb", build_notebook(f))
    write(f"{f['FOLDER']}/README.md", fill(PAPER_README, f))
    write(f"{f['FOLDER']}/results/.gitkeep", "")


def scaffold_all() -> None:
    write("README.md", root_readme())
    write(".gitignore", GITIGNORE)
    write("requirements.txt", REQUIREMENTS)
    write("LICENSE", LICENSE_MIT)
    write("LICENSE-docs", LICENSE_DOCS)
    write("mkdocs.yml", mkdocs_yml())
    write("common/__init__.py", COMMON_INIT)
    write("common/env.py", COMMON_ENV)
    write("common/results.py", COMMON_RESULTS)
    write("common/plotting.py", COMMON_PLOTTING)
    write("tools/make_student_version.py", MAKE_STUDENT)
    write_json("templates/paper_template.ipynb", build_notebook(None))
    write("docs/index.md", DOCS_INDEX)
    for track, (letter, name, doc) in TRACKS.items():
        ps = [paper_fields(p) for p in PAPERS if p[8] == track]
        paper_list = "\n".join(
            f"- **{f['NUM']} · {f['SHORT']}** ({f['YEAR']}): *{f['TITLE']}*. {f['DEPTH']}. "
            f"[Code](https://github.com/{GITHUB_USER}/top30-papers/tree/main/{f['FOLDER']})"
            for f in ps
        )
        result_rows = "\n".join(f"| {f['SHORT']} | | | | |" for f in ps)
        write(f"docs/tracks/{doc}", TRACK_DOC.format(letter=letter, name=name,
                                                      paper_list=paper_list, result_rows=result_rows))
    write("huggingface/README.md", HF_README)
    write("huggingface/model_card_template.md", MODEL_CARD)
    write("huggingface/model_cards/.gitkeep", "")
    write("huggingface/spaces/.gitkeep", "")
    write("teaching/README.md", TEACHING_README)
    for d in ["student_notebooks", "slides", "video_scripts"]:
        write(f"teaching/{d}/.gitkeep", "")
    for p in PAPERS:
        scaffold_paper(p)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    add = sub.add_parser("add", help="add one extra paper folder from the template")
    for name in ["num", "slug", "track", "short", "title", "authors", "year", "venue", "link"]:
        add.add_argument(f"--{name}", required=True, type=int if name == "num" else str)
    add.add_argument("--depth", default="Standard")
    args = ap.parse_args()

    if args.cmd == "add":
        if args.track not in TRACKS:
            ap.error(f"--track must be one of {list(TRACKS)}")
        scaffold_paper((args.num, args.slug, args.short, args.title, args.authors, args.year,
                        args.venue, args.link, args.track, args.depth))
    else:
        scaffold_all()
    print(f"Created {len(created)} file(s).")
    for c in created:
        print("  +", c)


if __name__ == "__main__":
    main()
