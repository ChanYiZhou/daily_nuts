; ===============================================
; 目的:
; 根据给定的日期，生成一定范围内的日期序列；
; 给定日期的格式：%Y%m%d%H
; ===============================================
undef ("make_date")
; -----------------------------------------------
function make_date(Sdate:string,TimeLen:numeric,Timestep:numeric)
local SYear, SMonth, SDay, SHour, hour_add, day_add, SMonth_days, \
        thehour, theday, themonth, theyear, TheHour, TheDay, TheMonth, \
        TheYear, ilen, RDate
begin
    SYear  = toint(str_get_cols(Sdate, 0, 3))
    SMonth = toint(str_get_cols(Sdate, 4, 5))
    SDay   = toint(str_get_cols(Sdate, 6, 7))
    SHour  = toint(str_get_cols(Sdate, 8, 9))
    Sminutes = "00"
    Sseconds = "00"
    RDate  = new((/TimeLen,19/), "character")
; ----------------------------------------------------------------
    ; ==== 处理日期integer, 此处设定时间间隔单位为Hour
    if(isatt(Timestep, "units")) then
        if (Timestep@units .eq. "hours") then
            hour_add    = ispan(0, TimeLen*Timestep-1, Timestep) + SHour
            thehour     = hour_add % 24
            SMonth_days = days_in_month(SYear, SMonth)
            day_add     = hour_add / 24 + SDay
            theday      = (day_add - 1) % SMonth_days + 1
            themonth    = (day_add - 1) / SMonth_days + SMonth
            theyear     = SYear + (themonth - 1) / 12
        else
            print("ERROR: Timestep's units is not correct.")
            print("Please make sure your Timestep's units is hours")
            exit
        end if
    else
        print("ERROR: Timestep lack of units attributes.")
        print("Please check your Timestep's attributes")
        exit
    end if
    

    ; ==== 处理日期string
    TheYear  = tostring(theyear)
    TheMonth = where((themonth .lt. 10), "0"+tostring(themonth), \
                     tostring(themonth))
    TheDay   = where((theday .lt. 10), "0"+tostring(theday), \
                     tostring(theday))
    TheHour  = where((thehour .lt. 10), "0"+tostring(thehour), \
                     tostring(thehour))
    
    ; ==== 处理成需要的日期字符数组
    RDate(:,4)   = tochar("-")
    RDate(:,7)   = tochar("-")
    RDate(:,10)  = tochar("_")
    RDate(:,13)  = tochar(":")
    RDate(:,16)  = tochar(":")
    do ilen = 0, TimeLen-1
        RDate(ilen,:3)      = tochar(TheYear(ilen))    
        RDate(ilen,5:6)     = tochar(TheMonth(ilen))
        RDate(ilen,8:9)     = tochar(TheDay(ilen))
        RDate(ilen,11:12)   = tochar(TheHour(ilen))
        RDate(ilen,14:15)   = tochar(Sminutes)
        RDate(ilen,17:18)   = tochar(Sseconds)
    end do

    return(RDate)
; ----------------------------------------------------------------
end





    


