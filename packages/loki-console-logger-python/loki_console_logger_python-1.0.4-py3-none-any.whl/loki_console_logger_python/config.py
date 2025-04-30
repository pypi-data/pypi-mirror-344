from typing import Callable, Dict, Optional, Any

class LokiLoggerOptions:
    def __init__(
        self,
        url: str,
        tenant_id: str,
        app_name: str,
        auth_token: Optional[str] = None,
        batch_size: int = 10,
        flush_interval: int = 2,
        labels: Optional[Dict[str, str]] = None,
        dynamic_labels: Optional[Dict[str, Callable[[], Any]]] = None,
    ):
        self.url = url
        self.tenant_id = tenant_id
        self.app_name = app_name
        self.auth_token = auth_token
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.labels = labels or {}
        self.dynamic_labels = dynamic_labels or {}
