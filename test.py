import dataclasses
import random
import uuid

import requests
from codetiming import Timer
from tqdm import tqdm


@dataclasses.dataclass
class Payload:
    step: int
    sketch : int
    payload: list


steps = [1, 10, 100]
sketches = [1, 10, 100]
payloads = []


for step in steps:
    for sketch in sketches:
        hll_sketches = {}
        for _ in tqdm(range(step)):
            key = uuid.uuid4().hex
            random_int = random.randint(1,50000)
            value = {str(i) for i in range(1, random_int)}
            hll_sketches[key] = value


        payloads.append(Payload(step=step, sketch=sketch, payload=[
            {
                "key": uuid.uuid4().hex,
                "sketches": list(hll_sketches)
            } for _ in range(sketch)

        ]))

for payload in payloads:
    timer = Timer(name="timer")
    timer.start()
    r = requests.post("http://0.0.0.0:8080/count/", json=payload.payload)
    timer.stop()
    print(f"Step: {payload.step}, sketch: {payload.sketch}, seconds: {timer.last}")
    assert r.status_code == 200
    print(r.json()[-1])
