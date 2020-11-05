text = """id,name,fmw,rank,active
1,Firdaus,Sembawang,ME3,1
2,Kok,Sembawang,ME2,1
3,Amir,Sembawang,ME2,1
4,Rizal Zainal,Sembawang,ME2,1
5,Thinakaran,Sembawang,ME2,1
6,Nur Asraf,Sembawang,ME2,1
7,Din,Sembawang,ME1,1
8,Iskandar,Sembawang,ME1,1
9,Farizwan,Sembawang,ME1,1
10,Haiqal,Sembawang,ME1,1
11,Hari,Sembawang,ME1,1
12,Rizal,Sembawang,ME1,1
13,Nurhan,Sembawang,ME1,1
14,Sakthish,Sembawang,ME1,1
15,Rasul,Sembawang,ME1,1
16,Keng Wee,Sembawang,ME1,1
17,Qaiyuum,Sembawang,ME1T,1
18,Tze Kean,Sembawang,LTA,1
19,Karthik,Sembawang,3SG,1
20,Asyraaf,Sembawang,3SG,1
21,Kah Leong,Sembawang,3SG,1
22,Donavon,Sembawang,3SG,1
23,Mian Yan,Sembawang,3SG,1
24,Erwin,Sembawang,LCP,1
25,Jia Hao,Sembawang,CPL,1
26,Shafiq,Sembawang,LCP,1
27,Hakim J,Sembawang,LCP,1
28,Shi Jian,Sembawang,LCP,1
29,Amirrul,Sembawang,LCP,1
30,Wang Xing Yu,Sembawang,CPL,1
31,Jun Yi,Sembawang,CPL,1
32,Cheng,Sembawang,LCP,1
33,Jin Wei,Sembawang,LCP,1
34,Ragul,Sembawang,LCP,1
35,Zafrullah,Sembawang,LCP,1
36,Qin Hao,Sembawang,LCP,1
37,Anwar,Sembawang,LCP,1
38,Hakim A,Sembawang,LCP,1
39,Christabelle,Sembawang,ME1T,1
40,Faiz,Sembawang,ME1T,1
41,Syakir,Sembawang,ME1T,1
42,Sean Tan,Sembawang,REC,1
43,Ramdan,Sembawang,PTE,1
44,See Hua,Sembawang,PTE,1
45,Manus,Sembawang,PTE,1
46,Jun Ho,Sembawang,PTE,1
47,Royce,Sembawang,REC,1
48,Rohit Kiran,Sembawang,PTE,1
49,Wei Jun,Sembawang,PTE,1
50,Elfian,Sembawang,PTE,1
51,Danish,Sembawang,PTE,1
52,Danial,Sembawang,PTE,1
53,Mikail Islam Bin Khairuddin,Sembawang,PTE,1
54,Jeremy,Sembawang,PTE,1
55,Irfan Syahril Bin Mohamed Salleh,Sembawang,PTE,1
56,Doan Phi Colby,Sembawang,PTE,1
57,Daven,Sembawang,PTE,1
58,Darren,Sembawang,REC,1
59,Yean Jun,Sembawang,PTE,1
60,Bryan,Sembawang,PTE,1"""
text = text.split('\n')
for line in text:
    p_id,name,fmw,rank,active=line.split(',')
    print("(" +p_id+","+"'"+name+"'"+","+"'"+rank+"'"+","+active+ ",2),")