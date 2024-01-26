import asyncio
#pip install telnetlib3
import telnetlib3

async def keep_alive(writer):
    '''loops infinitely and sends a carriage return every 60 seconds'''
    while True:
        writer.write("\n".encode()) 
        await writer.drain()
        await asyncio.sleep(60) 

async def shell(writer):
    asyncio.create_task(keep_alive(writer)) # run in parallel and will not block the execution of the shell function

    writer.write("enable\n".encode())
    await writer.drain()

    writer.write("configure terminal\n".encode())
    await writer.drain()

    '''
    put fctp
    '''

    writer.close()

loop = asyncio.get_event_loop()
coro = telnetlib3.open_connection('your_router_host', 23, shell=shell)
loop.run_until_complete(coro)