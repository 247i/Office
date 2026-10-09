if not modules then modules = { } end modules ['t-calendar'] = {
    version   =  "2023.04.15",
    comment   = "Date calculation collection",
    author    = "Willi Egger",
    copyright = "Willi Egger",
    email     = "w.egger@boede.nl",
    license   = "Public Domain"
  }

thirddata          = thirddata     or { }
thirddata.calendar = { }
local calendar     = thirddata.calendar

local report       = logs.reporter("Calendar")

-- Determine whether the year is a leap year

function calendar.isleapyear(year)
  local yeardays
  if (year % 4 == 0) and (year % 100 ~= 0 or year % 400 == 0) then
    yeardays = 366
  else
    yeardays = 365
  end
  
  -- report("Days in the year in function calendar.isleapyear: %d",yeardays)
    
  return yeardays
end

-- Lua calculates day 1 = sunday, day 0 = saturday
-- 
-- Calculate the weekday of 1st of january according to S. Babwani
-- w = floor(5*year/4)+f(m)+d- 2 * mod(cn,4)
-- where w is the week day
-- where year is the last two digits of the full year.
-- where f(m) is 0 for january (See table 3 of Babwani's congruence)
-- where d is the day: 1 for january
-- where cn is the century

function calendar.janfirst(y)
  local year = y
  
  -- report("Working in function: calendar.janfirst")
  -- report("Year in function: calendar.janfirst: %d",year)
      
  local cn = math.floor(year/100)  -- century
  local yr = math.fmod(year,100)   -- year without century
  local leap_year = calendar.isleapyear(year) -- returns values 365 or 366

  -- report("Century %d",cn)
  -- report("Year without century %d",yr)
  -- report("Result of check for leapyear (days) %d",leap_year)

  local janfirst
  
  if leap_year == 365  then
    janfirst = math.fmod((math.floor((5 * yr) / 4)
       + 0 + 1 - (2 * (math.fmod(cn,4)))),7)
  else
    janfirst = math.fmod((math.floor((5 * yr) / 4)
       + 6 + 1 - (2 * (math.fmod(cn,4)))),7)
  end

  --report("Weekday of January 1st in function calendar.janfirst: %d",janfirst)
  
  return janfirst
end

-- Calculate the ordinal number of a given day of the year from the weeknumber

function calendar.wknrordinal(wkdjf,wk,yr)
  local weekdayjanfirst = wkdjf
  local weeknumber      = wk
  local year            = yr

  report("Working in calendar.wknrordinal")  
  --report("Weeknumber %d, Year: %d", weeknumber,year)

  -- This table contains the offset of the first monday after the 1st of
  -- january, 
  -- as used in the calculation of the ordinal number of a day of the year

  local dyearbegin = {1,0,6,5,4,3,2}

  local  ordinalday = (weeknumber - 1) * 7 + dyearbegin[weekdayjanfirst]

  --report("Ordinal day in calendar.wknrordinal: %d", ordinalday)
  
  leapyear = calendar.isleapyear(year)
  
  if ordinalday > leapyear then
    ordinalday = ordinalday - 7
  end
  
  return ordinalday
end

-- Calculate the first day of a week calendar based on the week day of the 1st
-- of january, date calculations based on the OS-timestamp

function calendar.weekcalendar(wk,mn,yr)
  local weeknumber = wk
  local month      = mn
  local year       = yr

  report("Working in function: calendar.weekcalendar")
  --report("Week number: %d Year: %d",weeknumber,year)

  --report("Week number in function calendar.weekcalendar %d", weeknumber)

  if month == 1 and weeknumber > 51 then
    year = year -1
  end

  local weekdayjanfirst = calendar.janfirst(year)  
  
  --report("Weekday of January 1st from function calendar.weekcalendar: %d",weekdayjanfirst)
    
  if weekdayjanfirst == 0 then weekdayjanfirst = 7 end
  
  local janfirsttimestamp = os.time({year=year,month=1,day=1})
  
  -- report("January 1st timestamp: %d", janfirsttimestamp)
  
  local startday         = janfirsttimestamp
  local ordinalday       = calendar.wknrordinal(weekdayjanfirst,weeknumber,year)
  
  --report("Ordinal day (function: calendar.weekcalendar): %d",ordinalday)

  if weekdayjanfirst > 1 and weekdayjanfirst <= 5 and weeknumber == 1 then
    startday = janfirsttimestamp - (weekdayjanfirst-1) * 24 * 60 * 60
  elseif
    weekdayjanfirst == 3 or weekdayjanfirst == 4 or weekdayjanfirst == 5 and weeknumber ~= 1 then
    startday = janfirsttimestamp + (ordinalday-8) * 24 * 60 * 60
  else
    startday = janfirsttimestamp + (ordinalday-1) * 24 * 60 * 60
  end
  
  if   ordinalday > 360 then
    startday = janfirsttimestamp + (ordinalday-1) * 24 * 60 * 60  
  end

  -- local q = os.date("%x",startday)
--
--report("Start day of chosen week from function calendar.janfirst: %s", q)
  
  return startday
end

-- Select a weekday from the os.date table and return the day name value to ConTeXt

function calendar.select_dayname(d,wk,mn,y)
  local weekday    = d
  local weeknumber = wk
  local month      = mn --not used but necessary for calendar.weekcalendar
  local year       = y
  
  local startday = calendar.weekcalendar(weeknumber,month,year)
  local d = startday + weekday * 24 * 60 * 60
  local s = string.lower(os.date("%a",d))
  
  -- report("Working in function: calendar.select_dayname")
  
  local t = os.date("%d-%m-%Y",d)
  
  -- report("Startday+day! : %s", t)
  -- report("Day name: %s", s)
  
  return s
end

-- Select a date from the os.date table and return the value to ConTeXt

function calendar.select_fulldate(weeknumber,year,day)
  
  local month    = 5 --not used but necessary for calendar.weekcalendar
  local startday = calendar.weekcalendar(weeknumber,month,year)
  local d = startday + day * 24 * 60 * 60
  local s = os.date("%d-%m-%Y",d)
  
  -- report("Working in function: calendar.select_fulldate")
    
  return context(s)
end

-- Select an ordinal day from the os.date table and return the day name value to ConTeXt

function calendar.select_dayofmonth(d,wk,mn,y)

  local day        = d
  local weeknumber = wk
  local month      = mn
  local year       = y
  
  -- report("Working in function: calendar.select_dayofmonth")
  -- report("Weeknumber: %s , Year: %s, Day: %s", weeknumber,year,day)
    
  local startday = calendar.weekcalendar(weeknumber,month,year)
  local d = startday + day * 24 * 60 * 60
  local s = os.date("%d",d)
  local b = string.lower(os.date("%a",d))
  local t = os.date("%d-%m-%Y",d)
  
  -- report("Asked day : %s", t)
  -- report("B Dayname: %s", b)
  
  s = tonumber(s)
  
  -- report("B Day number of month: %d", s)
  
  return s
end

-- Select the month number from the os.date table and return the value as a number

function calendar.select_month(d,wk,y)
  
  local weeknumber = wk
  local year       = y
  local day        = d
  local month      = 5 -- this is not used, but necessary for using calendar.weekcalendar
  
  -- report("Working in function: calendar.select_month")
  -- report("Day: %s, Weeknumber %s, Year: %s", day,weeknumber,year)

  local startday = calendar.weekcalendar(weeknumber,month,year)
  local d = startday + day * 24 * 60 * 60
  local s = os.date("%m",d)
  
  --  report("select month: %s", s)
  
  return s
end

-- Select the month name from the os.date table and return the name of the month

function calendar.select_monthname(d,wk,mn,y)

  local day        = d
  local weeknumber = wk
  local month      = mn -- this is not used, but necessary for using calendar.weekcalendar
  local year       = y    

  
  -- report("Working in function: calendar.select_monthname")
  -- report("Day: %s, Week: %s, Year: %s", day,weeknumber,year)
  
  local startday = calendar.weekcalendar(weeknumber,month,year)
  local t = startday + day * 24 * 60 * 60
  local s = string.lower(os.date("%B",t))
  

  return s
end

-- Select the fullyear from the os.date table and return the value

function calendar.select_fullyear(weeknumber,year,day)
  
  local month    = 5 --not used, but necessary for using calendar.weekcalendar
  local startday = calendar.weekcalendar(weeknumber,month,year)
  local d = startday + day * 24 * 60 * 60
  local s = os.date("%Y",d)
  
  -- report("Working in function: calendar.select_fullyear")
    
  return s
end

-- Select the monthname (long) based on month-number from os.date

function calendar.select_nameofmonth(mon,y)
  
  -- report("Working in function: calendar.select_nameofmonth")
  
  local monthnumber = mon
  local year        = y
  local d           = 1
  local m = string.lower(os.date("%B",
    os.time{year=year,month=monthnumber,day=d}))
  
  -- report("Month name %s",m)
  
  return m
end

-- Select the monthname (long) based on monthnumber from os.date and return it as a labeltext

function calendar.select_nameofmonthlabel(mon,y)
  
  -- report("Working in function: calendar.select_nameofmonthlabel")
  
  local monthnumber = mon
  local year        = y
  local d           = 1
  local m = string.lower(os.date("%B", 
    os.time{year=year,month=monthnumber,day=d}))
  
  -- report("Month name %s",m)
  
  return context.labeltext(m)
end

-- Select the year from the os.date table and return the value to ConTeXt

function calendar.select_year(weeknumber,year,day)
  local month = 5 --not used but necessary for calendar.weekcalendar
  local startday = calendar.weekcalendar(weeknumber,month,year)
  local d = startday + day * 24 * 60 * 60
  local s = os.date("%y",d)
  
  -- report("Working in function: calendar.select_year")
  
  return s --context(s)
end

--[[
  EASTER DATE CALCULATION FOR YEARS 1583 TO 4099

   y is a 4 digit year 1583 to 4099
   d returns the day of the month of Easter
   m returns the month of Easter
   
   Easter Sunday is the Sunday following the Paschal Full Moon
   (PFM) date for the year
   
   This algorithm is an arithmetic interpretation of the 3 step
   Easter Dating Method developed by Ron Mallen 1985, as a vast
   improvement on the method described in the Common Prayer Book
   
   Because this algorithm is a direct translation of the
   official tables, it can be easily proved to be 100% correct
   
   This algorithm derives values by sequential inter-dependent
   calculations, so ... DO NOT MODIFY THE ORDER OF CALCULATIONS!
   
   All variables are integer data types
   
   It's free!

  Comment: Translated from a BASIC-source into lua by W. Egger, 11-2010
--]]

function calendar.eastercalculation(y)
  local year = y
  local FirstDig = math.floor(year / 100)   --first 2 digits of year
  local Remain19 = math.fmod(year,19)       --remainder of year / 19
  local temp
  local a = {}
  local tA
  local tB
  local tC
  local tD
  local tE
  local m
  local d
  
  -- calculate Paschal Full Moon (PFM) date
  
  temp = math.floor((FirstDig - 15) / 2) + 202 - 11 * Remain19
  a = {21, 24, 25, 27, 28, 29, 30, 31, 32, 34, 35, 38}
  for val in pairs(a) do
     if val == FristDig then
      temp = temp - 1
      break
    end
  end
  
  a = {33, 36, 37, 39, 40}
  for val in pairs(a) do
     if val == FirstDig then
      temp = temp - 2
      break
    end
  end
    
  temp = math.fmod(temp, 30)
  tA = temp + 21
  
  if temp == 29 then 
    tA = tA - 1
  end
  
  if (temp == 28 and Remain19 > 10) then 
    tA = tA - 1
  end

  --find the next Sunday
  
  tB = math.fmod((tA - 19), 7)
  tC = math.fmod((40 - FirstDig), 4)
  
  if tC == 3 then 
    tC = tC + 1
  end  
  
  if tC > 1 then 
    tC = tC + 1
  end
    
  temp = math.fmod(year, 100)
  tD = math.fmod(temp + math.floor(temp/ 4), 7)
  tE = math.fmod((20 - tB - tC - tD), 7) + 1
  
  d = tA + tE

  -- return the date
  
  if d > 31 then
    d = d - 31
    m = 4
  else
    m = 3
  end
  
  -- return context("Year: " ..year .." month:" ..m .. " day: " ..d)
  
  local odes = calendar.ordinalday(d,m,year)
  
  -- report("Easter ordinal day: %s", odes)
  
  return odes
end

-- Calculate the ordinal daynumber from a given date with os.date and os.time

function calendar.ordinalday(day,month,year)
  
  -- report("Working in function: calendar.ordinalday")
    
  local t = os.date("*t",os.time{year=year,month=month,day=day})
  local od = t.yday
  return od 
end

--Check a date whether it is a Christian feast

function calendar.checkchristianfeast(d,m,y)

  --report("Working in function: calendar.checkchristianfeast")
  --report("Check Christian Feast: Day: %s, Month: %s, Year: %s", d,m,y)

  local daynumber = d
  local month     = m
  local year      = y
  local odes      = calendar.eastercalculation(year)
  local od        = calendar.ordinalday(daynumber,month,year)
  
  -- report("Result easter calculation: %s", odes)
  -- report("Ordinal day to be checked: %s", od)
  
  local s = nil
  if month == 1 and od == 1 then
    s = "nyd"
  end
  if month == 1 and od == 6 then
    s = "epi"
  end
  if month < 7 then -- Easter depending feasts are never later than june
    if od == odes - 46 then
      s = "ashw"
    elseif od == odes - 7 then
      s = "palms"
    elseif od == odes - 2 then
      s = "gfri"
    elseif od == odes then
      s = "esun"
    elseif od == odes + 1 then
      s = "esmo"
    elseif od == odes + 39 then
      s = "ascd"
    elseif od == odes + 49 then
      s= "pcst"
    elseif od == odes + 50 then
      s= "pcstmo"
    end
  end
  if month == 12 and daynumber == 25 then
     s = "xmas"
    end
  if month == 12 and daynumber == 26 then
     s = "bxd"
  end
  
  if s == nil then
    s = ""
  end
  
  -- report("Result of christian holiday: %s", s)
   
  return s
end 


--Create a table with the number of days per month, accounting for leapyears and return the number of days to the calling function

local dayspermonth = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 }  
local nofdays = 0

function calendar.nofdays_month(month,year)

  -- report("Working in function: calendar.nofdays_month")

  if month == 2 and calendar.isleapyear(year) ~= 365 then
    nofdays = dayspermonth[month] + 1
  else
    nofdays = dayspermonth[month]
  end
  
  return nofdays

end  

-- Create a table with the number of days per month, accounting for leapyears
-- and return the number of weeks of the given month to the calling function
  
function calendar.month(month,year)
  
  report("Working in function: calendar.month")
  
  local month = tonumber(month)
  
  if month == 2 and calendar.isleapyear(year) ~= 365 then
    nofdays = dayspermonth[month] + 1
  else
    nofdays = dayspermonth[month]
  end
  
  -- report ("Number of days : %s",nofdays)
      
  monthtable = {}
    
  local s = os.date("*t", os.time{year=year,month=month,day=1})
  
  -- report("os.date: week day : %s",s.wday)
  
  --Correcting the fact that lua starts the week on sunday
  
  local wday = s.wday - 1  
  if wday == 0 then 
    wday = 7
  end  
    
  -- report("Week day : %s",wday)
  
  local beginmonth = wday-1
  
  for i = 1, beginmonth do
    table.insert(monthtable, 0)
  end
  
  for i = wday, (nofdays + beginmonth) do 
    table.insert(monthtable, i - wday + 1)
  end
  
  for i = (nofdays + beginmonth + 1), 42 do --a month table is max. 7 x 6 fields
    table.insert(monthtable, 0)
  end
  
  local wkf = calendar.weeknumber(1,month,year)
  local wkl = calendar.weeknumber(nofdays,month,year)
  
  -- report("monthtable nofdays : %s",nofdays)
  -- report("monthtable wkf     : %s",wkf)
  -- report("monthtable wkl     : %s",wkl)
  
  local b = wkl - wkf + 1
  
  if month > 1 and month < 12 then  
    b = wkl - wkf + 1
  elseif month == 12 and wkl == 1 then
    wkl = 53
    b = wkl - wkf + 1
  elseif month == 1 and wkf > 51 then
    b = wkl + 1
  end
  
  --report("number of weeks %s in month %s",b,month)
  
  return  b
end

--Select a day from the month table return value to context

function calendar.dayselectofmonth(day)
  
  -- report("Working in function calendar.dayselectofmonth")
  -- report("Selected day : %s",day)
  
  local s = monthtable[day]
  
  -- report("Selected day from the monthtable: %s", s)
  
  if s == 0 then
    s = ""
    return s --context(s)
  else
    return s --context(s)
  end
end

--Generate the month name with os.date and os.time

function calendar.monthname(mon,y)
  local month = mon
  local year = y
  
  if  month > 12 then
    month = month - 12
      year = year + 1
  end
  
  local s = string.lower(os.date("%B",os.time{year=year,month=month,day=1}))
  
  -- report("month name : %s",s)
  
  return s
end


-- http://www.irt.org/script/914.htm, Java, Ferry van Schaik 
-- Get the ISO week number from a given date for Europe
--USA
--[[
function calendar.weeknumber(day,month,year)
  local when = os.time({year=year,month=month,day=day})
  local modDay = tonumber(os.date("%w",os.time({year=year,month=1,day=1})))
  
  report("modDay in US calendar.weeknumber: %s",modDay)
  
  local offset = 7 + 1 - modDay
    if offset == 8  then
      offset = 1
    end

  local daynum = math.round((when - os.time({year=year,month=1,day=1})) /60/60/24) + 1
  
  report("daynum in US calendar.weeknumber: %s",daynum) 
  
  local weeknum = math.floor((daynum-offset+7)/7);
  
  report("Week number in calendar.weeknumber %s", weeknum)
  
  if weeknum == 0 then
    year = year - 1
    local prevNewYear = tonumber(os.date
      ("%w",os.time({year=year,month=1,day=1})))
    local prevOffset = 7 + 1 - prevNewYear
    if prevOffset == 2 or prevOffset == 8 then
      weeknum = 53 
    else 
      weeknum = 52
    end
  end
  
  return weeknum
end
--]]
-- EUROPA

function calendar.weeknumber(d,month,year)
  local day = d
  
  -- report("Working in function calendar.weeknumber")
  -- report("Daynumber in function calendar.daynumber: %s", day)
    
  local when = os.time({year=year,month=month,day=day})
  local modDay = tonumber(os.date("%w",os.time({year=year,month=1,day=1})))
      
  if modDay == 0 then 
    modDay = 6
  else
    modDay = modDay - 1
  end
  
  local daynum = math.round((when - os.time({year=year,month=1,day=1})) /60/60/24) + 1
  local weeknum = 0

  if modDay < 4 then
    weeknum = math.floor((daynum+modDay-1)/7)+1
  else 
    weeknum = math.floor((daynum+modDay-1)/7)
    if weeknum == 0 then
      local prevmodDay = tonumber(os.date("%w",os.time({year=year-1,month=1,day=1})))
      if prevmodDay == 0 then 
        prevmodDay = 6 
      end
      if prevmodDay < 4 then
        weeknum = 53 
      else 
        weeknum = 52 
      end      
    end
  end
  
  return weeknum
end


-- Calculate the week number of a given monday of the year from the ordinal day number

function calendar.ordinaltowknr(ordinalday,year)
  
  -- This table contains the offset of the first monday after the 1st of
  -- january, 
  -- as used in the calculation of the ordinal number of a day of the year
  
  local dyearbegin = {1,0,6,5,4,3,2}
  local weekdayjanfirst = calendar.janfirst(year)
  
  if weekdayjanfirst == 0 then 
    weekdayjanfirst = 7 
  end
  
  local wknumber = math.div(ordinalday - dyearbegin[weekdayjanfirst],7) + 1
  
  return wknumber
end 
 