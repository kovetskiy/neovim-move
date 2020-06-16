import neovim
import logging
import os
import os.path
import glob
import sys
import shutil

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from editor import Vim

@neovim.plugin
class Main(object):
    def __init__(self, vim=None):
        if vim:
            self.vim = Vim(vim)

    def set_vim(self, vim):
        self.vim = vim

    def setup_log(self):
        handler = logging.FileHandler('/tmp/rplugin.log')
        handler.setLevel(logging.DEBUG)

        self.log = logging.getLogger('rplugin')
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(handler)

    @neovim.command('Move', nargs='*')
    def move(self, args):
        if len(args) < 1:
            return

        inputs = args[:-1]
        output = args[-1]

        if len(inputs) == 0:
            filename = self.vim.get_current_filename()
            if filename == "":
                return

            inputs = [filename]

        sources = []
        for i in range(len(inputs)):
            input = inputs[i]
            if "*" in input:
                matches = glob.glob(input, recursive=True)
                sources += matches
            else:
                sources += [input]

        sources_dirs = self.get_dirs(sources)
        sources = list(filter(self.get_filter(sources_dirs), sources))

        output_isdir = os.path.isdir(output) or output.endswith('/') or len(sources) > 1
        if output_isdir:
            os.makedirs(output, exist_ok=True)

        for src in sources:
            shutil.move(src, output)

        for buffer in self.vim.get_buffers():
            name = buffer.name
            if not name:
                continue

            relpath = os.path.relpath(name, os.getcwd())
            if relpath in sources:
                if output_isdir:
                    buffer.name = os.path.join(output, os.path.basename(relpath))
                else:
                    buffer.name = output

            dir = os.path.dirname(relpath)
            while dir != "":
                if (dir + "/") in sources_dirs:
                    buffer.name = os.path.join(output, relpath)
                    break

                dir = os.path.dirname(dir)

    def get_dirs(self, sources):
        dirs = filter(lambda file: os.path.isdir(file), sources)
        dirs = list(map(lambda dir: dir if dir.endswith('/') else dir + '/', dirs))
        return dirs

    def get_filter(self, dirs):
        def fn(src):
            for dir in dirs:
                # do not copy the file because the directory already copied
                if src.startswith(dir):
                    return False
            return True

        return fn
