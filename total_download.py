#!/usr/bin/env python3
# -*- Coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import re

# データファイル
df = pd.read_csv("./salmon_download.csv")

# ファイル名正規表現マッチング
ptn = re.compile(r"/download/SALMON-v[\.\d]*?.tar.gz")

df.index = pd.to_datetime(df["Date"])

flag = df["Filetitle"].apply(lambda x: ptn.match(x) is not None)
df["Count"] = 0
df.loc[flag, "Count"] = 1

# ダウンロード数集計処理 (2017-06-14以降)
df_day = df.resample("1D").sum()
df_total = df_day["2017-06-14" <= df_day.index].cumsum(axis=0)

# プロット
plt.figure(figsize=[7, 5])
plt.fill_between(df_total.index, df_total["Count"],
                 facecolor="salmon", edgecolor="darkred", lw=1.5)
plt.ylabel("Total Downloads")
plt.xlabel("Date")
plt.xlim(["2017-06-14", pd.datetime.today()])

count = max(df_total["Count"])
plt.title("Total %d downloads" % count)
plt.ylim([0, count * 1.1])

plt.tight_layout()
plt.grid()
plt.savefig("total_download.png", transparent=True)


