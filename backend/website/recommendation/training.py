import json
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

print('Fetching...')

with open('/home/aneta/Documents/quest-finder/backend/website/recommendation/training_data_pairs_shuffled.json', 'r') as f:
    loaded_data = json.load(f)

print('Loaded')
label_list = []
anchor_list = []
game_list = []

for entry in loaded_data:
    label_list.append(entry['label'])
    anchor_list.append(f"{entry['anchor']['features']}")
    game_list.append(f"{entry['game']['features']}")

from sklearn.model_selection import train_test_split

train_anchor, temp_anchor, train_game, temp_game, train_labels, temp_labels = train_test_split(
    anchor_list,
    game_list,
    label_list,
    test_size=0.8, random_state=42)
val_anchor, test_anchor, val_game, test_game, val_labels, test_labels = train_test_split(
    temp_anchor,
    temp_game,
    temp_labels,
    test_size=0.5, random_state=42)

MAX_LENGTH = max([len(d) for d in anchor_list + game_list])
print(MAX_LENGTH)
NUM_CLASSES = 1
MAX_TOKENS = 10000

anchor_input = tf.keras.Input(shape=(1,), name='anchor', dtype=tf.string)
game_input = tf.keras.Input(shape=(1,), name='game', dtype=tf.string)

vectorize_layer = layers.TextVectorization(max_tokens=MAX_TOKENS, output_mode='int')
vectorize_layer.adapt(anchor_list)
A_vectorized = vectorize_layer(anchor_input)
B_vectorized = vectorize_layer(game_input)

embedding_layer = layers.Embedding(input_dim=MAX_TOKENS, output_dim=128)
A_embedded = embedding_layer(A_vectorized)
B_embedded = embedding_layer(B_vectorized)

shared_lstm = layers.LSTM(64)
A_lstm = shared_lstm(A_embedded)
B_lstm = shared_lstm(B_embedded)

dense1 = layers.Dense(
    units=64,
    activation='relu')
A_dense = dense1(A_lstm)
B_dense = dense1(B_lstm)

dropout = layers.Dropout(0.5)
A_drop = dropout(A_dense)
B_drop = dropout(B_dense)

dense2 = layers.Dense(
    units=16,
    activation='relu')
A_output = dense2(A_drop)
B_output = dense2(B_drop)

merged = layers.concatenate(
    [A_output, B_output],
    axis=-1)

dense3 = layers.Dense(
    units=NUM_CLASSES,
    activation='sigmoid')

predictions = dense3(merged)

siamese_model = models.Model(inputs=[anchor_input, game_input],
                                  outputs=predictions,
                                  name='siamese_model')

#custom_adam = Adam(learning_rate=0.01)
siamese_model.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

siamese_model.summary()

history = siamese_model.fit(
    [np.array(train_anchor), np.array(train_game)],
    np.array(train_labels),
    epochs=15,
    batch_size=64,
    use_multiprocessing=True,
    workers=10,
    shuffle=True,
    validation_data=([np.array(val_anchor), np.array(val_game)], np.array(val_labels))
)

siamese_model.save('siamese_model_v4.keras')

from matplotlib import pyplot as plt

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

test_loss, test_accuracy = siamese_model.evaluate(
    (np.array(test_anchor), np.array(test_game)),
    np.array(test_labels),
)
print(f'Test Loss: {test_loss:.4f}, Test Accuracy: {test_accuracy * 100:.2f}%')
