"""Producer Consumer problem implemented using multiprocessing.Queue (IPC shared memory)"""

__author__ = 'Larisa Paliciuc'
__email__ = 'larisa.elena.paliciuc@gmail.com'
__version__ = '1.0.0'
__date__ = '2021.11.06'
__status__ = 'Beta'

from multiprocessing import Process, Queue

from scripts.producer import Producer
from scripts.consumer import Consumer


def main():
    queue = Queue()

    producer = Producer()
    consumer = Consumer()

    producer_process = Process(target=producer.run, args=(queue, ))
    consumer_process = Process(target=consumer.run, args=(queue, ))

    try:
        producer_process.start()
        consumer_process.start()

        producer_process.join()
        consumer_process.join()

    except Exception:
        # In case of main.py script termination, kill the spawned processes.
        producer_process.kill()
        consumer_process.kill()


if __name__ == '__main__':
    main()
