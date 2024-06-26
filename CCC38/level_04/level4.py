import numpy as np
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.models import Sequential, load_model as keras_load_model
from tensorflow.keras.layers import Conv2D, GlobalAveragePooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import RMSprop
from sklearn.model_selection import KFold


def merge_images(img1, img2):
    mask = np.all(img1 == [255, 255, 255], axis=-1)
    img1[mask] = img2[mask]
    return img1


def load_and_merge_images_from_folder(folder_path, labels_file=None):
    images = []
    labels = []

    if labels_file:
        with open(labels_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                x, y = map(int, line.strip().split(","))
                labels.append([x, y])

    num_images = len(labels) if labels_file else len(os.listdir(folder_path)) // 2

    for i in range(num_images):
        img_path1 = os.path.join(folder_path, f"field{i:03d}_sample0.png")
        img_path2 = os.path.join(folder_path, f"field{i:03d}_sample1.png")

        img1 = image.load_img(img_path1, target_size=(200, 200))
        img2 = image.load_img(img_path2, target_size=(200, 200))

        img1_array = image.img_to_array(img1)
        img2_array = image.img_to_array(img2)

        merged_img = merge_images(img1_array, img2_array)
        images.append(merged_img)

    return (np.array(images), np.array(labels)) if labels_file else np.array(images)


def create_model(path=None):
    if path and os.path.exists(path):
        return load_model(path)

    base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(200, 200, 3))

    for layer in base_model.layers[:-20]:
        layer.trainable = False

    model = Sequential()
    model.add(base_model)
    model.add(GlobalAveragePooling2D())
    model.add(BatchNormalization())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(2))

    optimizer = RMSprop(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss='mean_squared_error')
    return model


def load_model(path):
    return keras_load_model(path)


def train_model(train_images, train_labels):
    model = create_model('model.keras');

    early_stopping = EarlyStopping(monitor='loss', patience=15, verbose=1)
    reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.2, patience=5, verbose=1, min_delta=0.0001)

    model.fit(train_images, train_labels,
              epochs=40,
              callbacks=[early_stopping, reduce_lr])

    return model


def write_predictions(model, test_images):
    predictions = model.predict(test_images)
    with open('predictions.txt', 'w') as f:
        for x, y in predictions:
            f.write(f"{int(x)},{int(y)}\n")


if __name__ == '__main__':
    train_images, train_labels = load_and_merge_images_from_folder('train_data', 'train_data_labels.csv')

    best_model = train_model(train_images, train_labels)
    best_model.save('model.keras')

    test_images = load_and_merge_images_from_folder('test_data')
    write_predictions(best_model, test_images)
