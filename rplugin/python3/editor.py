import os
import os.path

class Vim:
    def __init__(self, vim):
        self.vim = vim

    def get_current_filename(self):
        return os.path.relpath(self.vim.current.buffer.name, os.getcwd())

    def get_buffers(self):
        return self.vim.buffers

class MockVim:
    def __init__(self, current_filename, buffers):
        self.current_filename = current_filename
        self.buffers = buffers

    def get_current_filename(self):
        return self.current_filename

    def get_buffers(self):
        return self.buffers

    def list_buffers(self):
        return list(map(lambda b: b.name, self.buffers))

class MockBuffer:
    def __init__(self, value):
        self.name = value

    @property
    def name(self):
        return self.name_value

    @name.setter
    def name(self, value):
        self.name_value = value

def mock_buffers(names):
    result = []
    for name in names:
        result.append(MockBuffer(name))
    return result
