```Python
from btree import BTreeSet

t = BTreeSet()

# add some values
for i in range(30):
    t.add(i)

# duplicates are ignored
for i in range(30):
    t.add(i)

# remove some values
for i in range(5, 10):
    t.remove(i)

# print tree as nested lists
print(t)
# BTreeSet([[[0, 1, 2],3,[4, 10],11,[12, 13],14,[15, 16]],17,[[18, 19],20,[21, 22],23,[24, 25],26,[27, 28, 29]]])

# print values as list
print(list(t))
# [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]

# print smallest value
print(t.min())
# 0

# print largest value
print(t.max())
# 29

# print if 4 is in tree
print(4 in t)
# True

# print if 5 is in tree
print(5 in t)
# False
```
