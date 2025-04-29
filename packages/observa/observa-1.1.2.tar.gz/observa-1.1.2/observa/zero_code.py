import time
import uuid

from observa.event import Event, EventType
from observa.server import Server, Session, Agent, Thread
from observa.config import API_KEY, API_HOST, PROJECT_ID
from typing import TypeVar, Callable, Any
from types import FunctionType, MethodType

fn_name_session_id = ''
fn_name_trace_event = []

apiServer = Server(API_KEY, PROJECT_ID, API_HOST)

T = TypeVar('T')


def wrap_class(obj: T) -> T:
    class Proxy:
        def __init__(self, target):
            self._target = target

        def __getattribute__(self, name):
            if name == "_target":
                return super().__getattribute__(name)

            target = super().__getattribute__("_target")
            attr = getattr(target, name)

            if callable(attr):
                return trace_fn(attr)
            else:
                return attr

    return Proxy(obj)  # 这里类型是 T


def trace_fn(fn: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args, **kwargs):
        global fn_name_session_id
        global fn_name_trace_event
        global apiServer
        fn_name = getattr(fn, '__name__', '<lambda>') or '<lambda>'
        session_id = ''
        log = Event(
            eventId=str(uuid.uuid4()),
            eventType=EventType.LLM,
            eventName="",
            startTime=int(time.time() * 1000),  # 毫秒
            input=list(args) + [{k: v} for k, v in kwargs.items()]
        )
        if isinstance(fn, MethodType):
            if len(fn_name_trace_event):
                parent_id = fn_name_trace_event[-1]['eventId']
                log.parentId = parent_id
                fn_name_trace_event.append(log)
            else:
                # 第一次调用，创建 session
                session = Session(fn_name)
                fn_name_session_id = apiServer.createSession(session)
                fn_name_trace_event.append(log)

            session_id = fn_name_session_id

        elif isinstance(fn, FunctionType):
            session = Session(fn_name)
            session_id = apiServer.createSession(session)
        else:
            raise TypeError(f"Expected a function, got {type(fn)}")

        try:

            output = fn(*args, **kwargs)
            log.endTime = int(time.time() * 1000)
            log.output = output
            if log.startTime:
                log.duration = log.endTime - log.startTime
            token_usage = 0
            if isinstance(log.output, dict) and 'llm_output' in log.output:
                token_usage = log.output['llm_output'].get('token_usage', {}).get("total_tokens", 0)
            log.tokenCount = token_usage

            apiServer.createEvent({
                "sessionId": session_id,
                "logList": [log.model_dump()]
            })
            return output
        except Exception as e:
            log.endTime = int(time.time() * 1000)
            if log.startTime:
                log.duration = log.endTime - log.startTime
            log.error = str(e)
            apiServer.createEvent({
                "sessionId": session_id,
                "logList": [log.model_dump()]
            })
            raise e

    return wrapper
