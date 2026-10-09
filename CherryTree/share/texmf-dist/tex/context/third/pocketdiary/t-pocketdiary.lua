if not modules then modules = { } end modules ['t-pocketdiary'] = {
    version   =  "2023.04.15",
    comment   = "Layouts of diary pages",
    author    = "Willi Egger",
    copyright = "Willi Egger",
    email     = "w.egger@boede.nl",
    license   = "Public Domain"
}

thirddata      = thirddata or { }
thirddata.diary = { }
local diary     = thirddata.diary

local report   = logs.reporter("Diary pages")

function diary.data(wd,wk,mn,yr,la,lo,to,cont)
  
  report("Working in function: diary.data")
  
  local weekday    = wd
  local weeknumber = wk
  local month      = mn
  local year       = yr
  local lon        = lo
  local lat        = la
  local timeoffset = to
  local continent  = cont
  local moon       = ""
  local srise,sset,lhours 
  
  local dayofmonth  = thirddata.calendar.select_dayofmonth(
    weekday,weeknumber,month,year)
  
  local dayname = thirddata.calendar.select_dayname(weekday,weeknumber,month,year)
  
  local holiday = thirddata.calendar.checkchristianfeast(
  dayofmonth,month,year)
  
  local monthname = thirddata.calendar.select_monthname(
    weekday,weeknumber,month,year)

  local moondata  = thirddata.moonphase.lunardays(year,month,dayofmonth)
  
  local dst_start, dst_stop,srise,sset,lhours
  
  if continent ~="" then 
    local dst_start,dst_stop = diary.DST(year,continent)
  
    report("DST start: %s DST stop: %s",dst_start,dst_stop)

    srise,sset,lhours = thirddata.srss.sundata(
      dayofmonth,month,year,lat,lon,timeoffset,dst_start,dst_stop)  
  else
    dst_start = "none"
    dst_stop  = 0
    report("No DST is applied")
  end 
  
  return weekday, weeknumber, month, year, lat, lon, timeoffset, dst_start,
    dst_stop, dayofmonth, dayname, holiday, monthname, moondata, srise, sset,
    lhours
end  

function diary.DST(year,continent)
    local report = logs.reporter("DST date")
    
    report("Working in function DST")
    
    local dstmonth_start
    local dstmonth_stop
    local dstday_start
    local dstday_stop 
    local dst_start
    local dst_stop
    
  if continent ~= "" then
    if continent == "EU" then
      dstmonth_start = 3
      dstmonth_stop  = 10
      dstday_start   = diary.DSTday(dstmonth_start,year,continent)
      dstday_stop    = diary.DSTday(dstmonth_stop,year,continent)
    else
      if continent == "US" then
        dstmonth_start = 3
        dstmonth_stop  = 11
        dstday_start   = diary.DSTday(dstmonth_start,year,continent)
        dstday_stop    = diary.DSTday(dstmonth_stop,year,continent)
      end
    end
    -- report("DSTday start: %s",dstday_start)
    -- report("DSTday stop: %s",dstday_stop)
    dst_start = year.."-"..dstmonth_start.."-"..dstday_start    
    dst_stop  = year.."-"..dstmonth_stop.."-"..dstday_stop
  else
   report("No DST to be taken in to account")    
   dst_start = "none"
   dst_stop  = 0
  end
  
  --report("DST start date: %s", dst_start)
  --report("DST stop date: %s", dst_stop)
  
  return dst_start, dst_stop
end

function diary.DSTday(month,year,continent)
  report("Working in function DSTday")

  local DSTday = {}
  local dayname
  
  if continent == "EU" then
    -- the last Sunday of March and October can only be between 25. and 31. of the month
    for i=25,31 do
      dayname = string.lower(os.date
        ("%a",os.time{day=i,month=month,year=year}))
      DSTday[dayname] = i
    end
  else
    -- for the US the second Sunday in March can be between 8. and 14. of March, first Sunday of November can be between 1. and 8. of November
    if month == 3 then
      for i=8,14 do
        dayname = string.lower(os.date
          ("%a",os.time{day=i,month=month,year=year}))
        DSTday[dayname]=i
      end
    else
      for i=1,7 do
        dayname = string.lower(os.date
          ("%a",os.time{day=i,month=month,year=year}))
          DSTday[dayname]=i
      end
    end
  end
  return DSTday.sun  
end
    
function diary.dayplan(...) --8 parameters
  
  report("Working in function: diary.dayplan")
    
  if weekday == 0 then
    weekday = 1
  end
  
  local weekday, weeknumber, month, year, lat, lon, timeoffset, dst_start,
    dst_stop, dayofmonth, dayname, holiday, monthname, moondata, srise, sset,
    lhours = diary.data(...)

  context.setupheadertexts{
    function()
      context.bTABLE({setups="table:topinfo"})
        context.bTR()
          context.bTD()
            if dayname == "sun" or holiday ~= "" then
              context.color({"red"},
                 function() context(dayofmonth) end) 
              context("~")
              context.color({"red"}, 
                function() context.labeltext(dayname) end)                
            else
              context(dayofmonth) 
              context("~")
              context.labeltext(dayname)
            end
          context.eTD()
          context.bTD()
            context.labeltext(holiday)
          context.eTD()
          context.bTD()
             context.labeltext(monthname) 
             context("~")
             context(year)
          context.eTD()
        context.eTR()
        context.bTR({style="\\switchtobodyfont[5pt]"})
          context.bTD()
          if tonumber(moondata) then
            context.labeltext("moondays")
          else
            context.labeltext("moon")
          end
            context(": ")
            context(moondata)
          context.eTD()
          context.bTD({nx="2"})
            context.dontleavehmode() 
            context("\\SunA[background=Sunrise,height=7pt]{\\strut}")
            context("~~~")
            context(srise)
            context("\\quad")
            context("\\SunA[background=Sunset,height=7pt]{\\strut}")
            context("~~~")
            context(sset)
            context("~~")
            context("\\SunB[background=Light,height=7pt]{\\strut}")
            context("~~")
            context(lhours)
          context.eTD()
        context.eTR()  
      context.eTABLE()
  end}
  context.strut()
  context.page()
end

function diary.weekplan(weekday,weeknumber,month,year,lat,lon,
  timeoffset,continent) --8 parameters
  
  report("Working in function: diary.weekplan")
    
  context.setupheadertexts{
    function()
      context.bTABLE({setups="table:topweekplan"})
        context.bTR()
          context.bTD()
              context("\\bf")
              context.labeltext("weekagenda")
          context.eTD()
          context.bTD()
          context.labeltext("month")
            context("~")
            context(month)
            context("\\quad")
            context.labeltext("week")
            context("~")
            context(weeknumber)
            context("\\quad")
            context(year)
          context.eTD()
        context.eTR()
      context.eTABLE()
    end}
    diary.thisweek(weeknumber,month,year,lat,lon,timeoffset,continent)
    context.page()
end

function diary.nextweekplan(...)

  local weekday,  weeknumber,  month, year, lat, lon, timeoffset, dst_start,
    dst_stop, dayofmonth, dayname, holiday, monthname, moondata, srise, sset,
    lhours = diary.data(...)

  report("Working in function: diary.nextweekplan")
  
  context.setupheadertexts{
    function()
      context.bTABLE({setups="table:topinfo"})
        context.bTR()
          context.bTD()
              context("\\bf\\labeltext{weekagenda}")
          context.eTD()
          context.bTD()
            context.strut()
          context.eTD()
          context.bTD()
            context.labeltext("week")
            context("~")
            context(weeknumber)
            context("\\quad")
            context(year)
          context.eTD()
        context.eTR()
      context.eTABLE()
    end}
    diary.thisweek(weeknumber,month,year,lat,lon,timeoffset,continent)
    context.page()
end

function diary.weekendplan(weekday,weeknumber,month,year,lat,
  lon,timeoffset,continent)
  
  local weekday, weeknumber, month, year, lat, lon, timeoffset, dst_start, 
    dst_stop, dayofmonth, dayname, holiday, monthname, moondata, srise, 
    sset, lhours =
    diary.data(weekday,weeknumber,month,year,lat,lon,timeoffset,continent)
  
  report(" Working in function: diary.weekendplan")
  
  context.setupheadertexts{
    function()
      context.bTABLE({setups="table:topinfo"})
        context.bTR()
          context.bTD()
            context(dayofmonth) 
            context("~")
            context.labeltext(dayname)              
          context.eTD()
          context.bTD()
            context.labeltext(holiday)
          context.eTD()
          context.bTD()
             context.labeltext(monthname) 
             context("~")
             context(year)
          context.eTD()
        context.eTR()
        context.bTR({style="\\switchtobodyfont[5pt]"})
          context.bTD()
          if tonumber(moondata) then
            context.labeltext("moondays")
          else
            context.labeltext("moon")
          end
            context(": ")
            context(moondata)
          context.eTD()
          context.bTD({nx="2"})
            context.dontleavehmode() 
            context("\\SunA[background=Sunrise,height=7pt]{\\strut}")
            context("~~~:~")
            context(srise)
            context("\\quad")
            context("\\SunA[background=Sunset,height=7pt]{\\strut}")
            context("~~~")
            context(sset)
            context("~~")
            context("\\SunB[background=Light,height=7pt]{\\strut}")
            context("~~")
            context(lhours)
          context.eTD()
        context.eTR()  
      context.eTABLE()
  end}
  
  local wday = 7
  local weekday, weeknumber, month, year, lat, lon, timeoffset, dst_start,
    dst_stop, dayofmonth, dayname, holiday, onthname,moondata,srise,sset,
    lhours = diary.data(wday, weeknumber, month, year, lat, lon, timeoffset,
    continent)
    
  -- report("Working in function: diary.weekendplan: Sunday"
  
  context.strut()    
  context("\\godown[.4\\textheight]")
  context.bTABLE({setups="table:topinfo"})
    context.bTR()
      context.bTD()
      context.color({"red"},
         function() context(dayofmonth) end) 
      context("~")
      context.color({"red"}, 
        function() context.labeltext(dayname) end)              
      context.eTD()
      context.bTD()
        context.labeltext(holiday)
      context.eTD()
      context.bTD()
         context.labeltext(monthname) 
         context("~")
         context(year)
      context.eTD()
    context.eTR()
    context.bTR({style="\\switchtobodyfont[5pt]"})
      context.bTD()
      if tonumber(moondata) then
        context.labeltext("moondays")
      else
        context.labeltext("moon")
      end
        context(": ")
        context(moondata)
      context.eTD()
      context.bTD({nx="2"}) 
        context.dontleavehmode()
        context("\\SunA[background=Sunrise,height=7pt]{\\strut}")
        context("~~~~")
        context(srise)
        context("\\quad")
        context("\\SunA[background=Sunset,height=7pt]{\\strut}")
        context("~~~")
        context(sset)
        context("~~")
        context("\\SunB[background=Light,height=7pt]{\\strut}")
        context("~~")
        context(lhours)
      context.eTD()
    context.eTR()  
  context.eTABLE()
  context.par()
  context("\\godown[3pt]")
  context.blackrule({"color=\\getvariable{PocketDiaryColors}{Separatorline},height=0.5pt,width=\\textwidth"})
  context.page()
end

function diary.monthcurrentplan(mon,y)
  local month = mon
  local year = y
  
  report("Working in function: diary.monthcurrentplan")
  
  local month_name = thirddata.calendar.select_nameofmonth(month,year)
    
  context.setupheadertexts{
     function()
      context.bTABLE({setups="table:topweekplan"})
        context.bTR()
          context.bTD()
             context.labeltext(month_name)
          context.eTD()
           context.bTD()
             context(year)
           context.eTD()
        context.eTR()
      context.eTABLE()
     end}
  
  diary.monthtableH(month,year)
  context.page()
end  

function diary.monthnextplan(mn,yr)

  report("Working in function: diary.monthnextplan")

  local month = mn
  local year  = yr
  
  month = month + 1
  
  if month > 12 then
    month = 1
    year = year + 1
  end  
  
  local month_name = thirddata.calendar.select_nameofmonth(month,year)
    
  context.setupheadertexts{
     function()
      context.bTABLE({setups="table:topweekplan"})
        context.bTR()
          context.bTD()
               context.labeltext(month_name)
          context.eTD()
           context.bTD()
             context(year)
           context.eTD()
        context.eTR()
      context.eTABLE()
     end}
  
  diary.monthtableH(month,year)
  context.page()
end  

function diary.yearplan(yr,nxt)
  
  report("Working in function: diary.yearplan")
    
  local year = yr
  local next = nxt
  
  if next == "yes" then
    year = year + 1
  end
    
  context.setupheadertexts{
     function()
      context.bTABLE({setups="table:topinfo"})
        context.bTR()
          context.bTD()
               context(year)
          context.eTD()
           context.bTD()
             context.strut()
           context.eTD()
           context.bTD()
             context.strut()
           context.eTD()
        context.eTR()
      context.eTABLE()
     end}
  context.start()
      context.switchtobodyfont({"4pt"})
      diary.yearcalendar(year)
  context.stop()
  context.page()
end    

function diary.daybydayplan(weekday,weeknumber,month,year,lat,lon,
  timeoffset,continent) --8 parameters
  
  report("Working in function: diary.daybyday")
  
  --Working days
  for i = 1,5 do
  
    thirddata.diary.dayplan(i,weeknumber,month,year,lat,lon,
      timeoffset, continent)
  end
  
  -- Weekend
  thirddata.diary.weekendplan(6, weeknumber,month,year,lat,lon,
       timeoffset, continent)
  context.page()     
end  

-- Generate a Context table containing the days of a given month, 
-- topline weeknumber

function diary.monthtableH(mn,yr)
  local month = mn
  local year  = yr
  
  report("Working in function: diary.monthtableH")
    
  if month > 12 then
    month = month - 12
    year = year + 1
  end
    
  context.bTABLE({setups="table:month"})
  context.bTR()
  
    local w = {"mon","tue","wed","thu","fri","sat","sun"}
     for a,d in ipairs(w) do
       context.bTD({align="middle,lohi"}) 
         context.labeltext(d) 
       context.eTD()   
     end
     
  context.eTR()
  
  ----returns number of weeks in a given month
  
  local c = thirddata.calendar.month(month,year) 
  
  for i = 1, c do
    context.bTR()
    for j=(i-1)*7+1,(i-1)*7+7 do
      local day = thirddata.calendar.dayselectofmonth(j)
      local holiday
      if day ~= "" then
        holiday = thirddata.calendar.checkchristianfeast(
          day,month,year)
      end

      context.bTD()

        if holiday ~= "" then
          context.color({"red"},
             function() context(day) end) 
        else
          context(day)
        end

      context.eTD()
    end 
    context.eTR()
  end
  
  context.eTABLE()
end

-- Generate a Context table containing the days of a given month, topline
-- weekday names

function diary.monthtableV(month,year)
  
  report("Working in function diary.monthtableV")
  
  local c = thirddata.calendar.month(month,year) --returns number of weeks in a given month
  local wkf = thirddata.calendar.weeknumber(1,month,year)
  
  local nofdays = 1
  
  if month == 2 and thirddata.calendar.isleapyear(year) ~= 365 then
    nofdays = thirddata.calendar.nofdays_month(month,year) + 1
  else
    nofdays = thirddata.calendar.nofdays_month(month,year)
  end
  
  local wkl = thirddata.calendar.weeknumber(nofdays,month,year)
  
  context.bTABLE({setups="table:year"})
    context.bTR({align="flushright"})
       context.bTD() 
        context.strut() 
      context.eTD()

      if month == 1 and wkf > 51 then
        context.bTD() 
          context(wkf) 
        context.eTD()
         wkf = 1
        for i = wkf, c - 1 do
          context.bTD() 
            context(i) 
          context.eTD()
        end 
      else
        for i = wkf, wkf + c - 1 do
          context.bTD() 
            context(i) 
          context.eTD()
        end
      end
    context.eTR() 
    
    local w = {"mon","tue","wed","thu","fri","sat","sun"}
    local row = 0 
    
    for a,d in ipairs(w) do
      if a == 7 then
        context.bTR({align="flushright",style="red"})
      else
        context.bTR({align="flushright"})
      end 
      
      context.bTD({align="flushleft"}) 
        context.labeltext(d) 
      context.eTD()
      
      for i=1,c*7,7 do
        local day = i + row
        local dayofmonth = thirddata.calendar.dayselectofmonth(day)

        --report("Day of month in monthtableV: %s",dayofmonth)
        local holiday

        if dayofmonth ~= "" then
          holiday = thirddata.calendar.checkchristianfeast(
      dayofmonth,month,year)
        end

        context.bTD()

        if holiday ~= "" then
          context.color({"red"},
             function() context(dayofmonth) end)
        else
          context(dayofmonth)
        end
        context.eTD()
      end
      row = row + 1
      context.eTR()      
    end
  context.eTABLE()
end

function diary.yearcalendar(year)
  
  report("Working in function: diary.year")
    
  context.startcombination({"4*3"})
    for i= 1,12 do
      local monthname = string.lower(os.date(
        "%B",os.time{year=year,month=i,day=1}))
      context.framedtext({frame="off",
              style="bold",
              width=number.todimen(0.23*tex.dimen.textwidth),
              offset="0.5pt",
              align="middle"},
      function() context.labeltext(monthname) end,
      function() diary.monthtableV(i,year) end
      )
    end
  context.stopcombination()
end

function diary.thisweek(wk,mn,yr,lat,lon,timeoffset,continent)
  
  report("Working in function: diary.thisweek")
  --report("Year %d", yr)
  --report("weeknumber in diary.thisweek %s",wk)

  
  local weeknumber = wk
  local year       = yr
  local month      = mn
      
  local mondaytimestamp = thirddata.calendar.weekcalendar(weeknumber,month,year)
  
  --report("Month based on mondaytimestamp: %s", m)
  local d = tonumber(os.date("%d",mondaytimestamp))     -- day part of date
  
  -- The following line will be deleted if it works
  local y = tonumber(os.date("%Y",mondaytimestamp))
  --report("Year: %d",y)
  
  --report("Now in diary.thisweek  at day %s",d)     

  diary.weektable(mondaytimestamp,month,year,
    lat,lon,timeoffset,continent)
end

function diary.nextweek(wk,mn,year,lat,lon,timeoffset,dst_start,dst_stop)
  
  report("Working in function: diary.nextweek")
    
  local weeknumber = wk + 1
  local mondaytimestamp = thirddata.calendar.weekcalendar(weeknumber,mn,year)

  diary.weektable(mondaytimestamp,mn,year,
                  lat,lon,timeoffset,continent)
end

function diary.weektable(mondaytimestamp,mn,year,
                           lat,lon,timeoffset,continent)
  local year = year
  local s    = mondaytimestamp
  local dst_start,dst_stop = diary.DST(year,continent)

  report("Working in function: diary.weektable")
    local x = os.date("%x",mondaytimestamp)

   --report("Actual date: %s",x)
       
  context.bTABLE({setups="table:week"}) 

    local yeardays = thirddata.calendar.isleapyear(year)  -- returns 365 or 366
     
    for i = 1,5 do
      local daystamp = s + i * 24 * 60 * 60
      local d = tonumber(os.date("%d",daystamp))     -- day part of date
      
      --report("Year in week-loop: %d",year)    
      --report("Day in week-loop: %s",d)
           
      local n = string.lower(os.date("%a",daystamp)) -- day name
      
      --report("Day name in week loop: %s",n)
      
      local m = tonumber(os.date("%m",daystamp))     -- month number
      
      --report("Month number in week-loop %d",m)
      
      local f = thirddata.calendar.checkchristianfeast(d,m,year)
      local t = os.date("*t",os.time{year=year,month=m,day=d}) -- This returns a table!
      local moondata  = thirddata.moonphase.lunardays(year,m,d)
       
      if not f then
          f = ""
      end
       
      context.bTR()
        context.bTD({nx=2})
          if f ~= "" and f ~= "ashw" then
            context.color({"red"},
            function() context(d) end) 
            context("~")
            context.color({"red"}, 
            function() context.labeltext(n) end)
          else
            context(d) 
            context("~")
            context.labeltext(n)
          end
          context.bgroup()
            context.switchtobodyfont({"6pt"})
            context("~")
            context(t.yday)
            context("/")
            context(yeardays)
               
            if not tonumber(moondata) then
              context("~")
              context(moondata)
            end
                                       
            if n == "tue" then
              local srise,sset,lhours = 
                    thirddata.srss.sundata(d,m,year,lat,lon,
                    timeoffset,dst_start,dst_stop)
              --report("Sun data %s,%s,%s", srise,sset,lhours)
              context("\\quad")   
              context("\\SunA[background=Sunrise,height=7pt]{\\strut}")
              context("\\quad ~")
              context(srise)
              context("~~~")
              context("\\SunA[background=Sunset,height=7pt]{\\strut}") 
              context("\\quad ~")
              context(sset)
              context("~~~")
              context("\\SunB[background=Light,height=7pt]{\\strut}")
                      context("~~")
              context(lhours)
            end
          context.egroup() 
          context("~") 
          context.labeltext(f) 
        context.eTD()
      context.eTR()
    end
         
    context.bTR()
      local daystamp = s + 6 * 24 * 60 * 60
      local d = tonumber(os.date("%d",daystamp))
      local n = string.lower(os.date("%a",daystamp))
      local m = tonumber(os.date("%m",daystamp))
      local f = thirddata.calendar.checkchristianfeast(d,m,year)
      local t = os.date("*t",os.time{year=year,month=m,day=d}) -- This returns a table!
                     
      --report("Weekend day in loop: %s",d)
                 
      if not f then
        f = ""
      end
             
      context.bTD()
        if f ~= "" then
          context.color({"red"},
          function() context(d) end) 
          context("~")
          context.color({"red"}, 
          function() context.labeltext(n) end)
        else
          context(d) 
          context("~")
          context.labeltext(n)
        end  
        context.bgroup()
          context("\\tfxx")
          context("~")
          context(t.yday)
          context("/")
          context(yeardays)
        context.egroup() 
        context("~") 
        context.labeltext(f) 
      context.eTD()
             
      local daystamp = s + 7 * 24 * 60 * 60
      local d = tonumber(os.date("%d",daystamp))
      local n = string.lower(os.date("%a",daystamp))
      local m = tonumber(os.date("%m",daystamp))
      local f = thirddata.calendar.checkchristianfeast(d,m,year)
      local t = os.date("*t",os.time{year=year,month=m,day=d}) -- This returns a table!
      --report("Weekend day in loop: %s",d)
      if not f then
        f = ""
      end
         
      context.bTD()  
        context.color({"red"},
          function() context(d) end) 
        context("~")
        context.color({"red"}, 
          function() context.labeltext(n) end)
        context.bgroup()
          context("\\tfxx")
          context("~")
          context(t.yday)
          context("/")
          context(yeardays)
        context.egroup() 
        context("~") 
        context.labeltext(f)
      context.eTD()
    context.eTR()
  context.eTABLE()
  context.page()
end