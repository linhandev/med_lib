from scipy import stats
from collections import defaultdict


with open("/home/lin/Desktop/stata.csv") as f:
    lines = f.readlines()
    lines = [l.split(",") for l in lines if len(l[1]) != 0]
    print(lines[0])
with open("/home/lin/Desktop/train.txt") as f:
    train_names = f.readlines()
    train_names = [l.rstrip("\n") for l in train_names]
# print(train_names)

with open("/home/lin/Desktop/int.txt") as f:
    int_names = f.readlines()
    int_names = [l.rstrip("\n") for l in int_names]
# print(int_names)

with open("/home/lin/Desktop/ext.txt") as f:
    ext_names = f.readlines()
    ext_names = [l.rstrip("\n") for l in ext_names]
# print(ext_names)


ages = {}
for l in lines:
    if len(l[3]) != 0:
        ages[l[0]] = int(l[3])
all_ages = [int(l[3]) for l in lines if len(l[3]) != 0]
# print(all_ages)


train_ages = []
for n in train_names:
    train_ages.append(ages[n])
# print(train_ages)

int_ages = []
for n in int_names:
    int_ages.append(ages[n])
# print(int_ages)

ext_ages = []
for n in ext_names:
    ext_ages.append(ages[n])
# print(ext_ages)

print("年龄 levene检验，检验两总体是否具有方差齐性")
print(stats.levene(all_ages, train_ages))
print(stats.levene(all_ages, int_ages))
print(stats.levene(all_ages, ext_ages))

print("年龄 T检验")
print(stats.ttest_ind(all_ages, train_ages))
print(stats.ttest_ind(all_ages, int_ages))
print(stats.ttest_ind(all_ages, ext_ages))

# obs = [102, 102, 96, 105, 95, 100]
# exp = [100, 100, 100, 100, 100, 100]


genders = [l[4] for l in lines if len(l[4]) != 0]
# print(genders)

gender = {}
for l in lines:
    if len(l[4]) != 0:
        gender[l[0]] = l[4]
# print(gender)


train_genders = []
for n in train_names:
    train_genders.append(gender[n])
# print(train_genders)

int_genders = []
for n in int_names:
    int_genders.append(gender[n])
# print(int_genders)

ext_genders = []
for n in ext_names:
    ext_genders.append(gender[n])
# print(ext_genders)


def count(data):
    counts = defaultdict(lambda: 0)
    for d in data:
        counts[d] += 1
    return [(k, counts[k]) for k in sorted(counts)]


# print(count(genders))
# print(count(train_genders))
# print(count(int_genders))
# print(count(ext_genders))
print("性别卡方检验")
print(stats.chisquare([t[1] for t in count(genders)], f_exp=[t[1] for t in count(train_genders)]))
print(stats.chisquare([t[1] for t in count(genders)], f_exp=[t[1] for t in count(int_genders)]))
print(stats.chisquare([t[1] for t in count(genders)], f_exp=[t[1] for t in count(ext_genders)]))


facs = [l[7] for l in lines if len(l[7]) != 0]
# print(facs)


fac = {}
for l in lines:
    if len(l[7]) != 0:
        fac[l[0]] = l[7]
# print(fac)


train_facs = []
for n in train_names:
    train_facs.append(fac[n])
# print(train_facs)

int_facs = []
for n in int_names:
    int_facs.append(fac[n])
# print(int_facs)

ext_facs = []
for n in ext_names:
    ext_facs.append(fac[n])
# print(ext_facs)


print("厂商卡方检验")
print(stats.chisquare([t[1] for t in count(facs)], f_exp=[t[1] for t in count(train_facs)]))
print(stats.chisquare([t[1] for t in count(facs)], f_exp=[t[1] for t in count(int_facs)]))
print(stats.chisquare([t[1] for t in count(facs)], f_exp=[t[1] for t in count(ext_facs)]))
