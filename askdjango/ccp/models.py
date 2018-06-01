from django.db import models

# Create your models here.

# URL PATH 메타정보 DB
class TBCP_MARKET_META_INFO(models.Model):
    MARKET_INFO = models.CharField(max_length=30)



class TBCP_PRODUCT_META_INFO(models.Model):
    PRODUCT_INFO = models.CharField(max_length=30)



class TBCP_MEMBER_INFO(models.Model):
    MARKET_INFO = models.CharField(max_length=30)
    PRODUCT_INFO = models.CharField(max_length=30)
    MEMBER_INFO = models.CharField(max_length=30)
    LOGIN_INFO = models.CharField(max_length=30) #CCP_USD-IRS_00002_01
    PASSWORD_INFO = models.CharField(max_length=30)
    PERMISSION_INFO = models.CharField(max_length=30)
    OLDPASS_INFO = models.CharField(max_length=30, blank=True )
    TOKEN_INFO = models.TextField()
    OLDTOKEN_INFO = models.TextField(blank=True)
    OLD_DATE_USE = models.CharField(max_length= 30)
    CREATE_INFO = models.DateTimeField(auto_now_add=True)
    UPDATE_INFO = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'tbcp_member_info'
        unique_together = (('MARKET_INFO', 'PRODUCT_INFO', 'MEMBER_INFO'),)



class TBCP_ITEM_META_INFO(models.Model):
    ITEM_GROUP = models.CharField(max_length=30)
    ITEM_CODE = models.CharField(max_length=30)



class TBCP_MEMBER_LIST_STAT_INFO(models.Model):
    MARKET_INFO = models.CharField(max_length=30)
    PRODUCT_INFO = models.CharField(max_length=30)
    MEMBER_INFO = models.CharField(max_length=30)
    TRADE_DATE = models.CharField(max_length=30)
    PROCESS_INFO = models.CharField(max_length=30)
    ITEM_GROUP = models.CharField(max_length=30)
    ITEM_CODE = models.CharField(max_length=30)
    ITEM_SEQ = models.CharField(max_length=30)
    END_BIT = models.CharField(max_length=30)
    MEMBER_ASK_CNT = models.IntegerField(default=0)



class TBCP_MEMBER_LIST_DETAIL_INFO(models.Model):
    MARKET_INFO = models.CharField(max_length=30)
    PRODUCT_INFO = models.CharField(max_length=30)
    MEMBER_INFO = models.CharField(max_length=30)
    TRADE_DATE = models.CharField(max_length=30)
    PROCESS_INFO = models.CharField(max_length=30)
    ITEM_GROUP = models.CharField(max_length=30)
    ITEM_CODE = models.CharField(max_length=30)
    ITEM_SEQ = models.CharField(max_length=30)
    ITEM_DATA = models.CharField(max_length=99999)
    
