from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = 'ADMIN'
    INVESTOR = 'INVERSOR' 
    OPERATOR = 'OPERADOR'
    
    