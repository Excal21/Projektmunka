#from google.colab import files
import os
import tensorflow as tf
#assert tf.__version__.startswith('2')

import matplotlib.pyplot as plt
from mediapipe_model_maker import gesture_recognizer

# Reset TensorFlow environment
tf.keras.backend.clear_session()

assert tf.__version__.startswith('2')

dataset_path = "Samples"

print(dataset_path)
labels = []
for i in os.listdir(dataset_path):
    if os.path.isdir(os.path.join(dataset_path, i)):
        labels.append(i)
print(labels)

NUM_EXAMPLES = 5

for label in labels:
    label_dir = os.path.join(dataset_path, label)
    example_filenames = os.listdir(label_dir)[:NUM_EXAMPLES]
    fig, axs = plt.subplots(1, NUM_EXAMPLES, figsize=(10, 2))
    for i in range(NUM_EXAMPLES):
        axs[i].imshow(plt.imread(os.path.join(label_dir, example_filenames[i])))
        axs[i].get_xaxis().set_visible(False)
        axs[i].get_yaxis().set_visible(False)
    fig.suptitle(f'Showing {NUM_EXAMPLES} examples for {label}')

plt.show()

# Load dataset
data = gesture_recognizer.Dataset.from_folder(
    dirname=dataset_path,
    hparams=gesture_recognizer.HandDataPreprocessingParams(),
)
train_data, rest_data = data.split(0.8)
validation_data, test_data = rest_data.split(0.7)

# Set hyperparameters and options
hparams = gesture_recognizer.HParams(epochs=7 ,export_dir="exported_model")
options = gesture_recognizer.GestureRecognizerOptions(hparams=hparams)

# Create and train model
model = gesture_recognizer.GestureRecognizer.create(
    train_data=train_data,
    validation_data=validation_data,
    options=options
)

# Evaluate model
loss, acc = model.evaluate(test_data, batch_size=1)
print(f"Test loss: {loss}, Test accuracy: {acc}")

# Export model
model.export_model()