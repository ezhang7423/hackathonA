from flask import Flask
from flask import request
from keras import models
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
    rjson = request.get_json()
    uid = rjson['u']
    predictionArr = rjson['o']
    model = models.load_model('model.hdf5')
    fP = []
    for x in range(len(predictionArr)):
        fP.append(transformData(sConcat(uid, predictionArr[x])))
    fP = np.asarray(fP).astype('float32')
    rankedL = model.predict(fP)
    returnD = {}
    for x in range(len(rankedL)):
        returnD[predictionArr[x]] = rankedL[x]
    returnD = {k: v for k, v in sorted(
        returnD.items(), key=lambda item: item[1])}
    return returnD


if __name__ == "__main__":
    app.run()
