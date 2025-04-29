from typing import Union

def to_base(id: Union[str, int]): 
    if not isinstance(id, str) and not isinstance(id, int):
        raise TypeError(f"Value must be 'str' or 'int', not '{type(id).__name__}'.")
        
    if len(str(id)) != 5:
    	raise ValueError(f"The length of the input is {len(str(id))}, it must be 5.")
    	
    return f"{str(id)[:3]}{int(str(id)[-2:])+1}"

def to_standard(id: Union[str, int]):
    if not isinstance(id, str) and not isinstance(id, int):
        raise TypeError(f"Value must be 'str' or 'int', not '{type(id).__name__}'.")
        
    if len(str(id)) not in [4, 5]:
    	raise ValueError(f"The length of the input is {len(str(id))}, it must be 4 or 5.")
    
    if str(id)[3:] == "0":
         raise ValueError("The lowest value must be xxx1, not xxx0")
         
    return f"{str(id)[:3]}{int(str(id)[3:])-1:02}"