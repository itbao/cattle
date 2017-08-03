#!/usr/bin/env python

import numpy as np
import pandas as pd
import tushare as ts
from pandas import Series
from pandas import DataFrame
import json
import yaml



def get_now_stock(stock_dict):
    stock_series = Series(stock_dict)
    index_list = list(stock_series.index)
    open_list = Series({ index:open["open_interest"] for index,open in stock_dict.items()})
    tag_list = Series({ index:open["name"] for index,open in stock_dict.items()})

    data_df = ts.get_realtime_quotes(index_list).set_index("code")
    data_df["tag"] = tag_list

    pre_close_float = data_df["pre_close"].astype(np.float64)
    price_float = data_df["price"].astype(np.float64)

    p_change = (price_float - pre_close_float) / pre_close_float
    change = open_list * pre_close_float * p_change
    data_df["change"] = change
    data_df["p_change"] = p_change * 100
    data_df["open"] = open_list

    data_df.index = tag_list


    stock_all = data_df[['p_change','change']]
    print stock_all

    change_all = data_df["change"].astype(np.float64).sum()
    print "\nall_change:", change_all


if __name__ == "__main__":

    stock_file = file("cc.yaml")
    stock_dict = yaml.load(stock_file)



    cc_result = get_now_stock(stock_dict)

