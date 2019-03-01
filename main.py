import sys
import json
import numpy as np
import pandas as pd
from time import time
import multiprocessing as mp
from os import path

def count_colors(procnum, dict, img_part):
    print('process %d started' % (procnum+1))
    colors = {}
    for row in img_part:
        key = ','.join(map(lambda x: "{:03d}".format(x), row))
        if not key in colors:
            colors[key] = 0
        colors[key] += 1

    dict[procnum] = colors

def main():
    #Load configuration
    with open('config.json', encoding='utf-8') as json_data:
        config = json.load(json_data)

    #Check if path to image has been passed
    path_to_image = config['convert2csv_output']
    if len(sys.argv) > 1:
        path_to_image = sys.argv[1]
    if not path.isfile(path_to_image):
        print('No file '+ path_to_image +' found')
        return

    #load image
    print('Loading image from '+ path_to_image)
    img = pd.read_csv(path_to_image).values[:,3:]

    #Dictionary that allows for communication between processes
    manager = mp.Manager()
    dict = manager.dict()

    #Even distribution of tasks to processes
    img_length = len(img)
    process_tasks = [img_length // config['processes']] * min(config['processes'], img_length)
    for i in range(img_length % config['processes']):
        process_tasks[i] += 1

    processes = []
    last_task = 0
    processes_to_run = len(process_tasks)
    print('Creating %d process(es)' % processes_to_run)
    beginning = time()
    for i in range(processes_to_run):
        row_end = last_task + process_tasks[i]
        process = mp.Process(target=count_colors, args=(i, dict, img[last_task:row_end]))
        process.start()
        processes.append(process)
        last_task = row_end

    result = {}
    for i in range(processes_to_run):
        processes[i].join()
        print('process %d ended' % (i+1))
        for color in dict[i]:
            if not color in result:
                result[color] = 0
            result[color] += 1
    elapsed_time = time() - beginning

    print('Elapsed time: %.3fs' % elapsed_time)

    #Save result
    print('Saving to '+ config['main_output'])
    df = pd.DataFrame({
        'color': list(result.keys()),
        'count': list(result.values())
    })
    df.to_csv(config['main_output'], index=False)

if __name__ == "__main__":
    main()
