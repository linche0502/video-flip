from ffmpeg import compile
from ffmpeg.nodes import output_operator
import subprocess



# 原本的.run_async()在桌命應用程式狀態下，會開啟另一個cmd視窗
@output_operator()
def run_async(
    stream_spec,
    cmd='ffmpeg',
    pipe_stdin=False,
    pipe_stdout=False,
    pipe_stderr=False,
    quiet=False,
    overwrite_output=False,
):
    """Asynchronously invoke ffmpeg for the supplied node graph.

    Args:
        pipe_stdin: if True, connect pipe to subprocess stdin (to be
            used with ``pipe:`` ffmpeg inputs).
        pipe_stdout: if True, connect pipe to subprocess stdout (to be
            used with ``pipe:`` ffmpeg outputs).
        pipe_stderr: if True, connect pipe to subprocess stderr.
        quiet: shorthand for setting ``capture_stdout`` and
            ``capture_stderr``.
        **kwargs: keyword-arguments passed to ``get_args()`` (e.g.
            ``overwrite_output=True``).

    Returns:
        A `subprocess Popen`_ object representing the child process.

    Examples:
        Run and stream input::

            process = (
                ffmpeg
                .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
                .output(out_filename, pix_fmt='yuv420p')
                .overwrite_output()
                .run_async(pipe_stdin=True)
            )
            process.communicate(input=input_data)

        Run and capture output::

            process = (
                ffmpeg
                .input(in_filename)
                .output('pipe':, format='rawvideo', pix_fmt='rgb24')
                .run_async(pipe_stdout=True, pipe_stderr=True)
            )
            out, err = process.communicate()

        Process video frame-by-frame using numpy::

            process1 = (
                ffmpeg
                .input(in_filename)
                .output('pipe:', format='rawvideo', pix_fmt='rgb24')
                .run_async(pipe_stdout=True)
            )

            process2 = (
                ffmpeg
                .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
                .output(out_filename, pix_fmt='yuv420p')
                .overwrite_output()
                .run_async(pipe_stdin=True)
            )

            while True:
                in_bytes = process1.stdout.read(width * height * 3)
                if not in_bytes:
                    break
                in_frame = (
                    np
                    .frombuffer(in_bytes, np.uint8)
                    .reshape([height, width, 3])
                )
                out_frame = in_frame * 0.3
                process2.stdin.write(
                    frame
                    .astype(np.uint8)
                    .tobytes()
                )

            process2.stdin.close()
            process1.wait()
            process2.wait()

    .. _subprocess Popen: https://docs.python.org/3/library/subprocess.html#popen-objects
    """
    args = compile(stream_spec, cmd, overwrite_output=overwrite_output)
    stdin_stream = subprocess.PIPE if pipe_stdin else None
    stdout_stream = subprocess.PIPE if pipe_stdout or quiet else None
    stderr_stream = subprocess.PIPE if pipe_stderr or quiet else None
    return subprocess.Popen(
        args, stdin=stdin_stream, stdout=stdout_stream, stderr=stderr_stream, creationflags=subprocess.CREATE_NO_WINDOW
    )




# @output_operator()
# def run(
#     stream_spec,
#     cmd='ffmpeg',
#     capture_stdout=False,
#     capture_stderr=False,
#     input=None,
#     quiet=False,
#     overwrite_output=False,
# ):
#     """Invoke ffmpeg for the supplied node graph.
# 
#     Args:
#         capture_stdout: if True, capture stdout (to be used with
#             ``pipe:`` ffmpeg outputs).
#         capture_stderr: if True, capture stderr.
#         quiet: shorthand for setting ``capture_stdout`` and ``capture_stderr``.
#         input: text to be sent to stdin (to be used with ``pipe:``
#             ffmpeg inputs)
#         **kwargs: keyword-arguments passed to ``get_args()`` (e.g.
#             ``overwrite_output=True``).
# 
#     Returns: (out, err) tuple containing captured stdout and stderr data.
#     """
#     process = run_async(
#         stream_spec,
#         cmd,
#         pipe_stdin=input is not None,
#         pipe_stdout=capture_stdout,
#         pipe_stderr=capture_stderr,
#         quiet=quiet,
#         overwrite_output=overwrite_output,
#     )
#     out, err = process.communicate(input)
#     retcode = process.poll()
#     if retcode:
#         raise Error('ffmpeg', out, err)
#     return out, err