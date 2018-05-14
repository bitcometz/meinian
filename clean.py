import sys
import pandas as pd
import numpy as np
import re

reload(sys)
sys.setdefaultencoding('utf-8')


### functions ###


### clean
def xuetang(x):
    try:
        if x.find("糖尿病史（治疗中）") != -1:
            # print 'Test doing'
            y = 1
        elif x.find("糖尿病史（间断治疗）") != -1:
            y = 2
        elif x.find("糖尿病史（中断治疗）") != -1:
            y = 3
        elif x.find("糖尿病史（未治疗）") != -1:
            y = 4
        elif x.find("血糖偏高") != -1 or x.find("高血糖") != -1:
            y = 0.5
        elif x.find("血压、血脂、血糖、血粘度、血尿酸均偏高") != -1:
            y = 0.5
        elif x.find("糖尿病") != -1:
            y = 3.5
            # elif x.find("糖") != -1:
            # print x
            # y = 0
        else:
            y = 0

    except:
        y = 0
    return y


def xueya(x):
    try:
        if x.find("高血压史（治疗中）") != -1:
            y = 1
        elif x.find("高血压史（间断治疗）") != -1:
            y = 2
        elif x.find("高血压史（中断治疗）") != -1:
            y = 3
        elif x.find("高血压史（未治疗）") != -1:
            y = 4
        elif x.find("血压偏高") != -1:
            y = 0.5
        elif x.find("高血压") != -1:
            y = 3.5
        elif x.find("血压、血脂、血糖、血粘度、血尿酸均偏高") != -1:
            y = 0.5
            # elif x.find("血压") != -1:
            # print x
            # y = 0
        else:
            y = 0

    except:
        y = 0
    return y


def xuezhi(x):
    try:
        if x.find("高血脂") != -1:
            y = 1
        elif x.find("血脂偏高") != -1:
            y = 0.5
        elif x.find("血压、血脂、血糖、血粘度、血尿酸均偏高") != -1:
            y = 0.5

        else:
            y = 0

    except:
        y = 0
    return y


def zhifanggan(x):
    try:
        if x.find("脂肪肝") != -1:
            # print x
            y = 1

        else:
            y = 0

    except:
        y = 0
    return y


def jiazhuangxian(x):
    try:
        if x.find("甲状腺功能减退") != -1:
            y = -1
        elif x.find("甲状腺功能亢进") != -1:
            y = 1
        elif x.find("甲状腺癌") != -1:
            y = 0.5
        elif x.find("甲状腺良性病变") != -1:
            y = 0.2
        elif x.find("桥本甲状腺炎史") != -1:
            y = 0.3
        elif x.find("甲状腺双术后") != -1:
            y = 0.6

        else:
            y = 0

    except:
        y = 0
    return y


def xinzangbing(x):
    try:
        if x.find("心脏病") != -1 or x.find("冠心") != -1:
            y = 1

        else:
            y = 0

    except:
        y = 0
    return y


def xinlv_fun(x):
    try:
        if x.find("不齐") != -1 or x.find("早搏") != -1:
            y = 2
        elif x.find("绝对不规则") != -1 or x.find("绝对不齐") != -1:
            y = 3

        elif x.find("过") != -1 or x.find("房颤") != -1:
            y = 1
        else:
            y = 0

    except:
        y = 0
    return y


def xintiao_fun(x):
    try:
        y = re.search(reg, x).group(0)
        y = int(y)
    except:

        y = np.nan
    return y


def v10004_fun(x):
    try:
        y = float(x.split(";")[0])
        if y < 0:
            y = np.nan
    except:
        y = np.nan
    return y


def v2302(x):
    try:
        y = 0
        if x.find("健康") != -1:
            y = 0
        elif x.find("亚健康") != -1:
            y = 1
        elif x.find("疾病") != -1:
            y = 2
    except:
        y = 0
    return y


def yinyang(x):
    try:
        if type(x) == type(1.1):
            y = 0
        elif x.find("2") != -1:
            y = 2
        elif x.find("3") != -1:
            y = 3
        elif x.find("4") != -1:
            y = 4
        elif x.find("+") != -1:
            y = x.count("+")
        elif x.find("阳性") != -1:
            y = 1
        else:
            y = 0
    except:
        y = 0
    return y


def nao(x):
    try:
        if x.find("脑梗塞") != -1:
            y = 2
        elif x.find("脑") != -1:
            y = 1
        else:
            y = 0

    except:
        y = 0
    return y


def shen(x):
    try:
        if x.find("肾病综合") != -1:
            y = 2
        elif x.find("肾") != -1:
            # print x
            y = 1
        else:
            y = 0

    except:
        y = 0
    return y


def wei(x):
    try:
        if x.find("胃") != -1:
            y = 1

        else:
            y = 0

    except:
        y = 0
    return y


### functions ###


### Reading file ###
print '*****Reading file'


def new_results(df):
    x = ";".join(map(str, df['results']))
    return x


part1 = DataFrame(o.get_table('odps_tc_257100_f673506e024.meinian_round2_data_part1'))
part2 = DataFrame(o.get_table('odps_tc_257100_f673506e024.meinian_round2_data_part2'))
data1 = pd.concat([part1.to_pandas(), part2.to_pandas()])
data2 = data1.groupby(['vid', 'test_id'], as_index=False).apply(new_results)
data3 = pd.DataFrame(data2, columns=['results'])

print 'data3.info'
print data3.info()
print('The shape of data3:{}'.format(data3.shape))

### change format to unstack ###
print '*****Formatting and cleaning none'
data_fmt_all = data3.unstack(fill_value=None)  # fill_value=None
print data_fmt_all.shape
data_fmt_all.columns = data_fmt_all.columns.droplevel(level=0)
data_fmt_all.reset_index(inplace=True)

null_count = data_fmt_all.isnull().sum()

### filter null number > 5000
data_keep_5000 = data_fmt_all.drop(labels=null_count[null_count >= 5000].index, axis=1)
# print 'info for data_keep_5000'
# print data_keep_5000.info()
print('The shape of data_keep_5000:{}'.format(data_keep_5000.shape))
print('The type of data_keep_5000:{}'.format(type(data_keep_5000)))

### filter null numer > 2000
null_count = data_keep_5000.isnull().sum()
data_filter = data_keep_5000.drop(labels=null_count[null_count >= 1600].index, axis=1)
data_keep_60 = data_filter.copy()  # Copy
print ('Shape of data_keep_60:{}'.format(data_keep_60.shape))

### drop these lists
list1 = ['0101', '0102', '0113', '0114', '0115', '0116', '0117', '0118', '0420', '0426', '0430', '0434', '1001',
         '300005']
vital = data_filter.drop(list1, axis=1)
print('The shape for >2000 & drop lists:{}'.format(vital.shape))

### clean for list 0409, clean_0409.py
print '*****Cleaning 0409'
xuetang = vital['0409'].apply(xuetang)
xuetang.rename("xuetang", inplace=True)

xueya = vital['0409'].apply(xueya)
xueya.rename("xueya", inplace=True)

xuezhi = vital['0409'].apply(xuezhi)
xuezhi.rename("xuezhi", inplace=True)

zhifanggan = vital['0409'].apply(zhifanggan)
zhifanggan.rename("zhifanggan", inplace=True)

xinzangbing = vital['0409'].apply(xinzangbing)
xinzangbing.rename("xinzangbing", inplace=True)

jiazhuangxian = vital['0409'].apply(jiazhuangxian)
jiazhuangxian.rename("jiazhuangxian", inplace=True)

new = vital.drop(['0409'], axis=1)
frame = [new, xueya, xuezhi, xuetang, zhifanggan, xinzangbing, jiazhuangxian]
new = pd.concat(frame, axis=1)

print('The shape after clean0409:{}'.format(new.shape))
print('The type:{}'.format(type(new)))

### clean_other1.py
print '*****clean_other1.py'
xinlv = new['0421'].apply(xinlv_fun)
xinlv.rename("xinlv", inplace=True)

reg = re.compile("[0-9]{2,3}")
xintiao = new['0424'].apply(xintiao_fun)
xintiao.rename("xintiao", inplace=True)
ava = int(xintiao.mean())
xintiao = xintiao.fillna(ava)

v10004 = new['10004'].apply(v10004_fun)
v10004 = v10004.fillna(v10004.mean())
v10004.rename("v10004", inplace=True)

vlist = ['10004', '1814', '1815', '1840', '1850', '190', '191', '2403', '2404', '2405', '3193']
new_fea = new

for value in vlist:
    new_fea[value] = new_fea[value].apply(v10004_fun)
    new_fea[value] = new_fea[value].fillna(new_fea[value].mean())

new_fea['0421'] = new_fea['0421'].apply(xinlv_fun)
new_fea['0424'] = new_fea['0424'].apply(xintiao_fun)
new_fea['0424'] = new_fea['0424'].fillna(ava)

print('The shape after clean_other1:{}'.format(new_fea.shape))

### clean_other2.py
print '*****clean_other2.py'

v1 = new_fea['2302']
v1 = v1.apply(v2302)
new_fea['2302'] = v1
vlist = ['3190', '3191', '3192', '3195', '3196', '3197', '3430']

for value in vlist:
    new_fea[value] = new_fea[value].apply(yinyang)

new_fea.drop(['3429', '3730'], inplace=True, axis=1)
print('The shape after clean_other2:{}'.format(new_fea.shape))

### clean_0409other.py

bing = data_keep_60['0409']
nao = bing.apply(nao)
nao.rename("nao", inplace=True)

shen = bing.apply(shen)
shen.rename("shen", inplace=True)

wei = bing.apply(wei)
wei.rename("wei", inplace=True)

list3 = [data_keep_60['vid'], nao, shen, wei]
all_0409other = pd.concat(list3, axis=1)
print('The shape of all_0409other:{}'.format(all_0409other.shape))

### merge
all_0426 = pd.merge(new_fea, all_0409other, on=['vid'])
print('The shape of all_0426:{}'.format(all_0426.shape))

### Saving clean tables
print 'Saving cleant tables into SQL'

listadd = ['1301', '1302', '1304', '0201', '0217', '0222', '0405', '0406', '0407', '0413', '0423', '0431', '0432',
           '0901', '0911', '0912', '0929', '0947', '0433', '0974', '0975', '0976', '0978', '0979', '0985',
           '0949', '0954', '0980', '0435', '100010', '1308', '3207',
           'A201', 'A202', 'A601', '1329',
           '0120', '0202', '0203']

all_0426 = all_0426.drop(listadd, axis=1)
null_count = all_0426.isnull().sum()
print null_count

print('The shape of all_0426:{}'.format(all_0426.shape))

table_name = 'table_cleans'
odps.delete_table(table_name, if_exists=True)
DataFrame(all_0426).persist(table_name, odps=o)

# print all_0426.head(1)





