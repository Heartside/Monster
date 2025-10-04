import subprocess
from rpyc import Service, ThreadedServer

class QueueService(Service):
    current_encode = None

    def exposed_run(self, command):
        if self.current_encode is not None:
            assert self.current_encode.poll() is not None

        self.current_encode = subprocess.Popen(command, text=True)

    def exposed_poll2(self):
        assert self.current_encode is not None

        if self.current_encode.poll() is not None:
            return True
        else:
            return None

    def exposed_wait(self):
        assert self.current_encode is not None

        self.current_encode.wait()

    def exposed_shutdown(self):
        server.close()

server = ThreadedServer(QueueService(), port=port)
server.start()
