import asyncio


loop = asyncio.new_event_loop()


def db_forever():
    try:
        loop.run_forever()
        print(1)
    finally:
        print('Stop')


db_forever()
loop.close()
