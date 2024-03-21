import asyncio
import random
import os
import sys


async def handle_client(reader, writer):
    addr = writer.get_extra_info('sockname')
    port = addr[1]
    response = flag if port == chosen_port else bad_flag
    print(f"Received connection on {port}, chosen port {chosen_port}, sending: {response}")
    writer.write(response.encode())
    await writer.drain()

    print("Closing the connection")
    writer.close()


async def start_servers():
    tasks = []
    for port in range(1024, 4097):
        server = await asyncio.start_server(lambda r, w: handle_client(r, w), '0.0.0.0', port)

        tasks.append(server.serve_forever())

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    if os.environ.get('FLAG', '').strip() == '':
        # sys.stderr.write("Flag needs to be provided in FLAG env variable\n")
        # sys.exit(1)
        os.environ['FLAG'] = "flag{Q29uZ3JhdHMsIGdvb2QgZ2FtZSE=}"
    chosen_port = random.randint(1024, 4096)
    flag = os.environ['FLAG']
    bad_flag = "falg{RXZpbFdyb25nRmxhZw}"
    print(f"Chosen port for 'yep': {chosen_port}")

    asyncio.run(start_servers())
