import pwn
from json import dumps, loads
from tqdm import trange
import numpy as np



def xor(b1, b2):
    return bytes(p^q for p, q in zip(b1, b2))



import concurrent.futures


import math

def lucb(K, delta, pull):
    # Initialize
    counts = [0] * K
    sums = [0.0] * K

    # Pull each arm once
    for i in range(K):
        r = pull(i)
        counts[i] += 1
        sums[i] += r

    t = K

    def mu(i):
        return sums[i] / counts[i]

    def beta(i, t):
        return math.sqrt((1.0 / (2 * counts[i])) *
                         math.log((math.pi**2 / 3) * K * t**2 / delta))

    conv = 0
    i_t_ = None
    while True:
        t += 2
        # Compute empirical means
        means = [mu(i) for i in range(K)]

        # Best empirical arm
        i_t = max(range(K), key=lambda i: means[i])
        if i_t_ is not None and i_t == i_t_:
            conv += 1
        else:
            conv = 0
        i_t_ = i_t

        # Upper confidence bounds
        U = [means[i] + beta(i, t) for i in range(K)]

        # Challenger: highest UCB among others
        j_t = max([j for j in range(K) if j != i_t], key=lambda j: U[j])

        # Lower bound of best arm
        L_i = means[i_t] - beta(i_t, t)

        # Stopping condition
        # print(f"{t}\t{i_t}   \t{conv}", end="\r", flush=True)
        if L_i >= U[j_t] or (conv >= 50):
            return t, i_t
        elif t > 1000:
            return -1, -1

        # Pull both arms
        for arm in [i_t, j_t]:
            r = pull(arm)
            counts[arm] += 1
            sums[arm] += r

def attack(id):
    conn = pwn.remote("socket.cryptohack.org", 13423)
    # conn = pwn.remote("localhost", 13423)
    try:
    
        def send(d: dict):
            conn.sendline(dumps(d).encode())
            m = conn.recvline()
            return loads(m)

        def unpad(i: bytes, c: bytes):
            d = send({"option": "unpad", "ct": (i+c).hex()})
            return d["result"]

            
        conn.recvline()
        msg = bytes.fromhex(send({"option": "encrypt"})["ct"])
        iv = msg[:16]
        ct = msg[16:]

        msg_hex = b""
        remaining = 12000
        for cnt in range(1, 33):
            def pull(j):
                i = b"0123456789abcdef"[j]
                hx = i.to_bytes()
                if cnt <= 16:
                    ct0 = ct[:16-cnt] + xor(xor(ct[16-cnt:16], hx+msg_hex), cnt.to_bytes()*cnt)
                    return not unpad(iv, ct0 + ct[16:])
                else:
                    iv_ = iv[:32-cnt] + xor(xor(iv[32-cnt:16], hx+msg_hex[:-16]), (cnt-16).to_bytes()*(cnt-16))
                    return not unpad(iv_, ct[:16])
                
            # rounds_left = 32 - cnt + 1
            # k = np.zeros(16)
            # n = np.zeros(16)
            # tries = int(remaining / rounds_left)
            # for t in range(tries):
            #     pass
            used, best_arm = lucb(16, 0.1, pull)
            if used == -1:
                conn.close()
                return msg_hex

            # results.append(best_arm)
            remaining -= used
            msg_hex = b"0123456789abcdef"[best_arm].to_bytes() + msg_hex
            print(int((12000-remaining) / cnt), cnt)

        result = str(send({"option": "check", "message": msg_hex.decode("ascii")}))
        if "crypto{" in result:
            while 1:
                print(result)
        conn.close()
        return result
    except:
        conn.close()
        raise Exception

def run_pool(fn, total_tasks: int, max_workers: int):
    """
    Run `fn` across `total_tasks` jobs, keeping `max_workers`
    instances running at all times until the work is exhausted.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Seed the pool with the first `max_workers` tasks
        futures = {
            executor.submit(fn, task_id): task_id
            for task_id in range(min(max_workers, total_tasks))
        }
        next_task = max_workers

        while futures:
            # Block until the next job finishes
            done, _ = concurrent.futures.wait(
                futures, return_when=concurrent.futures.FIRST_COMPLETED
            )

            for future in done:
                task_id = futures.pop(future)
                try:
                    result = future.result()
                    print(f"[done]  {result}")
                except Exception as exc:
                    print(f"[error] Task {task_id} raised: {exc}")

                # Immediately submit a replacement if work remains
                if next_task < total_tasks:
                    new_future = executor.submit(fn, next_task)
                    futures[new_future] = next_task
                    print(f"[start] Task {next_task} submitted")
                    next_task += 1


if __name__ == "__main__":
    run_pool(attack, total_tasks=1000, max_workers=50)