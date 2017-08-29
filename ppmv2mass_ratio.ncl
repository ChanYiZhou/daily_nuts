; ====================================
; 目的:
; 将气体的单位从ppmv转换成mg/m3
; ====================================
undef ("ppmv2mass_ratio")
; -----------------------------------------------
; temp: unit must be in K.
; -----------------------------------------------
function ppmv2mass_ratio(species:string,mass_unit:string,temp:numeric,pressure:numeric)
local ratio, Astand_atom, Absolute_temp, molecular_weight, gas_Molar_volume
begin
    Astand_atom      = 1013.25  ; 1个标准大气压， 单位: hPa
    Absolute_temp    = 273.15   ; 绝对零度， 单位：K
    gas_Molar_volume = 22.4     ; 气体的摩尔体积, 单位: L/mol
; ----------------------------------------------------------------
    ; --- given the molecular weight
    if(species .eq. "co") then
        molecular_weight = 28
    end if

    if(species .eq. "so2") then
        molecular_weight = 64
    end if

    if(species .eq. "no2") then
        molecular_weight = 46
    end if

    if(species .eq. "o3") then
        molecular_weight = 48
    end if

    ; --- Computed the ration between different units
    if(pressure@units .eq. "Pa") then
        pressure = pressure / 100.
    end if
    if(temp@units .eq. "deg C") then
        temp = temp + Absolute_temp
    end if
    
    if(mass_unit .eq. "mg/m3") then
        ratio = molecular_weight / gas_Molar_volume * (Absolute_temp/temp) / (pressure/Astand_atom)
    end if

    if(mass_unit .eq. "ug/m3") then 
        ratio = molecular_weight / gas_Molar_volume * (Absolute_temp/temp) / (pressure/Astand_atom) * 1e3
    end if
    return(ratio)
; ------------------------------------------------------------------
end