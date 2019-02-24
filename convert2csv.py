import sys
import cv2
import json
import numpy as np
import pandas as pd

def main():
    #Check if path to image has been passed
    if len(sys.argv) == 1:
        print('Usage: python convert2csv.py path_to_image')
        return

    #Load configuration
    with open('config.json', encoding='utf-8') as json_data:
        config = json.load(json_data)

    #load image
    print('Loading image from '+ sys.argv[1])
    img = cv2.imread(sys.argv[1])

    #Convert img to csv
    pixels_countX = len(img)
    pixels_countY = len(img[0])
    result = {
        'x': np.repeat(np.arange(0, pixels_countX), pixels_countY),
        'y': np.tile(np.arange(0, pixels_countY), pixels_countX),
        'z': [0] * pixels_countX * pixels_countY, #Not sure about this one
        'r': img[:,:,0].ravel(),
        'g': img[:,:,1].ravel(),
        'b': img[:,:,2].ravel()
    }

    #Save result
    print('Saving to '+ config['convert2csv_output'])
    df = pd.DataFrame(result)
    df.to_csv(config['convert2csv_output'], index=False)

if __name__ == "__main__":
    main()
