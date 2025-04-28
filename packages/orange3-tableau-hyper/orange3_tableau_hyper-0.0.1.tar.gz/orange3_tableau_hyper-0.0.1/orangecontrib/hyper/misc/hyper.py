from Orange.data.io import FileFormat
from Orange.data.pandas_compat import table_from_frame, table_to_frame
import warnings
import pantab

class HyperReader(FileFormat):
    EXTENSIONS = ('.hyper',)
    DESCRIPTION = 'Tableau Hyper file'
    SUPPORT_COMPRESSED = False
    SUPPORT_SPARSE_DATA = False

    def read(self):
        if pantab is None:
            raise ImportError(
                "pantab is required to read Hyper files. Install it with 'pip install pantab'."
            )

        try:
            dfs = pantab.frames_from_hyper(self.filename)
            table_name = list(dfs.keys())[0]
            return table_from_frame(dfs[table_name])
        except Exception as e:
            raise IOError(f"Failed to read Hyper file '{self.filename}': {e}")

    @classmethod
    def write_file(cls, filename, data):
        try:
            df = table_to_frame(data, include_metas=True)
            pantab.frame_to_hyper(df, filename, table="table")
        except Exception as e:
            raise IOError(f"Failed to write Hyper file '{filename}': {e}")
