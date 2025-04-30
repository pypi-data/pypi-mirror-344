from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum
from typing import Optional,Union,List,Any

class Operator(str, Enum):
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NIN = "nin"
    LIKE = "like"
    ILIKE = "ilike"
    BETWEEN = "between"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"

class LogicalOperator(str, Enum):
    AND = "and"
    OR = "or"

class SortDirection(str, Enum):
    ASC = "ASC"
    DESC = "DESC"

class FieldTypeEnum(str, Enum):
    STR = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    LIST = "list"
    DICT = "dict"
    DATETIME = "datetime"


class BaseSchema(BaseModel):
    id:str
    uuid:str
    created_at:datetime
    updated_at:datetime

    model_config = ConfigDict(from_attributes=True)

class FindUniqueByFieldInput(BaseModel):
    field_name:str
    sort_order:Optional[SortDirection] = SortDirection.ASC


class FieldOperatorCondition(BaseModel):
    field: str
    operator: Operator
    value: Union[str,int,float,bool,list,dict,datetime]

class LogicalCondition(BaseModel):
    operator: LogicalOperator
    conditions: List["ConditionType"]

ConditionType = Union["LogicalCondition", "FieldOperatorCondition"]



# Top-level filter schema
class FilterSchema(BaseModel):
    operator: LogicalOperator
    conditions: List[ConditionType]

class SortSchema(BaseModel):
    field:str
    direction:SortDirection

class ListFilter(BaseModel):
    filters: Optional[FilterSchema] = None
    sort_order: Optional[List[SortSchema]] = None
    page: Optional[int] = 1
    page_size: Optional[int] = 20
    search: Optional[str] = None
    searchable_fields: Optional[List[str]] = None

class SearchOptions(BaseModel):
    search: Optional[str] = None
    sort_order: Optional[List[SortSchema]] = None
    page: Optional[int] = None
    page_size: Optional[int] = None
    total_pages: Optional[int] = None
    total_count: Optional[int] = None

class ListResponse(BaseModel):
    founds: List[Any]
    search_options: SearchOptions



class AddColumnField(BaseModel):
    column_field:str
    column_type:FieldTypeEnum
    column_default:Optional[Any] = None