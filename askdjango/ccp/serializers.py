from rest_framework import serializers
from .models import TBCP_MEMBER_INFO, TBCP_MEMBER_LIST_STAT_INFO, TBCP_MARKET_META_INFO, TBCP_PRODUCT_META_INFO, TBCP_ITEM_META_INFO, TBCP_MEMBER_LIST_DETAIL_INFO


class TBCP_MARKET_META_INFO_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TBCP_MARKET_META_INFO
        field = '__all__'



class TBCP_PRODUCT_META_INFO_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TBCP_PRODUCT_META_INFO
        field = '__all__'



class TBCP_ITEM_META_INFO_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TBCP_ITEM_META_INFO
        field = '__all__'



class TBCP_MEMBER_INFO_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TBCP_MEMBER_INFO
        fields = '__all__'



class TBCP_MEMBER_LIST_STAT_INFO_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TBCP_MEMBER_LIST_STAT_INFO
        # fields = '__all__'
        fields = ('MARKET_INFO', 'PRODUCT_INFO', 'MEMBER_INFO', 'TRADE_DATE', 'PROCESS_INFO','ITEM_GROUP', 'ITEM_CODE', 'ITEM_SEQ', 'END_BIT')



class TBCP_MEMBER_LIST_DETAIL_INFO_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TBCP_MEMBER_LIST_DETAIL_INFO
        fields = '__all__'


'''
class TBCP_MEMBER_REQUEST_STAT_INFO_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TBCP_MEMBER_REQUEST_STAT_INFO
        fields = '__all__'
'''
        