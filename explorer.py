import os
import shutil
from helpers import lg


class Explorer:
    def __init__(self, user):
        if user and user.is_authenticated:
            self.boofer = user.path + '/boofer'
        else:
            self.boofer = None

    def copy(self, name, where='копирование'):
        if not self.boofer:
            return
        if not os.path.exists(self.boofer):
            os.mkdir(self.boofer)
        else:
            self.clean_boofer()
        onlyname = name.split('/')[-1]
        try:
            if os.path.isdir(name):
                shutil.copytree(name, self.boofer + '/' + onlyname)
            else:
                shutil.copy(name, self.boofer + '/' + onlyname)
        except Exception as ex:
            self.log_error(where, ex)

    def delete(self, name):
        try:
            if os.path.isdir(name):
                shutil.rmtree(name)
            else:
                os.remove(name)
        except Exception as ex:
            self.log_error('удаление', ex)

    def cut(self, name):
        self.copy(name, where='вырезание')
        self.delete(name)

    def paste(self, dirname):
        old = self.get_file_name()
        if not old or not self.boofer:
            return
        new = dirname + '/' + old.split('/')[-1]
        try:
            if os.path.isdir(old):
                if os.path.exists(new):
                    self.delete(new)
                shutil.copytree(old, new)
            else:
                shutil.copy(old, new)
        except Exception as ex:
            self.log_error('вставка', ex)

    def get_file_name(self):
        if not self.boofer:
            return
        if not os.path.exists(self.boofer):
            os.mkdir(self.boofer)
        list_ = os.listdir(self.boofer)
        return None if not list_ else self.boofer + '/' + list_[0]

    def log_error(self, where, ex):
        lg.error('Ошибка проводника. Процесс: {}. Ошибка:\n{}'.format(where,
                                                                      ex))

    def clean_boofer(self):
        for name in os.listdir(self.boofer):
            self.delete(self.boofer + '/' + name)
