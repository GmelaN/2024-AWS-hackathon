from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from base.base_model import CommonResponseModel
from base.response_code import ResponseCode


app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(CommonResponseModel(success=False, data="", code=ResponseCode.INTERNAL_SERVER_ERROR))
    )


@app.get("/error")
async def read_error():
    raise HTTPException(status_code=404, detail="Item not found", code=ResponseCode.NOT_FOUND)
