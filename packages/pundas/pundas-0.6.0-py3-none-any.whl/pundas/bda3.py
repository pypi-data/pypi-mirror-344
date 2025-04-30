print('''
1 su hduser 
2 cd 
3 start-dfs.sh 
4 start-yarn.sh 
5 jps
6 ls
7   nano student_marks.csv 
{ 
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
}
8 cat student_marks.csv 
9   hadoop fs -mkdir /mapreduce_student_grade
10 hadoop fs -ls /
11 hadoop fs -put student_marks.csv /mapreduce_student_grade 
12  hadoop fs -ls /mapreduce_student_grade
13  hadoop fs -cat /mapreduce_student_grade/student_marks.csv 
14 nano mapper_student_grade.py 
{ 
# ---------------03_Mapper---------------
#!/usr/bin/env python3
import sys

# Input: student_id,subject,marks
for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("student_id"):
        continue
    student_id, subject, marks = line.split(",")
    print(f"{student_id}	{marks}")
}
15 nano reducer_student_grade.py
{ 
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
    student_id, marks = line.split("	")
    marks = float(marks)

    if current_id == student_id:
        total += marks
        count += 1
    else:
        if current_id:
            avg = total / count
            print(f"{current_id}	{avg:.2f}	{get_grade(avg)}")
        current_id = student_id
        total = marks
        count = 1

# Output for the last student
if current_id:
    avg = total / count
    print(f"{current_id}	{avg:.2f}	{get_grade(avg)}")
}

16 chmod +x mapper_student_grade.py 
17 chmod +x reducer_student_grade.py
18 new terminal 
su hduser 
19 cd
20 cd /usr/local/hadoop/share/hadoop/tools/lib 
21 ls
22 pwd 
out - /usr/local/hadoop/share/hadoop/tools/lib 
23 back terminal 
   /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar
24 hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar 
-input /mapreduce_student_grade/student_marks.csv -output /output_student_grade  
-mapper /home/hduser/mapper_student_grade.py -reducer /home/hduser/reducer_student_grade.py 
25 hadoop fs -ls /output_student_grade
26  hadoop fs -cat /output_student_grade/part-00000
27 stop-dfs.sh 
28 stop-yarn.sh 
  

      ''')
