import unittest
import os.path
import os
import tempfile
import shutil

from plugin import Main
from editor import MockVim, mock_buffers

class PluginTest(unittest.TestCase):
    def test_simple(self):
        args = ['a', 'b']

        tree = ['a', 'x']
        tree_exp = ['b', 'x']
        self._test(args, tree, tree_exp)

    def test_no_removals(self):
        args = ['a', 'b']

        tree = ['a', 'z/', 'y/a']
        tree_exp = ['b', 'z/', 'y/a']
        self._test(args, tree, tree_exp)

    def test_no_first_arg(self):
        args = ['b']

        tree = ['a', 'z/', 'y/a']
        tree_exp = ['a', 'z/', 'y/a']
        self._test(args, tree, tree_exp)

    def test_no_first_arg_but_with_current_file(self):
        args = ['b']

        tree = ['a', 'z/', 'y/a']
        tree_exp = ['b', 'z/', 'y/a']

        self._test(args, tree, tree_exp, current_filename="a")

    def test_glob(self):
        args = ['**/*.x', 'xs/']
        tree = ['x', 'b', 'a.x', 'aa.x', 'b.x', 'dir.x/f.x', 'dir.x/f', 'z/', 'y/a']
        tree_exp = ['b', 'x', 'z/', 'xs/a.x', 'xs/aa.x', 'xs/b.x', 'xs/dir.x/f', 'xs/dir.x/f.x', 'y/a']

        buffers = tree
        buffers_exp = ['x', 'b', 'xs/a.x', 'xs/aa.x', 'xs/b.x', 'xs/dir.x/f.x', 'xs/dir.x/f', 'z/', 'y/a']

        self._test(args, tree, tree_exp, buffers, buffers_exp)

    def test_dir(self):
        args = ['dir.x', 'xs/']
        tree = ['x', 'dir.x/f.x', 'dir.x/f', 'z/', 'y/a']
        tree_exp = ['x', 'z/', 'xs/dir.x/f', 'xs/dir.x/f.x', 'y/a']

        buffers = tree
        buffers_exp = ['x', 'xs/dir.x/f.x', 'xs/dir.x/f', 'z/', 'y/a']

        self._test(args, tree, tree_exp, buffers, buffers_exp)

    def test_dir_at(self):
        args = ['@', 'xs/']
        tree = ['x', 'dir.x/f.x', 'dir.x/f', 'z/', 'y/a']
        tree_exp = ['x', 'z/', 'xs/dir.x/f', 'xs/dir.x/f.x', 'y/a']

        buffers = tree
        buffers_exp = ['x', 'xs/dir.x/f.x', 'xs/dir.x/f', 'z/', 'y/a']

        self._test(args, tree, tree_exp, buffers, buffers_exp, current_filename='dir.x/f.x')

    def test_dir_at_glob(self):
        args = ['@/*.x', './xs/']
        tree = ['x', 'dir.x/f.x', 'dir.x/f', 'z/', 'y/a']
        tree_exp = ['x', 'z/', 'y/a', 'dir.x/f', 'dir.x/xs/f.x']

        buffers = tree
        buffers_exp = ['x', 'dir.x/xs/f.x', 'dir.x/f', 'z/', 'y/a']

        self._test(args, tree, tree_exp, buffers, buffers_exp, current_filename='dir.x/f.x')

    def setUp(self):
        self.basedir = tempfile.mkdtemp()
        os.chdir(self.basedir)

    def tearDown(self):
        shutil.rmtree(self.basedir)

    def _test(
        self,
        args=[],
        tree=[],
        tree_exp=[],
        buffers=[],
        buffers_exp=[],
        current_filename=""
    ):
        for item in tree:
            dirname = os.path.dirname(item)
            if dirname != '':
                os.makedirs(dirname, exist_ok=True)

            if os.path.isdir(item):
                continue

            if item.endswith('/'):
                os.makedirs(item)
                continue

            with open(item, 'w') as file:
                file.write(item)

        mockvim = MockVim(current_filename, mock_buffers(buffers))

        plugin = Main()
        plugin.set_vim(mockvim)
        plugin.setup_log()

        plugin.move(args)

        actual = []
        for root, dirs, files in os.walk("."):
            root = root[1:] # drop .
            if root != "":
                root = root[1:] # drop /

            for file in files:
                actual.append(os.path.join(root, file))

            for dir in dirs:
                if os.path.exists(dir) and not os.listdir(dir):
                    actual.append(dir + "/")

        self.assertListEqual(tree_exp, actual, "unexpected tree")
        self.assertListEqual(buffers_exp, mockvim.list_buffers(), "unexecpted buffers")

if __name__ == '__main__':
    unittest.main()
