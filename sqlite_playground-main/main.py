import databases
import fastapi as fa
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = fa.FastAPI(
    title="kate",
    debug=True,
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


@app.get("/author/{id}", response_class=HTMLResponse)
async def read_item(request: fa.Request, id: int):
    author = await db.fetch_one(
        """--sql
        select * from author
        left join author_died
            on author.id = author_died.author_id
        where author.id = :id
        """,
        {"id": id},
    )
    countries = await db.fetch_all(
        """--sql
        select * from author
        inner join author_country
            on author.id = author_country.author_id
        inner join country
            on country.id = author_country.country_id
        where author.id = :id
        """,
        {"id": id},
    )
    item_groups = await db.fetch_all(
        """--sql
        select category.name as 'category' from author
        inner join author_item
            on author.id = author_item.author_id
        inner join item
            on item.id = author_item.item_id
        inner join category
            on category.id = item.category_id
        where author.id = :id
        group by category.name
        """,
        {"id": id},
    )

    mapper = {}
    for group in item_groups:
        category_name = group["category"]
        print(category_name)
        items = await db.fetch_all(
            """--sql
            select item.name from author
            inner join author_item
                on author.id = author_item.author_id
            inner join item
                on item.id = author_item.item_id
            inner join category
                on category.id = item.category_id
            where author.id = :id and category.name = :category
        """,
            {"id": id, "category": category_name},
        )
        mapper[category_name] = [item.name for item in items]

    print(mapper)

    return templates.TemplateResponse(
        "author.html",
        {
            "request": request,
            "author": author,
            "countries": countries,
            "mapper": mapper,
        },
    )


@app.get("/author", response_class=HTMLResponse)
async def artsts(request: fa.Request):
    authors = await db.fetch_all("select * from author;")
    return templates.TemplateResponse(
        "authors.html", {"request": request, "authors": authors, "title": "Authors"}
    )


@app.get("/", response_class=HTMLResponse)
async def index(request: fa.Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/item/{id}", response_class=HTMLResponse)
async def item(request: fa.Request, id: int):
    item = await db.fetch_one(
        """--sql
        select * from item
        where item.id = :id
    """,
        {"id": id},
    )
    authors = await db.fetch_all(
        """--sql
        select * from author_item
        inner join author
            on author.id = author_item.author_id
        where author_item.item_id = :id
    """,
        {"id": id},
    )
    print(authors)
    countries = await db.fetch_all(
        """--sql
        select country.name from author_item
        inner join author
            on author.id = author_item.author_id
        inner join author_country
            on author.id = author_country.author_id
        inner join country
            on country.id = author_country.country_id
        where author_item.item_id = :id
    """,
        {"id": id},
    )
    print(countries)
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
        items = await db.fetch_all(
            """--sql
            select item.name, item.id from item
            inner join category
                on category.id = item.category_id
            where category.name = :category
        """,
            {"category": category_name},
        )
        mapper[category_name] = [(item.name, item.id) for item in items]

    print(mapper)

    return templates.TemplateResponse(
        "items.html",
        {
            "request": request,
            "mapper": mapper,
        },
    )
