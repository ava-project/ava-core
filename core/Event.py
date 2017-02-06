class Event:
    def __init__(self, cmd, is_builtin, nb_args):
        self._cmd = cmd
        self._is_builtin = is_builtin
        self._nb_args = nb_args

    def get_str(self):
        return self._str
