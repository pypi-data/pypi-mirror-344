import os
import pickle
import threading
from pathlib import Path

from saved_instance.db.sqllite_repo import SqliteRepo


def test_sqlite_repo():
    sr = SqliteRepo(Path("saved_instance_global.svd"))
    p_val = pickle.dumps(1)
    sr.write("dict", p_val)
    val = sr.read("dict")
    print(pickle.loads(val))


def worker(repo: SqliteRepo, thread_id: int):
    key = f"thread_{thread_id}"
    value = {"id": thread_id, "message": f"Hello from thread {thread_id}"}
    try:
        # print(f"Value: {value}")
        repo.write(key, value)
        read_back = repo.read(key)
        print(value)
        print(f"[{key}] Read Back:", read_back)
        if read_back != value:
            print(f"[❌] Mismatch! Thread {thread_id}: wrote {value}, read {read_back}")
    except Exception as e:
        print(f"[💥] Exception in thread {thread_id}: {e}")

    # assert read_back == value, f"thread {thread_id} data mismatch!"
_thread_lock = threading.Lock()

def multi_thread_test():
    db = "saved_instance_global.db"
    try:
        os.remove(db)
    except FileNotFoundError:
        pass

    threads = []
    ms = SqliteRepo(Path(db), lock=_thread_lock)
    for i in range(3):
        t = threading.Thread(target=worker, args=(ms, i))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    multi_thread_test()