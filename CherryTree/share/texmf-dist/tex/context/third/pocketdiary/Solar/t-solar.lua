if not modules then modules = { } end modules ['t-solar'] = {
    version   =  "2023.04.15",
    comment   = "Sun rise and sun set calculation",
    author    = "Alexander Yakushev, edited by Willi Egger",
    copyright = "Willi Egger",
    email     = "w.egger@boede.nl",
    license   = "CC0 http://creativecommons.org/about/cc0"
}

thirddata      = thirddata or { }
thirddata.srss = { }
local srss     = thirddata.srss

local report       = logs.reporter("Solar data")

--[[ Module for calculating sunrise/sunset times for a given location
  Based on algorithm by United States Naval Observatory, Washington
  Link: http://williams.best.vwh.net/sunrise_sunset_algorithm.htm
  @author Alexander Yakushev
  @license CC0 http://creativecommons.org/about/cc0
--]]

local rad   = math.rad
local deg   = math.deg
local floor = math.floor

local mcos  = math.cos
local msin  = math.sin
local mtan  = math.tan

local macos  = math.acos
local masin  = math.asin
local matan  = math.atan

local frac  = function(n) return n - floor(n) end
local cos   = function(d) return mcos(rad(d)) end
local acos  = function(d) return deg(macos(d)) end
local sin   = function(d) return msin(rad(d)) end
local asin  = function(d) return deg(masin(d)) end
local tan   = function(d) return mtan(rad(d)) end
local atan  = function(d) return deg(matan(d)) end

function srss.fit_into_range(val,min,max)
    local range = max - min
    if val < min then
        return val + (floor((min - val) / range) + 1) * range
    elseif val >= max then
        return val - (floor((val - max) / range) + 1) * range
    else
        return val
    end
end

function srss.day_of_year(date)
    local n1 = floor(275 * date.month / 9)
    local n2 = floor((date.month + 9) / 12)
    local n3 = (1 + floor((date.year - 4 * floor(date.year / 4) + 2) / 3))
    return n1 - (n2 * n3) + date.day - 30
end

function srss.sunturn_time(
	date,rising,latitude,longitude,zenith,local_offset,DST)
	
  local n = srss.day_of_year(date)

  -- report("working in function: srss.sunturn_time")
  -- report("Day: %s Month: %s Year: %s", date.day, date.month, date.year)
  -- report("Latitude: %s  Longitude %s Timeoffset %s", latitude, longitude,
	-- local_offset)
		
  -- Convert the longitude to hour value and calculate an approximate time
  local lng_hour = longitude / 15
		
	--report("longitude hour %s", lng_hour)
		
  local t
  if rising then -- Rising time is desired
      t = n + ((6 - lng_hour) / 24)
  else -- Setting time is desired
      t = n + ((18 - lng_hour) / 24)
  end

  -- Calculate the Sun's mean anomaly
  local M = (0.9856 * t) - 3.289

  -- Calculate the Sun's true longitude
	
  local L = srss.fit_into_range(M + (1.916 * sin(M)) + (0.020 * sin(2 * M)) +
	  282.634, 0, 360)

  -- Calculate the Sun's right ascension
  local RA = srss.fit_into_range(atan(0.91764 * tan(L)), 0, 360)

  -- Right ascension value needs to be in the same quadrant as L
	
  local Lquadrant  = floor(L / 90) * 90
  local RAquadrant = floor(RA / 90) * 90
  RA = RA + Lquadrant - RAquadrant

  -- Right ascension value needs to be converted into hours
  RA = RA / 15

  -- Calculate the Sun's declination
  local sinDec = 0.39782 * sin(L)
  local cosDec = cos(asin(sinDec))

  -- Calculate the Sun's local hour angle
	
  local cosH = (cos(zenith) - (sinDec * sin(latitude))) / (cosDec *
	  cos(latitude))

  if rising and cosH > 1 then
  
	  -- return "N/R" -- The sun never rises on this location on the specified
		-- date
	  report("Sun does not rise")
		
    return ("\\labeltext{sunrise}: --")
  elseif cosH < -1 then
    -- return "N/S" -- The sun never sets on this location on the specified date
		
		report("Sun does not set")
    return ("\\labletext{sunset}: --")
  end

  -- Finish calculating H and convert into hours
  local H
  if rising then
    H = 360 - acos(cosH)
  else
    H = acos(cosH)
  end
  H = H / 15

  -- Calculate local mean time of rising/setting
  local T = H + RA - (0.06571 * t) - 6.622

  -- Adjust back to UTC
  local UT = srss.fit_into_range(T - lng_hour, 0, 24)

  -- Convert UT value to local time zone of latitude/longitude
  local LT =  UT + local_offset
		
	-- Include daylight saving
  -- report("UT: %s", UT)
  -- report("LT: %s", LT)

	if DST == true then
		-- report("DST is on")
	  LT = LT + 1
	end

  -- report("DST: %s", LT)

  return LT
end

function srss.get(d,mon,yr,lat,lon,offset,dst_start,dst_stop)
	
  local date      = { year = yr, month = mon, day = d } -- os.date("*t")
  local lat       = lat 
  local lon       = lon 
  local offset    = offset
  local zenith    = 90.83 
  local dst_start = dst_start
  local dst_stop  = dst_stop
  	
    -- report("Latidude    : %s",lat)
    -- report("Longitude   : %s",lon)
    -- report("Offset      : %s",offset)
    -- report("Zenith      : %s",zenith)
    -- report("Datum       : %02i-%02i-%02i",date.year,date.month,date.day)
    -- report("DST begin in srss.get  : %s",dst_start)
    -- report("DST end in srss.get    : %s",dst_stop)
    
  -- determine whether the day for sun rise/set is with daylight saving
	local DST
		 
  if dst_start ~= "none" then	
    local dst_startday = tonumber(srss.ordinalday(dst_start))
    local dst_endday   = tonumber(srss.ordinalday(dst_stop))
    local calendarday  = srss.ordinalday(date.year.."/" 
    ..date.month.."/"..date.day)
  
    --report("Ordinal calendar day: %s", calendarday)
   
    if (calendarday <= dst_endday) and (calendarday >= dst_startday) then
  	  DST = true
    else
  	  DST = false
    end
	else
		DST = false
	end
  
  local rise_time = srss.sunturn_time(date,true,lat,lon,zenith,offset,DST)
  local set_time  = srss.sunturn_time(date,false,lat,lon,zenith,offset,DST)
  
  if type(rise_time) ~= "number" then return rise_time end
  if type(set_time)  ~= "number" then return set_time  end
  
  local hourfraction = srss.minutes(rise_time)
  local rise_hour    = floor(rise_time)..":"..hourfraction
  local hourfraction = srss.minutes(set_time)
  local set_hour     = floor(set_time)..":"..hourfraction
  local length       = (set_time - rise_time)
  local hourfraction = srss.minutes(length)
  local light_hours  = floor(length)..":"..hourfraction
  
  --report("Sun rise    : %s",rise_hour)
  --report("Sun set     : %s",set_hour)
  --report("Light hours : %s",light_hours)
  
  return rise_hour, set_hour, light_hours
end

function srss.minutes(time)
	return string.formatters["%02i"](floor((time - floor(time))*60))
end

function srss.ordinalday(inputstr)
	
	--report("Input : %s",inputstr)
	
	local sep = "%-%s/"
	if sep == nil then
		sep = "%s"
	end
	local t={}
	i=1
	for str in string.gmatch(inputstr, "([^"..sep.."]+)") do
		t[i] = str 
		i = i + 1	
	end
	
	--report("Datum strings: %s, %s, %s", t[1],t[2],t[3])
	
	local daynumber = os.date("*t",os.time{year=t[1],month=t[2],day=t[3]})
	local ordinalday = daynumber.yday
	
	--report("Day of year : %s",ordinalday)
	
	return ordinalday
end

function srss.sundata(...)		
  local r, s, l = srss.get(...)
  
  report("Working in function: srss.sundata")
  	
  if r and s and l then
    return r, s, l
  else
    return r 
  end
end
