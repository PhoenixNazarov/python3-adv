import codecs
import logging
import multiprocessing
import threading
import time

logging.basicConfig(
    filename='artifacts/task3.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


def process_A(input_pipe, output_pipe):
    logger.info("[Process A] started")
    while True:
        message = input_pipe.recv()
        lower_message = message.lower()
        logger.info(f"[Process A] received: {message}, transformed: {lower_message}")
        output_pipe.send(lower_message)
        time.sleep(5)


def process_B(input_pipe, output_queue):
    logger.info("[Process B] started")
    while True:
        message = input_pipe.recv()
        transformed_message = codecs.encode(message, 'rot_13')
        logger.info(f"[Process B] received: {message}, transformed: {transformed_message}")
        output_queue.put(transformed_message)


def input_thread(input_pipe):
    logger.info("[Input Thread] started")
    while True:
        message = input("Введите сообщение: ")
        logger.info(f"[Input Thread] user input: {message}")
        input_pipe.send(message)


# Главный процесс
def main():
    # Каналы для обмена данными
    parent_A, child_A = multiprocessing.Pipe()
    parent_B, child_B = multiprocessing.Pipe()
    main_queue = multiprocessing.Queue()

    # Запуск дочерних процессов
    process_a = multiprocessing.Process(target=process_A, args=(child_A, parent_B))
    process_b = multiprocessing.Process(target=process_B, args=(child_B, main_queue))

    process_a.start()
    process_b.start()

    # Запуск потока для асинхронного ввода данных
    thread = threading.Thread(target=input_thread, args=(parent_A,))
    thread.start()

    logger.info("[Main Process] started")
    try:
        while True:
            transformed_message = main_queue.get()
            logger.info(f"[Main Process] received: {transformed_message}")
    except KeyboardInterrupt:
        pass

    process_a.join()
    process_b.join()
    thread.join()


if __name__ == "__main__":
    main()
