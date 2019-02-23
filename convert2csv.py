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
    img = cv2.imread(sys.argv[1])

    #Define structure for .csv format
    csv = {
        'x': [],
        'y': [],
        'z': [], #Not sure about this one
        'r': [],
        'g': [],
        'b': [],
    }

    #Convert img to csv
    pixels_countX = len(img)
    pixels_countY = len(img[0])
    pixels_count_total = pixels_countX * pixels_countY
    print('Conversion started')
    for x in range(pixels_countX):
        for y in range(pixels_countY):
            pixel = img[x][y]
            csv['x'].append(x)
            csv['y'].append(y)
            csv['z'].append(0)
            csv['r'].append(pixel[0])
            csv['g'].append(pixel[1])
            csv['b'].append(pixel[2])

            progress = (x * pixels_countY + y) / pixels_count_total * 100
            print('%.2f%%\r' % progress, end='')

    #Save result
    print('Saving to '+ config['convert2csv_output'])
    df = pd.DataFrame(csv)
    df.to_csv(config['convert2csv_output'], index=False)

if __name__ == "__main__":
    main()
