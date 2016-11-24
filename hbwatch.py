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
    w = Watcher()
    w.run()
