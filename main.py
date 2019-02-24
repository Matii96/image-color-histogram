import sys
import json
import numpy as np
import pandas as pd
from time import time
import multiprocessing as mp
#import matplotlib.pyplot as plt

def count_colors(procnum, dict, df, row_start, row_end):
    print('Thread %d started' % procnum)
    colors = np.array([[[0] * 256] * 256] * 256)
    for index, row in df.loc[row_start:row_end].iterrows():
        colors[row['r']][row['g']][row['b']] += 1

    dict[procnum] = colors

def main():
    #Load configuration
    with open('config.json', encoding='utf-8') as json_data:
        config = json.load(json_data)

    #Check if path to image has been passed
    path_to_image = config['convert2csv_output']
    if len(sys.argv) > 1:
        path_to_image = sys.argv[1]

    #load image
    print('Loading image from '+ path_to_image)
    df = pd.read_csv(path_to_image)

    #Dictionary that allows communication between threads
    manager = mp.Manager()
    dict = manager.dict()

    #Even distribution of tasks to threads
    thread_tasks = [df.shape[0] // config['threads']] * config['threads']
    for i in range(df.shape[0] % config['threads']):
        thread_tasks[i] += 1

    threads = []
    last_task = 0
    print('Creating %d thread(s)' % config['threads'])
    beginning = time()
    for i in range(config['threads']):
        row_end = last_task + thread_tasks[i]
        thread = mp.Process(target=count_colors, args=(i, dict, df, last_task, row_end))
        last_task = row_end + 1
        threads.append(thread)
        thread.start()

    result = np.array([[[0] * 256] * 256] * 256)
    for i in range(config['threads']):
        threads[i].join()
        print('Thread %d ended' % i)
        result = np.add(result, dict[i])
    elapsed_time = time() - beginning

    print('Elapsed time: %.3fs' % elapsed_time)

    #Print result
    result_csv = {
        'r': np.repeat(np.arange(0,256), 256 * 256),
        'g': np.tile(np.repeat(np.arange(0,256), 256), 256),
        'b': np.tile(np.arange(0,256), 256 * 256),
        'count': result.ravel()
    }

    #Save result
    print('Saving to '+ config['main_output'])
    df = pd.DataFrame(result_csv)
    df.to_csv(config['main_output'], index=False)

if __name__ == "__main__":
    main()
