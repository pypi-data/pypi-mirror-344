![Logo de Synapse.AI](https://github.com/LScelza/Libreria/blob/main/Logo.png)


# `synapse_ai` 

`synapse_ai` is a Python package designed for artificial intelligence development, offering utilities for machine learning (ML), deep learning (DL), data processing, and model deployment. It provides a comprehensive set of tools for AI developers to efficiently create and deploy AI models.

## Features

- **Machine Learning**: Utilities to facilitate the development and training of machine learning models.
- **Deep Learning**: Tools and models specific to deep learning to accelerate AI development.
- **Data Processing**: A set of utilities to preprocess and transform datasets for model training.
- **Model Deployment**: Tools for easy deployment of AI models, including model evaluation and optimization.
- **Modular Design**: The package is designed with modular components, so you can use only what you need.

## Modules and Functions


### **Module `phonemes`**

1. **`phoneme`**: Transforms Spanish text into a simplified phonetic representation based on predefined rules.

2. **`accent`**: Applies prosodic accentuation to Spanish text based on predefined phonetic and grammatical rules.

3. **`dictionaries`**: Generates two dictionaries from the input text: a phoneme-to-index dictionary and a phoneme frequency dictionary.

4. **`phoneme_graphs`**: Visualizes the frequency of phonemes in a bar chart.


### **Module `mel_spectrograms`**

1. **`load_audio_to_mel`**: Converts an audio file to a mel spectrogram.

2. **`graph_mel_spectrogram`**: Visualizes and optionally saves a mel spectrogram as an image.


### **Module `eda`**

1. **`heatmap_correlation`**: Generates and optionally saves a heatmap of correlation values for selected columns in a DataFrame.

2. **`outliers`**: Analyzes numerical outliers in a specified column of a DataFrame, visualizing its distribution, boxplot, and basic statistics.

3. **`nulls`**: Analyzes and prints the number and percentage of null values in a specified column of a DataFrame.

4. **`pca`**: This function performs Principal Component Analysis (PCA) on a DataFrame to reduce its dimensionality and, optionally, visualize the results. It works in both 2D and 3D modes and can include the target variable in the output and visualization if desired. The function scales features when a scaler is provided and enforces the use of 2 or 3 dimensions, raising errors for invalid inputs.

*Use Cases*:
- **Feature Exploration**: To uncover the underlying structure in high-dimensional data.
- **Visualization**: To generate 2D or 3D scatter plots that reveal patterns, clusters, or trends in the data.
- **Target Analysis**: Optionally include the target variable in the PCA output to analyze its distribution relative to the principal components.


### Class: ModelConfigurator

**`ModelConfigurator`**: A GUI-based tool that provides a step-by-step wizard for configuring deep learning models using Keras. This class allows users to:
- Define the input shape.
- Add various types of layers (e.g., Dense, Conv1D, Conv2D, pooling layers, Dropout, LSTM, Bidirectional LSTM, Flatten, BatchNormalization).
- Configure optimizers, loss functions, and evaluation metrics.
- Optionally save the final model along with an architecture diagram and summary.

**Important**: Due to potential version compatibility issues with TensorFlow, NumPy, and other dependencies, it is strongly recommended to work within a virtual environment. For example, you can create and activate a virtual environment as follows:

```bash
python -m venv myenv
# On Windows:
myenv\Scripts\activate
# On Unix or macOS:
source myenv/bin/activate

After activating the environment, install the required dependencies (e.g., Python, TensorFlow, NumPy) within it.
```

## Installation

To install the package, you can use `pip`:

```bash
pip install synapse_ai_tools
