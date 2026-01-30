import dill as pickle
import zstandard as zstd
import errno
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from contextlib import contextmanager


@contextmanager
def safe_write(path):
    """
    Context manager to write a file in two steps: first use a tmp file,
    then rename the file if everything went well.
    In case of error, the temp file is deleted.
    """
    path = Path(path)
    with NamedTemporaryFile(mode="wb", dir=path.parent, delete=False) as tmpfile:
        tmp_path = Path(tmpfile.name)
        try:
            yield tmpfile
            # Proper closure of temp file
            tmpfile.close()
            # Atomic renaming
            tmp_path.replace(path)
        except Exception:
            # Error => delete the temp file
            if tmp_path.exists():
                tmp_path.unlink()
            raise  # Propagate error


class MixInIO:
    """
    Provide basic save/load capacities to other classes.
    """

    def dump(
        self, filename: str, path=".", overwrite=False, compress=True, stemize=True
    ):
        """
        Save instance to file.

        Parameters
        ----------
        filename: str
            The stem of the filename.
        path: :py:class:`str` or :py:class:`~pathlib.Path`, optional
            The location path.
        overwrite: bool, default=False
            Should existing file be erased if it exists?
        compress: bool, default=True
            Should Zstd compression be used?
        stemize: bool, default=True
            Trim any extension (e.g. .xxx)

        Examples
        ----------

        >>> import tempfile
        >>> v1 = ToyClass(42)
        >>> v2 = ToyClass()
        >>> v2.value
        0
        >>> with tempfile.TemporaryDirectory() as tmpdirname:
        ...     v1.dump(filename='myfile', compress=True, path=tmpdirname)
        ...     dir_content = [file.name for file in Path(tmpdirname).glob('*')]
        ...     v2 = ToyClass.load(filename='myfile', path=Path(tmpdirname))
        ...     v1.dump(filename='myfile', compress=True, path=tmpdirname) # doctest.ELLIPSIS
        File ...myfile.pkl.zst already exists! Use overwrite option to overwrite.
        >>> dir_content
        ['myfile.pkl.zst']
        >>> v2.value
        42

        >>> with tempfile.TemporaryDirectory() as tmpdirname:
        ...     v1.dump(filename='myfile', compress=False, path=tmpdirname)
        ...     v1.dump(filename='myfile', compress=False, path=tmpdirname) # doctest.ELLIPSIS
        File ...myfile.pkl already exists! Use overwrite option to overwrite.

        >>> v1.value = 51
        >>> with tempfile.TemporaryDirectory() as tmpdirname:
        ...     v1.dump(filename='myfile', path=tmpdirname, compress=False)
        ...     v1.dump(filename='myfile', path=tmpdirname, overwrite=True, compress=False)
        ...     v2 = ToyClass.load(filename='myfile', path=tmpdirname)
        ...     dir_content = [file.name for file in Path(tmpdirname).glob('*')]
        >>> dir_content
        ['myfile.pkl']
        >>> v2.value
        51

        >>> with tempfile.TemporaryDirectory() as tmpdirname:
        ...    v2 = ToyClass.load(filename='thisfilenamedoesnotexist')
        Traceback (most recent call last):
         ...
        FileNotFoundError: [Errno 2] No such file or directory: ...
        """
        path = Path(path)
        fn = Path(filename)
        if stemize:
            fn = Path(fn.stem)
        if compress:
            destination = path / (fn.name + ".pkl.zst")
            if destination.exists() and not overwrite:
                print(
                    f"File {destination} already exists! Use overwrite option to overwrite."
                )
            else:
                with safe_write(destination) as f:
                    cctx = zstd.ZstdCompressor(level=3)
                    with cctx.stream_writer(f) as z:
                        pickle.dump(self, z, protocol=5)
        else:
            destination = path / (fn.name + ".pkl")
            if destination.exists() and not overwrite:
                print(
                    f"File {destination} already exists! Use overwrite option to overwrite."
                )
            else:
                with safe_write(destination) as f:
                    pickle.dump(self, f)

    @classmethod
    def load(cls, filename: str, path="."):
        """
        Load instance from file.

        Parameters
        ----------
        filename: str
            The stem of the filename.
        path: :py:class:`str` or :py:class:`~pathlib.Path`, optional
            The location path.
        """
        path = Path(path)
        dest = path / Path(filename).with_suffix(".pkl")
        if dest.exists():
            with open(dest, "rb") as f:
                return pickle.load(f)
        else:
            dest = dest.with_suffix(".pkl.zst")
            if dest.exists():
                dctx = zstd.ZstdDecompressor()
                # Load compressed data
                with open(dest, "rb") as f, dctx.stream_reader(f) as z:
                    return pickle.load(z)
            else:
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), dest)


class ToyClass(MixInIO):
    def __init__(self, value=0):
        self.value = value
