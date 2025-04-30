print('''
1 su hduser 
2 cd
3 start-dfs.sh 
4 start-yarn.sh 
5 jps 
6 ls
7 nano matrix.txt 
{ 
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
}
8 cat matrix.txt 
9hadoop fs -ls / 
10  hadoop fs -mkdir /
 mapreduce_matrix_multiplication 
11  hadoop fs -ls / 
12  hadoop fs -put matrix.txt /mapreduce_matrix_multiplication
13 hadoop fs -ls /mapreduce_matrix_multiplication
14 hadoop fs -cat /mapreduce_matrix_multiplication/matrix.txt
15 nano mapper_matrix.py 
{ 
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
            print(f"{i},{col}	A,{j},{value}")
    elif matrix == "B":
        for row in range(m):
            # Key: row,j ; Value: B,i,value
            print(f"{row},{j}	B,{i},{value}")
}
16 nano reducer_matrix.py 
{ 
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
    print(f"{key}	{total}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    key, val = line.split("	")
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
} 
17  chmod +x mapper_matrix.py 
18  chmod +x reducer_matrix.py
19   new terminal 
      su hduser 
20 cd 
21  cd /usr/local/hadoop/share/hadoop/tools/lib
22  pwd 
out - /usr/local/hadoop/share/hadoop/tools/lib 
23 back to 
   usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar 
26 hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar 
-input /mapreduce_matrix_multiplication/matrix.txt 
-output /output_matrix -mapper /home/hduser/mapper_matrix.py 
-reducer /home/hduser/reducer_matrix.py 
27  hadoop fs -ls /output_matrix 
28  hadoop fs -cat /output_matrix/part-00000 
      ''')
