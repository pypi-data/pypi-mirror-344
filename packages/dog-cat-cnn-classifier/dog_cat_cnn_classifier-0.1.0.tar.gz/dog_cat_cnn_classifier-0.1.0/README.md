# Dog-Cat Classifier

A deep learning-based image classification project that distinguishes between dogs and cats using a VGG16-based CNN architecture.

## Project Overview

This project implements an end-to-end deep learning solution for binary classification of dog and cat images. It uses a transfer learning approach with VGG16 as the base model, fine-tuned for the specific task of dog-cat classification.

## Features

- Transfer learning using VGG16 pre-trained model
- Data augmentation for improved model robustness
- Binary classification with softmax activation
- Comprehensive logging system
- Modular pipeline architecture
- Model evaluation and metrics tracking

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nishantbadhautiya100/dog-cat-classifier.git
cd dog-cat-classifier
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Prepare your dataset:
   - Place your dog and cat images in the appropriate directories
   - The structure should be:
     ```
     training_data/
     ├── dogs/
     └── cats/
     ```

2. Run the training pipeline:
```bash
python main.py
```

The pipeline will:
- Prepare the base model (VGG16)
- Train the model on your dataset
- Evaluate the model performance
- Save the trained model

## Model Architecture

- Base Model: VGG16 (pre-trained on ImageNet)
- Transfer Learning: Fine-tuning approach
- Output Layer: Dense layer with softmax activation
- Loss Function: Categorical Crossentropy
- Optimizer: Adam

## Configuration

The project can be configured through:
- `params.yaml`: Model parameters and training settings
- `config/config.yaml`: Pipeline configuration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- VGG16 model architecture
- TensorFlow and Keras
- ImageNet dataset for pre-training 
