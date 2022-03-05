import os
import PyPDF2
import pandas as pd
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout



class LaunchingApp(App):
    pass


class SearchMerge(BoxLayout):
    format = StringProperty("Enter the Format ")
    filename = StringProperty("Enter the File Name")
    file_locations = StringProperty("File Locations will be displayed here.")
    combined = StringProperty("final file name")

    def merge_app(self):
        file_format = self.ids.input.text
        print(file_format)
        filename = self.merge(file_format)
        print(filename)
        self.combined = filename

    def search_app(self):
        file_name = self.ids.input1.text
        print(file_name)
        data = self.search(file_name)
        print(data)
        self.file_locations ="\n".join(data)
        print(self.file_locations)

    def merge(self, file_format):
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

        # input
        extension = file_format.strip().lower()
        extension = extension.replace(extension, str("." + extension))

        file_obj = open('Combined' + extension, 'ab')
        merge_obj = PyPDF2.PdfFileMerger()
        excel_data = pd.DataFrame()
        print()

        for (root, _, files) in os.walk(os.getenv('HOME')+os.sep+"Documents", topdown=True):

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
                    print("Broken file Exists: \n Location with  ")
                    reference = root + os.sep + file
                    print(reference)
                    continue
                except MemoryError:
                    print(MemoryError)
                    break
                except Exception:
                    continue

        file_obj.close()
        merge_obj.write("Combined.pdf")
        merge_obj.close()
        excel_data.to_excel('Combined.xlsx')
        list_of_files = list(os.listdir())
        list_of_files = os.listdir()
        files_to_be_not_removed = ['sample.py', 'launching.kv', 'main.py', 'venv', '.idea', '.git', 'requirements.txt',
                                   "Combined" + extension]

        for file in files_to_be_not_removed:
            list_of_files.remove(file)

        for file in list_of_files:
            print
            os.system("rm -r " + file)

        return "Combined"+extension

    def search(self, file_name):
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
        filename = file_name.strip()
        for (root, _, files) in os.walk(os.getenv('HOME'), topdown=True):
            for file in files:
                if filename in file:
                    locations.append(root)
        return list(set(locations))


if __name__ == '__main__':
    LaunchingApp().run()
