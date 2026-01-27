from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from typing import Optional, Iterator, TextIO


class DatasetChangedError(RuntimeError):
    pass


@dataclass(frozen=True)
class Checkpoint:
    """
    Snapshot of iterator state.
    - offset is a byte offset in the file
    - lineno is a logical line counter (debug / metrics)
    - size+mtime_ns is a lightweight fingerprint to detect file changes
    """
    path: str
    offset: int
    lineno: int
    size: int
    mtime_ns: int

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @staticmethod
    def from_json(s: str) -> "Checkpoint":
        d = json.loads(s)
        return Checkpoint(**d)


class ResumableFileIterator(Iterator[str]):
    """
    Resumable iterator over a large newline-delimited file.

    Streaming: reads one line at a time (O(1) memory).
    Resumable: stores file byte offset in a Checkpoint.
    Safe: detects dataset changes between pause/resume using stat fingerprint.
    """

    def __init__(self, path: str) -> None:
        self._path = path
        self._fh: Optional[TextIO] = None
        self._offset: int = 0
        self._lineno: int = 0

    # ---------- internal helpers ----------

    def _open(self) -> None:
        if self._fh is None:
            # newline="" keeps newline handling consistent for tell()/seek() in text mode
            self._fh = open(self._path, "r", encoding="utf-8", newline="")

    def _stat(self) -> tuple[int, int]:
        st = os.stat(self._path)
        return st.st_size, st.st_mtime_ns

    # ---------- iterator protocol ----------

    def __iter__(self) -> "ResumableFileIterator":
        return self

    def __next__(self) -> str:
        self._open()
        assert self._fh is not None

        # Ensure file cursor matches our tracked offset
        self._fh.seek(self._offset)

        line = self._fh.readline()
        if line == "":
            # EOF: we are "done"; offset remains at EOF
            raise StopIteration

        # Update state
        self._offset = self._fh.tell()
        self._lineno += 1
        return line.rstrip("\n")

    # Explicit next() method (work-like interface)
    def next(self) -> str:
        return self.__next__()

    # ---------- pause / resume / position ----------

    def position(self) -> Checkpoint:
        """
        Return a checkpoint representing the current state.
        Safe to call anytime.
        """
        size, mtime_ns = self._stat()
        return Checkpoint(
            path=self._path,
            offset=self._offset,
            lineno=self._lineno,
            size=size,
            mtime_ns=mtime_ns,
        )

    def pause(self) -> Checkpoint:
        """
        Pause is just "take a checkpoint snapshot".
        """
        return self.position()

    def resume(self, ckpt: Checkpoint) -> None:
        """
        Resume from a checkpoint. Detects dataset changes.
        """
        if ckpt.path != self._path:
            raise ValueError(f"Checkpoint path mismatch: {ckpt.path} != {self._path}")
        if ckpt.offset < 0 or ckpt.lineno < 0:
            raise ValueError("Invalid checkpoint: negative offset/lineno.")

        # Detect file changes
        size, mtime_ns = self._stat()
        if (size, mtime_ns) != (ckpt.size, ckpt.mtime_ns):
            raise DatasetChangedError(
                "Dataset changed since checkpoint. "
                f"Expected size={ckpt.size}, mtime_ns={ckpt.mtime_ns}; "
                f"got size={size}, mtime_ns={mtime_ns}."
            )

        # Restore state
        self._open()
        assert self._fh is not None
        self._fh.seek(ckpt.offset)

        self._offset = ckpt.offset
        self._lineno = ckpt.lineno

    # ---------- persistence helpers ----------

    def serialize_checkpoint(self) -> str:
        return self.position().to_json()

    @staticmethod
    def load_checkpoint(s: str) -> Checkpoint:
        return Checkpoint.from_json(s)

    # ---------- cleanup ----------

    def close(self) -> None:
        if self._fh is not None:
            self._fh.close()
            self._fh = None

if __name__ == "__main__":
    it = ResumableFileIterator("big_dataset.csv")

    print(it.next())  # line 1
    print(it.next())  # line 2

    ckpt = it.pause()
    ckpt_json = ckpt.to_json()

    it.close()

    # Later...
    it2 = ResumableFileIterator("big_dataset.csv")
    it2.resume(Checkpoint.from_json(ckpt_json))

    print(it2.next())  # continues where it left off
    it2.close()