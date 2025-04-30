print('''#-----------01_Text_File----------------
"""
Hadoop is an open-source framework used for storing and processing large datasets across clusters of computers. It uses a distributed file system (HDFS) and the MapReduce programming model. Designed for scalability and fault tolerance, Hadoop enables efficient data analysis and is widely used in big data applications across industries.
"""

#01_Mapper
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    words = line.strip().split()
    for word in words:
        print(f"{word}\t1")


# ---------------01_Reducer---------------
#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

for line in sys.stdin:
    word, count = line.strip().split("\t")
    count = int(count)

    if current_word == word:
        current_count += count
    else:
        if current_word:
            print(f"{current_word}\t{current_count}")
        current_word = word
        current_count = count

if current_word == word:
    print(f"{current_word}\t{current_count}")




# ---------------02_Matrix---------------
"""
A,0,0,1
A,0,1,2
A,1,0,3
A,1,1,4
B,0,0,5
B,0,1,6
B,1,0,7
B,1,1,8

"""


# ---------------02_Mapper---------------
#!/usr/bin/env python3
import sys

# Dimensions (hardcoded or passed through env/config)
# A is m x n
# B is n x p
m = 2  # rows in A
n = 2  # cols in A / rows in B
p = 2  # cols in B

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    matrix, i, j, value = line.split(",")
    i = int(i)
    j = int(j)
    value = float(value)

    if matrix == "A":
        for col in range(p):
            # Key: i,col ; Value: A,j,value
            print(f"{i},{col}\tA,{j},{value}")
    elif matrix == "B":
        for row in range(m):
            # Key: row,j ; Value: B,i,value
            print(f"{row},{j}\tB,{i},{value}")



# ---------------02_Reducer---------------
#!/usr/bin/env python3
import sys
from collections import defaultdict

current_key = None
a_vals = defaultdict(float)
b_vals = defaultdict(float)

def emit_result(key, a_vals, b_vals):
    total = 0
    for k in a_vals:
        if k in b_vals:
            total += a_vals[k] * b_vals[k]
    print(f"{key}\t{total}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    key, val = line.split("\t")
    if key != current_key and current_key is not None:
        emit_result(current_key, a_vals, b_vals)
        a_vals.clear()
        b_vals.clear()

    current_key = key
    tag, k, v = val.split(",")
    k = int(k)
    v = float(v)

    if tag == "A":
        a_vals[k] = v
    elif tag == "B":
        b_vals[k] = v

if current_key is not None:
    emit_result(current_key, a_vals, b_vals)



#--------------- 03_CSV---------------
"""
student_id,subject,marks
8018,BI,85
8018,BDA,90
8018,CI,78
8018,DC,93
8028,BI,97
8028,BDA,99
8028,CI,95
8028,DC,90
8032,BI,86
8032,BDA,94
8032,CI,85
8032,DC,96
8034,BI,60
8034,BDA,55
8034,CI,40
8034,DC,40
8095,BI,85
8095,BDA,90
8095,CI,96
8095,DC,97
"""


# ---------------03_Mapper---------------
#!/usr/bin/env python3
import sys

# Input: student_id,subject,marks
for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("student_id"):
        continue
    student_id, subject, marks = line.split(",")
    print(f"{student_id}\t{marks}")



# ---------------03_Reducer---------------
#!/usr/bin/env python3
import sys

def get_grade(avg):
    avg = float(avg)
    if avg >= 90:
        return 'A'
    elif avg >= 80:
        return 'B'
    elif avg >= 70:
        return 'C'
    elif avg >= 60:
        return 'D'
    else:
        return 'F'

current_id = None
total = 0
count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    student_id, marks = line.split("\t")
    marks = float(marks)

    if current_id == student_id:
        total += marks
        count += 1
    else:
        if current_id:
            avg = total / count
            print(f"{current_id}\t{avg:.2f}\t{get_grade(avg)}")
        current_id = student_id
        total = marks
        count = 1

# Output for the last student
if current_id:
    avg = total / count
    print(f"{current_id}\t{avg:.2f}\t{get_grade(avg)}")
''')
