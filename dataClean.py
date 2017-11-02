from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from sklearn import preprocessing


dropOutColumn = ['CarName', 'MakeId', 'Url', 'FrontImagePath', 'PhotoCount', 'Price', 'Km', 'ModelName', 'VersionName', 'AdditionalFuel',
                 'VideoCount', 'OfferStartDate', 'OfferEndDate', 'LastUpdatedOn', 'AreaName', 'CityId', 'StateName',
                 'CertifiedLogoUrl', 'NoOfOwners', 'Emi', 'EmiFormatted', 'AbsureWarranty', 'AbsureScore', 'FinanceUrl',
                 'MakeMapping', 'RootMapping', 'ApiFlag', 'MaskingNumber', 'SellerContact', 'HostUrl', 'OriginalImgPath',
                 'CertificationId', 'InspectionText', 'HasWarranty', 'DealerQuickBloxId', 'NearbyCityText', 'NBCityStripId',
                 'DeliveryText', 'DeliveryCity', 'IsNearbyCityListing', 'Responses', 'IsEligibleForFinance', 'ResponsesText',
                 'MfgDate', 'ValuationUrl', 'CertificationScore', 'SellerNote', 'SellerName', 'IsHotDeal', 'MakeName', 'MakeMonth', 'InquiryId',
                 'RootId', 'ModelId', 'VersionId', 'MaskingName', 'SubSegmentID', 'VersionSubSegmentID', 'IsPremium', 'IsPremiumPackage',
                 'FinanceUrlText', 'SortScore']

def create_dstinct_data():
    df = pd.read_csv('dataCrap/secondHandCar/rawDataCopy.csv')
    print("Before: ",df.shape)
    df = df.drop_duplicates(subset=['ProfileId'], keep='first')
    df.to_csv('raw_data.csv',index=False)
    print("After delete: ",df.shape)


def clean_trainig_data(file_path='raw_data.csv'):

    raw_df = pd.read_csv(file_path)

    # drop useless column
    raw_df.drop(dropOutColumn, axis=1, inplace=True)

    # after drop column
    raw_df.to_csv("useful_data.csv")

    raw_df.drop(['ProfileId'], axis=1, inplace=True)

    # remove outlier based on Km
    raw_df = raw_df[raw_df['KmNumeric'] < 1500000]
    raw_df = raw_df[raw_df['KmNumeric'] >0]

    raw_df = one_hot_encoding(raw_df)

    # write to CSV
    raw_df.to_csv("refined_data.csv")
    return raw_df


def one_hot_encoding(raw_df):
    # one-hot encoding
    raw_df['enc_seller'] = pd.get_dummies(raw_df.Seller).Dealer
    raw_df['enc_gearBox'] = pd.get_dummies(raw_df.GearBox).Manual
    raw_df['enc_fuel'] = pd.get_dummies(raw_df.Fuel).Diesel
    # colors
    raw_df['enc_color_silver'] = pd.get_dummies(raw_df.Color).Silver
    raw_df['enc_color_white'] = pd.get_dummies(raw_df.Color).White
    raw_df['enc_color_grey'] = pd.get_dummies(raw_df.Color).Grey
    raw_df['enc_color_gold'] = pd.get_dummies(raw_df.Color).Gold
    raw_df['enc_color_black'] = pd.get_dummies(raw_df.Color).Black
    raw_df['enc_color_blue'] = pd.get_dummies(raw_df.Color).Blue
    def encode_other_color(x):
        return 0 if (x == 'White' or x == 'Silver' or x == 'Grey' or x == 'Gold' or x == 'Black' or x == 'Blue') else 1
    raw_df['enc_color_other'] = raw_df.Color.apply(encode_other_color)

    # city
    raw_df['enc_color_other'] = raw_df.Color.apply(encode_other_color)
    raw_df['enc_city_new_delhi'] = pd.get_dummies(raw_df.CityName)['New Delhi']
    raw_df['enc_city_mumbai'] = pd.get_dummies(raw_df.CityName)['Mumbai']
    raw_df['enc_city_bangalore'] = pd.get_dummies(raw_df.CityName)['Bangalore']
    raw_df['enc_city_hyderabad'] = pd.get_dummies(raw_df.CityName)['Hyderabad']
    raw_df['enc_city_chennai'] = pd.get_dummies(raw_df.CityName)['Chennai']
    raw_df['enc_city_pune'] = pd.get_dummies(raw_df.CityName)['Pune']
    raw_df['enc_city_ahmedabad'] = pd.get_dummies(raw_df.CityName)['Ahmedabad']
    def encode_other_city(x):
        return 0 if (x == 'New Delhi' or x == 'Hyderabad' or x == 'Mumbai' or x == 'Hyderabad' or x == 'Chennai' or x == 'Pune' or x=='Ahmedabad') else 1
    raw_df['enc_city_other'] = raw_df.CityName.apply(encode_other_city)

    # model
    raw_df['enc_name_innova'] = pd.get_dummies(raw_df.RootName)['Innova']
    raw_df['enc_name_fortuner'] = pd.get_dummies(raw_df.RootName)['Fortuner']
    raw_df['enc_name_corolla_altis'] = pd.get_dummies(raw_df.RootName)[
        'Corolla Altis']
    raw_df['enc_name_etios'] = pd.get_dummies(raw_df.RootName)['Etios']
    raw_df['enc_name_etios_liva'] = pd.get_dummies(raw_df.RootName)['Etios Liva']
    raw_df['enc_name_etios_corolla'] = pd.get_dummies(raw_df.RootName)['Corolla']
    def encode_other_name(x):
        return 0 if (x == 'Innova' or x == 'Corolla Altis' or x == 'Fortuner' or x == 'Etios' or x=='Etios Liva' or x=='Corolla') else 1
    raw_df['enc_name_other'] = raw_df.RootName.apply(encode_other_name)

    # split km to 4 column
    raw_df["km_type"] = 0
    raw_df.loc[raw_df['KmNumeric'].between(114274, 1500000, inclusive=True),'km_type'] = 1
    raw_df.loc[raw_df['KmNumeric'].between(75363, 114273, inclusive=True),'km_type'] = 2
    raw_df.loc[raw_df['KmNumeric'].between(52215, 75362, inclusive=True),'km_type'] = 3
    raw_df.loc[raw_df['KmNumeric'].between(250, 52214, inclusive=True),'km_type'] = 4
    raw_df.drop(['KmNumeric'],axis=1,inplace=True)
    
    return raw_df


def clean_post_data(df):

    # init this template
    # convert String to float/int
    df['OwnerTypeId'] = df['OwnerTypeId'].astype(int)
    df['BodyStyleId'] = df['BodyStyleId'].astype(int)
    # Normalization . Method is selected based on distribution
    df['enc_seller'] = 0
    df['enc_gearBox'] = 0
    df['enc_fuel'] = 0
    df['enc_color_silver'] = 0
    df['enc_color_white'] = 0
    df['enc_color_grey'] = 0
    df['enc_color_gold'] = 0
    df['enc_color_black'] = 0
    df['enc_color_blue'] = 0
    df['enc_color_other'] = 0
    df['enc_city_new_delhi'] = 0
    df['enc_city_mumbai'] = 0
    df['enc_city_bangalore'] = 0
    df['enc_city_hyderabad'] = 0
    df['enc_city_chennai'] = 0
    df['enc_city_pune'] = 0
    df['enc_city_ahmedabad'] = 0
    df['enc_city_other'] = 0
    df['enc_name_innova'] = 0
    df['enc_name_fortuner'] = 0
    df['enc_name_corolla_altis'] = 0
    df['enc_name_etios'] = 0
    df['enc_name_etios_liva'] = 0
    df['enc_name_etios_corolla'] = 0
    df['enc_name_other'] = 0
    df["km_type"] = 0
    df['MakeYear'] = df['MakeYear'].astype(float)/2000

    # normalize km and year
    # km = pd.read_csv("km.csv",header=None)
    # km.columns = ['KmNumeric']
    # year = pd.read_csv("year.csv",header=None)
    # year.columns = ['MakeYear']
    # km = km.append(pd.DataFrame(df['KmNumeric'].astype(float)),ignore_index=True)
    # year = year.append(pd.DataFrame(df['MakeYear'].astype(float)),ignore_index=True)
    # year_norm = preprocessing.scale(year)
    # km_norm = preprocessing.minmax_scale(km)
    # df['KmNumeric'] = km_norm[-1]
    # df['MakeYear'] = year_norm[-1]
    # change value for certain case
    
    if df['KmNumeric'][0] > 114274:
        df["km_type"] = 1
    elif df['KmNumeric'][0] > 75363:
        df['km_type'] = 1
    elif df['KmNumeric'][0] > 52215:
        df['km_type'] = 1
    else:
        df['km_type'] = 1

    if df['Seller'][0] == 'Dealer':
        df['enc_seller'] = 1
    if df['GearBox'][0] == 'Manual':
        df['enc_gearBox'] = 1
    if df['Fuel'][0] == 'Diesel':
        df['enc_fuel'] = 1
    city_string = 'enc_city_' + df['CityName'][0].lower().replace(' ', '_')
    df[city_string][0] = 1
    color_string = 'enc_color_' + df['Color'][0].lower()
    df[color_string][0] = 1
    model_string = 'enc_name_' + df['RootName'][0].lower().replace(' ', '_')
    df[model_string][0] = 1

    return df.select_dtypes(include=[np.number])


def store_all_km_year():
    df = pd.read_csv('raw_data.csv')
    df = df[0 < df['KmNumeric'] < 1500000]
    km = df['KmNumeric']
    year = df['MakeYear']
    km.to_csv('km.csv',index=False)
    year.to_csv('year.csv',index=False)


if __name__ == "__main__":
    print("")