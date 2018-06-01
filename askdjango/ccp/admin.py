from django.contrib import admin
from .models import TBCP_MEMBER_INFO, TBCP_MEMBER_LIST_STAT_INFO, TBCP_MARKET_META_INFO, TBCP_PRODUCT_META_INFO, TBCP_ITEM_META_INFO, TBCP_MEMBER_LIST_DETAIL_INFO


# Register your models here.

@admin.register(TBCP_MEMBER_INFO)
class TBCP_MEMBER_INFO_Admin(admin.ModelAdmin):
    list_display = ('MARKET_INFO', 'PRODUCT_INFO', 'MEMBER_INFO', 'LOGIN_INFO', 'PASSWORD_INFO', 'TOKEN_INFO', 'PERMISSION_INFO','OLD_DATE_USE','CREATE_INFO','UPDATE_INFO')

@admin.register(TBCP_MEMBER_LIST_STAT_INFO)
class TBCP_MEMBER_LIST_STAT_INFO_Admin(admin.ModelAdmin):
    list_display = ('MARKET_INFO', 'PRODUCT_INFO', 'MEMBER_INFO','TRADE_DATE','PROCESS_INFO', 'ITEM_GROUP', 'ITEM_CODE', 'ITEM_SEQ', 'END_BIT','MEMBER_ASK_CNT')

@admin.register(TBCP_MEMBER_LIST_DETAIL_INFO)
class TBCP_MEMBER_LIST_DETAIL_INFO_Admin(admin.ModelAdmin):
    list_display = ('MARKET_INFO', 'PRODUCT_INFO', 'MEMBER_INFO','TRADE_DATE','PROCESS_INFO', 'ITEM_GROUP', 'ITEM_CODE', 'ITEM_SEQ', 'ITEM_DATA')

@admin.register(TBCP_MARKET_META_INFO)
class TBCP_MARKET_META_INFO_Admin(admin.ModelAdmin):
    list_display = ('MARKET_INFO',)

@admin.register(TBCP_PRODUCT_META_INFO)
class TBCP_PRODUCT_META_INFO_Admin(admin.ModelAdmin):
    list_display = ('PRODUCT_INFO',)

@admin.register(TBCP_ITEM_META_INFO)
class TBCP_ITEM_META_INFO_Admin(admin.ModelAdmin):
    list_display = ('ITEM_GROUP', 'ITEM_CODE')
