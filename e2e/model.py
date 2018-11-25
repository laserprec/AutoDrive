import h5py
import cv2
from keras.models import load_model
from keras import __version__ as keras_version

KERAS_VERSION = keras_version

def loadTrainedModel(filename):
    """ Load in pretrained model
    Arguments:
        filename {str} -- filepath of the .h5 file containing the trained weights
    Returns:
        [keras.model] -- trained model
    """
    # check that model Keras version is same as local Keras version
    f = h5py.File(filename, mode='r')
    model_version = f.attrs.get('keras_version')
    keras_version = str(KERAS_VERSION).encode('utf8')

    if model_version != keras_version:
        print('WARNING: You are using Keras version ', keras_version,
            ', but the model was built using ', model_version)
    return load_model(filename)


def preprocess(img, new_size=(200,64), top_row=40, bot_row=10):
    """[summary]
    
    Arguments:
        img {np.array} -- 2D array representation of the image
    
    Keyword Arguments:
        new_size {tuple} -- the size to resize into (default: {(200,64)})
        top_row {int} -- the number of top rows to be removed from the image (default: {20})
        bot_row {int} -- the number of bottom rows to be removed from the image (default: {10})
    
    Returns:
        [np.array] -- 2D array representation of the preprocessed image
    """
    # Crop the top sections
    top = top_row
    bot = img.shape[0] - bot_row
    img = img[top:bot:]
    # Resize to 64x200
    img = cv2.resize(img, new_size)
    
    return img
