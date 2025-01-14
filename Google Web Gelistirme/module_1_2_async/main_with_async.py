import asyncio
'''
In this situation we run xfunc and yfunc in parallel.
This way we don't have to wait for xfunc to complete to start yfunc.
'''
async def xfunc():
    print('xfunc started')
    await asyncio.sleep(5)
    return(5)

async def yfunc():
    print('yfunc started')
    await asyncio.sleep(5)
    return(10)

async def main(): # This is the main function that runs the other functions
    task1 = asyncio.create_task(xfunc())
    task2 = asyncio.create_task(yfunc())

    await task1
    await task2

    print(task1.result())
    print(task2.result())

if __name__ == '__main__':
    asyncio.run(main())

# Its important to have in web development because we can run multiple functions at the same time.