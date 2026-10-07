# Week 3 - Task 3.1: TensorFlow/Keras Model

Skill Set Go EduTech — AI/ML Internship (Offer ID: SSG/AIML/B1/0291)

## Objective
Build and train a TensorFlow/Keras neural network and compare it with the earlier PyTorch model (Week 3 Task 3.1).

## Setup
Both frameworks get identical conditions: same Titanic dataset and preprocessing, same split, same architecture (9 → 16 → 8 → 1), Adam (lr=0.01), batch size 32, 50 epochs, seed 42.

## Results
| Metric | PyTorch | TensorFlow/Keras |
|---|---|---|
| Test accuracy | 0.8101 | 0.7765 |
| Final train loss | 0.3500 | 0.3179 |
| Training time | 3.06 s | 5.70 s |
| Trainable parameters | 305 | 305 |

The 3.4-point accuracy gap comes from a single run/seed on 179 test rows, so it is within normal noise and is not evidence that either framework is better. The notebook's comparison notes also cover API/developer-experience differences (training loop, metrics, saving).

## Note on running both frameworks
Importing TensorFlow before training the PyTorch model crashed the Python kernel (native thread-pool clash) in the build environment, so the notebook trains PyTorch first and imports TensorFlow afterwards. Keep that order.

## Tools
Python, TensorFlow/Keras, PyTorch, scikit-learn, Pandas, Matplotlib.

## Setup
```bash
pip install tensorflow torch pandas numpy scikit-learn matplotlib jupyter
jupyter notebook 3.1_tensorflow_keras.ipynb
```

## Files
- `3.1_tensorflow_keras.ipynb` — full notebook
- `data/titanic_cleaned.csv` — dataset (from Task 1.2)
- `framework_comparison.csv` — comparison table
- `pytorch_vs_keras_loss.png` — training loss curves for both
- `titanic_keras_model.keras` — saved Keras model

## Next improvements
- Repeat both runs over several random seeds and report mean ± std before drawing any conclusion about accuracy.
