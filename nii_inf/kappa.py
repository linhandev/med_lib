import sklearn.metrics

p = "1	0	2	1	1	2	0	2	0	0	1	2	2	0	1	2	1	1	0	0	1	0	0	0	1	0	0	0	0	0	1	0	2	1	2	0	1	1	2	2	1	0	0	2	0	1	0	1	0	2	0	2	2	1	1	0	1	1	2	1	1	1	0	0	1	0	0	1	0	1"
q = "1	0	2	1	1	1	0	2	0	0	1	2	2	0	1	2	1	1	0	0	1	0	0	0	1	0	0	0	0	0	1	0	2	1	2	0	2	1	2	2	1	0	0	2	0	1	0	0	0	2	0	2	2	1	1	0	1	1	2	1	1	2	0	0	1	0	2	1	0	1"
p = p.split("\t")
p = [int(p) for p in p]
q = q.split("\t")
q = [int(q) for q in q]
print(p)
print(sklearn.metrics.cohen_kappa_score(p, q, weights="linear"))
