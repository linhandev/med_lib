import requests
import os
from multiprocessing import Process


def download(workerid):
    img_url = "http://lalalayl.top/uploads/allimg/20201129/6c830b507b1f4ab31979b0092483b566.png"
    for ind in range(10000):
        res = requests.get(img_url)
        print(workerid, ind)

        with open("../{}.png".format(workerid), "wb") as f:
            f.write(res.content)


ps = []
for ind in range(8):
    ps.append(Process(target=download, args=(ind,)))
    ps[-1].start()
