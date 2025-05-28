import sys
sys.stderr = open("error_log.txt", "w")
sys.stdout = open("output_log.txt", "w")

from ui.main_window import BGRemoverApp

if __name__ == "__main__":
    app = BGRemoverApp()
    app.mainloop()