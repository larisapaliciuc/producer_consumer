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
        producer_process.kill()
        consumer_process.kill()


if __name__ == '__main__':
    main()


