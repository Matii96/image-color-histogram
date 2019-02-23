import sys
import json
import numpy as np
import pandas as pd
from time import time
import multiprocessing as mp
#import matplotlib.pyplot as plt

def count_colors(procnum, dict, df, row_start, row_end):
    colors = {}
    for index, row in df.loc[row_start:row_end].iterrows():
        color = ','.join(map(lambda x: str(x), [row['r'], row['g'], row['b']]))

        if not color in colors:
            colors[color] = 0
        colors[color] += 1

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
    for i in range(config['threads']):
        row_end = last_task + thread_tasks[i]
        thread = mp.Process(target=count_colors, args=(i, dict, df, last_task, row_end))
        last_task = row_end + 1
        threads.append(thread)
        thread.start()

    result = {}
    print('Counting started')
    beginning = time()
    for i in range(config['threads']):
        threads[i].join()
        for color in dict[i]:
            if not color in result:
                result[color] = 0
            result[color] += dict[i][color]
    elapsed_time = time() - beginning

    print('Elapsed time: %.3fs' % elapsed_time)

    for color, count in result.items():
        print('%s: %d' % (color, count))

    #Draw chart
    '''
    result = {
        'colors': list(result.keys()),
        'counts': list(result.values()),
    }
    fig, ax = plt.subplots()
    ind = np.arange(1, len(result['colors'])+1)
    chart = plt.bar(ind, result['counts'])
    ax.set_xticks(ind)
    ax.set_title('Colors histogram')
    plt.axis([40, 160, 0, 0.03])
    plt.grid(True)
    plt.show()
    '''

if __name__ == "__main__":
    main()
