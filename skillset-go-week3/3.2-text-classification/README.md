# Week 3 - Task 3.2: Text Classification Project (TensorFlow)

Skill Set Go EduTech — AI/ML Internship (Offer ID: SSG/AIML/B1/0291)

## Problem
Classify SMS messages as spam or legitimate ("ham").

## Dataset
SMS Spam Collection: 5,574 real text messages (4,827 ham / 747 spam), loaded from `data/sms.tsv` (tab-separated: label, message). The class imbalance (13% spam) means accuracy alone is misleading, so evaluation focuses on spam-class precision, recall and F1.

## Method
- Stratified 80/20 train/test split (test set untouched during training)
- TensorFlow/Keras model with the vectorizer inside it (raw text in): `TextVectorization → Embedding(32) → GlobalAveragePooling → Dense(16) → Dropout(0.3) → Dense(1, sigmoid)`
- Class weights to offset the imbalance; early stopping on a validation split
- Compared against a TF-IDF + Logistic Regression baseline

## Results (held-out test set, 1,115 messages)
| Model | Accuracy | Spam precision | Spam recall | Spam F1 |
|---|---|---|---|---|
| TF-IDF + LogReg (baseline) | 0.9839 | 0.9517 | 0.9262 | 0.9388 |
| TensorFlow text classifier | 0.9857 | 0.9716 | 0.9195 | 0.9448 |

The TensorFlow model caught 137 of 149 spam messages and falsely flagged 4 legitimate ones. It is roughly on par with the baseline (a difference of a few messages on a single split), not clearly better. The notebook includes an error analysis of missed spam and false alarms.

## Limitations
Single split/seed, no cross-validation; older SMS corpus so modern spam patterns may be under-represented; no hyperparameter tuning.

## Tools
Python, TensorFlow/Keras, scikit-learn, Pandas, Matplotlib.

## Setup
```bash
pip install tensorflow scikit-learn pandas numpy matplotlib jupyter
jupyter notebook 3.2_text_classification.ipynb
```

## Files
- `3.2_text_classification.ipynb` — full notebook
- `data/sms.tsv` — dataset (SMS Spam Collection, from the public `justmarkham/pycon-2016-tutorial` repository on GitHub)
- `spam_classifier.keras` — trained model (accepts raw strings)
- `model_comparison.csv`, `text_training_curves.png`, `text_confusion_matrix.png` — results

## Next improvements
Cross-validation, a pretrained text encoder, and threshold tuning to trade off missed spam vs. false alarms.
