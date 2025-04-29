import os
import redis
import json
import subprocess
import time
import atexit

class _Signella:
    def __init__(self, host='localhost', port=6379, db=0, autostart=True):
        """
        :param host: Redis host
        :param port: Redis port (overridden by RADIOVAR_PORT if set)
        :param db: Redis DB
        :param autostart: If True, auto-start a local redis-server if not found
        """
        env_port = os.getenv('RADIOVAR_PORT')
        if env_port:
            port = int(env_port)

        self._host = host
        self._port = port
        self._db = db
        self._process = None

        if autostart and not self._can_connect():
            self._start_redis_server()

        # Now connect
        self.r = redis.Redis(host=self._host, port=self._port, db=self._db, decode_responses=False)

        # Optional namespace: e.g. if RADIOVAR_NS="calendar", 
        # all keys become "calendar::..." in Redis
        self._namespace = os.getenv('RADIOVAR_NS', '')

    def _can_connect(self):
        """Check if a Redis server is up on self._host:self._port."""
        try:
            test_r = redis.Redis(
                host=self._host, port=self._port, db=self._db, decode_responses=True
            )
            test_r.ping()
            return True
        except redis.exceptions.ConnectionError:
            return False

    def _start_redis_server(self):
        """Launch a local Redis server on the specified port as a subprocess."""
        cmd = ["redis-server", "--port", str(self._port)]
        self._process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        time.sleep(1)  # give it a moment to spin up

        if not self._can_connect():
            raise RuntimeError("Failed to auto-start local Redis server.")

        # Clean up on exit
        atexit.register(self.stop_redis_server)

    def stop_redis_server(self):
        """Stop our spawned Redis server if still running."""
        if self._process and self._process.poll() is None:
            self._process.terminate()
            self._process.wait()

    def _make_key(self, key):
        """
        Convert user key(s) into final Redis key string.
        If there's a namespace, it goes up front.
        """
        if not isinstance(key, tuple):
            # single item => make it a tuple
            key = (key,)

        parts = []
        if self._namespace:
            parts.append(self._namespace)

        # e.g. key could be ('name', True, 123)
        parts.extend(str(k) for k in key)

        # 'calendar::name::True::123' for example
        return "::".join(parts)

    def __getitem__(self, key):
        """Retrieve the item from Redis, JSON-decoding if possible."""
        redis_key = self._make_key(key)
        raw_data = self.r.get(redis_key)
        if raw_data is None:
            return None
        try:
            return json.loads(raw_data)
        except json.JSONDecodeError:
            return raw_data

    def __setitem__(self, key, value):
        """Store the item in Redis as JSON."""
        redis_key = self._make_key(key)
        self.r.set(redis_key, json.dumps(value))


# -- Here is the critical bit: a SINGLETON instance of `_Signella`.
# So from signella import signal, you get THIS instance, not the class.
signal = _Signella()