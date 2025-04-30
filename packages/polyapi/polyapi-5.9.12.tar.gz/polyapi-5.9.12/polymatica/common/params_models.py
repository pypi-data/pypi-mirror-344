from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict


class SetMeasuresParams(BaseModel):
    model_config = ConfigDict(strict=True)
    measure_names: List[str]
    measure_formats: List[dict]
    set_to_default: bool = False


class GetMeasuresParams(BaseModel):
    model_config = ConfigDict(strict=True)
    measure_names: Optional[List[str]] = None
    return_id: Optional[bool] = False


class CreateSphereParams(BaseModel):
    model_config = ConfigDict(strict=True)
    cube_name: str
    source_name: str
    file_type: str
    update_params: Optional[dict] = None
    sql_params: Optional[dict] = None
    user_interval: str = "с текущего дня"
    filepath: str = ""
    separator: str = ""
    increment_dim: str = ""
    interval_dim: str = ""
    interval_borders: Optional[list] = None
    encoding: str = ""
    delayed: bool = False
    modified_records_params: Optional[dict] = None


class UpdateCubeParams(BaseModel):
    model_config = ConfigDict(strict=True)
    cube_name: str
    new_cube_name: Optional[str] = None
    update_params: Optional[dict] = None
    user_interval: str = "с текущего дня"
    delayed: bool = False
    increment_dim: str = ""
    interval_dim: str = ""
    interval_borders: Optional[list] = None
    modified_records_params: Optional[dict] = None


class CleanUpParams(BaseModel):
    model_config = ConfigDict(strict=True)
    cube_name: str
    dimension_name: str
    sql_params: dict
    is_update: bool = True


class RenameDimsParams(BaseModel):
    model_config = ConfigDict(strict=True)
    dim_name: str
    new_name: str


class SetMeasureVisibilityParams(BaseModel):
    model_config = ConfigDict(strict=True)
    measure_names: Union[str, List[str]]
    is_visible: bool = False


class DeleteDimFilterParams(BaseModel):
    model_config = ConfigDict(strict=True)
    dim_name: str
    filter_name: Union[str, list, set, tuple]
    num_row: int = 100


class CreateLayerParams(BaseModel):
    model_config = ConfigDict(strict=True)
    set_active: bool = True


class CreateConsistentDimParams(BaseModel):
    model_config = ConfigDict(strict=True)
    formula: str
    separator: str
    dimension_list: List[str]
