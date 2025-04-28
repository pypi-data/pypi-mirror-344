from typing import Dict, Optional, Any, List, Union, Callable, Awaitable

from kiwoom_rest_api.core.sync_client import make_request
from kiwoom_rest_api.core.async_client import make_request_async


class StockInfo:
    """한국 주식 종목 정보 관련 API를 제공하는 클래스"""
    
    def __init__(
        self, 
        base_url: str = None, 
        token_manager=None, 
        use_async: bool = False
    ):
        """
        StockInfo 클래스 초기화
        
        Args:
            base_url (str, optional): API 기본 URL
            token_manager: 토큰 관리자 객체
            use_async (bool): 비동기 클라이언트 사용 여부 (기본값: False)
        """
        self.base_url = base_url
        self.token_manager = token_manager
        self.use_async = use_async
        
        # 사용할 request 함수 결정
        self._request_func = make_request_async if use_async else make_request
    
    def _get_access_token(self) -> Optional[str]:
        """토큰 매니저로부터 액세스 토큰을 가져옵니다."""
        if self.token_manager:
            return self.token_manager.get_token()
        return None
    
    async def _get_access_token_async(self) -> Optional[str]:
        """토큰 매니저로부터 비동기적으로 액세스 토큰을 가져옵니다."""
        if self.token_manager and hasattr(self.token_manager, 'get_token_async'):
            return await self.token_manager.get_token_async()
        return self._get_access_token()  # 비동기 메서드가 없으면 동기 버전 사용
    
    def _make_request(self, method: str, tr_id: str, url: str, **kwargs):
        """API 요청을 실행합니다."""
        headers = kwargs.pop("headers", {})
        headers["api-id"] = tr_id
        headers["content-type"] = "application/json;charset=UTF-8"
        
        # Check if there's a nested headers in kwargs (e.g. in json payload)
        if "json" in kwargs and "headers" in kwargs.get("json", {}):
            headers.update(kwargs["json"]["headers"])
            del kwargs["json"]["headers"]
        elif "headers" in kwargs:
            headers.update(kwargs["headers"])
            del kwargs["headers"]
        
        if self.token_manager:
            access_token = self._get_access_token()
            headers["Authorization"] = f"Bearer {access_token}"
            
        return make_request(
            endpoint=url,
            method=method,
            headers=headers,
            **kwargs
        )
    
    async def _make_request_async(self, method: str, tr_id: str, url: str, **kwargs):
        """API 요청을 비동기적으로 실행합니다."""
        headers = kwargs.pop("headers", {})
        headers["api-id"] = tr_id
        headers["content-type"] = "application/json;charset=UTF-8"
        
        if self.token_manager:
            access_token = await self._get_access_token_async()
            headers["Authorization"] = f"Bearer {access_token}"
        
        return await make_request_async(
            endpoint=url,
            method=method,
            headers=headers,
            **kwargs
        )
    
    def _execute_request(self, method: str, tr_id: str, url: str, **kwargs):
        """동기 또는 비동기 요청을 실행합니다."""
        if self.use_async:
            return self._make_request_async(method, tr_id, url, **kwargs)
        else:
            return self._make_request(method, tr_id, url, **kwargs)
    
    def basic_stock_information_request_ka10001(
        self, stock_code: str, cont_yn: str = "N", next_key: str = "0"
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """
        주식기본정보요청
        API ID: ka10001

        Args:
            stock_code (str): 종목코드 (예: '005930')

        Returns:
            Dict[str, Any] or Awaitable[Dict[str, Any]]: 주식 기본 정보
        """
        url = f"{self.base_url}/api/dostk/stkinfo" if self.base_url else "/api/dostk/stkinfo"
        data = {"stk_cd": stock_code, "headers": {"cont-yn": cont_yn, "next-key": next_key}}
        
        return self._execute_request("POST", "ka10001", url=url, json=data)
    
    def stock_trading_agent_request_ka10002(
        self, stock_code: str, cont_yn: str = "N", next_key: str = "0"
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """
        주식 거래원 요청
        API ID (TR_ID): ka10002 (명세서 예시 ID, 실제 TR ID 확인 필요)

        Args:
            stock_code (str): 종목코드 (예: '005930', 'KRX:039490')
            cont_yn (str, optional): 연속조회여부. Defaults to "N".
            next_key (str, optional): 연속조회키. Defaults to "".

        Returns:
            Dict[str, Any] or Awaitable[Dict[str, Any]]: 현재가 정보 딕셔너리 또는 Awaitable 객체
        """

        url = f"{self.base_url}/api/dostk/stkinfo" if self.base_url else "/api/dostk/stkinfo"
        
        data = {
            "stk_cd": stock_code,
            "headers": {
                "cont-yn": cont_yn,
                "next-key": next_key
            }
        }

        return self._execute_request("POST", "ka10002", url=url, json=data)
    
    def daily_stock_price_request_ka10003(
        self,
        stock_code: str,
        cont_yn: str = "N",
        next_key: str = ""
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """
        체결 정보 요청
        API ID (TR_ID): ka10003 (명세서 예시 ID, 실제 TR ID 확인 필요)

        Args:
            stock_code (str): 종목코드 (예: '005930', 'KRX:039490')
            cont_yn (str, optional): 연속조회여부. 응답 헤더의 값을 사용. Defaults to "N".
            next_key (str, optional): 연속조회키. 응답 헤더의 값을 사용. Defaults to "".

        Returns:
            Dict[str, Any] or Awaitable[Dict[str, Any]]: 체결 정보 딕셔너리 또는 Awaitable 객체
        """
        url = f"{self.base_url}/api/dostk/stkinfo" if self.base_url else "/api/dostk/stkinfo"
        
        data = {
            "stk_cd": stock_code,
            "headers": {
                "cont-yn": cont_yn,
                "next-key": next_key
            }
        }
        return self._execute_request("POST", "ka10003", url=url, json=data)
    
    def multiple_stock_quotes_request_ka10004(
        self, stock_codes: List[str]
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """
        복수종목 현재가를 조회합니다.
        API ID: ka10004

        Args:
            stock_codes (List[str]): 종목코드 리스트 (최대 50개)

        Returns:
            Dict[str, Any] or Awaitable[Dict[str, Any]]: 복수종목 현재가 데이터
        """
        if len(stock_codes) > 50:
            raise ValueError("최대 50개의 종목코드만 한 번에 조회할 수 있습니다.")
            
        url = f"{self.base_url}/api/dostk/multiquote" if self.base_url else "/api/dostk/multiquote"
        data = {"stk_cd_list": ";".join(stock_codes)}
        return self._execute_request("POST", "ka10004", url=url, json=data)
    
    def stock_volume_trend_request_ka10005(
        self, stock_code: str
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """
        거래량 급증 종목을 조회합니다.
        API ID: ka10005

        Args:
            stock_code (str): 종목코드 (예: '005930')

        Returns:
            Dict[str, Any] or Awaitable[Dict[str, Any]]: 거래량 급증 데이터
        """
        url = f"{self.base_url}/api/dostk/volume" if self.base_url else "/api/dostk/volume"
        data = {"stk_cd": stock_code}
        return self._execute_request("POST", "ka10005", url=url, json=data)
    
    def stock_order_book_request_ka10006(
        self, stock_code: str
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """
        호가 정보를 조회합니다.
        API ID: ka10006

        Args:
            stock_code (str): 종목코드 (예: '005930')

        Returns:
            Dict[str, Any] or Awaitable[Dict[str, Any]]: 호가 정보 데이터
        """
        url = f"{self.base_url}/api/dostk/orderbook" if self.base_url else "/api/dostk/orderbook"
        data = {"stk_cd": stock_code}
        return self._execute_request("POST", "ka10006", url=url, json=data)
