from defusedxml.ElementTree import parse
from datetime import datetime, timedelta


def process_cluster(cluster):
    start_time = min(datetime.fromisoformat(x.attrib["start-time"]) for x in cluster)
    end_time = max(datetime.fromisoformat(x.attrib["end-time"]) for x in cluster)
    pass_len = (end_time - start_time).total_seconds()

    try:
        rec_start_time = min((datetime.fromisoformat(elt.attrib["start-time"])
                             for elt in cluster if elt.attrib["rec"] == "True"))
        rec_end_time = min((datetime.fromisoformat(elt.attrib["end-time"])
                             for elt in cluster if elt.attrib["rec"] == "True"))
    except ValueError:
        return 0, pass_len
    return (rec_end_time - rec_start_time).total_seconds(), pass_len

root = parse("sortedallres")

prev_start_time = datetime(1970, 1, 1)
prev_end_time = datetime(1970, 1, 1)
cluster = []
res = []

for pass_elt in root.iter():
    if pass_elt.tag == "xml":
        continue
    start_time = datetime.fromisoformat(pass_elt.attrib["start-time"])

    if start_time - prev_start_time < timedelta(minutes=10):
        cluster.append(pass_elt)
    else:
        # do the computation on the previous cluster
        if cluster:
            res.append(process_cluster(cluster))
        prev_start_time = start_time
        cluster = [pass_elt]

print(f"{len(res)} passes in sight")
print(f"{len([x for x in res if x[0] != 0])} passes received")
print(f"{sum([x[0] for x in res])} seconds received")
print(f"{sum([x[1] for x in res])} out of seconds in sight")
print(f"{sum([x[1] for x in res if x[0] != 0])} out of seconds in sight for received passes")





