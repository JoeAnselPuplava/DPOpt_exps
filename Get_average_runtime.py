import os

# Get average for each epsilon 0.5
def average_runtime(case):
    data_dict ={}
    for i in range(0, 10):
        f = open(f"obl_wn_nullfrac_{case}_runs/rtimes_run{i}_obl_wn_nullfrac_{case}.txt")
        for line in f:
            line_lst = line.strip().split(" ")
            if line_lst[0] in data_dict:
                data_dict[line_lst[0]].append(float(line_lst[1]))
            else:
                data_dict[line_lst[0]] = [float(line_lst[1])]
        f.close()
    # print(data_dict)
    print(case)
    for key in data_dict:
        print(f"{key}: {sum(data_dict[key]) / len(data_dict[key])}")
    print("============================================================")

average_runtime("0_5")
average_runtime("1")
average_runtime("10")
