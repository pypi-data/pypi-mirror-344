import sys
import traceback
import threading

def _format_traceback(exc_type, exc_value, exc_traceback):
    tb = traceback.extract_tb(exc_traceback)
    formatted = []

    for frame in tb:
        path = frame.filename
        line = frame.lineno
        name = frame.name
        line_text = frame.line
        formatted.append(f'File "{path}", line {line}, in {name}\n    {line_text}')

    output = ["Traceback (most recent call last):"]
    output.extend(formatted)
    output.append(f"{exc_type.__name__}: {exc_value}")
    return "\n".join(output)

def _custom_excepthook(exc_type, exc_value, exc_traceback):
    print(_format_traceback(exc_type, exc_value, exc_traceback))

# Internal: setprofile hook to catch all exceptions (even handled ones)
def _profile(frame, event, arg):
    if event == 'exception':
        exc_type, exc_value, exc_traceback = arg
        # Avoid printing KeyboardInterrupts or SystemExit
        if issubclass(exc_type, (KeyboardInterrupt, SystemExit)):
            return
        print(_format_traceback(exc_type, exc_value, exc_traceback))

def detail():
    """Install global traceback formatting for all exceptions, handled or not."""
    sys.excepthook = _custom_excepthook
    sys.setprofile(_profile)
    threading.setprofile(_profile)
