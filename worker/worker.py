from multiprocessing import Process, Pipe, Event

import packages.logging as logging
from worker.communication.channel.request_channel import RequestChannel
from worker.result_sending.result_sending_pipeline import ResultSendingPipeline
from worker.task_processing.task_processing_pipeline import TaskProcessingPipeline
from worker.work_requesting.work_requesting_pipeline import WorkRequestingPipeline
from worker.worker_config import WorkerConfig


class Worker(Process):
    def __init__(self, config: WorkerConfig):
        super().__init__()
        self.config = config

    def run(self):
        log = logging.setup_logging('work_requesting')

        log.info(f'starting worker-{self.config.identity}')
        
        request_channel = RequestChannel(self.config.producer_ip, self.config.producer_port, self.config.identity)
        request_channel.connect()
        log.debug(f'established connection to producer-{request_channel}')

        work_config = self._register_at_producer(request_channel)

        if work_config is None:
            log.info(f'failed to register at producer {request_channel}')
            return

        log.info(f'registered at producer {request_channel}. Received config {work_config}')

        task_pipe_recv_end, task_pipe_send_end = Pipe(False) # task-requester -> task-processor
        result_pipe_recv_end, result_pipe_send_end = Pipe(False) # task processor -> result-sender

        task_handler_ready = Event()
        task_handler = TaskProcessingPipeline(self.config.identity, work_config, task_handler_ready, task_pipe_recv_end, result_pipe_send_end)
        task_requester = WorkRequestingPipeline(request_channel, task_pipe_send_end)
        result_sender = ResultSendingPipeline(self.config.collector_ip, self.config.collector_port, result_pipe_recv_end)

        task_handler.start()
        result_sender.start()

        # only start requesting work, when the task-handler is ready
        task_handler_ready.wait()
        task_requester.run() # avoid spawning additional process

        task_handler.join()
        result_sender.join()

    def _register_at_producer(self, control_channel: RequestChannel):
        return control_channel.register()