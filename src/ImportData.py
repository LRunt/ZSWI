import json
import zipfile


class ImportData():

    def __init__(self):
        super(self).__init__()

    """
    Metoda necita data z JSONU, at kompresovana nebo normalni 
    @return data from JSON
    """

    def load_data(path):
        if path.endswith(".zip"):
            with zipfile.ZipFile(path) as zf:
                jsonstring = zf.read(zf.filelist[0]).decode('utf-8')
            data = json.loads(jsonstring)
        else:
            with open(path, 'r') as json_file:
                data = json.load(json_file)
        return data