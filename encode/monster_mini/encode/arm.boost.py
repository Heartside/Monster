import subprocess
from rpyc import Service, ThreadedServer

class QueueService(Service):
    current_encode = None

    def exposed_run(self, command):
        if current_encode is not None:
            assert current_encode.poll() is not None

        current_encode = subprocess.Popen(command, text=True)

    def exposed_poll2():
        assert current_encode is not None

        if current_encode.poll() is not None:
            return True
        else:
            return None

    def exposed_wait():
        assert current_encode is not None

        current_encode.wait()

    def exposed_shutdown(self):
        server.close()

server = ThreadedServer(QueueService(), port=port)
server.start()
