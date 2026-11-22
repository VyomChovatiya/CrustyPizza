from uuid import UUID, uuid4
from datetime import date
from decimal import Decimal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator

from service import ROOT, REGIONS, create, review

app = FastAPI(title="Warehouse lease diligence")
pages = Jinja2Templates(directory=str(ROOT / "templates"))

class Intake(BaseModel):
    request_id: UUID
    landlord: str | None = Field(default=None, max_length=250)
    site: str = Field(min_length=1, max_length=500)
    region: str
    area: Decimal | None = Field(None, gt=0, max_digits=12, decimal_places=2)
    rate: Decimal | None = Field(None, gt=0, max_digits=10, decimal_places=2)
    quote_date: date | None = None

    @field_validator("landlord","site",mode="before")
    @classmethod
    def trim(cls, value):
        return value.strip() if isinstance(value,str) else value

    @model_validator(mode="after")
    def check_inputs(self):
        if self.region not in REGIONS:
            raise ValueError("Select a listed state or union territory.")
        if any((self.area,self.rate,self.quote_date)) and not all((self.area,self.rate,self.quote_date)):
            raise ValueError("Supply area, rate and quote date together.")
        return self

@app.get("/")
def intake(request: Request):
    return pages.TemplateResponse(request=request,name="case.html",context={"regions":REGIONS,"token":uuid4()})

@app.post("/api/cases")
def submit(data: Intake):
    try:
        key = create(str(data.request_id),data.model_dump(mode="json",exclude={"request_id"}))
    except ValueError as exc:
        raise HTTPException(409,str(exc)) from exc
    return {"id":key,"report":f"/cases/{key}"}

@app.post("/cases")
async def submit_form(request: Request):
    fields = dict(await request.form())
    try:
        data = Intake(**{k:v for k,v in fields.items() if v != ""})
    except ValidationError as exc:
        return pages.TemplateResponse(request=request,name="case.html",context={"regions":REGIONS,"token":fields.get("request_id"),"values":fields,"error":exc.errors()[0]["msg"]},status_code=422)
    return RedirectResponse(submit(data)["report"],303)

@app.get("/api/cases/{key}")
def result(key: UUID):
    try:
        return review(str(key))
    except KeyError:
        raise HTTPException(404,"Case not found")

@app.get("/cases/{key}")
def show(request: Request,key: UUID):
    return pages.TemplateResponse(request=request,name="case.html",context={"case":result(key)})

from landlord import run_for_case


@app.api_route("/cases/{key}/landlord", methods=["GET", "POST"])
def landlord_discovery(request: Request, key: UUID):
    try:
        context = run_for_case(str(key), run=request.method == "POST")
    except KeyError:
        raise HTTPException(404, "Case not found")
    if request.method == "POST":
        return RedirectResponse(f"/cases/{key}/landlord", 303)
    return pages.TemplateResponse(request=request, name="landlord.html", context=dict(context, key=key))
