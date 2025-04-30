import os

from tomlkit import parse as toml_parse

from . import Exshell
from .wizards import PleaseInputExcelApplicationPath


class ExshellBuilder():


    def __init__(self, abs_path_to_workbook):
        self._abs_path_to_workbook = abs_path_to_workbook
        self._abs_path_to_config = None


    @property
    def abs_path_to_workbook(self):
        return self._abs_path_to_workbook

    @property
    def abs_path_to_config(self):
        return self._abs_path_to_config


    def config_is_ok(self):
        # エクセルの実行ファイルへのパスが設定されているならＯｋ
        return os.path.isfile(self.config_doc_rw['excel']['path'])


    def load_config(self, abs_path, create_if_not_exists=False):
        """設定ファイル読取
        """

        self._abs_path_to_config = abs_path

        try:
            with open(self._abs_path_to_config, mode='r', encoding='utf-8') as f:
                print(f'🔧　Read 📄［ {self._abs_path_to_config} ］config file...')
                config_text = f.read()

        except FileNotFoundError:
            if not create_if_not_exists:
                raise

            config_text = """\
[excel]
path = ''
"""
            with open(self._abs_path_to_config, mode='w', encoding='utf-8') as f:
                print(f'🔧　Write 📄［ {self._abs_path_to_config} ］config file...')
                f.write(config_text)
            

        self.config_doc_rw = toml_parse(config_text)


    def start_tutorial(self):
        """チュートリアルの開始
        """
        PleaseInputExcelApplicationPath.play(
                exshell_builder=self)


    def build(self):
        return Exshell(
                excel_application_path=self.config_doc_rw['excel']['path'],
                abs_path_to_workbook=self.abs_path_to_workbook)
