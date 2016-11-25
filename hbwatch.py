import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from os import path, popen
from subprocess import call

class Watcher:
    WATCH = '/path'
    OUTPUT = '/path'

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print "Error"

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            print "New video added to the folder - %s." % event.src_path
            convertedFileName = path.splitext(path.basename(event.src_path))[0]
            call("/path/HandBrakeCLI -i {input_file} -o {output_file} -e x264 --audio 'none' --preset='iPhone & iPod Touch'".
            format(input_file=event.src_path, output_file=path.join(Watcher.OUTPUT, "{fileName}.mp4".format(fileName = convertedFileName))), shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Handbrake watcher for automated video converting")

    parser.add_argument("-z", "--preset", help="""Select preset by name (case-sensitive)
                           Enclose names containing spaces in double quotation
                           marks. (By default set to 'iPhone & iPod Touch')""")
    parser.add_argument("-i", "--input",
                        help="Set input file or device ('source')", required=True)
    parser.add_argument("-o", "--output", help="<filename> Set destination file name", required=True)
    parser.add_argument("-e", "--encoder", help="""<string>  Select video encoder:
                               x264
                               x265
                               mpeg4
                               mpeg2
                               VP8
                               VP9
                               theora
                               By default set to x264""")
    parser.add_argument("-r", "--rate", help="""<float>      Set video framerate
                           (5/10/12/15/20/23.976/24/25/29.97/
                           30/48/50/59.94/60/72/75/90/100/120
                           or a number between 1 and 1000).
                           Be aware that not specifying a framerate lets
                           HandBrake preserve a source's time stamps,
                           potentially creating variable framerate video""")
    parser.add_argument("-q", "--quality", help="<float>   Set video quality (e.g. 22.0)")
    parser.add_argument("-a", "--audio", help="""<string>    Select audio track(s), separated by commas
                           ('none' for no audio, '1,2,3' for multiple
                           tracks, default: first one).
                           Multiple output tracks can be used for one input. By default set to 'none'""")

    args = parser.parse_args()

    #do something with args
    w = Watcher()
    w.run()
