import asyncio
import random


async def produce(queue, n):
    for x in range(1, n + 1):
        # produce an item
        print('producing task {}/{}'.format(x, n))
        # simulate i/o operation using sleep
        await asyncio.sleep(random.randint(0, 10)/10)
        item = str(x)
        # put the item in the queue
        await queue.put(item)

    # indicate the producer is done
    await queue.put(None)


async def consume(queue):
    while True:
        # wait for an item from the producer
        item = await queue.get()
        if item is None:
            # the producer emits None to indicate that it is done
            break

        # process the item
        print('consuming item {}...'.format(item))
        # simulate i/o operation using sleep
        await asyncio.sleep(random.randint(0, 10)/10)


import time

start = time.perf_counter()
loop = asyncio.get_event_loop()
queue = asyncio.Queue(loop=loop)
consumer_coro = consume(queue)

consumer_coro = consume(queue)
producer_coro = produce(queue, 100)
loop.run_until_complete(asyncio.gather(producer_coro, consumer_coro))
loop.close()
end = time.perf_counter()
total = end - start
print(f"total = {total}")
