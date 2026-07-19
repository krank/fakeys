import logging

from typing import TYPE_CHECKING, TextIO

if TYPE_CHECKING:
    _StreamHandler = logging.StreamHandler[TextIO]
else:
    _StreamHandler = logging.StreamHandler



class CollectHandler(_StreamHandler):
    _log_records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord):
        self._log_records.append(record)

    def clear(self):
        self._log_records.clear()
      
    def has_records(self):
        return len(self._log_records) > 0
    
    def get_records(self, log_level: int):
        return [record for record in self._log_records if record.levelno >= log_level]
    
    def get_records_dicts(self, log_level: int) -> list[dict[str,str|int]]:
        return [
            {
                "loglevel": record.levelno,
                "message": record.getMessage()
            }
            for record in self._log_records if record.levelno >= log_level
        ]