print('''
      1su hduser
2cd
3start-dfs.sh
4start-yarn.sh
5jps
6ls
7  nano word_count.txt
{ Wordcount.txt file will open in nano
}
8cat word_count.txt
9hadoop fs -ls /
10  hadoop fs -mkdir /mapreduce_word_count
11  hadoop fs -ls /
12  hadoop fs -put word_count.txt /mapreduce_word_count
13  hadoop fs -ls /mapreduce_word_count
14   hadoop fs -cat /mapreduce_word_count/word_count.txt
15 nano mapper_word_count.py
{
#01_Mapper
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    words = line.strip().split()
    for word in words:
        print(f"{word}	1")
}
16 nano reducer_word_count.py
{
# ---------------01_Reducer---------------
#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

for line in sys.stdin:
    word, count = line.strip().split("	")
    count = int(count)

    if current_word == word:
        current_count += count
    else:
        if current_word:
            print(f"{current_word}	{current_count}")
        current_word = word
        current_count = count

if current_word == word:
    print(f"{current_word}	{current_count}")
}
17  ls
18 chmod +x mapper_word_count.py

19 chmod +x reducer_word_count.py
20 # new terminal
   su hduser
21 cd
22  cd /usr/local/hadoop/share/hadoop/tools/lib
23 ls
24 pwd
/usr/local/hadoop/share/hadoop/tools/lib
24 #back to terminal
   /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar
25 hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar
 -input /mapreduce_word_count/word_count.txt -output /output
-mapper /home/hduser/mapper_word_count.py -reducer /home/hduser/reducer_word_count.py
26 hadoop fs -ls /output
27 hadoop fs -cat /output/part-00000
28 stop-dfs.sh
29 stop-yarn.sh
      ''')
