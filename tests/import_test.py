import asyncio
import random
import pandas as pd

text = ''


async def add_text(process_num: int) -> str:
    print(f'[{process_num}] start')
    text = ''
    for i in range(1_000_000):
        if i % 100_000 == 0:
            print(f'[{process_num}] Index {i :_}')

        text += str(random.randint(0, 1000)) + '\t'
    return text


async def main():
    global text
    nums = await asyncio.gather(*[add_text(i) for i in range(10)])
    text = '\n'.join(nums)
    with open('data.txt', 'w') as file:
        file.write(text)

if __name__ == '__main__':
    asyncio.run(main())

# data = pd.read_csv("data.txt", sep="\t", header=None)
# print(data)
