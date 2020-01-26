import ffmpeg
import os


def downloadRTSP(url, videoName, seconds=9999999, debug=False):
    """
    Downloads an RTSP livestream to a specific location.
    """
    print("Trying to download from: " + url)
    stream = ffmpeg.output(ffmpeg.input(url),
                           videoName,
                           reorder_queue_size=1000,
                           timeout=1000, stimeout=1000, t=seconds,
                           rtsp_flags="listen", rtsp_transport="tcp")
    if os.path.exists(videoName):
        os.remove(videoName)
    if debug is False:
        return ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
    return ffmpeg.run(stream, capture_stdout=False, capture_stderr=False)