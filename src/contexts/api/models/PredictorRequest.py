from enum import Enum
from pydantic import BaseModel, validator


class EmailEnum(str, Enum):
    
    a= "yahoo"  
    b= "sapo"   
    c= "omcast"   
    d= "jetbrains" 
    e= "woodstock"
    f= "surfeu"
    g= "jubii"    
    h= "embraer"   
    i= "google"    
    j= "riotur"   
    k= "hotmail"   
    l= "gmail"    
    m= "aol"   
    n= "rediff"    
    o= "wp"   
    p= "rogers"    
    q= "shaw"
    r= "microsoft" 
    s= "yachoo"    
    t= "apple"     
    u= "uol"       

class PredictorRequest(BaseModel):
    email: EmailEnum
    nuevo: int

    @validator("email")
    def validate_sex(cls, email):
        email_ranges = [EmailEnum.a, EmailEnum.b]
        if email not in email_ranges:
            raise ValueError("Invalid email range")
        return email
    
    @validator("nuevo")
    def validate_nuevo(cls, nuevo):
        try:
            int(nuevo)
        except ValueError:
            raise ValueError("nuevo must be an integer")
        return nuevo
    


