if not modules then modules = { } end modules ['t-moonphase'] = {
    version   = "2023.04.15",
    comment   = "Moonphase calculation",
    author    = "SubSystems www.subsystems.us edited by Willi Egger",
    copyright = "Willi Egger",
    email     = "w.egger@boede.nl",
    license   = "Public Domain"
}

thirddata           = thirddata     or { }
thirddata.moonphase = { }
local moonphase = thirddata.moonphase

local report   = logs.reporter("Lunar")

--[[
From an article published by SubSystems www.subsystems.us:

Let’s calculate the phase of the moon on 3/1/2017:
1) Express the date as Y = 2017, M = 3, D = 1.
2) If the month is January or February, subtract 1 from the year and add 12 to     the month
   Since the month March (M=3), we don’t need to adjust the values.
3) With a calculator, do the following calculations:

a. A = Y/100                                              A = 20
b. B = A/4               and then record the integer part B = 5
c. C = 2-A+B             and then record the integer part C = -13
d. E = 365.25 x (Y+4716) record the integer part          E = 2459228 
e. F = 30.6001 x (M+1)   record the integer part          F = 122 
f. JD = C+D+E+F-1524.5                                   JD = 2457813.5
 
Now that we have the Julian day, let’s calculate the days since the last new moon:
Day since New = 2457813.5 - 2451549.5 = 6264 days
If we divide this by the period, we will have how many new moons there have been:
New Moons = 6264 / 29.53 = 212.123 cycles
Now, multiply the fractional part by 29.53:
Days into cycle = 0.123 x 29.53 = 3.63 days since New Moon
--]]

function moonphase.julianday(y,m,d)
	local year  = y
	local month = m
	local day   = d
	
	if month == 1 or month == 2 then
		year = year - 1
		month = month + 12
	end
	local a = year/100
	local b = math.floor(a/4)
	local c = math.floor(2-a+b)
	local e = math.floor(365.25*(year+4716))
	local f = math.floor(30.6001*(month+1))
 	local jd = c + day + e + f - 1524.5
	
	return jd
end	

function moonphase.lunardays(y,m,d)
	local year  = y
	local month = m
	local day   = d
	
	report("Working in function: moonphase.lunardays")
	
	local JD    = moonphase.julianday(year,month,day)
	local days  = JD - 2451549.5  --2451549.5 is Julian date of 06-01-2000, a new moon date
	local cycles = days / 29.53  --29.53 is lunar month
	local moonphasedays = (cycles-math.floor(cycles))
	moonphasedays = moonphase.round(moonphasedays*29.53)
	
	--report("Tage im Mondzyclus: %s", moonphasedays)

	if moonphasedays == 29 then
	    moonphasedays = 0;
	end
	if moonphasedays == 0 then
		report("New Moon")
		return ("\\Moon[background=newmoon]{}")
	elseif moonphasedays == 7 then
		report("Quarter Moon")
		return ("\\Moon[background=growingmoon]{}")
	elseif moonphasedays == 15 then
		report("Full Moon")
		return ("\\Moon[background=fullmoon]{}")
	elseif moonphasedays == 22 then
		report("Three Quarter Moon")
		return ("\\Moon[background=waningmoon]{}")
	else
	  	return (moonphasedays);
  	end
	---return moonphasedays
end

--Lua does not have a round function. From the Internet:

function moonphase.round(num)
	local under = math.floor(num)
  local upper = math.floor(num) + 1
  local underV = -(under - num)
  local upperV = upper - num

  if (upperV > underV) then
    return under
  else
    return upper
  end
end
