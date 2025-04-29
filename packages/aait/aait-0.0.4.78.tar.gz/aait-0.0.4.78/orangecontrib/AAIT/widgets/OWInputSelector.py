import os
import tempfile
import subprocess
import subprocess
import time
import uuid
from AnyQt.QtWidgets import QPushButton, QApplication
from AnyQt import uic
import ctypes
import ctypes.wintypes
from Orange.widgets.widget import OWWidget, Output, Input
from Orange.data import Table, Domain, StringVariable

class OWInputSelector(OWWidget):
    name = "Input Selector"
    description = "Select a file or a folder and assign it as a path"
    icon = "icons/in_or_out.png"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/in_or_out.png"
    gui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/ow_in_or_out_path.ui")
    priority = 10

    class Inputs:
        file_input = Input("File", Table)
        folder_input = Input("Folder", Table)

    class Outputs:
        path = Output("Path", Table)

    def __init__(self):
        super().__init__()
        self.selected_path = ""
        self.in_data = None

        # Load UI
        uic.loadUi(self.gui_path, self)

        self.file_button = self.findChild(QPushButton, 'fileButton')
        self.folder_button = self.findChild(QPushButton, 'folderButton')

        # Connect buttons
        self.file_button.clicked.connect(self.on_click_file_button)
        self.folder_button.clicked.connect(self.on_click_folder_button)

    @Inputs.file_input
    def set_file_input(self, data):
        self.in_data = data
        if data is not None:
            self.select_file()

    @Inputs.folder_input
    def set_folder_input(self, data):
        self.in_data = data
        if data is not None:
            self.select_folder()

    def on_click_file_button(self):
        self.in_data = None
        self.select_file()

    def on_click_folder_button(self):
        self.in_data = None
        self.select_folder()

    import ctypes
    import os

    import ctypes
    import ctypes.wintypes
    import time

    def select_folder_ctypes(self):
        BIF_RETURNONLYFSDIRS = 0x0001
        BIF_NEWDIALOGSTYLE = 0x0040
        MAX_PATH = 260

        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        SWP_SHOWWINDOW = 0x0040
        HWND_TOPMOST = -1

        # Structures
        class BROWSEINFO(ctypes.Structure):
            _fields_ = [
                ("hwndOwner", ctypes.wintypes.HWND),
                ("pidlRoot", ctypes.c_void_p),
                ("pszDisplayName", ctypes.c_wchar_p),
                ("lpszTitle", ctypes.c_wchar_p),
                ("ulFlags", ctypes.wintypes.UINT),
                ("lpfn", ctypes.c_void_p),
                ("lParam", ctypes.c_void_p),
                ("iImage", ctypes.wintypes.INT),
            ]

        # Fonctions Windows
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        shell32 = ctypes.windll.shell32

        SHBrowseForFolderW = shell32.SHBrowseForFolderW
        SHGetPathFromIDListW = shell32.SHGetPathFromIDListW
        CoTaskMemFree = ctypes.windll.ole32.CoTaskMemFree

        SHGetPathFromIDListW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p]
        SHGetPathFromIDListW.restype = ctypes.wintypes.BOOL
        SHBrowseForFolderW.argtypes = [ctypes.POINTER(BROWSEINFO)]
        SHBrowseForFolderW.restype = ctypes.c_void_p

        # Récupérer les fenêtres ouvertes AVANT
        hwnd_list_before = []

        def enum_windows_proc(hwnd, lParam):
            hwnd_list_before.append(hwnd)
            return True

        EnumWindows = user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
        EnumWindows(EnumWindowsProc(enum_windows_proc), 0)

        # Préparer browseinfo
        display_name_buffer = ctypes.create_unicode_buffer(MAX_PATH)

        browse_info = BROWSEINFO()
        hwnd_owner = int(self.winId())  # Si PyQt5/PyQt6
        browse_info.hwndOwner = hwnd_owner
        browse_info.pidlRoot = None
        browse_info.pszDisplayName = ctypes.cast(display_name_buffer, ctypes.c_wchar_p)
        browse_info.lpszTitle = "select a directory"
        browse_info.ulFlags = BIF_RETURNONLYFSDIRS | BIF_NEWDIALOGSTYLE
        browse_info.lpfn = None
        browse_info.lParam = None
        browse_info.iImage = 0

        # Ouvrir boîte de dialogue
        pidl = SHBrowseForFolderW(ctypes.byref(browse_info))

        # Petit délai pour être sûr que la fenêtre soit affichée
        time.sleep(0.1)

        # Récupérer les fenêtres ouvertes APRES
        hwnd_list_after = []

        def enum_windows_proc_after(hwnd, lParam):
            hwnd_list_after.append(hwnd)
            return True

        EnumWindows(EnumWindowsProc(enum_windows_proc_after), 0)

        # Détecter la nouvelle fenêtre
        new_hwnds = list(set(hwnd_list_after) - set(hwnd_list_before))

        for hwnd in new_hwnds:
            # Forcer au premier plan
            user32.SetForegroundWindow(hwnd)
            user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)

        folder_path = ""

        if pidl:
            path_buffer = ctypes.create_unicode_buffer(MAX_PATH)
            success = SHGetPathFromIDListW(pidl, path_buffer)
            if success:
                folder_path = path_buffer.value
            else:
                folder_path =""

            CoTaskMemFree(ctypes.c_void_p(pidl))
        return folder_path

    def select_file(self):
        return self.select_folder_ctypes()



    # def select_file(self):
    #     ps_code = """
    #         Add-Type -AssemblyName System.Windows.Forms
    #         Add-Type -AssemblyName System.Drawing
    #
    #         $parentForm = New-Object System.Windows.Forms.Form -Property @{
    #             Size = New-Object System.Drawing.Size(0,0)
    #             StartPosition = 'CenterScreen'
    #             TopMost = $true
    #             ShowInTaskbar = $false
    #             FormBorderStyle = 'None'
    #             Opacity = 0
    #         }
    #
    #         $openFileDialog = New-Object System.Windows.Forms.OpenFileDialog -Property @{
    #             Filter = "All files (*.*)|*.*"
    #             Multiselect = $false
    #         }
    #
    #         $result = $openFileDialog.ShowDialog($parentForm)
    #         if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
    #             $openFileDialog.FileName
    #         }
    #
    #         $parentForm.Close()
    #     """
    #
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=".ps1", mode="w", encoding="utf-8") as temp_ps1:
    #         temp_ps1.write(ps_code)
    #         temp_ps1_path = temp_ps1.name
    #
    #     try:
    #         completed = subprocess.run(
    #             ["powershell", "-ExecutionPolicy", "Bypass", "-File", temp_ps1_path],
    #             capture_output=True, text=True
    #         )
    #         file_path = completed.stdout.strip()
    #         if file_path:
    #             self.selected_path = file_path
    #             self.commit_path()
    #     finally:
    #         os.remove(temp_ps1_path)

    def select_folder(self):
        from AnyQt.QtWidgets import QFileDialog
        folder_path = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier")
        if folder_path:
            self.selected_path = folder_path
            self.commit_path()

    def commit_path(self):
        if not self.selected_path:
            return

        var = StringVariable("path")

        if self.in_data is not None:
            domain = Domain(
                self.in_data.domain.attributes,
                self.in_data.domain.class_vars,
                list(self.in_data.domain.metas) + [var]
            )
            new_table = Table.from_table(domain, self.in_data)
            new_meta_column = [self.selected_path] * len(new_table)
            new_table.metas[:, -1] = new_meta_column
        else:
            domain = Domain([], metas=[var])
            new_table = Table(domain, [[]])
            new_table.metas[0] = [self.selected_path]

        self.Outputs.path.send(new_table)

    def handleNewSignals(self):
        pass


# Test standalone
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = OWInputSelector()
    window.show()
    sys.exit(app.exec_())
