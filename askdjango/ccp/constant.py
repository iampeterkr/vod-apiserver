#ccp/constant.py

# URL PATH MARKET/PRODUCT/MEMBER/PROCESS/ITEM/SEQ
# URL ex   ccp/IRS-WON/00002/LIST/ALL/00000000001
CHECK_OK      = "CHECK_OK"
CHECK_ERR_URL = "CHECK_ERROR_URL"
CHECK_MARKET  = "CHECK_MARKET"
CHECK_PRODUCT = "CHECK_PRODUCT"
CHECK_MEMBER  = "CHECK_MEMBER"
CHECK_DATE    = "CHECK_DATE"
CHECK_PROCESS = "CHECK_PROCESS"
CHECK_ITEM    = "CHECK_ITEM"
CHECK_SEQ     = "CHECK_SEQ"

# URS PATH ACCOUNTS
CHECK_ACCOUNTS= "CHECK_ACCOUNTS"
CHECK_USERNAME= "CHECK_USERNAME"
CHECK_PASSWORD= "CHECK_PASSWORD"


URL_MARKET_CCP      = "ccp"
URL_PRODUCT_IRS_WON = "irs_won"
URL_PRODUCT_IRS_USD = "irs_usd"
URL_MARKET_MEMBER   = "url_member"
URL_ITEM_LIST       = "api_list"
URL_ITEM_DETAIL     = "api_detail"
URL_ITEM_DATA       = "api_data"
URL_SEQ             = "url_seq"


MARKET_CCP      = "ccp"
IRS_WON         = "irs_won"
IRS_USD         = "irs_usd"
NDF             = "ndf"
FX              = "fx"

MARKET_INFO = "market_info:"
PRODUCT_INFO = "irs-won:"
ITEM_GROUP = ["all", "clearing", "settlement", 'risk', 'pricing']
ITEM_CODE = ['tcpmih00101', 'tcpmih00201', 'tcpmih00102', 'tcpmih00202']
