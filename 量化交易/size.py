# coding: utf-8
# ==========================================因子检测==============================================================
import alphalens
import pandas as pd
import numpy as np
import time
import statsmodels.api as sm
import scipy as sp



class FactorAnalyse(object):
    # ==========================================因子检测参数设置==============================================================
    start_date = '2016-06-12'  # 回测开始时间
    end_date = '2020-07-12'  # 回测结束时间
    benchindex = '000300.SH'  # 基准指数设置
    stockpool = '000300.SH'  # 股票池设置
    quantiles = 3  # 因子分组数量
    periods = 1  # 调仓周期
    frequency = 'monthly'  # 调仓频率'daily','weekly','monthly'一周按5个交易日计算，一月按21个交易日计算

    # ==========================================添加因子==============================================================
    # 添加因子名称，保持list形式，系统因子对应字段参照 http://quant.10jqka.com.cn/platform/html/help-api.html?t=data#222/436
    factor_input = ["size_factor"]

    # ==========================================因子数据处理参数设置==============================================================
    # 对应的因子数据处理选项
    # 缺失值处理 fillna：0—不处理，1—均值法，2—回归填充法
    # 极值处理 winsorize：0—不处理，1—中位数法，2—三倍标准差，3—四分位
    # 标准化处理 standardize：0—不处理，1—标准化法，2—rank值标准化，3—极差正规化
    factor_dp = {
        "size_factor": {"fillna": 1, "winsorize": 2, "standardize": 2},
    }

    # ==========================================因子合成参数设置==============================================================
    # 因子合成参数
    # direct表示因子方向，weight表示因子权重
    # 因子方向：一共有两种1和-1。1表示正序，从小到大排列，因子值越大的股票会分组至前几组；-1表示倒序，效果反之
    factor_set = {
        "size_factor": {"direct": 1, "weight": 1},
    }

    # ==========================================合成因子数据处理参数设置==============================================================
    # 合成因子数据处理选项
    dataprcess = {"fillna": 1, "winsorize": 0, "neutralize": 0, "standardize": 0}

    # ==========================================用户自定义因子算法========================================================
    # 在此函数下编写依赖因子获取，返回的结果需为{name: DataFrame}，列名（columns）为时间，行名（index）为股票代码
    close_prices = pd.DataFrame()

    def sfactor_data(self, start_date, end_date, stocks, names):
        mak_value = get_sfactor_data(self.start_date, self.end_date, self.stocks, ["current_market_cap"])[
            "current_market_cap"]

        size = np.log(mak_value)

        # 返回结果
        return {'size_factor': size}

    # ===================================================生成因子=====================================================================
    # 在此函数编写因子入库更新，返回的结果需为DataFrame，列名（columns）为时间，行名（index）为股票代码
    def factor_gen(self, start_date, end_date, stocks=None, industry_data=None, mak_value=None):
        # ==========================================生成基础因子==========================================================
        # 获取因子数据
        log.info("正在获取因子数据......： %s " % time.strftime("%H:%M:%S"))
        factor_df = self.sfactor_data(start_date, end_date, stocks, self.factor_input)
        log.info("获取因子数据完毕： %s 因子名称： %s" % (time.strftime("%H:%M:%S"), self.factor_input))
        log.info(factor_df)

        # ==========================================因子数据处理=========================================================
        # 按设置进行数据处理
        log.info("正在进行因子数据预处理......： %s " % time.strftime("%H:%M:%S"))
        for ia in self.factor_input:
            # 缺失值填充
            factor_df[ia] = self.fillnan_data(factor_df[ia], self.factor_dp[ia]["fillna"], industry_data, mak_value)
            # 极值处理
            factor_df[ia] = self.winsorize_data(factor_df[ia], self.factor_dp[ia]["winsorize"])
            # 标准化处理
            factor_df[ia] = self.standardize_data(factor_df[ia], self.factor_dp[ia]["standardize"])
        log.info("因子数据预处理完成： %s " % time.strftime("%H:%M:%S"))

        # ==========================================因子合成=========================================================
        factors = factor_df[self.factor_input[0]].copy()
        factors.iloc[:, :] = 0
        for ia in self.factor_input:
            factors = factors + self.factor_set[ia]["direct"] * self.factor_set[ia]["weight"] * factor_df[ia]
        log.info("因子数据合成完成： %s " % time.strftime("%H:%M:%S"))

        return factors

    # ==========================================因子检测前进行数据准备及数据处理========================================================
    def calc(self):
        log.info("回测区间： %s / %s" % (self.start_date, self.end_date))
        log.info("开始时间： %s " % time.strftime("%H:%M:%S"))
        if self.frequency == "daily":
            period = self.periods
        elif self.frequency == "weekly":
            period = self.periods * 5
        elif self.frequency == "monthly":
            period = self.periods * 21

        # 获取股票池
        self.get_stocks()
        # 价格数据price_df
        log.info("正在获取行情数据......： %s " % time.strftime("%H:%M:%S"))
        price_df = get_price(self.stocks, self.start_date, self.end_date, str(period) + "d", ["close"], bar_count=0,
                             skip_paused=False, fq="pre", is_panel=1)["close"]
        self.close_prices = price_df
        log.info(price_df)
        days = get_trade_days(self.start_date, self.end_date)
        day_index = pd.Index((days[min(i + period - 1, len(days) - 1)] for i in range(0, len(days), period)))
        price_df = price_df.loc[day_index, :]

        log.info("行情数据提取完成： %s " % time.strftime("%H:%M:%S"))

        # ==========================================获取行业分类==============================================================
        # 获取行业分类哑变量,行业分类数据groupby
        log.info("正在获取行业分类数据......： %s " % time.strftime("%H:%M:%S"))
        industry_data, ind_dict = get_sfactor_industry(self.start_date, self.end_date, self.stocks,
                                                       industry="s_industryid1")
        log.info("行业分类数据提取完毕： %s " % time.strftime("%H:%M:%S"))
        log.info(ind_dict)
        # 确保行业数据与因子数据日期对齐
        industry_data = {date: industry_data[date] for date in industry_data if date in price_df.index}

        # ==========================================获取流通市值==============================================================
        log.info("正在获取流通市值数据......： %s " % time.strftime("%H:%M:%S"))
        mak_value = get_sfactor_data(self.start_date, self.end_date, self.stocks, ["current_market_cap"])[
            "current_market_cap"]
        log.info("流通市值数据提取完毕： %s " % time.strftime("%H:%M:%S"))

        # ==========================================根据用户自定义因子算法生成因子=========================================================
        factors = self.factor_gen(self.start_date, self.end_date, self.stocks, industry_data, mak_value)
        log.info("自定义因子数据计算完成： %s " % time.strftime("%H:%M:%S"))
        log.info(factors)

        # ==========================================合成因子数据处理=========================================================
        # 缺失值填充
        factors = self.fillnan_data(factors, self.dataprcess["fillna"])
        # 极值处理
        factors = self.winsorize_data(factors, self.dataprcess["winsorize"])
        # 标准化处理
        factors = self.standardize_data(factors, self.dataprcess["standardize"])
        log.info("因子合成数据预处理完成： %s " % time.strftime("%H:%M:%S"))

        # ==========================================使用alphalens进行因子数据预处理=========================================================
        log.info("正在使用alphalens进行数据处理......： %s " % time.strftime("%H:%M:%S"))
        factor_data = get_clean_factor_data(factors, price_df, self.quantiles, ind_dict, [1])
        factor_data.rename(columns={"1D": str(period) + "D"}, inplace=True)

        log.info("因子数据处理完成： %s " % time.strftime("%H:%M:%S"))
        return factor_data

    # ==========================================获取股票池中股票代码========================================================
    def get_stocks(self):
        if self.stockpool == "stock":
            self.stocks = list(get_all_securities("stock", self.start_date).index)
        else:
            self.stocks = get_index_stocks(self.stockpool, self.start_date)

    # ==========================================因子数据处理函数=========================================================
    # 缺失值处理
    def fillnan_data(self, df, fillna=0, industry_data=None, mak_value=None):
        if fillna == 0:
            pass
        elif fillna == 1:
            # 均值法
            M = df.mean()
            for ix in df.columns:
                locate = df[ix].apply(lambda x: True if x is None or np.isnan(x) else False)
                if sum(locate) > 0:
                    df.loc[locate, ix] = M[ix]
        elif fillna == 2:
            # 回归法
            if industry_data is None or mak_value is None:
                log.info(
                    "缺少行业标签/市值数据：\n行业标签类型为dict，key为日期，内容为DataFrame,            index为股票代码，columns为行业名称，内容为哑变量；\n 市值数据类型为DataFrame，index为股票代码，columns为日期")
                return None

            df.dropna(axis="columns", how="all", inplace=True)
            df.dropna(axis="index", how="all", inplace=True)
            for date in df.columns:
                data_raw = industry_data[date].copy()
                data_raw["mak_value"] = np.log(mak_value[date])
                data_raw["factor"] = df[date]
                data = data_raw.loc[df.index]
                factor_raw = df[date].copy()
                factor_raw_nan = data[np.isnan(factor_raw)]
                for code in factor_raw_nan.index:
                    # 获取股票code没有缺失的列
                    reg_c = data.loc[code].dropna().index.tolist()  # 记录有值的因子名称，reg_c因子名称
                    if reg_c:
                        # 缺失股票的剩余因子值（计算填补值用）
                        X_c = data[reg_c].loc[code]  # 获取对应股票有数据的因子值
                        reg_c.append("factor")
                        # 获取用于回归的数据，包括因变量和自变量
                        X = data[reg_c].dropna()  # n*m矩阵，n为股票数，m为因子数，最后一列为需填补的因子
                        # 回归计算参数
                        A = np.hstack((X.iloc[:, 0:-1].values, np.ones((len(X), 1))))
                        a = np.linalg.lstsq(A, X.iloc[:, -1])
                        Y = np.hstack((X_c.values, 1.0))
                        factor_raw[code] = np.dot(Y, a[0])  # 用剩余因子乘以截距求缺失值
                    else:
                        factor_raw[code] = np.nan
                df[date] = factor_raw
        return df

    # 去极值
    def winsorize_data(self, df, winsorize=0):
        if winsorize == 0:
            pass
        elif winsorize == 1:
            # 5.2倍中位数去极值法
            m = df.median()
            med = 5.2 * (abs(df - m).median())  # 5.2* median(abs(xi-MedianX))
            temp1 = m - med
            temp2 = m + med
            lower = df < temp1
            higher = df > temp2
            for ix in df.columns:
                df[ix][lower[ix]] = temp1[ix]
                df[ix][higher[ix]] = temp2[ix]

        elif winsorize == 2:
            # 3倍标准差去极值法
            m = df.std()
            temp1 = df.mean() - 3 * m
            temp2 = df.mean() + 3 * m
            lower = df < temp1
            higher = df > temp2
            for ix in df.columns:
                df[ix][lower[ix]] = temp1[ix]
                df[ix][higher[ix]] = temp2[ix]

        elif winsorize == 3:
            # 四分位去极值法
            M1 = df.quantile(0.25)
            M2 = df.quantile(0.75)
            M = df.median()
            gap1 = M - M1
            gap2 = M2 - M
            temp1 = M1 - 1.5 * gap1
            temp2 = M2 + 1.5 * gap2
            lower = df < temp1
            higher = df > temp2
            for ix in df.columns:
                df[ix][lower[ix]] = temp1[ix]
                df[ix][higher[ix]] = temp2[ix]
        return df

    # 标准化函数
    def standardize_data(self, df, standardize=0):
        if standardize == 0:
            pass
        elif standardize == 1:
            # 原始值标准化
            df = (df - df.mean()) / df.std()
        elif standardize == 2:
            # rank值标准化
            df = df.rank(axis=0, ascending=True)
            df = (df - df.mean()) / df.std()
        elif standardize == 3:
            # 极差正规化
            df = (df - df.min()) / (df.max() - df.min())
        return df


# ==========================================使用alphalens进行因子检测=========================================================
try:
    __IPYTHON__
    alphalens.tears.create_full_tear_sheet(FactorAnalyse().calc(), long_short=True, group_neutral=True, by_group=True)
    log.info("因子检测完成： %s " % time.strftime("%H:%M:%S"))
except NameError:
    pass
