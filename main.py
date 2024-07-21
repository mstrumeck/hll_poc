import binascii

import robyn
from robyn import Robyn
from HLL import HyperLogLog
from dataclasses import dataclass, asdict
import orjson

app = Robyn(__file__)

@dataclass
class Counter:
    key: str
    value: int


@app.post("/count")
async def handler(request: robyn.Request):
    sketch_groups = orjson.loads(request.body)
    counters = []

    if not sketch_groups:
        return robyn.jsonify(counters)

    total_hll = HyperLogLog(14)

    for sketch_group in sketch_groups:
        group_hll = HyperLogLog(14)

        for sketch in sketch_group['sketches']:
            try:
                parsed_sketch = binascii.unhexlify(sketch)
                group_hll.add(parsed_sketch)
            except ValueError:
                return robyn.jsonify({"error": "Cannot calculate!"})

        total_hll.merge(group_hll)
        counter = Counter(key=sketch_group['key'], value=int(group_hll.cardinality()))
        counters.append(asdict(counter))

    total_counter = Counter(key="_total", value=int(total_hll.cardinality()))
    counters.append(asdict(total_counter))

    return robyn.jsonify(counters)

app.start(port=8080, host="0.0.0.0")