import numpy as np

p = """1
0
1
0
0
1
0
1
0
0
1
1
1
0
1
1
1
1
0
0
1
0
0
0
1
0
0
0
0
0
1
0
1
1
1
0
1
1
1
1
1
0
0
1
0
1
0
1
0
1
0
1
1
1
1
0
1
1
1
1
1
1
0
0
1
0
0
1
0
1
"""
q = """1
0
1
1
1
1
0
1
0
0
1
1
1
0
1
1
1
1
0
0
1
0
0
0
1
0
0
0
0
0
1
0
1
1
1
0
1
1
1
1
1
0
0
1
0
1
0
0
0
1
0
1
1
1
1
0
1
1
1
1
1
1
0
0
1
0
1
1
0
1
"""
p = p.split("\n")
q = q.split("\n")
print(p, q)
p = [int(t) for t in p if len(t) != 0]
q = [int(t) for t in q if len(t) != 0]
print(p)

#
# # true positive
# TP = np.sum(np.logical_and(np.equal(y_true, 1), np.equal(y_pred, 1)))
# print(TP)
#
# # false positive
# FP = np.sum(np.logical_and(np.equal(y_true, 0), np.equal(y_pred, 1)))
# print(FP)
#
# # true negative
# TN = np.sum(np.logical_and(np.equal(y_true, 1), np.equal(y_pred, 0)))
# print(TN)
#
# # false negative
# FN = np.sum(np.logical_and(np.equal(y_true, 0), np.equal(y_pred, 0)))
# print(FN)
