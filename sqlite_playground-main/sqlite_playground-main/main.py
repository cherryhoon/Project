import databases
import fastapi as fa
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import queries

app = fa.FastAPI(
    title="kate",
)

db = databases.Database("sqlite:///./db/main.db")
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/", response_class=HTMLResponse)
async def index(request: fa.Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/author/{id}", response_class=HTMLResponse)
async def read_item(request: fa.Request, id: int):
    author = await db.fetch_one(queries.author, {"id": id})
    countries = await db.fetch_all(queries.author_country, {"id": id})
    item_groups = await db.fetch_all(queries.item_groups, {"id": id})

    mapper = {}
    for group in item_groups:
        category_name = group["category"]
        items = await db.fetch_all(
            queries.author_one_group, {"id": id, "category": category_name}
        )
        mapper[category_name] = [item.name for item in items]

    return templates.TemplateResponse(
        "author.html",
        {"request": request, "author": author, "countries": countries, "mapper": mapper},
    )


@app.get("/author", response_class=HTMLResponse)
async def artsts(request: fa.Request):
    authors = await db.fetch_all("select * from author;")
    return templates.TemplateResponse(
        "authors.html", {"request": request, "authors": authors, "title": "Authors"}
    )


@app.get("/item/{id}", response_class=HTMLResponse)
async def item(request: fa.Request, id: int):
    item = await db.fetch_one(queries.item, {"id": id})
    authors = await db.fetch_all(queries.item_author, {"id": id})
    countries = await db.fetch_all(queries.item_countries, {"id": id})
    return templates.TemplateResponse(
        "item.html",
        {"request": request, "item": item, "authors": authors, "countries": countries},
    )


@app.get("/item", response_class=HTMLResponse)
async def items(request: fa.Request):
    item_groups = await db.fetch_all("select category.name as 'category' from category")
    mapper = {}
    for group in item_groups:
        category_name = group["category"]
        items = await db.fetch_all(queries.item_category, {"category": category_name})
        mapper[category_name] = [(item.name, item.id) for item in items]
    return templates.TemplateResponse(
        "items.html",
        {"request": request, "mapper": mapper},
    )
