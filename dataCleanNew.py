from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

dropOutColumn = ['MakeId', 'Url', 'FrontImagePath', 'PhotoCount', 'Price', 'Km', 'ModelName', 'VersionName', 'AdditionalFuel',
                 'VideoCount', 'OfferStartDate', 'OfferEndDate', 'LastUpdatedOn', 'AreaName', 'CityId', 'StateName',
                 'CertifiedLogoUrl', 'NoOfOwners', 'Emi', 'EmiFormatted', 'AbsureWarranty', 'AbsureScore', 'FinanceUrl',
                 'MakeMapping', 'RootMapping', 'ApiFlag', 'MaskingNumber', 'SellerContact', 'HostUrl', 'OriginalImgPath',
                 'CertificationId', 'InspectionText', 'HasWarranty', 'DealerQuickBloxId', 'NearbyCityText', 'NBCityStripId',
                 'DeliveryText', 'DeliveryCity', 'IsNearbyCityListing', 'Responses', 'IsEligibleForFinance', 'ResponsesText',
                 'MfgDate', 'ValuationUrl', 'CertificationScore', 'SellerNote', 'SellerName', 'IsHotDeal', 'MakeName', 'MakeMonth', 'InquiryId',
                 'RootId', 'ModelId', 'VersionId', 'MaskingName', 'SubSegmentID', 'VersionSubSegmentID', 'IsPremium', 'IsPremiumPackage',
                 'FinanceUrlText', 'SortScore','Seller','Fuel','GearBox','BodyStyleId','RootName']



def clean_trainig_data(file_path='raw_data.csv'):

    raw_df = pd.read_csv(file_path)

    # drop useless column
    raw_df.drop(dropOutColumn, axis=1, inplace=True)

    # after drop column
    raw_df.to_csv("useful_data.csv")

    raw_df.drop(['ProfileId'], axis=1, inplace=True)
    print(raw_df.head)
    raw_df = dummy(raw_df)

    # write to CSV
    raw_df.to_csv("refined_data.csv",index=False)
    # return raw_df

def dummy(raw_df):
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

    raw_df.drop(['Color'],axis=1,inplace=True)
    raw_df = pd.get_dummies(raw_df)
    return raw_df


clean_trainig_data();