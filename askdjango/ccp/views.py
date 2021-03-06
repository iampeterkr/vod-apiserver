''' [완료]  URL PATH 사용 기능 '''
''' [완료]  DB queryset 처리  '''
''' [완료]  print를 logging 모듈을 사용하여 대체..'''
'''        logging reference :  http://www.jinniahn.com/2016/10/python-logger.html '''
''' [완료]  회원별 LIST 조회하는 기능 구현 '''
''' [완료]  UrlCheckView -> Common , List 로 분리  '''
''' [완료]  LIST 응답 데이타(JSON) 만들기, Response 오름차순 해결(OrderedDict) '''


from rest_framework import viewsets
from .models import TBCP_MEMBER_INFO, TBCP_MEMBER_LIST_STAT_INFO, TBCP_MARKET_META_INFO, TBCP_PRODUCT_META_INFO, TBCP_ITEM_META_INFO, TBCP_MEMBER_LIST_DETAIL_INFO
from .serializers import TBCP_MEMBER_INFO_Serializer, TBCP_MEMBER_LIST_STAT_INFO_Serializer, TBCP_MARKET_META_INFO_Serializer, TBCP_PRODUCT_META_INFO_Serializer, TBCP_ITEM_META_INFO_Serializer, TBCP_MEMBER_LIST_DETAIL_INFO_Serializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import list_route
from django.http import JsonResponse, HttpResponse
from django.utils.http import urlencode
from django.core.exceptions import ObjectDoesNotExist
from . import constant
from . import constant as const 
import datetime
from django.db.models import Q
#OrderedDict
from collections import OrderedDict



# logging
import logging                            #<---- 1. 로그 모듈 
logger = logging.getLogger('ccp')       #<---- 2. 로그 생성 
# 기본 로그 환경 , 1개의 환경일때 사용, 여러개 사용일때는 Handler 사용   
# logging.basicConfig( format='%(asctime)s:%(message)s',
#                      filename='example.log',
#                      filemode='a',
#                      level=logging.DEBUG)  
logger.setLevel(logging.DEBUG)            #<-----3. 레벨 생성
# 파일 핸들러 생성 
debugHandler = logging.FileHandler('debug.log') #DEBUG 이하 저장 
debugHandler.setLevel(logging.DEBUG)    
releaseHandler = logging.FileHandler('release.log')  #<---- 5
releaseHandler.setLevel(logging.ERROR)  #ERROR 이하 저장
# 화면에 출력하는 핸들러
ch = logging.StreamHandler()                      #<---- 6
ch.setLevel(logging.ERROR) ## ERROR 이하 저장 
# 포멧터 생성 & 핸들러에 등록                     
formatter = logging.Formatter(                    #<---- 7
    '%(asctime)s\t%(levelname)s\t%(name)s\t%(module)s.py[%(lineno)d]\t%(message)s ')
ch.setFormatter(formatter)                        #<---- 8
debugHandler.setFormatter(formatter)
releaseHandler.setFormatter(formatter)
# 핸들러를 로거에 등록, 다수의 핸들러를 등록할 수 있다.
logger.addHandler(ch)                             #<---- 9
logger.addHandler(releaseHandler)
logger.addHandler(debugHandler)
# 로그 출력 DEMO, 아래와 같이 debug, info, warn, error, critical 단계로 사용 
# logger.debug('debug:[D]')
# logger.info('info:[I]')
# logger.warn('warn:[W]')
# logger.error('error:[E]')
# logger.critical('critical:[C]')


# ViewSet.as_view를 호출시, 'get' 으로 호출되면, 클래스에 정의된 'public_list'를 호출하게끔만들어진다
class TBCP_MEMBER_LIST_STAT_INFO_ViewSet(viewsets.ModelViewSet):
    def __init__(self):
        self.logger = logging.getLogger('ccp.TBCP_MEMBER_LIST_STAT_INFO_ViewSet')
        self.logger.info('TBCP_MEMBER_LIST_STAT_INFO_ViewSet.__init__ is callled')


    queryset = TBCP_MEMBER_LIST_STAT_INFO.objects.all()
    # serializer_class = TBCP_MEMBER_LIST_STAT_INFO_Serializer
    serializer_class = TBCP_MEMBER_LIST_STAT_INFO_Serializer(queryset)

    @list_route()
    def api_list(self, request, *args, **kwargs):
        item_dic = OrderedDict()

        logger.info('# api_list() is called....')
        temp_path = self.request.path[1:] # 맨앞 '/' 제거
        temp_path = temp_path.lower() # 입력값 lower 변경 
        temp_path = temp_path.split('/')  # path 사이 '/' 모두 제거      
        v_api_list = temp_path[0]
        v_market = temp_path[1]
        v_product = kwargs['u_product'].lower()
        v_member = kwargs['u_member'].lower()
        v_date = kwargs['u_date'].lower()
        v_item = kwargs['u_item'].lower()

        # 당일 system 시간 조회 
        business_date = datetime.datetime.today().strftime('%Y%m%d')
        logger.info('# SystemDate[%s]...' %business_date)

        # URL Check, 입력된 값이 기본 URL 메타 값이 맞는지 사전 확인 
        rtUrlCheck = {}
        #UrlCheckViewCommon() : URL 각 META값 확인
        logger.info('# UrlCheckViewCommon() is called .....')
        rtUrlCheck = UrlCheckViewCommon(v_market, v_product, v_member, v_date, v_item)

        #error 처리 
        if rtUrlCheck['error'] != constant.CHECK_OK:
            self.logger.error('# UrlCheckViewCommon() ERROR_PATH [%s]' % rtUrlCheck['error'])
            return Response('UrlCheckViewCommon() ERROR_PATH [%s]' %temp_path, status = status.HTTP_400_BAD_REQUEST)
            # return HttpResponse('UrlCheckViewCommon() ERROR_PATH : ', rtUrlCheck['error'])
        else: # O.K
            self.logger.info('# UrlCheckViewCommon() Return O.K!! rtUrlCheck[%s]' % rtUrlCheck['error'])
            pass

        #URLCheckViewList() : LIST 인 경우에 해당 CASE만 확인
        self.logger.info('# Call UrlCheckViewList()....')
        rtUrlCheck = UrlCheckViewList(v_market, v_product, v_member, v_date, v_item)
        if rtUrlCheck['error'] != constant.CHECK_OK:
            #error 처리
            self.logger.error('# UrlCheckViewList ERROR_PATH [%s]' % rtUrlCheck['error'])
            return HttpResponse('UrlCheckViewList ERROR_PATH : ', rtUrlCheck['error'])
        else: # O.K 
            pass


        # item_code check 
        if v_item == 'all':
            qs = TBCP_MEMBER_LIST_STAT_INFO.objects.filter(MEMBER_INFO = v_member)
            print('qs count = %s' %qs.count())
        elif v_item in constant.ITEM_GROUP:
            qs = TBCP_MEMBER_LIST_STAT_INFO.objects.filter(ITEM_GROUP = v_item)
            print('qs count = %s' %qs.count())
        elif v_item in constant.ITEM_CODE:
            qs = TBCP_MEMBER_LIST_STAT_INFO.objects.filter(ITEM_CODE = v_item)
            print('qs count = %s' %qs.count())
        else:
            print ('error')

        temp_list = []
        temp_str = ''
        for i in qs:
            temp_list.append(constant.MARKET_INFO +  i.MARKET_INFO)
            temp_list.append(constant.PRODUCT_INFO + i.PRODUCT_INFO)
            print (temp_list)
        # return Response(temp_list, status=None)
        # response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return Response(
                        {
                            'data' :qs.values(  'MARKET_INFO',\
                                                'PRODUCT_INFO',\
                                                'MEMBER_INFO',\
                                                'TRADE_DATE',\
                                                'ITEM_GROUP',\
                                                'ITEM_CODE',\
                                                'ITEM_SEQ',\
                                                'END_BIT'),
                            'ErrorCode' :'Error number explain ',
                            'ErrorText':'error text explaing',
                            'Input URL PATH' : temp_path
                        },
                        status=status.HTTP_200_OK,
                        )


        if qs_itemcode:
            print ('개별 입력 ')
            # Query Memeber's List Data information 
            try:
                # qs = TBCP_MEMBER_LIST_STAT_INFO.objects.get(MARKET_INFO = v_market, PRODUCT_INFO = v_product, MEMBER_INFO = v_member, ITEM_CODE = v_item)
                qs = TBCP_MEMBER_LIST_STAT_INFO.objects.all()
                qs = qs.filter(MARKET_INFO = v_market, PRODUCT_INFO = v_product, MEMBER_INFO = v_member, ITEM_CODE = v_item)
                qs_cnt = qs.count()
                if qs_cnt == 1:
                # if qs:
                    
                    item_dic['MARKET_INFO'] = qs.MARKET_INFO
                    item_dic['PRODUCT_INFO']= qs.PRODUCT_INFO
                    item_dic['MEMBER_INFO'] = qs.MEMBER_INFO
                    item_dic['TRADE_DATE']  = qs.TRADE_DATE
                    item_dic['TRADE_DATE']  = qs.TRADE_DATE
                    item_dic['ITEM_GROUP']  = qs.ITEM_GROUP
                    item_dic['ITEM_CODE']   = qs.ITEM_CODE
                    item_dic['ITES_SEQ']    = qs.ITEM_SEQ
                    item_dic['END_BUT']     = qs.END_BIT
                    item_dic['ERROR_CODE']  = constant.CHECK_OK 
                    item_dic['ERROR_TEXT']  = constant.CHECK_OK
                    
                    self.logger.info('# Query exist O.K !!' )
                    self.logger.info('# Input v_market[%s]' % v_market)
                    self.logger.info('# Input v_product[%s]' % v_product)
                    self.logger.info('# Input v_member[%s]' % v_member)
                    self.logger.info('# DB MARKET_INFO[%s]' % item_dic['MARKET_INFO'])
                    self.logger.info('# DB PRODUCT_INFO[%s]'% item_dic['PRODUCT_INFO'])
                    self.logger.info('# DB MEMBER_INFO[%s]' % item_dic['MEMBER_INFO'])
            except ObjectDoesNotExist as err:
                    self.logger.error('# DB[TBCP_MEMBER_LIST_STAT_INFO] ObjectDoesNotExist ')
                    self.logger.info('# Input v_market[%s]' % v_market)
                    self.logger.info('# Input v_product[%s]' % v_product)
                    self.logger.info('# Input v_member[%s]' % v_member)
                    self.logger.info('# DB MARKET_INFO[%s]' %item_dic['MARKET_INFO'])
                    self.logger.info('# DB PRODUCT_INFO[%s]' %item_dic['PRODUCT_INFO'])
                    self.logger.info('# DB MEMBER_INFO[%s]' %item_dic['MEMBER_INFO'])
                    return HttpResponse('DB[TBCP_MEMBER_LIST_STAT_INFO] ObjectDoesNotExist : {}'.format(ObjectDoesNotExist))
            else :
                self.logger.info('#---------Result------------' )
                self.logger.info('# MEMBER_ASK_CNT[%s] Before' %qs.MEMBER_ASK_CNT)
                qs.MEMBER_ASK_CNT = qs.MEMBER_ASK_CNT + 1
                qs.save()
                self.logger.info('# MEMBER_ASK_CNT[%s] After' %qs.MEMBER_ASK_CNT)
                if qs:
                    self.logger.info('# Finds Query Data [%s]' %temp_path )
                    # return Response(item_dic)
                    return Response(qs.values())
                else:
                    self.logger.critical('# No Finds Query Data [%s]' %temp_path )
                    return Response('No Finds Query Data, Check the path & system, please !! [{}]'.format(temp_path), status=status.HTTP_400_BAD_REQUEST)
                #    return HttpResponse('No Finds Query Data, Check the path & system, please !! [{}]'.format(temp_path))
        else:
            # all, RISK, CLEARING ....
            qs = TBCP_ITEM_META_INFO.objects.filter(ITEM_GROUP=v_item)
            if qs or v_item =='all':
                print('그룹입력[%s] ' %v_item)
                # Query Memeber's List Data Group information 
                try:
                    qs = TBCP_MEMBER_LIST_STAT_INFO.objects.all()
                    if v_item =='all':
                        qs = qs.filter(MARKET_INFO = v_market, PRODUCT_INFO = v_product, MEMBER_INFO = v_member)
                    else:
                        qs = qs.filter(MARKET_INFO = v_market, PRODUCT_INFO = v_product, MEMBER_INFO = v_member, ITEM_GROUP=v_item)

                    if qs: 
                        cnt = qs.count()
                        print('cnt %s' %cnt)
                        print('qs.value() [%s]' %qs.values())
                        print('qs.row(pk=1) : %s' %qs.values())

                        # case : As using 'qs.ojbects.all()' 
                        # for item in qs:
                        #     item_dic['MARKET_INFO'] = item.MARKET_INFO
                        #     item_dic['PRODUCT_INFO'] = item.PRODUCT_INFO
                        #     item_dic['MEMBER_INFO'] = item.MEMBER_INFO
                        # item_dic.update = ({'MARKET_INFO':qs.MARKET_INFO})
                        item_list = []

                        for item in qs:
                            print ('@@ item loop')
                            temp= '{"MARKET_INFO":"%s"}' %item.MARKET_INFO
                            item_list.append (temp)
                            temp = '{"PRODUCT_INFO":"%s"}' %item.PRODUCT_INFO
                            item_list.append (temp) 
                        
                        # for key, value in item_dic.items():
                            # print(key, value)   
                        # return Response('all querying : %s' %item_list)
                        # return Response('all querying : %s' %qs.values())
                        return Response(qs.values())
                    else:
                        return Response(' not equal - qs ')
                except ObjectDoesNotExist as err:
                        self.logger.error('# DB[TBCP_MEMBER_LIST_STAT_INFO] ObjectDoesNotExist ')
                        self.logger.info('# Input v_market[%s]' % v_market)
                        self.logger.info('# Input v_product[%s]' % v_product)
                        self.logger.info('# Input v_member[%s]' % v_member)
                        self.logger.info('# DB MARKET_INFO[%s]' %item_dic['MARKET_INFO'])
                        self.logger.info('# DB PRODUCT_INFO[%s]' %item_dic['PRODUCT_INFO'])
                        self.logger.info('# DB MEMBER_INFO[%s]' %item_dic['MEMBER_INFO'])
                        return HttpResponse('DB[TBCP_MEMBER_LIST_STAT_INFO] ObjectDoesNotExist : {}'.format(ObjectDoesNotExist))

                else :
                    self.logger.info('#---------Result------------' )
                    self.logger.info('# MEMBER_ASK_CNT[%s] Before' %qs.MEMBER_ASK_CNT)
                    qs.MEMBER_ASK_CNT = qs.MEMBER_ASK_CNT + 1
                    qs.save()
                    self.logger.info('# MEMBER_ASK_CNT[%s] After' %qs.MEMBER_ASK_CNT)
                    if qs:
                        self.logger.info('# Finds Query Data [%s]' %temp_path )
                        return Response(item_dic)
                    else:
                        self.logger.critical('# No Finds Query Data [%s]' %temp_path )
                        return Response('No Finds Query Data, Check the path & system, please !! [{}]'.format(temp_path), status=status.HTTP_400_BAD_REQUEST)
            else:
                print(' check the item_code: %s' %v_item)
                return HttpResponse('check the item [%s] '%v_item)
            




#api_detail 호출 
class TBCP_MEMBER_LIST_DETAIL_INFO_ViewSet(viewsets.ModelViewSet):
    
    def __init__(self):
        self.logger = logging.getLogger('ccp.TBCP_MEMBER_LIST_DETAIL_INFO_ViewSet') 
        self.logger.info('TBCP_MEMBER_LIST_DETAIL_INFO_ViewSet.__init__ is callled') 

    @list_route()
    def api_detail(self, request, *args, **kwargs):
        logger.info('# api_detail() start....')
        temp_path = self.request.path[1:] # 맨앞 '/' 제거
        temp_path = temp_path.lower() # 입력값 lower 변경 
        temp_path = temp_path.split('/')  # path 사이 '/' 모두 제거      
        v_api_list = temp_path[0]
        v_market = temp_path[1]
        v_product = kwargs['u_product'].lower()
        v_member = kwargs['u_member'].lower()
        v_date = kwargs['u_date'].lower()
        v_item = kwargs['u_item'].lower()

        # 당일 system 시간 조회 
        business_date = datetime.datetime.today().strftime('%Y%m%d')
        logger.info('BusinessDate[%s]' %business_date)

        # URL Check, 입력된 값이 기본 URL 메타 값이 맞는지 사전 확인 
        rtUrlCheck = {}
        rtUrlCheck = UrlCheckViewCommon(v_market, v_product, v_member, v_date, v_item)










#UrlCheckViewCommon 
def UrlCheckViewCommon(v_market, v_product, v_member, v_date, v_item):
    ErrorBit = 'NO'
    logger.info('# def UrlCheckViewCommon() is called...')

    #MARKET CHECK
    qs = TBCP_MARKET_META_INFO.objects.get(MARKET_INFO = v_market)
    # qs = TBCP_MARKET_META_INFO.objects.all()
    # qs = qs.filter(MARKET_INFO = v_market)
    # if qs.exists():
    if qs:
        logger.info('# MARKET_INFO[%s] Existing  O.K !!' % qs.MARKET_INFO)
        pass
    else:
        ErrorBit = 'YES'
        logger.info('# MARKET_INFO[%s] No Existing. Error return !!' % v_market)
        return {'error':constant.CHECK_MARKET}

   #PRODUCT CHECK
    qs = TBCP_PRODUCT_META_INFO.objects.get(PRODUCT_INFO = v_product)
    if qs:
        logger.info('# PRODUCT_INFO[%s] Existing  O.K !!' % qs.PRODUCT_INFO)
        pass
    else:
        ErrorBit = 'YES'
        logger.info('# PRODUCT_INFO[%s] No Existing. Error return !!' % v_product)
        return {'error':constant.CHECK_PRODUCT}

    #ITEM CHECK
    if v_item == 'all':
        pass
    else:
        qs = TBCP_ITEM_META_INFO.objects.all()
        qs = qs.filter(Q(ITEM_GROUP = v_item) | Q(ITEM_CODE = v_item))
        if qs:
            logger.info('# ITEM_INFO[%s] Existing  O.K !!' % v_item)
            pass
        else:
            ErrorBit = 'YES'
            logger.info('# ITEM_INFO[%s] No Existing. Error return !!' % v_item)
            return {'error':constant.CHECK_ITEM}


    #MEMBER CHECK
    qs = TBCP_MEMBER_INFO.objects.get(MARKET_INFO = v_market, PRODUCT_INFO = v_product, MEMBER_INFO = v_member)
    if qs:
        logger.info('# Input v_market:[%s] v_product:[%s] v_member:/[%s]' %(v_market, v_product, v_member))
        pass
    else:
        logger.error('# Input v_market:[%s] v_product:[%s] v_member:[%s]' %(v_market, v_product, v_member))
        logger.error('# This Member[%s] does not have [%s] or [%s], Check the input Market, Product, Member in TBCP_MEMBER_INFO~ !!' %(v_member, v_market, v_product) )
        ErrorBit = 'YES'
        return {'error':constant.CHECK_MEMBER}

    if ErrorBit == 'NO':
        logger.info('# RtUrlCheck O.K !!.....')
        return {'error': constant.CHECK_OK}
    else:
        logger.critical('[C] ---------------------------')
        logger.critical('[C] Something are wrong !!!')
        logger.critical('[C] ErrorBit [%s]' % ErrorBit)
        logger.critical('[C] Input Path : v_marekt[%s]' % v_market)
        logger.critical('[C] Input Path : v_product[%s]' % v_market)
        logger.critical('[C] Input Path : v_member[%s]' % v_market)
        logger.critical('   ')


# LIST check
def UrlCheckViewList(v_market, v_product, v_member, v_date, v_item):
    ErrorBit = 'NO'
    logger.info('# UrlCheckViewList() starts ....')

    #DATE CHECK
    old_date_use = 'no' # It is permit bit to use past data 

    # date Check, 당일 여부 check 
    # temp_date = datetime.datetime.today().strftime('%Y-%m-%d')
    temp_date = datetime.datetime.today().strftime('%Y%m%d')
    logger.info('# SystemDate[%s] , InputDate[%s]' %(temp_date, v_date))

    # 회원정보에서 과거 데이타 조회 기능(old_date_bit) 이 있으면 과거 날짜도 허용 
    delta_date = int(temp_date) - int(v_date)
    if (delta_date < 0): # 금일 보다 미래 일자
        logger.error(' ') 
        logger.error('------------------------')
        logger.error('#[E] Check the InputDate : Future Date has Inputed')
        logger.error('------------------------')
        logger.error('# BusinessDate[%s] < InputDate[%s]' %(temp_date, v_date))
        logger.error(' ') 
        ErrorBit = 'YES'
        return {'error': constant.CHECK_DATE, 'old_date_bit':old_date_use}
    elif (delta_date > 0):
        logger.warn(' ') 
        logger.warn('------------------------')
        logger.warn('#[W] Check the InputDate : Past Date has Inputed')
        logger.warn('------------------------')
        logger.warn('# BusinessDate[%s] > InputDate[%s]' %(temp_date, v_date))

        # 과거 데이타 조회 가능 여부 확인( OLD_DATE_USE == 'yes') 
        qs = TBCP_MEMBER_INFO.objects.get(MARKET_INFO=v_market, PRODUCT_INFO=v_product, MEMBER_INFO=v_member)
        if qs:
            logger.info('# Query O.K !! v_market[%s] v_product[%s] v_member[%s]' %(v_market, v_product, v_member))
            old_date_use = qs.OLD_DATE_USE
            if old_date_use == 'yes':
                pass
            else:
                logger.error('Check the Input Date[%s], old_date_use[%s]' % (v_date, old_date_use))
                ErrorBit = 'YES'
                return {'error': constant.CHECK_DATE}
        else:
            logger.error('[E] Check the Path, we can not find the member')
            logger.error('[E] v_market[%s] v_product[%s] v_member[%s]' %(v_marekt, v_product, v_member))
            ErrorBit = 'YES'
            return {'error': constant.CHECK_DATE, 'old_date_bit':old_date_use}
    elif delta_date == 0:
        logger.info('Business Date Request !!')
        logger.info('Input Data O.K !! [%s]' %v_date)
    else:
        logger.critical('[C] ---------------------------')
        logger.critical('[C] Check the date BusinessDate[%s] , InputDate[%s]' %(temp_date, v_date))
        logger.critical('   ')
        ErrorBit = 'YES'
        return {'error': constant.CHECK_DATE, 'old_date_bit':old_date_use}

    if ErrorBit == 'NO':
        return {'error':constant.CHECK_OK, 'old_date_bit':old_date_use}
    else:
        logger.critical('[C] ---------------------------')
        logger.critical('[C] Something are wrong !!!') 
        logger.critical('[C] ErrorBit [%s]' %ErrorBit)
        logger.critical('[C] Input Path : v_marekt[%s]' %v_market)
        logger.critical('[C] Input Path : v_product[%s]' %v_market)
        logger.critical('[C] Input Path : v_member[%s]' %v_market)
        logger.critical('   ')

    
def UrlCheckViewDetail(v_market, v_product, v_member, v_date, v_item):
    pass


def UrlCheckViewData(v_market, v_product, v_member, v_date, v_item):
    pass




class TBCP_MEMBER_INFO_ViewSet(viewsets.ModelViewSet):

    queryset = TBCP_MEMBER_INFO.objects.all()
    serializer_class = TBCP_MEMBER_INFO_Serializer

    @list_route()
    def api_list(self, request, *args, **kwargs ):
        # wsgi-full-path:  print('api_list : ', self.request.get_full_path())
        # include http path : print('abosultepath : ', request.build_absolute_uri())
        print('api_list : ', (self.request.path).lower())
        temp_path = self.request.path[1:] #맨앞 '/' 삭제 
        temp_path = temp_path.split('/')   #'/' 제거후 path item만 parsing

        v_api_list = temp_path[0]
        v_market = temp_path[1]
        v_product = kwargs['u_product'].lower()
        v_member = kwargs['u_member'].lower()
        v_date = kwargs['u_date'].lower()
        v_item = kwargs['u_item'].lower()
        
        # compare member status to input path
        try:
            qs = TBCP_MEMBER_INFO.objects.filter(MEMBER_INFO = v_member)
            if qs:
                print('v_market: ', v_market)
                qs = qs.filter(MARKET_INFO = v_market)
                if qs:
                    print('v_product: ', v_product)
                    qs = qs.filter(PRODUCT_INFO = v_product)
                    for item in qs:
                        print('CREATE INFO : ', item.CREATE_INFO)

        except ObjectDoesNotExist as err:
                print ('DB does not find it ')
                return HttpResponse('Not Found : {}'.format(ObjectDoesNotExist))
        else :
            print ('-----------Result----------')
            if qs:
               print(' maching ::::', temp_path)
               print(' RESULTS DATE TIME : ', item.CREATE_INFO)
               return HttpResponse('Matching : {}'.format(temp_path))
            else:
               print('No Maching :::')
               return HttpResponse('No matching : {}'.format(temp_path))

    def api_detail(self, request):
        print('api_detail')
        return HttpResponse('api_detail')

    def api_post(self, request):
        print('api_post')
        return HttpResponse('api_post')

# api_list : urls-api-list.py 에서 호출한 api_list  
# 함수는 1개만 호출됨(마지막 )
api_list = TBCP_MEMBER_LIST_STAT_INFO_ViewSet.as_view({
    'get' : 'api_list', # class 의 함수명 호출
})

api_detail = TBCP_MEMBER_LIST_DETAIL_INFO_ViewSet.as_view({
    'get' : 'api_detail',
})

api_post = TBCP_MEMBER_LIST_STAT_INFO_ViewSet.as_view({
    'post' : 'api_post',
})

# ViewSet.as_view를 호출시, 'get' 으로 호출되면, 클래스에 정의된 'api_list'를 호출하게끔만들어진다
member_list = TBCP_MEMBER_INFO_ViewSet.as_view({
   # 'get' : 'list',
    'get' : 'api_list',

})
