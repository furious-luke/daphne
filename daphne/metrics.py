import time
from datetime import datetime, timedelta
import threading


class MetricsThread(threading.Thread):
    def __init__(self, logger=None, source=None):
        super().__init__()
        self.source = ('source=%s ' % source) if source else ''
        self.logger = logger if logger is not None else self
        self.daemon = True

    def run(self):
        while 1:
            delay = self._delay()
            time.sleep(delay)
            msg = self.source
            mem = self.get_memory_usage()
            msg += 'sample#usage_b={usage_b} sample#limit_b={limit_b}'.format(**mem)
            self.logger.info(msg)

    def get_memory_usage(self):
        results = {}
        with open('/sys/fs/cgroup/memory/memory.usage_in_bytes') as f:
            results['usage_b'] = int(f.read())
        with open('/sys/fs/cgroup/memory/memory.limit_in_bytes') as f:
            results['limit_b'] = int(f.read())
        return results

    def info(self, msg):
        print(msg)

    def _delay(self):
        now = datetime.now()
        delta = (now + timedelta(minutes=1)).replace(second=30, microsecond=0) - now
        return delta.total_seconds()
