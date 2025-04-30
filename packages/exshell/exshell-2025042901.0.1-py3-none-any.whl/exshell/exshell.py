import subprocess
import time


class Exshell():
    """エクシェル
    """


    def __init__(self, excel_application_path, abs_path_to_workbook):
        self._config_doc_rw = None
        self._excel_application_path = excel_application_path
        self._abs_path_to_workbook = abs_path_to_workbook
        self._opened_excel_process = None


    @property
    def config_doc_rw(self):
        return self._config_doc_rw


    @config_doc_rw.setter
    def config_doc_rw(self, value):
        self._config_doc_rw = value


    @property
    def excel_application_path(self):
        return self._excel_application_path


    @excel_application_path.setter
    def excel_application_path(self, value):
        self._excel_application_path = value


    @property
    def abs_path_to_workbook(self):
        return self._abs_path_to_workbook


    @abs_path_to_workbook.setter
    def abs_path_to_workbook(self, value):
        self._abs_path_to_workbook = value


    @property
    def opened_excel_process(self):
        return self._opened_excel_process


    @opened_excel_process.setter
    def opened_excel_process(self, value):
        self._opened_excel_process = value


    def open_virtual_display(self):
        """仮想ディスプレイを開く
        """
        print(f'🔧　Open virtual display...')
        # 外部プロセスを開始する（エクセルを開く）
        self.opened_excel_process = subprocess.Popen([self.excel_application_path, self.abs_path_to_workbook])   # Excel が開くことを期待
        time.sleep(1)


    def close_virtual_display(self):
        """仮想ディスプレイを閉じる
        """

        print(f'🔧　Close virtual display...')
        # 外部プロセスを終了する（エクセルを閉じる）
        self.opened_excel_process.terminate()
        self.opened_excel_process = None
        time.sleep(1)


    def save_workbook(self, wb):
        print(f'🔧　Save 📄［ {self.abs_path_to_workbook} ］contents file...')
        wb.save(self.abs_path_to_workbook)
