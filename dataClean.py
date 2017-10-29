import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

dropOutColumn = ['CarName','MakeId','Url', 'FrontImagePath','PhotoCount', 'Price','Km','ModelName','VersionName','AdditionalFuel',
                'VideoCount','OfferStartDate','OfferEndDate','LastUpdatedOn','AreaName','CityId','StateName',
                'CertifiedLogoUrl','NoOfOwners','Emi','EmiFormatted','AbsureWarranty','AbsureScore','FinanceUrl',
                 'MakeMapping','RootMapping','ApiFlag','MaskingNumber','SellerContact','HostUrl','OriginalImgPath',
                'CertificationId','InspectionText','HasWarranty','DealerQuickBloxId','NearbyCityText','NBCityStripId',
                'DeliveryText','DeliveryCity','IsNearbyCityListing','Responses','IsEligibleForFinance','ResponsesText',
                'MfgDate','ValuationUrl','CertificationScore','SellerNote','SellerName','IsHotDeal','MakeName','MakeMonth','InquiryId',
                 'RootId','ModelId','VersionId','MaskingName','SubSegmentID','VersionSubSegmentID','IsPremium','IsPremiumPackage',
                 'FinanceUrlText','SortScore']

def cleanColumn():
    
    raw_df = pd.read_csv('dataCrap/secondHandCar/rawDataCopy.csv')
    raw_df = raw_df.drop_duplicates(subset=['ProfileId'], keep='first')
    raw_df.to_csv('raw_data.csv')
    
    print(raw_df.shape)
    
    # drop useless column
    raw_df.drop(dropOutColumn, axis=1, inplace=True)
    
    # after drop column
    raw_df.to_csv("refinedData.csv")
    
    raw_df.drop(['ProfileId'],axis=1, inplace=True)
    
    # one-hot encoding
    raw_df['enc_seller'] = pd.get_dummies(raw_df.Seller).Dealer
    # 1 - manual 0 - auto
    raw_df['enc_gearBox'] = pd.get_dummies(raw_df.GearBox,drop_first=True)
    raw_df['enc_fuel'] = pd.get_dummies(raw_df.Fuel).Diesel
    raw_df['enc_color_silver'] = pd.get_dummies(raw_df.Color).Silver
    raw_df['enc_color_white'] = pd.get_dummies(raw_df.Color).White
    raw_df['enc_color_grey'] = pd.get_dummies(raw_df.Color).Grey
    raw_df['enc_color_gold'] = pd.get_dummies(raw_df.Color).Gold
    raw_df['enc_color_black'] = pd.get_dummies(raw_df.Color).Black
    raw_df['enc_color_blue'] = pd.get_dummies(raw_df.Color).Blue
    def encode_other_color(x): 
        return 0 if (x == 'White' or x == 'Silver' or x == 'Grey' or x == 'Gold' or x == 'Black' or x == 'Blue') else 1
    raw_df['enc_color_other'] = raw_df.Color.apply(encode_other_color)
    raw_df['enc_city_newDelhi'] = pd.get_dummies(raw_df.CityName)['New Delhi']
    raw_df['enc_city_mumbai'] = pd.get_dummies(raw_df.CityName)['Mumbai']
    raw_df['enc_city_bangalore'] = pd.get_dummies(raw_df.CityName)['Bangalore']
    raw_df['enc_city_hyderabad'] = pd.get_dummies(raw_df.CityName)['Hyderabad']
    raw_df['enc_city_chennai'] = pd.get_dummies(raw_df.CityName)['Chennai']
    raw_df['enc_city_thane'] = pd.get_dummies(raw_df.CityName)['Thane']
    def encode_other_city(x): 
        return 0 if (x == 'New Delhi' or x == 'Hyderabad' or x == 'Mumbai' or x == 'Hyderabad' or x=='Chennai' or x=='Thane') else 1
    raw_df['enc_city_other'] = raw_df.CityName.apply(encode_other_city)
    raw_df['enc_name_innova'] = pd.get_dummies(raw_df.RootName)['Innova']
    raw_df['enc_name_fortuner'] = pd.get_dummies(raw_df.RootName)['Fortuner']
    raw_df['enc_name_corolla'] = pd.get_dummies(raw_df.RootName)['Corolla Altis']
    raw_df['enc_name_etios'] = pd.get_dummies(raw_df.RootName)['Etios']
    def encode_other_name(x): 
        return 0 if (x == 'Innova' or x == 'Corolla Altis' or x == 'Fortuner' or x == 'Etios') else 1
    raw_df['enc_city_other'] = raw_df.RootName.apply(encode_other_name)
    
    # remove outlier
    raw_df = raw_df[raw_df['KmNumeric'] < 1500000]
    
    # write to CSV
    raw_df.to_csv("refinedDataWithEncode.csv")
    return raw_df