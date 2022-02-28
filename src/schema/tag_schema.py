from typing import List

import pydantic as _pydantic



class _TagBase(_pydantic.BaseModel):
    title : str
   
    

    def __str__(self) :
        return self.title


class TagCreate(_TagBase):
    pass
    

class Tag(_TagBase):
    id: int
    

    class Config:
        orm_mode = True #TODO
