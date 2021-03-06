from datasets import DataManager
from datasets import split_data
from preprocess import preprocess_input
from keras.callbacks import CSVLogger, ModelCheckpoint, EarlyStopping
from keras.callbacks import ReduceLROnPlateau
from keras.preprocessing.image import ImageDataGenerator
from cnn1 import mini_XCEPTION
from keras.layers import InputLayer, MaxPooling2D, Flatten, Dense, Conv2D
from keras.models import Model
import keras
from keras.models import Sequential

validation_split = .2
input_shape = (64, 64, 1)
batch_size = 32  #in each iteration, we consider 32 training examples at once
num_epochs = 90   # we iterate 90 times over the entire training set
verbose = 1
num_classes = 7
patience = 50
base_path = '/home/akanksha/code/trained_models/emotion_models'

# data generator
data_generator = ImageDataGenerator(
                        featurewise_center=False,
                        featurewise_std_normalization=False,
                        rotation_range=10,
                        width_shift_range=0.1,
                        height_shift_range=0.1,
                        zoom_range=.1,
                        horizontal_flip=True
			)

# model parameters/compilation

model = mini_network(input_shape, num_classes)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

dataset_name = 'fer2013'
print('Training Dataset: ', dataset_name)

#callbacks
log_base_path = base_path + dataset_name + '_emotion_training.log'
csv_logger = CSVLogger(log_base_path, append=False)
early_stop = EarlyStopping('val_loss', patience=patience)
reduce_lr = ReduceLROnPlateau('val_loss', factor=0.1, patience=int(patience/4), verbose=1)
trained_models_path = base_path + dataset_name + '_mini_XCEPTION'
model_names = trained_models_path + '.{epoch:02d}-{val_acc:.2f}.hdf5'
model_checkpoint = ModelCheckpoint(model_names, 'val_loss', verbose=1, save_best_only=True)
callbacks = [model_checkpoint, csv_logger, early_stop, reduce_lr]


# loading dataset
data_loader = DataManager(dataset_name, image_size=input_shape[:2])
faces, emotions = data_loader.get_data()
faces = preprocess_input(faces)
num_samples, num_classes = emotions.shape
train_data, val_data = split_data(faces, emotions, validation_split)
train_faces, train_emotions = train_data
model.fit_generator(data_generator.flow(train_faces, train_emotions,
                                            batch_size),
                        steps_per_epoch=len(train_faces) / batch_size,
                        epochs=num_epochs, verbose=1, callbacks=callbacks,
                        validation_data=val_data)
