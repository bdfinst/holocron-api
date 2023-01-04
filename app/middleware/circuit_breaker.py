"""Circuit breaker middleware."""
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

from flask import Response, request

ONE_MINUTE = 60


class CircuitBreaker:
    """Circuit breaker class."""

    break_times: Dict[str, datetime] = {}

    def check_break(self, addr: str) -> bool:
        """Check if an ip address has a circuit break."""
        return addr in self.break_times

    def set_break(self, addr: str):
        """Set circuit break for a given ip address."""
        self.break_times[addr] = datetime.now() + timedelta(minutes=1)
        threading.Thread(target=self.reset_break, args=(addr,)).start()

    def reset_break(self, addr: str):
        """Clear a circuit break from memory."""
        time.sleep(ONE_MINUTE)
        self.break_times.pop(addr)


breaker = CircuitBreaker()


def circuit_breaker_check() -> Optional[Tuple[str, int]]:
    """Check if user set circuit breaker."""
    if breaker.check_break(getattr(request, "remote_addr", "")):
        return "Too many requests", 429
    return None


def circuit_breaker_validation(response: Response) -> Response:
    """Set breaker if request caused a server error."""
    if response.status_code >= 500:
        breaker.set_break(getattr(request, "remote_addr", ""))
    return response
