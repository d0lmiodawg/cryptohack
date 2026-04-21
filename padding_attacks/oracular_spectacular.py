import pwn
from json import dumps, loads
from tqdm import trange



def xor(b1, b2):
    return bytes(p^q for p, q in zip(b1, b2))



    

import concurrent.futures
import time
import random


import numpy as np
from math import log, sqrt

def beta(n, delta_eff):
    """Simpler, tighter confidence radius."""
    if n == 0:
        return float('inf')
    return sqrt(log(1 / delta_eff) / (2 * n))

def lucb_round(query_fn, K=16, delta=0.05, max_queries=1000, warmup=5):
    # Warm start
    pulls = np.full(K, warmup, dtype=int)
    sums = np.zeros(K)
    for i in range(K):
        for _ in range(warmup):
            sums[i] += query_fn(i)
    t = K * warmup
    
    # Effective per-arm, per-step failure prob (union bound)
    # delta_eff ~ delta / (K * expected_steps). Use a loose estimate.
    delta_eff = delta / (K * 10)
    
    while t < max_queries-1:
        means = sums / pulls
        radii = np.array([beta(pulls[i], delta_eff) for i in range(K)])
        
        lcb = means - radii
        ucb = means + radii
        
        h = int(np.argmin(means))
        lcb_others = lcb.copy()
        lcb_others[h] = np.inf
        l = int(np.argmin(lcb_others))
        
        # Stop when challenger's LCB exceeds leader's UCB
        if lcb[l] >= ucb[h]:
            return h, t
        
        sums[h] += query_fn(h); pulls[h] += 1
        sums[l] += query_fn(l); pulls[l] += 1
        t += 2
    
    return int(np.argmin(sums / pulls)), t


def attack():
    conn = pwn.remote("socket.cryptohack.org", 13423)
    
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
                return unpad(iv, ct0 + ct[16:])
            else:
                iv_ = iv[:16-cnt] + xor(xor(iv[16-cnt:16], hx+msg_hex[:-16]), cnt.to_bytes()*cnt)
                return unpad(iv_, ct[:16])
            
        rounds_left = 32 - cnt + 1
        soft_cap = min(remaining, int(3 * remaining / rounds_left))
        
        best_arm, used = lucb_round(
            pull, K=16, delta=0.05, max_queries=12000/32#soft_cap
        )
        # results.append(best_arm)
        remaining -= used
        msg_hex = b"0123456789abcdef"[best_arm].to_bytes() + msg_hex
        print(12000-remaining, cnt, msg_hex)


    print(send({"option": "check", "message": msg_hex.decode("ascii")}))

def solve_all_rounds(query_fns, total_budget=12000, n_rounds=32, K=16):
    """query_fns: list of 32 callables, each taking arm_idx."""
    results = []
    remaining = total_budget
    
    for r in range(n_rounds):
        rounds_left = n_rounds - r
        soft_cap = min(remaining, int(3 * remaining / rounds_left))
        
        best_arm, used = lucb_round(
            query_fns[r], K=K, delta=0.0016, max_queries=soft_cap
        )
        results.append(best_arm)
        remaining -= used
    
    return results

attack()