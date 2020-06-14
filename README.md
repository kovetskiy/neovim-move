# neovim-move

A pretty straightforward plugin for NeoVim. Does only one thing — moves files/directories.

Usage:
```
:Move [<file>] <dst>
```

Features:
* Move one specified file: `:Move main.c test.c`;
* Move multiple specified files: `:Move main.c lib.c dst`;
* Move the current file (opened in the current buffer) to the destination. This is used if you invoke the command without
    specifying the first argument: `:Move src/`;
* Move a file to a directory: `:Move main.c src/`;
* Move a directory to a directory: `:Move dir src/`;
* Move by glob to a directory: `:Move **/*.x xfiles/`;
* Creates nested directories if needed.
* Works asynchronously.

And the most cool feature in here:
* Re-open files after moving them in-place. Glob supported.

Neat things:
* Zero lines in Vim language have been used for writing the plugin. Everything is written in Python & NeoVim RPC
    bindings.

# Installation

```
Plug 'kovetskiy/neovim-move', { 'do' : ':UpdateRemotePlugins' }
```

NOTE: Vim's restart is required due to the nature of _neovim remote plugins_.

# Testing

```
make test
```

# License

MIT
