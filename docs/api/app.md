<a id="app"></a>

# app

<a id="app.Book"></a>

## Book Objects

```python
class Book(BaseModel)
```

图书数据模型。

<a id="app.create_book"></a>

#### create\_book

```python
@app.post("/books/", status_code=201)
def create_book(book: Book)
```

创建一个新的图书记录。

- **book**: 符合 Book 模型的 JSON 数据
- **返回**: 创建成功的图书对象

<a id="app.health_check"></a>

#### health\_check

```python
@app.get("/health")
def health_check()
```

简单的健康检查接口

