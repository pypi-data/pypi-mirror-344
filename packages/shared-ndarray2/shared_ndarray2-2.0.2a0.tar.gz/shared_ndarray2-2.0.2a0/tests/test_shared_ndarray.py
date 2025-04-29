import multiprocessing
from multiprocessing.managers import SharedMemoryManager
from multiprocessing.shared_memory import SharedMemory

import numpy as np
import pytest

from shared_ndarray2 import SharedNDArray, shared_ndarray


def test_main_constructor():
    x = np.arange(1024)
    shm = SharedMemory(name="x", create=True, size=x.nbytes)
    # Test the basic constructor
    arr = SharedNDArray(shm, x.shape, x.dtype)
    assert arr.shm is shm
    assert arr.dtype is x.dtype
    assert arr.shape == x.shape
    # Test that the shape must match
    with pytest.raises(ValueError):
        _ = SharedNDArray(shm, (1023,), x.dtype)
    shm.close()
    shm.unlink()


def test_from_shape_constructor():
    x = np.arange(1024)
    with SharedMemoryManager() as mem_mgr:
        arr = shared_ndarray.from_shape(mem_mgr, x.shape, x.dtype)
        assert arr.dtype is x.dtype
        assert arr.shm.size == x.nbytes
        assert arr.shape == x.shape


def test_from_array_constructor():
    x = np.arange(1024)
    with SharedMemoryManager() as mem_mgr:
        arr = shared_ndarray.from_array(mem_mgr, x)
        assert arr.dtype is x.dtype
        assert arr.shm.size == x.nbytes
        assert arr.shape == x.shape
        assert all(arr[:] == x[:])


def test_modify_shape():
    x = np.arange(1024)
    with SharedMemoryManager() as mem_mgr:
        arr = shared_ndarray.from_array(mem_mgr, x)
        arr.shape = (8, 128)  # expect no error
        assert arr.shape == (8, 128)
        arr.shape = (2, -1)
        assert arr.shape == (2, 512)
        with pytest.raises(ValueError):
            arr.shape = (7, 128)


def test_single_mp_proc():
    data = np.arange(1024, dtype=np.int16)

    def add_ten(arr: SharedNDArray):
        arr[:] += 10

    with SharedMemoryManager() as shmem_mgr:
        shared_arr = shared_ndarray.from_array(shmem_mgr, data)
        proc = multiprocessing.Process(target=add_ten, args=(shared_arr,))
        proc.start()
        proc.join()
        assert all(shared_arr.get() == data + 10)
