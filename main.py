import os
import PyPDF2
import pandas as pd
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
import logging as lg
from kivy.core.window import Window



class LaunchingApp(App):
    pass


class SearchMerge(BoxLayout):
    format = StringProperty("Enter the Format ")
    filename = StringProperty("Enter the File Name")
    file_locations = StringProperty("File Locations will be displayed here.")
    combined = StringProperty("final file name")


    def log_data(self, log, level):
        """
        Description:
            This function is used for setting up the logging process

        Input:
            Nothing.

        Output:
            returns a logging object which can be used for creating the various users logs.
        """
        for handler in lg.root.handlers[:]:
            lg.root.removeHandler(handler)
        # changing To current directory.
        os.chdir(os.getcwd())
        print(os.getcwd())
        lg.basicConfig(filename="programFlowData.log", level=lg.INFO,
                       format="%(name)s %(asctime)s %(levelname)s %(message)s", filemode="a")
        if level == 'info':
            lg.info(log)
        if level == "error":
            lg.error(log)
        if level == "warning":
            lg.warning(log)
    def merge_app(self):
        """
        Description:
            This will take the extension name and returns
            the single file containing the data of all the files with the extension mentioned
            from the Documents directory.
        Input:
            Takes extension in text format
        Output:
            File Containing the Merged data of all the file of Same extension.
        """
        # logging variable for merge_operations



        # input
        extension = self.ids.input.text.strip().lower()

        extension = extension.replace(extension, str("." + extension))

        self.log_data("Passed File format: {0} ".format(extension), "info")

        file_obj = open('Combined' + extension, 'ab')
        merge_obj = PyPDF2.PdfFileMerger()
        excel_data = pd.DataFrame()

        for (root, _, files) in os.walk(os.getenv('HOME') + os.sep + "Documents", topdown=True):

            if 'anaconda3' in root or 'PycharmProjects' in root:
                continue

            else:
                try:
                    for file in files:
                        if file.endswith(extension):

                            pdf_file = PyPDF2.PdfFileReader(r'' + root + os.sep + file, 'rb')
                            merge_obj.append(pdf_file)

                        elif file.endswith(extension):
                            excel_data = excel_data.append(root + os.sep + file, ignore_index=True)

                        else:
                            with open(r'' + root + os.sep + file, 'rb') as data_obj:
                                file_obj.write(data_obj.read())
                except FileNotFoundError:
                    self.log_data("Broken file Exists: \n Location with  ", "error")
                    reference = root + os.sep + file
                    self.log_data("Location where file is Broken: " + reference, "error")
                    continue
                except MemoryError:
                    self.log_data("MemoryError: ".format(MemoryError), "error")
                    break
                except Exception as e:
                    self.log_data("Exception Raised: {0}".format(e), "error")

        file_obj.close()
        merge_obj.write("Combined.pdf")
        merge_obj.close()
        excel_data.to_excel('Combined.xlsx')
        list_of_files = list(os.listdir())
        list_of_files = os.listdir()
        files_to_be_not_removed = ['sample.py', 'launching.kv', 'main.py', 'venv', '.idea', '.git', 'requirements.txt',
                                   "Combined" + extension, "programFlowData.log"]

        for file in files_to_be_not_removed:
            list_of_files.remove(file)

        for file in list_of_files:
            os.system("rm -r " + file)
        self.log_data("File name Saved {0} ".format("Combined" + extension), "info")

        self.combined = "Combined" + extension

    def search_app(self):
        """
        Description:
            This function takes the filename and searches over all the directories
            starting from the root directory.
        Input:
            Nothing.
        Output:
            returns list of folder locations
        """

        locations = []
        filename = self.ids.input1.text.strip()
        self.log_data("File name or reference for file searching: {0}".format(filename), "info")
        try:
            for (root, _, files) in os.walk(os.getenv('HOME'), topdown=True):
                for file in files:
                    if filename in file:
                        pointing = "==> " + root + "\n"
                        locations.append(pointing)

        except Exception as e:
            self.log_data("Exception: {0}".format(e))

        self.file_locations = "\n".join(list(set(locations)))
        self.log_data(self.file_locations, "info")


if __name__ == '__main__':
    Window.clearcolor = (0, 1, 0, 0.2)
    LaunchingApp().run()

