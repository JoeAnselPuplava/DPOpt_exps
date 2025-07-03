import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

def get_data(fname):
    f = open(fname, "r")
    data_dict = {}
    for line in f:
        line_lst = line.strip().split(" ")
        data_dict[line_lst[0]] = float(line_lst[1])
    f.close()
    return data_dict

# Updated to take 5 arrays for 5 bars
def plot_bars(array1, array2, array3, array4, array5, labels, plotname):
    x = np.arange(len(labels))
    width = 0.15  # smaller width to fit more bars

    fig, ax = plt.subplots()

    # 5 bars: Oblivious, DP 0.5, DP 1, DP 10, Public
    ax.bar(x - 2 * width, array1, width, label='Oblivious', color="#122862")
    ax.bar(x - width, array2, width, label='DP 0.5', color="#294E91")
    ax.bar(x, array3, width, label='DP 1', color="#517DD0")
    ax.bar(x + width, array4, width, label='DP 10', color="#83ACF7")
    ax.bar(x + 2 * width, array5, width, label='Public', color='#ABCDEF')

    ax.set_xlabel("Queries")
    ax.set_ylabel("Runtimes as ratio of Public Runtimes")
    ax.set_title("Runtime Ratio Bar Chart")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()

    plt.tight_layout()
    plt.savefig("rt_bars_" + plotname + ".jpg", dpi=500)
    # plt.show()

def plot_aggregates(rtimes_obl, rtimes_pub, rtimes_0_5, rtimes_1, rtimes_10, case):
    dpf_sr = [0, 0, 0, 0, 0]    # Oblivious, DP 0.5, DP 1, DP 10, Public
    ndpf_sr = [0, 0, 0, 0, 0]
    all_sr = [0, 0, 0, 0, 0]

    labels = ["DP-friendly", "Not DP-friendly", "Full Workload"]
    queries_included_dict = {label: [] for label in labels}

    for query in rtimes_obl:
        if (
            query in rtimes_pub and query in rtimes_0_5 and
            query in rtimes_1 and query in rtimes_10
        ):
            obl_rt = rtimes_obl[query]
            dp_0_5_rt = rtimes_0_5[query]
            dp_1_rt = rtimes_1[query]
            dp_10_rt = rtimes_10[query]
            pub_rt = rtimes_pub[query]

            if dp_0_5_rt < obl_rt:
                dpf_sr[0] += obl_rt
                dpf_sr[1] += dp_0_5_rt
                dpf_sr[2] += dp_1_rt
                dpf_sr[3] += dp_10_rt
                dpf_sr[4] += pub_rt
                queries_included_dict["DP-friendly"].append(query)
            else:
                ndpf_sr[0] += obl_rt
                ndpf_sr[1] += dp_0_5_rt
                ndpf_sr[2] += dp_1_rt
                ndpf_sr[3] += dp_10_rt
                ndpf_sr[4] += pub_rt
                queries_included_dict["Not DP-friendly"].append(query)

            all_sr[0] += obl_rt
            all_sr[1] += dp_0_5_rt
            all_sr[2] += dp_1_rt
            all_sr[3] += dp_10_rt
            all_sr[4] += pub_rt

    def normalize(ratios):
        if ratios[4] > 0:  # avoid division by zero
            return [v / ratios[4] for v in ratios]
        return [0] * 5

    dpf_sr = normalize(dpf_sr)
    ndpf_sr = normalize(ndpf_sr)
    all_sr = normalize(all_sr)

    print("DP-friendly queries:", queries_included_dict["DP-friendly"])
    print("DP-friendly ratios:", dpf_sr)
    print("Not DP-friendly queries:", queries_included_dict["Not DP-friendly"])
    print("Not DP-friendly ratios:", ndpf_sr)
    print("Overall ratios:", all_sr)

    # Plot all five bars
    plot_bars(
        [dpf_sr[0], ndpf_sr[0], all_sr[0]],  # Oblivious
        [dpf_sr[1], ndpf_sr[1], all_sr[1]],  # DP 0.5
        [dpf_sr[2], ndpf_sr[2], all_sr[2]],  # DP 1
        [dpf_sr[3], ndpf_sr[3], all_sr[3]],  # DP 10
        [dpf_sr[4], ndpf_sr[4], all_sr[4]],  # Public
        labels,
        case + "_sum_ratios"
    )


def main():
    parser = argparse.ArgumentParser(description='Plot runtimes for oblivous/noisy/public scenarios.')
    parser.add_argument('case', type=str, help='Name of the scenario it is, eg: oblivious_w_noisy_nullfrac')
    args = parser.parse_args()

    rtimes_pub = get_data("rtimes_public.txt")
    rtimes_noisy = get_data("avg_0_5.txt")
    rtimes_1 = get_data("avg_1.txt")
    rtimes_10 = get_data("avg_10.txt")
    rtimes_obl = get_data("rtimes_oblivious.txt")

    y1, y2, y3, y4, y5 = [], [], [], [], []  # Added y4, y5 for DP 1 and DP 10
    labels = []

    excluded_queries = {"2a", "2d", "30b", "30c", "31b", "31a", "2b", "2c",
                        "11b", "11d", "13b", "13c", "14a", "20a", "21b", "21c",
                        "23c", "24a", "24b", "25a"}

    for query in rtimes_obl:
        if (query in rtimes_pub) and (query in rtimes_noisy) and (query in rtimes_1) and (query in rtimes_10) and (query.strip() not in excluded_queries):
            pub_runtime = rtimes_pub[query]
            dp_runtime = rtimes_noisy[query]
            dp_1_runtime = rtimes_1[query]
            dp_10_runtime = rtimes_10[query]
            oblivious_runtime = rtimes_obl[query]

            y1.append(oblivious_runtime / pub_runtime)
            y2.append(dp_runtime / pub_runtime)
            y3.append(1)
            y4.append(dp_1_runtime / pub_runtime)
            y5.append(dp_10_runtime / pub_runtime)
            labels.append(query)

    for i in range(0, len(y1), 10):
        plot_bars(
            y1[i:i+10],
            y2[i:i+10],
            y4[i:i+10],
            y5[i:i+10],
            y3[i:i+10],
            labels[i:i+10],
            args.case + "_" + str(i) + "_" + str(i+10)
        )

    plot_aggregates(rtimes_obl, rtimes_pub, rtimes_noisy, rtimes_1, rtimes_10, args.case)

if __name__ == '__main__':
    main()
