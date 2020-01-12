from flask import Flask
from flask import request
import keras
import json
import numpy as np

app = Flask(__name__)


def transformData(array):
    x_train = np.asarray(array).astype('float32')
    mean = x_train.mean(axis=0)
    x_train -= mean
    std = x_train.std(axis=0)
    x_train /= std
    return x_train


def sConcat(arr1, arr2):
    return arr1[4:] + arr2[4:]


@app.route("/cnnapi", methods=["POST"])
# need user vectors of users and filter list
# returns sorted list of user vectors
def cnnapi():
    print('received request')
    rjson = request.get_json()
    uid = rjson['u']
    predictionArr = rjson['o']
    print(uid, predictionArr)
    print('starting prediction')
    print(len(predictionArr[0]))
    model = keras.models.load_model('model.hdf5')
    fP = []
    for x in range(len(predictionArr)):
        fP.append(transformData(sConcat(uid, predictionArr[x])))
    fP = np.asarray(fP).astype('float32')
    rankedL = model.predict(fP)
    print(rankedL)
    rankedD = []
    for x in range(len(rankedL)):
        rankedD.append(rankedL[x][0])
    keras.backend.clear_session()
    return json.dumps(np.argsort(rankedD)[::-1].tolist())


if __name__ == "__main__":
    app.run()


# curl -v -d '{"u": [0, 0, 0, 1, 3.21, 4.79, 6.1, 7.44, 4.61, 0.45, 0.55, 10, 7.29, 0.58, 0.68, 10, 3.17, 5.4, 7.86, 7.56, 4.86, 3.26, 2.2, 5.49, 9.63, 9.1, 0.0, 2.79, 9.91, 6.66, 0.0, 8.66, 2.66, 2.07], "o": [[0, 0, 0, 1, 3.33, 5.17, 7.9, 10, 5.02, 0.29, 0.36, 7.99, 7.39, 0.57, 0.48, 6.57, 2.39, 5.01, 8.88, 3.96, 4.75, 2.25, 0.0, 6.01, 7.69, 10, 1.85, 3.15, 9.91, 9.7, 3.26, 5.72, 4.85, 1.21], [0, 0, 1, 0, 0.34, 7.86, 1.71, 0.4, 4.39, 4.9, 0.52, 4.36, 1.8, 7.44, 5.45, 5.2, 10, 2.71, 4.01, 8.84, 1.3, 7.48, 10, 6.9, 7.11, 9.65, 7.34, 8.82, 2.99, 7.12, 5.48, 0.0, 6.7, 4.29]]}' -H "Content-Type: application/json" localhost:5000/cnnapi
