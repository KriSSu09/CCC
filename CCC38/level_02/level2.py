import numpy as np
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential, load_model as keras_load_model
from tensorflow.keras.layers import Conv2D, GlobalAveragePooling2D, Flatten, Dense, Dropout, BatchNormalization


def load_images_from_folder(folder_path, labels_file=None):
    images = []
    labels = []

    if labels_file:
        with open(labels_file, 'r') as f:
            labels = [int(line.strip()) for line in f.readlines()]

    num_images = len(labels) if labels_file else len(os.listdir(folder_path))

    for i in range(num_images):
        img_path = os.path.join(folder_path, f"field{i:03d}.png")
        img = image.load_img(img_path, target_size=(200, 200))
        img_array = image.img_to_array(img)
        images.append(img_array)

    return (np.array(images), np.array(labels)) if labels_file else np.array(images)


def create_model(path=None):
    if path and os.path.exists(path):
        return load_model(path)

    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(200, 200, 3))

    for layer in base_model.layers:
        layer.trainable = False

    model = Sequential()
    model.add(base_model)
    model.add(GlobalAveragePooling2D())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(6, activation='softmax'))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


def load_model(path):
    return keras_load_model(path)


def train_model(train_images, train_labels):
    model = create_model('model.keras')
    model.fit(train_images, train_labels, epochs=10)
    return model


def write_predictions(model, test_images):
    predictions = model.predict(test_images)
    predicted_counts = np.argmax(predictions, axis=1)

    with open('predictions.txt', 'w') as f:
        for count in predicted_counts:
            f.write(str(count) + '\n')


if __name__ == '__main__':
    train_images, train_labels = load_images_from_folder('train_data', 'train_data_labels.csv')
    model = train_model(train_images, train_labels)
    model.save('model.keras')
    test_images = load_images_from_folder('test_data')
    write_predictions(model, test_images)
