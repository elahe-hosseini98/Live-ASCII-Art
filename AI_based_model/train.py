from data.dataset_loader import DataLoader
from config import BATCH_SIZE, EPOCHS, saved_model_path, ASCII_CHARS, target_dataset_input_size
import os
from AI_based_model.model import build_cnn_model
from tensorflow.keras.callbacks import ModelCheckpoint


def train():
    
    dataset_loader = DataLoader()

    train_dataset = dataset_loader.create_tf_dataset(batch_size=BATCH_SIZE, is_training=True)
    val_dataset = dataset_loader.create_tf_dataset(batch_size=BATCH_SIZE, is_training=False)
        
    steps_per_epoch = len(dataset_loader.img_train) // BATCH_SIZE
    validation_steps = len(dataset_loader.img_val) // BATCH_SIZE

    ascii_height, ascii_width = target_dataset_input_size
    num_classes = len(ASCII_CHARS)
    
    cnn_model = build_cnn_model(ascii_height, ascii_width, num_classes)

    cnn_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    checkpoint = ModelCheckpoint(filepath=os.path.join(saved_model_path, 'best_performing_model.h5'),
                                 monitor='val_loss', save_best_only=True, verbose=1)
    

    history = cnn_model.fit(
        train_dataset, 
        epochs=EPOCHS, 
        steps_per_epoch=steps_per_epoch,
        validation_data=val_dataset, 
        validation_steps=validation_steps,
        callbacks=[checkpoint]
    )

    cnn_model.save(os.path.join(saved_model_path, 'cnn_model_final.h5'))