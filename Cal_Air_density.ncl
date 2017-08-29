; ===============================================
; 目的:
; 计算空气密度, 单位: kg/m^3
; 最近温度使用范围: 0~70摄氏度, 超过70度函数产生缺省值
; ===============================================
undef ("Cal_Air_density")
; -----------------------------------------------
function Cal_Air_density(temp:numeric,pressure:numeric,Rh:numeric)
local density, Absolute_Ztemp, defined_wet, Saturated_vapor_p, Ta
begin
    Absolute_Ztemp   = 273.15   ; 绝对零度, 单位：K
    defined_wet = 10  ; 用相对湿度值确定空气干湿状况: >10, 湿空气; <10, 干空气
; ----------------------------------------------------------------
    ; --- check temperature and pressure units
    if(temp@units .eq. "deg C") then
        Ta   = temp
        temp = temp + Absolute_Ztemp
    else  ; 气温单位：K
        Ta = temp - Absolute_Ztemp
    end if
    ; print(Ta)

    if(pressure@units .eq. "Pa") then
        pressure = pressure / 100.
    end if
    
    ; --- computed Saturated_vapor_pressure(units: hPa)
    Saturated_vapor_p = where((Ta.ge. 0) .and. (Ta .le. 70), \
                              exp(12.062-(4309.558/(Ta+235.379)))*1000., \
                              -32766.)
    Saturated_vapor_p = where((Ta.gt. -5) .and. (Ta .lt. 0), 6.106, Saturated_vapor_p)
    Saturated_vapor_p = where((Ta.gt. -10) .and. (Ta .le. -5), 4.2263, Saturated_vapor_p)
    Saturated_vapor_p = where((Ta.gt. -15) .and. (Ta .le. -10), 2.8798, Saturated_vapor_p)
    Saturated_vapor_p = where((Ta.gt. -20) .and. (Ta .le. -15), 1.9332, Saturated_vapor_p)
    Saturated_vapor_p = where((Ta .le. -20), 1.28, Saturated_vapor_p)

    Saturated_vapor_p@_FillValue = -32766.
    ; print(Saturated_vapor_p)
    
    ; --- Computed the ration between different units
    density = where(Rh .ge. defined_wet, \
                    10^(-1.)*3.48*pressure*(1 - 0.378*Rh*Saturated_vapor_p/pressure)/temp, \
                    10^(-1.)*3.48*pressure/temp)
    density@_FillValue = -32766.

    return(density)
; ------------------------------------------------------------------
end