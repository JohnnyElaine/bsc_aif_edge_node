from multiprocessing import Process

from producer.communication.old_push_data.old_stream_generation.local.local_message_stream_generator import LocalMessageStreamGenerator
from shared.setup_logging import setup_logging

class Producer(Process):
    def __init__(self, port: int, video_path, nodes):
        """
        Initialize the coordinator with the video path and edge node information.
        :param video_path: Path to the input video file.
        :param nodes: List of (node_id, (host, port)) tuples representing edge nodes.
        """
        super().__init__()
        self._port = port
        self._video_path = video_path
        self._nodes = nodes

    def run(self):
        log = setup_logging('producer')

        log.info("starting producer")
        stream_generator = LocalMessageStreamGenerator(self._port, self._video_path, self._nodes)
        stream_generator.run()
