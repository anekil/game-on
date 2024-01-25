import json

from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

print('Fetching...')

with open('/mnt/c/Users/agata/Documents/quest-finder/backend/website/recommendation/training_data_pairs_shuffled.json', 'r') as f:
    loaded_data = json.load(f)

print('Loaded')


def extract_features_and_labels(data):
    features_anchor = [entry['anchor']['features'] for entry in data]
    features_game = [entry['game']['features'] for entry in data]
    labels = [entry['label'] for entry in data]
    return (features_anchor, features_game, labels)


features_anchor, features_game, labels = extract_features_and_labels(loaded_data)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(features_anchor + features_game)
vocab_size = len(tokenizer.word_index) + 1
max_sequence_length = max(
    max(len(seq) for seq in features_anchor),
    max(len(seq) for seq in features_game),
)

print('1')

def tokenize_and_pad(sequences):
    tokenized_sequences = tokenizer.texts_to_sequences(sequences)
    padded_sequences = pad_sequences(tokenized_sequences, maxlen=max_sequence_length, padding='post')
    return padded_sequences


features_anchor = tokenize_and_pad(features_anchor)
features_game = tokenize_and_pad(features_game)

print('2')

train_anchor, temp_anchor, train_game, temp_game, train_labels, temp_labels = train_test_split(
    features_anchor,
    features_game,
    labels,
    test_size=0.8, random_state=42)
val_anchor, test_anchor, val_game, test_game, val_labels, test_labels = train_test_split(
    temp_anchor,
    temp_game,
    temp_labels,
    test_size=0.5, random_state=42)

print('Data ready')


def build_siamese_network(input_shape, vocab_size):
    model = models.Sequential()
    model.add(layers.Embedding(input_dim=vocab_size, output_dim=128, input_length=input_shape))
    model.add(layers.LSTM(64))
    model.add(layers.Dense(32, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(16, activation='relu'))
    return model


# Define the input shapes
input_shape = max_sequence_length

# Create the Siamese network
anchor_input = tf.keras.Input(shape=(input_shape,), name='anchor')
game_input = tf.keras.Input(shape=(input_shape,), name='game')

siamese_network = build_siamese_network(input_shape, vocab_size)

# Generate the encodings (feature vectors) for the anchor and game
encoded_anchor = siamese_network(anchor_input)
encoded_game = siamese_network(game_input)

# Calculate the similarity between the anchor and game
similarity = layers.Dot(axes=1, normalize=True)([encoded_anchor, encoded_game])

# Create the Siamese model
siamese_model = tf.keras.Model(inputs=[anchor_input, game_input], outputs=similarity)

# Compile the Siamese model with binary crossentropy loss
# custom_adam = Adam(learning_rate=0.001)
siamese_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Print the model summary
print(siamese_model.summary())

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# Train the Siamese model with your padded_sequences_anchor, padded_sequences_game, and labels
siamese_model.fit(
    [train_anchor, train_game],
    np.array(train_labels),
    epochs=10,
    batch_size=128,
    # validation_split=0.2,
    use_multiprocessing=True,
    workers=10,
    validation_data=([val_anchor, val_game], np.array(val_labels))
)

siamese_model.save('siamese_model.keras')

# Evaluate the model on the test set
test_loss, test_accuracy = siamese_model.evaluate(
    (test_anchor, test_game),
    np.array(test_labels),
)
print(f'Test Loss: {test_loss:.4f}, Test Accuracy: {test_accuracy * 100:.2f}%')
