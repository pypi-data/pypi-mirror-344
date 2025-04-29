# procaaso-log

Simple logging library for use with ConSynSys Procaaso ENS, etc. tasks

## Usage

1. Configure the logging backend at the root package within the `__init__.py` file.  Enable all desired module loggers.

```python
import procaaso_log
procaaso_log.standard_config("app.foo", "lib.bar.baz")
```

2. Create a logger for each python file.

```python
from procaaso_log import get_logger
logger = get_logger(__name__)
```

3. Emit logs.

```python
logger.info("something happened!")
# -> {"event":"incoming!", ...}
logger.info("incoming!", extra="single log context")
# -> {"event":"incoming!","extra"="single log context", ...}
```

4. Create a contextual logger.

```python
look_logger = logger.bind(look="over there")
look_logger.info(
# -> {"event":"incoming!","extra"="single log context"}
```
