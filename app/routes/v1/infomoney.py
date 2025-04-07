import requests
from fastapi import APIRouter, HTTPException, Request

from app.middleware.rate_limit import limiter  # ⬅️ importa o limiter
from app.services.webscraping.infomoney_service import \
    fetch_infomoney_headlines

router = APIRouter()


@router.get("/infomoney", tags=["WEBSCRAPING"])
@limiter.limit("10/minute")
async def get_infomoney_news(request: Request):
    try:
        # return fetch_infomoney_headlines()
        return await fetch_infomoney_headlines()
    except HTTPException as http_exc:
        raise http_exc
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Request timed out")
    except ConnectionError:
        raise HTTPException(status_code=502, detail="Bad Gateway")
    except requests.exceptions.RequestException as req_exc:
        raise HTTPException(status_code=502, detail="Bad Gateway")
    except requests.exceptions.HTTPError as http_err:
            status_code=http_err.response.status_code if http_err.response else 500,
            status_code=http_err.response.status_code,
            detail=str(http_err)
    except requests.exceptions.ConnectionError as conn_err:
        raise HTTPException(status_code=502, detail=str(conn_err))
    except requests.exceptions.Timeout as timeout_err:
        raise HTTPException(status_code=504, detail=str(timeout_err))
    except requests.exceptions.TooManyRedirects as redirect_err:
        raise HTTPException(status_code=500, detail=str(redirect_err))
    except requests.exceptions.RequestException as req_err:
        raise HTTPException(status_code=502, detail=str(req_err))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
