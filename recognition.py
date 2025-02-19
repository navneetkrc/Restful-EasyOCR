from flask import Flask, request, abort
import urllib
import numpy as np
import cv2
import easyocr
import os
from flask import jsonify 


reader = easyocr.Reader(['en','hi'], gpu=False)

app = Flask(__name__)

'''
def url_to_image(url):
    """
    download the image, convert it to a NumPy array, and then read it into OpenCV format
    :param url: url to the image
    :return: image in format of Opencv
    """
    print("-------inside url to image--------")
    resp = urllib.request.urlopen(url)
    print("-------resp in  url to image-------- ", str(resp))

    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    print("url = ", url)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    print("--iamge in url_to_image ",str(url_to_image))
    return image
    '''

'''
def data_process(data):
    """
    read params from the received data
    :param data: in json format
    :return: params for image processing
    """
    print("--data process")
    image_url = data["image"]
    print("--image url -- ",str(image_url))
    #secret_key = data["secret_key"]

    return image_url #url_to_image(image_url)#, secret_key
    '''

def recognition(image_url):
    """

    :param image:
    :return:
    """
    try:
        print("-inside recognition")
        results = []
        #data = []
        texts = reader.readtext(image_url)
        
        print("==texts = ",str(texts))
        for (bbox, text, prob) in texts:
            #output = {
                #"coordinate": [list(map(float, coordinate)) for coordinate in bbox],
                #"text": data,
                #"score": prob
            #}
            results.append(text)
            #results.append(output)
        print("==results = "+str(results))
        return results
    except Exception as e:
        print("image not processed by easy ocr - "+str(e))
        return[{'text':'na','score':'na'}]


@app.route('/ocr', methods=['GET', 'POST'])
def process():
    """
    received request from client and process the image
    :return: dict of width and points
    """
    print("--process start inside OCR flask endpoint--")
    data = request.get_json()
    #print("--data : "+str(data))
    #image  = data_process(data)
    #print("--image : "+str(image))
    image_url = data["image"] 
    print("--imageurl : "+str(image_url))
    # if secret_key == SECRET_KEY:
    results = recognition(image_url)
    print("======RESULTS RECEIVED-------")
    #return jsonify({"results": results})
    return jsonify(results)
    # else:
    #     abort(401)


if __name__ == "__main__":
    print("--main-- received request")
    app.run(debug=True,host='0.0.0.0', port=2000)
