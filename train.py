import os
import tensorflow as tf
assert tf.__version__.startswith('2')

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



#Adathalmaz beállításai
data = gesture_recognizer.Dataset.from_folder(
    dirname=dataset_path,
    hparams=gesture_recognizer.HandDataPreprocessingParams(),
)
train_data, rest_data = data.split(0.8)
validation_data, test_data = rest_data.split(0.8)

#Hiperparaméterek
hparams = gesture_recognizer.HParams(batch_size=2, epochs=10, shuffle= True ,export_dir="exported_model")
options = gesture_recognizer.GestureRecognizerOptions(hparams=hparams)

#Model létrehozása
model = gesture_recognizer.GestureRecognizer.create(
    train_data=train_data,
    validation_data=validation_data,
    options=options
)

#Model kiértékelése
loss, acc = model.evaluate(test_data, batch_size=1)
print(f"Test loss: {loss}, Test accuracy: {acc}")

#Model mentése
model.export_model()