from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(title="图书管理系统 API")


class Book(BaseModel):
    """
    图书数据模型。
    """
    id: int = Field(..., gt=0, description="图书的唯一 ID，必须大于 0")
    title: str = Field(..., min_length=1, max_length=100, description="书名")
    author: str = Field(..., description="作者姓名")
    is_published: bool = Field(True, strict=True)




@app.post("/books/", status_code=201)
def create_book(book: Book):
    """
    创建一个新的图书记录。

    - **book**: 符合 Book 模型的 JSON 数据
    - **返回**: 创建成功的图书对象
    """
    return book


@app.get("/health")
def health_check():
    """简单的健康检查接口"""
    return {"status": "ok"}