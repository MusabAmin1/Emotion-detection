# 😊 Emotion AI

> An NLP-based emotion classification project that predicts the emotion expressed in a piece of text using **TF-IDF** and a **Tuned Random Forest** classifier.

---

## 🚀 Overview

**Emotion AI** is a Natural Language Processing (NLP) project designed to classify text into one of six emotions.

The project compares multiple machine learning algorithms using both **Bag of Words** and **TF-IDF** representations. The final model uses **TF-IDF + a tuned Random Forest classifier** and is deployed through a **Streamlit web application**.

---

## ✨ Features

- 🎯 Classifies text into **6 different emotions**
- 📊 Displays prediction confidence
- 📈 Shows probability distribution for all emotion classes
- 🎨 Page theme changes according to the predicted emotion
- 📱 Responsive design for desktop and mobile
- 🌐 Interactive Streamlit interface

---

## 😊 Supported Emotions

| Label | Emotion |
|:---:|---|
| 0 | Sadness 😢 |
| 1 | Anger 😡 |
| 2 | Love ❤️ |
| 3 | Surprise 😮 |
| 4 | Fear 😨 |
| 5 | Joy 😊 |

---

## ⚙️ How It Works

### 1. 🧹 Text Preprocessing

The text goes through several preprocessing steps:

- Convert text to lowercase
- Remove punctuation
- Remove numbers
- Remove emojis and non-ASCII characters
- Remove English stopwords
- Preserve negation words such as `not`, `no`, and `never`

Keeping negation words helps preserve the meaning of sentences where negation changes the emotion.

### 2. 🔤 Feature Extraction

Two text representations were compared:

- **Bag of Words** using `CountVectorizer`
- **TF-IDF** using `TfidfVectorizer`

TF-IDF was selected for the final model.

### 3. 🤖 Model Building

Multiple machine learning classifiers were trained and compared:

- Logistic Regression
- K-Nearest Neighbors
- Support Vector Machine
- Multinomial Naive Bayes
- Decision Tree
- Random Forest
- XGBoost

### 4. 🎛️ Hyperparameter Tuning

The Random Forest classifier was optimized using `RandomizedSearchCV` with **3-fold cross-validation**.

The following hyperparameters were explored:

- `n_estimators`
- `max_depth`
- `min_samples_split`
- `min_samples_leaf`
- `max_features`

---

## 📊 Results

### Final Model

**TF-IDF + Tuned Random Forest**

| Metric | Score |
|---|---:|
| Testing Accuracy | **88.75%** |
| Training Accuracy | **92.66%** |
| Train-Test Split | **80/20** |

The final model was selected after comparing multiple machine learning approaches and applying hyperparameter tuning to Random Forest.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| 🐍 Python | Programming language |
| 🧠 Scikit-learn | Machine learning |
| 🐼 Pandas | Data manipulation |
| 🔢 NumPy | Numerical operations |
| 📝 NLTK | Text preprocessing |
| 🚀 XGBoost | Model comparison |
| 📊 Matplotlib | Visualization |
| 📈 Seaborn | Visualization |
| 💾 Joblib | Model serialization |
| 🌐 Streamlit | Web application |
