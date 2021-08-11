import netCDF4 as nc
import pandas as pd
import os
import glob
import sqlalchemy as sq
import functools
from datetime import datetime
import logging
import warnings
import xarray as xr
# 利用过滤器来实现忽略告警
warnings.filterwarnings("ignore")
# nc文件所在目录
nc_dir = r'D:\merra1'
# 创建数据库引擎
con = sq.create_engine('mysql+pymysql://root:123456@localhost/merra_aer')
logger = logging.getLogger(__name__)  # 创建一个全局logger记录器
logger.setLevel(logging.INFO)  # logger等级总开关
fh = logging.FileHandler(".\\GOSAT_L4B.log", mode='a',
                         encoding='utf8')  # 创建一个handle处理器,用于写入log文件
fh.setLevel(logging.INFO)  # 设置输出到log文件的等级
ch = logging.StreamHandler()  # 创建一个handle处理器，用于输出到控制台
ch.setLevel(logging.INFO)  # 设置输出到控制台的等级
formatter = logging.Formatter(
    "[%(asctime)s] - %(filename)s - %(levelname)s : %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S')  # 创建一个Formatter格式化器，定义log的输出格式
ch.setFormatter(formatter)  # 设置格式
fh.setFormatter(formatter)
logger.addHandler(fh)  # 设置文件输出到logger
logger.addHandler(ch)  # 设置控制台输出到logger

def obtain_name():
    """
        建立数据库表名
    """
    lev_list = [400]
    return (('aer_' + str(x).zfill(3)) for x in lev_list)

def get_file():
    """
    返回所有nc文件的绝对路径和日期信息
    """
    nc_path = glob.glob(os.path.join(nc_dir, '*.nc4'))
    nc_name = os.listdir(nc_dir)
    nc_date = [''.join(os.path.splitext(name)[0][27:33]) for name in nc_name]
    return nc_path, nc_date

def timer(func):
    """
    自定义装饰器用于计时
    """
    @functools.wraps(func)
    def wrapper(*args):
        print('开始时间:', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        func(*args)
        print('结束时间:', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return wrapper

@timer
def nc_to_mysql(tb_name, path_list, date_list):
    """
    遍历每个nc文件，分层处理存入数据库
    """
    print('共%s个nc4文件' % (len(path_list)))
    # num为索引，从0到文件总数；path_and_date为元组，包含两部分，第一个为文件绝对路径，第二个为文件日期
    for num, path_and_date in enumerate(zip(path_list, date_list)):
        name ='aer_400'
        nc_dir = path_and_date[0]
        nc_data = xr.open_dataset(nc_dir)
        lon = nc_data['lon'].data
        lat = nc_data['lat'].data
        BCSMASS1 = []  # 炭黑表面质量浓度
        lat_list = []
        lon_list = []
        for i in range(len(lat)):
            for j in range(len(lon)):
                BCSMASS = nc_data['BCSMASS'][0,i,j].data
                # 剔除小于0的无效值，对剩下有效值值求均
                BCSMASS1.append(BCSMASS)
                lat_list.append(lat[i])
                lon_list.append(lon[j])
        df = pd.DataFrame({
            'BCSMASS': BCSMASS1,
            'lat': lat_list,
            'lon': lon_list
        })
        df['BCSMASS'] = df['BCSMASS'].apply(lambda x: x * 10**10).round(3)
        # df["month-day"] = df["date"].apply(lambda x: x.strftime("%Y-%m"))
        df['date'] =  pd.to_datetime(path_and_date[1],format='%Y%m')
        # df["date"] = df["date"].apply(lambda x: x.strftime("%Y-%m"))
            # 重建列索引
        df = df.reindex(columns=['date', 'lon', 'lat', 'BCSMASS'])
            # 重置行索引
        df = df.reset_index(drop=True)
        # print(df)
        df.to_sql(name,
                    con,
                    if_exists='append',
                    index=False,
                    chunksize=10000)
        # 终端打印当前文件信息
    logger.info(
        f'Num:{num+1} -> {os.path.basename(path_and_date[0])} imported MySQL successfully.'
    )

if __name__ == "__main__":
    tb_name = obtain_name()
    path_list, date_list = get_file()
    nc_to_mysql(tb_name, path_list, date_list)
