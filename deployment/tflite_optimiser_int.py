import tensorflow as tf
import pathlib

data_dir = pathlib.Path("/Users/daniel/Documents/CNN Training/real_data/augmented_real_line/test/")

batch_size = 64
img_h = 224
img_w = 224
epochs = 1000
history = None


#split data into train test (not validation) 0.2
train_ds = tf.keras.utils.image_dataset_from_directory(
	data_dir,
	seed = 123,
	image_size=(img_h, img_w),
	batch_size=batch_size,
	label_mode='categorical',
    subset="training",
    validation_split=0.2)

model = tf.keras.models.load_model('/Users/daniel/Documents/aiPrint-Publishable/aiPrint-Data-Creation/cnn-training/results-transfer/MobileNetV3Small_line.h5')
def representative_data_gen():
  for image_batch, labels_batch in train_ds.take(3):
    yield [image_batch]

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen
# Ensure that if any ops can't be quantized, the converter throws an error
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
# Set the input and output tensors to uint8 (APIs added in r2.3)
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8

tflite_model_quant = converter.convert()


tflite_models_dir = pathlib.Path("./")
tflite_models_dir.mkdir(exist_ok=True, parents=True)

# Save the quantized model:
tflite_model_quant_file = tflite_models_dir/"MobileTransfer_line_quant.tflite"
tflite_model_quant_file.write_bytes(tflite_model_quant)
