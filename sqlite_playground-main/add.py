db = databases.Database("sqlite:///./db/main.db")
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")