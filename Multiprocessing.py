import time
import concurrent.futures

def sleep_for_a_while(seconds):
    time.sleep(seconds)
    print("I've slept for {} seconds.".format(seconds))
    return seconds

if __name__ == '__main__':
    start = time.time()

    seconds_list = [5,4,3,2,1]

    # sequential taking 15 seconds
    # for i in seconds_list:
    #     sleep_for_a_while(i)

    with concurrent.futures.ProcessPoolExecutor() as p:
        results = p.map(sleep_for_a_while, seconds_list)
    
    for result in results:
        print(result)

    end = time.time()

    print("Time taken: {}".format(round(end-start, 2)))
