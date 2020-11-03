# %%
import numpy
from keras import models
from keras import layers


with open("matches.out", 'r') as data, open("labels.out", 'r') as labels:
    data = data.read().splitlines()
    fmtD = []
    for x in range(len(data)):
        temp = eval(data[x])
        fmtD.append(temp)
    labels = labels.read().splitlines()
    for x in range(len(labels)):
        labels[x] = float(labels[x])

# %%
numpy.random.seed(0)


def shuffle_in_unison_scary(a, b):
    rng_state = numpy.random.get_state()
    numpy.random.shuffle(a)
    numpy.random.set_state(rng_state)
    numpy.random.shuffle(b)


# %%

shuffle_in_unison_scary(fmtD, labels)

# %%
train_data = fmtD[:20352]
test_data = fmtD[20352:len(fmtD)]

# %%


def vectorize_sequences(sequences, dimension=60):
    results = numpy.zeros((len(sequences), dimension))
    for i in range(len(sequences)):
        for j in range(4, 34):
            results[i, j - 4] = sequences[i][j]
        for j in range(38, 68):
            results[i, j - 8] = sequences[i][j]
    return results


#         results[i, sequence] = .
#     return results
x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)

# %%
train_labels = labels[:20352]
test_labels = labels[20352:len(labels)]

y_train = numpy.asarray(train_labels).astype('float32')
y_test = numpy.asarray(test_labels).astype('float32')

# %%
mean = x_train.mean(axis=0)
x_train -= mean
std = x_train.std(axis=0)
x_train /= std
x_test -= mean
x_test /= std

# %%


def build_model():
    model = models.Sequential()
    model.add(layers.Dense(64, activation='relu', input_shape=(60, )))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1, activation="sigmoid"))
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    return model


# %%
model = build_model()
history = model.fit(
    x_train,
    y_train,
    epochs=20,
    batch_size=512,
)

# %%
model.predict(x_test)

# %%
for y in y_test:
    print(y)

# %%
model.save("model.hdf5")

# %%
