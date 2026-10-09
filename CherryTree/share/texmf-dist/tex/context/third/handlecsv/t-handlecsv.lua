-- %D \module
-- %D   [     file=t-handlecsv.lua,
-- %D      version=2025.10.29,
-- %D        title=HandleCSV module,
-- %D     subtitle=CSV file handling,
-- %D       author=Jaroslav Hajtmar (orig.), modifications by using ChatGPT,
-- %D         date=2025-02-25,
-- %D    copyright=Jaroslav Hajtmar,
-- %D        email=hajtmar@gyza.cz,
-- %D      license=GNU General Public License]
--
-- %C Copyright (C) 2019-2025 Jaroslav Hajtmar
-- %C
-- %C This program is free software: you can redistribute it and/or modify
-- %C it under the terms of the GNU General Public License as published by
-- %C the Free Software Foundation, either version 3 of the License, or
-- %C (at your option) any later version.
-- %C
-- %C This program is distributed in the hope that it will be useful,
-- %C but WITHOUT ANY WARRANTY; without even the implied warranty of
-- %C MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- %C GNU General Public License for more details.
-- %C
-- %C You should have received a copy of the GNU General Public License
-- %C along with this program.  If not, see <http://www.gnu.org/licenses/>.

--[[
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% t‑handlecsv module – Complete Listing of Defined Macros and Commands
%
% This section provides an overview of all the macros defined in the module,
% along with a brief description of their functionality.
%
% Status Condition Macros:
%   \ifissetheader           - Tests if the CSV header flag is set.
%   \ifnotsetheader          - Tests if the CSV header flag is not set.
%   \ifEOF                   - True if end-of-file for the CSV is reached.
%   \ifnotEOF                - True if not at the end-of-file.
%   \ifemptyline             - Tests if the current CSV row is empty.
%   \ifnotemptyline          - Tests if the current CSV row is not empty.
%   \ifemptylinesmarking     - True if empty lines marking is active.
%   \ifemptylinesnotmarking  - True if empty lines are not marked.
%
% Hook Macros:
%   \hookson                - Enable hooks (custom processing for rows/columns).
%   \hooksoff               - Disable hooks.
%   \resethooks             - Resets hook macros (\bfilehook, \efilehook,
%                             \blinehook, \elinehook, \bch, \ech) to empty.
%
% CSV Setup Macros:
%   \setheader              - Set the CSV header flag (first row contains names).
%   \unsetheader            - Unset the CSV header flag.
%   \setsep{<separator>}    - Set the CSV field separator.
%   \unsetsep               - Restore the default separator.
%   \setfiletoscan{<file>}   - Define the CSV file to be processed.
%
% Global Information Macros:
%   \numrows                - Returns the total number of rows in the CSV table.
%   \numemptyrows           - Returns the number of empty rows.
%   \numnotemptyrows        - Returns the number of non-empty rows.
%   \numcols                - Returns the total number of columns in the CSV table.
%   \csvfilename            - Contains the name of the current CSV file.
%
% Expression Tools:
%   \thenumexpr{<expression>} - Evaluates a TeX numeric expression.
%   \addto\macro{<text>}     - Appends non-expanded text to the macro.
%   \eaddto\macro{<text>}    - Appends fully expanded text to the macro.
%
% Cell Access Macros:
%   \getcsvcell[<col>,<row>] - Returns the content of the cell at the specified
%                             column (number or name) and row.
%   \csvcell[<col>,<row>]    - Alias for \getcsvcell.
%   \currentcell{<col>}      - Returns content of column <col> in the current row.
%   \nextcell{<col>}         - Returns content of column <col> in the next row.
%   \previouscell{<col>}     - Returns content of column <col> in the previous row.
%                             (Aliases: \currcell, \nextcell, \prevcell)
%
% Column Name Macros:
%   \colname[<n>]           - Returns the name of the nth column.
%   \xlscolname[<n>]        - Returns the Excel-style column name (A, B, …).
%   \cxlscolname[<n>]       - Returns the Excel-style column name prefixed with "c".
%   \texcolname[<n>]        - Returns a TeX-friendly version of the column name.
%   \indexcolname[<name>]    - Returns the column index for a given column name.
%
% Content Macros:
%   \columncontent[<col>]   - Returns the content of the specified column in the
%                             current row.
%   \numberxlscolname[<name>] - Converts an Excel column name to its numeric index.
%
% Line Pointer and Counter Macros:
%   \linepointer             - Returns the current CSV row pointer.
%   \lineno, \sernumline     - Synonyms for \linepointer.
%   \resetlinepointer        - Resets the row pointer to the first row.
%   \setlinepointer{<n>}     - Sets the row pointer to a specified row.
%   \savelinepointer         - Saves the current row pointer.
%   \setsavedlinepointer     - Restores the saved row pointer.
%
%   \numline                - Returns the current row counter (processed rows).
%   \setnumline{<n>}        - Sets the row counter to <n>.
%   \resetnumline           - Resets the row counter.
%   \addtonumline{<n>}      - Adds a number to the row counter.
%
% Row Indexing Macros:
%   \indexofnotemptyline{}  - Returns the index of the nth non-empty row.
%   \indexofemptyline{}     - Returns the index of the nth empty row.
%
% Empty Line Handling:
%   \markemptylines         - Marks empty rows in the CSV.
%   \notmarkemptylines      - Disables empty rows marking.
%   \resetmarkemptylines    - Resets the empty row marking.
%   \removeemptylines       - Removes empty rows from the CSV table.
%
% Navigation Macros:
%   \nextlineof[<file>]     - Advances the row pointer of the specified file.
%   \nextline                - Advances the row pointer of the current CSV.
%   \prevlineof[<file>]     - Moves the row pointer back in the specified file.
%   \prevline                - Moves the row pointer back in the current CSV.
%   \nextnumline            - Increments the row counter.
%   \nextrowof[<file>], \nextrow  - Reads the next row.
%   \prevrowof[<file>], \prevrow  - Reads the previous row.
%   \exitlooptest           - Macro to test and exit loops based on EOF.
%
% File Handling Macros:
%   \opencsvfile           - Opens a CSV file (optionally with a filename argument).
%   \closecsvfile{<file>}   - Closes the specified CSV file.
%
% Reading Macros:
%   \readline              - Reads a CSV row (optionally from a specified line).
%   \readline{<n>}         - Reads the nth row.
%
% Internal Parameter Processing:
%
% Cycle (Loop) Macros:
%   \doloopfromto{<start>}{<end>}{<action>}
%      - Executes <action> for each row from <start> to <end>.
%   \doloopforall, \doloopforall{<action>}
%      - Executes <action> for all rows (defaults to \lineaction if omitted).
%   \doloopaction, \doloopaction{<action>}, \doloopaction{<action>}{<end>},
%      \doloopaction{<action>}{<start>}{<end>}
%      - Executes <action> for a specified range of rows.
%   \doloopif{<val1>}{<operator>}{<val2>}{<action>}
%      - Executes <action> on rows satisfying the comparison condition.
%      (Synonym: \doloopifnum for numeric comparisons.)
%   \doloopuntil{<val1>}{<val2>}{<action>}
%      - Repeats <action> until <val1> equals <val2> (alias: \repeatuntil).
%   \doloopwhile{<val1>}{<val2>}{<action>}
%      - Repeats <action> while <val1> equals <val2> (alias: \whiledo).
%   \filelineaction, \filelineaction{<file>}
%      - Executes \lineaction for all rows of the specified CSV file.
%   \doloopfornext{<n>}{<action>}
%      - Executes <action> for the next <n> rows starting from the current row.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


--]]

thirddata           = thirddata           or {}
thirddata.handlecsv = thirddata.handlecsv or {}
local H = thirddata.handlecsv

--------------------------------------------------------------------------------
-- Local shortcuts – functions from string and math:
--------------------------------------------------------------------------------

local gsub, sub, byte, char, upper, floor = string.gsub, string.sub, string.byte, string.char, string.upper, math.floor
local match = string.match
local setmacro = interfaces.setmacro or ""

--------------------------------------------------------------------------------
-- Global variables and state tables:
--------------------------------------------------------------------------------

H.gUserCSVSeparator      = H.gUserCSVSeparator      or ';'
H.gUserCSVQuoter         = H.gUserCSVQuoter         or '"'
H.gUserCSVHeader         = (H.gUserCSVHeader ~= nil) and H.gUserCSVHeader or false
H.gUserUseHooks          = (H.gUserUseHooks  ~= nil) and H.gUserUseHooks or false
H.gUserColumnNumbering   = H.gUserColumnNumbering   or 'XLS'
H.gUserMarkingEmptyLines = (H.gUserMarkingEmptyLines ~= nil) and H.gUserMarkingEmptyLines or false

H.gCurrentlyProcessedCSVFile = nil
H.gMarkingEmptyLines         = (H.gMarkingEmptyLines ~= nil) and H.gMarkingEmptyLines or H.gUserMarkingEmptyLines
H.gUseHooks                  = (H.gUseHooks ~= nil) and H.gUseHooks or H.gUserUseHooks
H.gCSVHeader                 = (H.gCSVHeader ~= nil) and H.gCSVHeader or H.gUserCSVHeader
H.gCSVSeparator              = (H.gCSVSeparator ~= nil) and H.gCSVSeparator or H.gUserCSVSeparator
H.gCSVQuoter                 = (H.gCSVQuoter ~= nil) and H.gCSVQuoter or H.gUserCSVQuoter

H.gOpenFiles        = H.gOpenFiles        or {}
H.gNumLine          = H.gNumLine          or {}
H.gNumRows          = H.gNumRows          or {}
H.gNumEmptyRows     = H.gNumEmptyRows     or {}
H.gNumNotEmptyRows  = H.gNumNotEmptyRows  or {}
H.gNumCols          = H.gNumCols          or {}
H.gCurrentLinePointer = H.gCurrentLinePointer or {}
H.gColumnNames      = H.gColumnNames      or {}
H.gColNames         = H.gColNames         or {}
H.gTableRows        = H.gTableRows        or {}
H.gTableRowsIndex   = H.gTableRowsIndex   or {}
H.gTableEmptyRows   = H.gTableEmptyRows   or {}
H.gTableNotEmptyRows= H.gTableNotEmptyRows or {}

H.gSavedLinePointerNo = H.gSavedLinePointerNo or 1

--------------------------------------------------------------------------------
-- Helper Lua functions:
--------------------------------------------------------------------------------


function H.isEOF()
  local csvfile = H.getcurrentcsvfilename()
  local ptr = H.gCurrentLinePointer[csvfile] or 1
  local maxr = H.gNumRows[csvfile] or 0
  return ptr >= maxr
end



function H.texmacroisdefined(macroname)
  return token.get_cmdname(token.create(macroname)) ~= "undefined_cs"
end

function H.ParseCSVLine(line, sep)
  local splitter = utilities.parsers.rfc4180splitter{
      separator = sep,
      quote     = '"',
      strict    = true,
  }
  local list = splitter(line)
  return list[1]
end

function H.tmn(s)
  if not s or s == "" then s = "nil" end
  local maxmacrolength = 50
  local diachar  = {"á","ä","č","ď","é","ě","í","ň","ó","ř","š","ť","ú","ů","ý","ž",
                   "Á","Ä","Č","Ď","É","Ě","Í","Ň","Ó","Ř","Š","Ť","Ú","Ů","Ý","Ž"}
  local asciichar = {"a","a","c","d","e","e","i","n","o","r","s","t","u","u","y","z",
                     "A","A","C","D","E","E","I","N","O","R","S","T","U","U","Y","Z"}
  for i = 1, #diachar do
    s = gsub(s, diachar[i], asciichar[i])
  end
  s = gsub(s, "0", "O")
  s = gsub(s, "1", "I")
  s = gsub(s, "2", "II")
  s = gsub(s, "3", "III")
  s = gsub(s, "4", "IV")
  s = gsub(s, "5", "V")
  s = gsub(s, "6", "VI")
  s = gsub(s, "7", "VII")
  s = gsub(s, "8", "VIII")
  s = gsub(s, "9", "IX")
  s = gsub(s, "%A", "x")
  if #s > maxmacrolength then
    s = sub(s, 1, maxmacrolength)
  end
  return s
end

function H.xls2ar(colname)
  local colnumber = 0
  colname = upper(colname)
  for i = 1, #colname do
    local c = sub(colname, i, i)
    colnumber = 26 * colnumber + (byte(c) - byte('A') + 1)
  end
  return colnumber
end

function H.ar2xls(arnum)
  local part = floor(arnum / 26)
  local remainder = arnum % 26
  part = part - ((arnum % 26) == 0 and 1 or 0)
  remainder = remainder + ((arnum % 26) == 0 and 26 or 0)
  local ctl = ''
  if arnum < 703 then
    if part > 0 then ctl = char(64 + part) end
    ctl = ctl .. char(64 + remainder)
  else
    ctl = 'overZZ'
  end
  return ctl
end

function H.ar2colnum(arnum)
  if (H.gUserColumnNumbering or ''):lower() == 'xls' then
    return H.ar2xls(arnum)
  else
    return (converters and converters.romannumerals)
           and upper(converters.romannumerals(arnum))
           or tostring(arnum)
  end
end

function H.substitutecontentofcellof(csvfile, column, row, whattoreplace, substitution)
  local cfile = H.handlecsvfile(csvfile)
  local col = H.gColNames[cfile][column]
  local text = H.getcellcontentof(cfile, col, row)
  return text:gsub(tostring(whattoreplace), tostring(substitution))
end

function H.substitutecontentofcell(column, row, whattoreplace, substitution)
  local csvfile = H.getcurrentcsvfilename()
  local col = H.gColNames[csvfile][column]
  return H.substitutecontentofcellof(csvfile, col, row, whattoreplace, substitution)
end

function H.substitutecontentofcellofcurrentrow(column, whattoreplace, substitution)
  local row = H.linepointer()
  return H.substitutecontentofcell(column, row, whattoreplace, substitution)
end

function H.processinputvalue(inputparam, replacingnumber)
  if type(inputparam) ~= 'number' then
    return replacingnumber
  end
  return inputparam
end

--------------------------------------------------------------------------------
-- Functions for setting hooks, headers, and delimiters:
--------------------------------------------------------------------------------

function H.hookson()  H.gUseHooks = true  end
function H.hooksoff() H.gUseHooks = false end

function H.setfiletoscan(filetoscan)
  local inpcsvfile = H.handlecsvfile(filetoscan)
  H.gCurrentlyProcessedCSVFile = inpcsvfile
end

function H.setheader()
  H.gCSVHeader = true
  tex.sprint([[\global\issetheadertrue]])
  tex.sprint([[\global\notsetheaderfalse]])
end

function H.unsetheader()
  H.gCSVHeader = false
  tex.sprint([[\global\issetheaderfalse]])
  tex.sprint([[\global\notsetheadertrue]])
end

function H.setsep(sep)
  H.gCSVSeparator = sep
end

function H.unsetsep()
  H.gCSVSeparator = H.gUserCSVSeparator
end

--------------------------------------------------------------------------------
-- Functions for processing empty lines:
--------------------------------------------------------------------------------

function H.indexofnotemptyline(sernumline)
  local csvfilename = H.getcurrentcsvfilename()
  return H.gTableNotEmptyRows[csvfilename][sernumline]
end

function H.indexofemptyline(sernumline)
  local csvfilename = H.getcurrentcsvfilename()
  return H.gTableEmptyRows[csvfilename][sernumline]
end

function H.notmarkemptylines()
  local csvfilename = H.getcurrentcsvfilename()
  H.gMarkingEmptyLines = false
  for row = 1, (H.gNumRows[csvfilename] or 0) do
    H.gTableNotEmptyRows[csvfilename][row] = row
  end
  H.gTableEmptyRows[csvfilename] = {}
  H.gNumEmptyRows[csvfilename] = 0
  H.gNumNotEmptyRows[csvfilename] = H.gNumRows[csvfilename] or 0
  tex.sprint([[\global\emptylinefalse]])
  tex.sprint([[\global\notemptylinetrue]])
  tex.sprint([[\global\emptylinesmarkingfalse]])
  tex.sprint([[\global\emptylinesnotmarkingtrue]])
end

function H.markemptylines()
  local csvfilename = H.getcurrentcsvfilename()
  H.gTableEmptyRows[csvfilename] = {}
  H.gTableNotEmptyRows[csvfilename] = {}
  H.gMarkingEmptyLines = true

  local countempty = 0
  local countnonempty = 0
  local nrows = H.gNumRows[csvfilename] or 0
  for row = 1, nrows do
    if H.testemptyrow(row) then
      countempty = countempty + 1
      H.gTableEmptyRows[csvfilename][countempty] = row
    else
      countnonempty = countnonempty + 1
      H.gTableNotEmptyRows[csvfilename][countnonempty] = row
    end
  end
  H.gNumEmptyRows[csvfilename] = countempty
  H.gNumNotEmptyRows[csvfilename] = countnonempty
  tex.sprint([[\global\emptylinesmarkingtrue]])
  tex.sprint([[\global\emptylinesnotmarkingfalse]])
end

function H.resetmarkemptylines()
  local csvfilename = H.getcurrentcsvfilename()
  H.gMarkingEmptyLines = H.gUserMarkingEmptyLines
  if H.gMarkingEmptyLines then
    H.markemptylines()
  else
    H.notmarkemptylines()
  end
end

function H.testemptyrow(lineindex)
  local csvfilename = H.getcurrentcsvfilename()
  local ncols = H.gNumCols[csvfilename] or 0
  local linecontent = ""
  for column = 1, ncols do
    linecontent = linecontent .. (H.gTableRows[csvfilename][lineindex][column] or "")
  end
  local isempty = (linecontent == "")
  H.gTableRowsIndex[csvfilename][lineindex] = isempty
  return isempty
end

function H.emptylineevaluation(lineindex)
  local csvfilename = H.getcurrentcsvfilename()
  local isemp = H.gTableRowsIndex[csvfilename][lineindex]
  if isemp then
    tex.sprint([[\global\emptylinetrue]])
    tex.sprint([[\global\notemptylinefalse]])
  else
    tex.sprint([[\global\emptylinefalse]])
    tex.sprint([[\global\notemptylinetrue]])
  end
  return isemp
end

function H.removeemptylines()
  H.markemptylines()
  local csvfilename = H.getcurrentcsvfilename()
  local nnot = H.gNumNotEmptyRows[csvfilename] or 0
  local nrows = H.gNumRows[csvfilename] or 0
  for i = 1, nnot do
    local idx = H.gTableNotEmptyRows[csvfilename][i]
    H.gTableRows[csvfilename][i] = H.gTableRows[csvfilename][idx]
  end
  for i = (nnot + 1), nrows do
    H.gTableRows[csvfilename][i] = nil
  end
  H.gNumRows[csvfilename] = nnot
  H.markemptylines()
  H.gTableEmptyRows[csvfilename] = {}
  H.gTableNotEmptyRows[csvfilename] = {}
end

--------------------------------------------------------------------------------
-- Functions for evaluating hooks:
--------------------------------------------------------------------------------


function H.hooksevaluation()
  local csvf = H.getcurrentcsvfilename()
  for i = 1, #(H.gColumnNames[csvf] or {}) do
    local bname = 'bch' .. H.gColumnNames[csvf][i]
    if not H.texmacroisdefined(bname) then
      context.setgvalue(bname, '')
    end
    local ename = 'ech' .. H.gColumnNames[csvf][i]
    if not H.texmacroisdefined(ename) then
      context.setgvalue(ename, '')
    end
  end
end

--------------------------------------------------------------------------------
-- Functions for working with files and pointers:
--------------------------------------------------------------------------------

local function file_noext(filename)
  return match(filename, "^(.-)%.") or filename
end

function H.setgetcurrentcsvfile(filename)
  if filename then
    H.gCurrentlyProcessedCSVFile = filename
  end
  return tostring(H.gCurrentlyProcessedCSVFile)
end

function H.handlecsvfile(filename)
  local f = tostring(filename or "")
  f = gsub(f, '"', '')
  f = gsub(f, "'", "")
  if not H.isopenfile(f) then
    if f == "" then
      f = H.gCurrentlyProcessedCSVFile or ""
    end
  end
  return f
end

function H.getcurrentcsvfilename()
  return tostring(H.gCurrentlyProcessedCSVFile or "")
end

function H.isopenfile(csvfilename)
  return (H.gOpenFiles[csvfilename] ~= nil)
end

function H.closecsvfile(csvfilename)
  H.gOpenFiles[csvfilename] = nil
end

function H.getnumberofopencsvfiles()
  local count = 0
  for k, _ in pairs(H.gOpenFiles) do
    count = count + 1
  end
  return count
end

function H.setpointersofopeningcsvfile(inpcsvfile)
  H.gCurrentLinePointer[inpcsvfile] = 1
  H.gNumLine[inpcsvfile] = 1
  H.resetlinepointerof(inpcsvfile)
  H.setnumlineof(inpcsvfile, 1)
  tex.sprint([[\global\EOFfalse]])
  tex.sprint([[\global\notEOFtrue]])
  H.resetmarkemptylines()
end

function H.opencsvfile(filetoscan)
  local inpcsvfile = H.setgetcurrentcsvfile(filetoscan)
  if H.isopenfile(inpcsvfile) then
    H.setpointersofopeningcsvfile(inpcsvfile)
  else
    H.gOpenFiles[inpcsvfile] = inpcsvfile
    H.gColNames[inpcsvfile] = {}
    H.gColumnNames[inpcsvfile] = {}
    H.gTableRowsIndex[inpcsvfile] = {}
    H.gTableRows[inpcsvfile] = {}
    H.gTableEmptyRows[inpcsvfile] = {}
    H.gTableNotEmptyRows[inpcsvfile] = {}

    local data = io.loaddata(inpcsvfile) or ""
    local mycsvsplitter = utilities.parsers.rfc4180splitter{
      separator = H.gCSVSeparator,
      quote = H.gCSVQuoter,
      strict = true,
    }

    if H.gCSVHeader then
      H.gTableRows[inpcsvfile], H.gColumnNames[inpcsvfile] = mycsvsplitter(data, true)
    else
      H.gTableRows[inpcsvfile], H.gColumnNames[inpcsvfile] = mycsvsplitter(data)
      -- Pokud CSV neobsahuje hlavičku, vygenerujeme výchozí názvy sloupců
      if (not H.gColumnNames[inpcsvfile]) or (#H.gColumnNames[inpcsvfile] == 0) then
        H.gColumnNames[inpcsvfile] = {}
        local n = #H.gTableRows[inpcsvfile][1] or 0
        for i = 1, n do
          H.gColumnNames[inpcsvfile][i] = "col" .. i
        end
      end
    end

    if #H.gTableRows[inpcsvfile] > 0 then
      local ncols = #H.gTableRows[inpcsvfile][1]
      for i = 1, ncols do
        local coln = H.tmn(H.gColumnNames[inpcsvfile][i])
        H.gColNames[inpcsvfile][coln] = i
        H.gColNames[inpcsvfile][H.gColumnNames[inpcsvfile][i]] = i
        H.gColNames[inpcsvfile][H.ar2xls(i)] = i
        H.gColNames[inpcsvfile]["c" .. H.ar2xls(i)] = i
        H.gColNames[inpcsvfile][tostring(i)] = i
        H.gColNames[inpcsvfile][i] = i
        -- Definice maker pro sloupce se provede jen jednou při otevření CSV
        H.createxlscommandof(H.ar2colnum(i), inpcsvfile)
      end
    end

    H.gNumRows[inpcsvfile] = #H.gTableRows[inpcsvfile]
    if #H.gTableRows[inpcsvfile] > 0 then
      H.gNumCols[inpcsvfile] = #H.gTableRows[inpcsvfile][1]
    else
      H.gNumCols[inpcsvfile] = 0
    end
    H.gNumEmptyRows[inpcsvfile] = 0
    H.gNumNotEmptyRows[inpcsvfile] = H.gNumRows[inpcsvfile]

    H.setpointersofopeningcsvfile(inpcsvfile)
    if H.gUseHooks then
      H.hooksevaluation()
    end
  end
end

--------------------------------------------------------------------------------
-- Functions for reading lines and updating macros:
--------------------------------------------------------------------------------

function H.readlineof(inpcsvfile, numberofline)
  local nline = numberofline
  if type(nline) ~= 'number' then
    if not nline then
      nline = H.gCurrentLinePointer[inpcsvfile] or 1
    else
      nline = 0
    end
  end

  local maxrows = H.gNumRows[inpcsvfile] or 0
  local result = false

  if nline > 0 and nline <= maxrows then
    H.addtonumlineof(inpcsvfile, 1)
    H.gCurrentLinePointer[inpcsvfile] = nline
    H.assigncontentsof(inpcsvfile, H.gTableRows[inpcsvfile][nline])
    if nline == maxrows then
      tex.sprint([[\global\EOFtrue\global\notEOFfalse]])
    else
      tex.sprint([[\global\EOFfalse\global\notEOFtrue]])
    end
    result = true
  else
    H.assigncontentsof(inpcsvfile, 'nil_line')
    tex.sprint([[\global\EOFtrue\global\notEOFfalse]])
  end
  return result
end

function H.readline(numberofline)
  local csvfile = H.getcurrentcsvfilename()
  if type(numberofline) == 'number' then
    H.readlineof(csvfile, numberofline)
  else
    H.readlineof(csvfile, H.gCurrentLinePointer[csvfile])
  end
end

--------------------------------------------------------------------------------
-- Definitions of column macros – defined only once upon opening the CSV file
--------------------------------------------------------------------------------

function H.createxlscommandof(xlsname, csvfile)
  local inpcsvfile = H.handlecsvfile(csvfile)
  local docxlsname = "docol" .. xlsname
  local cxlsname = "col" .. xlsname

  if not H.texmacroisdefined(docxlsname) then
    interfaces.definecommand(docxlsname, {
      arguments = { { "option", "string" } },
      macro = function(opt_1)
        if #opt_1 > 0 then
          tex.sprint(H.getcellcontentof(inpcsvfile, xlsname, tonumber(opt_1)))
        else
          tex.sprint(H.getcellcontentof(inpcsvfile, xlsname, H.gCurrentLinePointer[inpcsvfile]))
        end
      end
    })
  end

  if not H.texmacroisdefined(cxlsname) then
    interfaces.definecommand(cxlsname, {
      macro = function()
        context.dosingleempty()
        context[docxlsname]()
      end
    })
  end
end

function H.createxlscommand(xlsname)
  local inpcsvfile = H.getcurrentcsvfilename()
  H.createxlscommandof(xlsname, inpcsvfile)
end

--------------------------------------------------------------------------------
-- Assignment of row content into macros – only updating values (macro definitions are NOT performed here)
--------------------------------------------------------------------------------

function H.assigncontentsof(inpcsvfile, line)
  if not inpcsvfile or inpcsvfile == "" then return end
  local cutoff = file_noext(inpcsvfile)
  local ncols = H.gNumCols[inpcsvfile] or 0
  local colnames = H.gColumnNames[inpcsvfile] or {}
  for i = 1, ncols do
    local content = (line == 'nil_line') and '' or line[i] or ''
    local puremacroname = H.tmn(colnames[i] or ("col" .. i))
    local purexlsname = H.ar2colnum(i)
    local xlsname = 'c' .. purexlsname
    local xlsfilename = H.tmn(cutoff) .. 'c' .. purexlsname
    local hookxlsname = 'h' .. xlsname
    local hookmacroname = 'h' .. puremacroname

    context.setgvalue(xlsname, content)
    context.setgvalue(xlsfilename, content)
    context.setgvalue(puremacroname, content)
    context.setgvalue('col' .. puremacroname, '\\col' .. purexlsname)
    if H.gUseHooks then
            -- context.setgvalue(hookxlsname,'\\bch\\bch' .. xlsname .. '\\' .. xlsname .. '\\ech' .. xlsname .. '\\ech')
       context.setgvalue(hookxlsname,'\\bch\\' .. xlsname .. '\\ech')
            -- context.setgvalue(hookmacroname,'\\bch\\bch' .. puremacroname .. '\\' .. xlsname .. '\\ech' .. puremacroname .. '\\ech ')
       context.setgvalue(hookmacroname,'\\bch\\' .. puremacroname .. '\\ech ')
    end
  end
end

function H.assigncontents(line)
  H.assigncontentsof(H.getcurrentcsvfilename(), line)
end

--------------------------------------------------------------------------------
-- Reading cell content:
--------------------------------------------------------------------------------

function H.getcellcontentof(csvfile, column, row)
  local cfile = H.handlecsvfile(csvfile)
  local col = column
  local r = row
  if type(col) == 'string' then
    local testcol = H.gColNames[cfile][col]
    if not testcol then
      col = H.xls2ar(col)
    else
      col = testcol
    end
  else
    col = tonumber(col) or 0
  end
  if col < 1 then col = 1 end
  local maxcol = H.gNumCols[cfile] or 0
  if col > maxcol then col = maxcol end
  if type(r) == 'string' then
    r = tonumber(r) or 0
  end
  local returnparametr = ''
  if type(col) == 'number' and type(r) == 'number' then
    local maxrows = H.gNumRows[cfile] or 0
    if r > 0 and r <= maxrows then
      returnparametr = H.gTableRows[cfile][r][col]
    elseif r == 0 then
      returnparametr = H.gColumnNames[cfile][col]
    end
  end
  return returnparametr or ''
end

function H.getcellcontent(column, row)
  return H.getcellcontentof(H.getcurrentcsvfilename(), column, row)
end

--------------------------------------------------------------------------------
-- Row Pointer Adjustments – Fix for Proper EOF Setting:
--------------------------------------------------------------------------------

function H.nextlineof(csvfile)
  local cfile = H.handlecsvfile(csvfile)
  local ptr = H.gCurrentLinePointer[cfile] or 1
  local maxr = H.gNumRows[cfile] or 0
  if ptr >= maxr then
    tex.sprint([[\global\EOFtrue\global\notEOFfalse]])
  else
    ptr = ptr + 1
    tex.sprint([[\global\EOFfalse\global\notEOFtrue]])
    H.gCurrentLinePointer[cfile] = ptr
  end
end

function H.nextline()
  H.nextlineof(H.getcurrentcsvfilename())
end

function H.previouslineof(csvfile)
  local cfile = H.handlecsvfile(csvfile)
  local ptr = H.gCurrentLinePointer[cfile] or 1
  if ptr <= 1 then
    ptr = 1
    tex.sprint([[\global\EOFtrue\global\notEOFfalse]])
  else
    ptr = ptr - 1
    tex.sprint([[\global\EOFfalse\global\notEOFtrue]])
    H.gCurrentLinePointer[cfile] = ptr
  end
end

function H.previousline()
  H.previouslineof(H.getcurrentcsvfilename())
end

--------------------------------------------------------------------------------
-- Row Pointer Setup:
--------------------------------------------------------------------------------

function H.setlinepointerof(csvfile, numberofline)
  local cfile = H.handlecsvfile(csvfile)
  local nline = H.processinputvalue(numberofline, H.gCurrentLinePointer[cfile])
  local maxr = H.gNumRows[cfile] or 0
  if nline < 1 then nline = 1 end
  if nline > maxr then nline = maxr end
  H.gCurrentLinePointer[cfile] = nline
  H.readlineof(cfile, nline)
end

function H.setlinepointer(numberofline)
  local csvfile = H.getcurrentcsvfilename()
  H.setlinepointerof(csvfile, numberofline)
end

function H.savelinepointer()
  local csvfile = H.getcurrentcsvfilename()
  H.gSavedLinePointerNo = H.gCurrentLinePointer[csvfile]
end

function H.setsavedlinepointer()
  H.setlinepointer(H.gSavedLinePointerNo)
end

function H.resetlinepointerof(csvfile)
  H.setlinepointerof(csvfile, 1)
end

function H.resetlinepointer()
  H.setlinepointerof(H.getcurrentcsvfilename(), 1)
end

function H.linepointerof(csvfile)
  return H.gCurrentLinePointer[csvfile]
end

function H.linepointer()
  local csvfile = H.getcurrentcsvfilename()
  return floor(tonumber(H.gCurrentLinePointer[csvfile] or 1))
end

function H.getcurrentlinepointer()
  return H.linepointer()
end

function H.getlinepointer()
  return H.linepointer()
end

--------------------------------------------------------------------------------
-- Row Counter Setup:
--------------------------------------------------------------------------------

function H.setnumlineof(csvfile, numline)
  local cfile = H.handlecsvfile(csvfile)
  H.gNumLine[cfile] = numline
end

function H.setnumline(numline)
  local csvfile = H.getcurrentcsvfilename()
  H.setnumlineof(csvfile, numline)
end

function H.resetnumlineof(csvfile)
  H.setnumlineof(csvfile, 0)
end

function H.resetnumline()
  H.resetnumlineof(H.getcurrentcsvfilename())
end

function H.addtonumlineof(inpcsvfile, numline)
  local cfile = H.handlecsvfile(inpcsvfile)
  H.gNumLine[cfile] = (H.gNumLine[cfile] or 0) + numline
end

function H.addtonumline(numline)
  local csvfile = H.getcurrentcsvfilename()
  H.addtonumlineof(csvfile, numline)
end

function H.numlineof(csvfile)
  local cfile = H.handlecsvfile(csvfile)
  return H.gNumLine[cfile]
end

function H.numline()
  return H.numlineof(H.getcurrentcsvfilename())
end

function H.nextnumlineof(csvfile)
  local cfile = H.handlecsvfile(csvfile)
  H.gNumLine[cfile] = (H.gNumLine[cfile] or 0) + 1
end

function H.nextnumline()
  local csvfile = H.getcurrentcsvfilename()
  H.nextnumlineof(csvfile)
end

--------------------------------------------------------------------------------
-- Number of rows, columns, etc.:
--------------------------------------------------------------------------------

function H.numrowsof(csvfile)
  local cfile = H.handlecsvfile(csvfile)
  return H.gNumRows[cfile] or 0
end

function H.numrows(optionalfile)
  local file = optionalfile or H.getcurrentcsvfilename() or ""
  return H.gNumRows[file] or 0
end

function H.numemptyrows()
  return H.gNumEmptyRows[H.getcurrentcsvfilename()] or 0
end

function H.numnotemptyrows()
  local cfile = H.getcurrentcsvfilename()
  local total = (H.gNumRows[cfile] or 0)
  local empt = (H.gNumEmptyRows[cfile] or 0)
  return total - empt
end

function H.numcolsof(csvfile)
  local cfile = H.handlecsvfile(csvfile)
  tex.sprint(H.gNumCols[cfile] or 0)
end

function H.numcols()
  local cfile = H.getcurrentcsvfilename()
  tex.sprint(H.gNumCols[cfile] or 0)
end


--------------------------------------------------------------------------------
-- Looping functions (cycles):
--------------------------------------------------------------------------------

-- New fast version of basic function
function H.doloopfromto(from, to, action)
  local output = {}
  local function append(s) table.insert(output, s) end
  append([[\opencsvfile ]])
  append([[\edef\tempnumline{\numline}]])
  append([[\resetnumline ]])

  local hooks = H.gUseHooks
  if hooks then append([[\bfilehook ]]) end

  local csvfile = H.getcurrentcsvfilename()
  local maxr = H.gNumRows[csvfile] or 0
  local f = from + 0
  local t = to + 0
  local step = 1
  local docycle = true
  if (f > maxr and t > maxr) then
    docycle = false
  end
  if docycle then
    if f > t then
      step = -1
      if f > maxr then f = maxr end
      if t < 1 then t = 1 end
    else
      if t > maxr then t = maxr end
      if f < 1 then f = 1 end
    end
    for i = f, t, step do
      if hooks then append([[\blinehook ]]) end
      append("\\readline{" .. i .. "}")
      append("\\removeunwantedspaces "..action) -- it was append(action)
      if hooks then append([[ \elinehook ]]) end
    end
  end
  if hooks then append([[\efilehook ]]) end
  append([[\setnumline{\tempnumline}]])
  tex.sprint(table.concat(output))
end


-- Old version of basic function
function H.doloopfromtooriginal(from, to, action)
  H.opencsvfile()
  local tempnumline = H.numline()
  H.resetnumline()
  H.inserthook("bfilehook")
  local csvfile = H.getcurrentcsvfilename()
  local maxr = H.gNumRows[csvfile] or 0
  local f = tonumber(from) or 0
  local t = tonumber(to) or 0
  local step = 1
  local docycle = true
  if (f > maxr and t > maxr) then
    docycle = false
  end
  if docycle then
    if f > t then
      step = -1
      if f > maxr then f = maxr end
      if t < 1 then t = 1 end
    else
      if t > maxr then t = maxr end
      if f < 1 then f = 1 end
    end
    for i = f, t, step do
      H.inserthook("blinehook")
      H.readline(i)
      tex.sprint("\\removeunwantedspaces "..action)
--      tex.sprint(action)
      H.inserthook("elinehook")
    end
  end
  H.inserthook("efilehook")
  H.setnumline(tempnumline)
  tex.sprint('\\removeunwantedspaces')
end


-- Old version of basic function
function H.doloopfornextoriginal(numberofrows, action)
  H.inserthook("bfilehook")
  tex.sprint([[\removeunwantedspaces]])
  local csvfile = H.getcurrentcsvfilename()
  local maxr = H.gNumRows[csvfile] or 0
  local from = H.gCurrentLinePointer[csvfile] or 1
  local to = from + numberofrows
  local step = 1
  if from > to then
    step = -1
    if from > maxr then from = maxr end
    if to < 1 then to = 1 end
  else
    if to > maxr then to = maxr end
    if from < 1 then from = 1 end
  end
  for i = from, (to - step), step do
      H.inserthook("blinehook")
      H.readline(i)
      tex.sprint(action)
      H.inserthook("elinehook")
  end
  H.addtonumline(-1)
  H.inserthook("efilehook")
  tex.sprint([[\nextrow]])
end



-- New fast version of basic function
function H.doloopfornext(numberofrows, action)
  local csvfile = H.getcurrentcsvfilename()
  local from = H.gCurrentLinePointer[csvfile] or 1
  local to = from + numberofrows - 1
  H.doloopfromto(from, to, action)
  H.addtonumline(-1)
  tex.sprint([[\nextrow]])
end




-- Actually in testing
function H.xdoloopif(first, op, third, action)
    H.opencsvfile()
    local tempnumline = H.numline()
    H.setnumline(1)
    local csvfile = H.getcurrentcsvfilename()
    local maxr = H.gNumRows[csvfile] or 0

    -- Normalizace operátorů
    if op == "=<" then op = "<=" end
    if op == "=>" then op = ">=" end
    if op == "<>" then op = "~=" end

       -- Určení, zda se jedná o číselné porovnání
         firstnum = tonumber(first)
         thirdnum = tonumber(third)
         isNumeric = (firstnum and thirdnum) and true or false

        if (isNumeric) then tex.sprint("numeric") else tex.sprint("nonumeric") end
        -- Pro operátory "==" a "~=" pokud nelze provést číselné porovnání, přepíšeme je na stringové varianty
        if (op == "==" or op == "~=") and not isNumeric then
            if op == "==" then op = "eq" else op = "neq" end
        end

        local paroperator = op  -- normalizovaný operátor


    local function processRow(condition)
        if condition then
         --   tex.sprint(first, paroperator, third,action)
            tex.sprint("horni")
        else
           tex.sprint("dolni")
            H.addtonumline(-1)
        end
    end


    for i = 1, maxr do
          H.readline(i)
--      tex.sprint("\\readline{" .. i .. "}")
--          tex.sprint(i)
--          tex.sprint(first,op,third,action)
--          local firstnum=tostring(first)
--          local thirdnum=tostring(third)


        if paroperator == "==" then
             tex.sprint (", firstnum=",firstnum, ", operator=",paroperator,", thirdnum=", thirdnum, ", i=",i,", ")

             processRow(isNumeric and (firstnum == thirdnum))
            tex.sprint("i=",i," rovno")
        elseif paroperator == "<" then
            processRow(firstnum and thirdnum and (firstnum < thirdnum))
        elseif paroperator == ">" then
            processRow(firstnum and thirdnum and (firstnum > thirdnum))
        elseif paroperator == "<=" then
            processRow(firstnum and thirdnum and (firstnum <= thirdnum))
        elseif paroperator == ">=" then
            processRow(firstnum and thirdnum and (firstnum >= thirdnum))
        elseif paroperator == "eq" then
            processRow(first == third)
        elseif paroperator == "neq" then
            processRow(first ~= third)
        elseif paroperator == "in" then
            processRow(string.find(third, first) ~= nil)
        elseif paroperator == "~in" then
            processRow(string.find(third, first) == nil)
        end
      tex.sprint("\\nextline")
    end


    H.setnumline(tempnumline)

end


--------------------------------------------------------------------------------
-- ConTeXt Maker Block of macros in Lua
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- Reset hooks and conversion of string to TeX context:
--------------------------------------------------------------------------------

function H.inserthook(hookname)
  if H.gUseHooks then
    local hookcontent = token.get_macro(hookname)
    if hookcontent and hookcontent ~= "" then
      tex.sprint(hookcontent)
    end
  end
end




-- This corresponds to the definition of the resethooks macro in ConText ie. \def\resethooks{blabla...}
token.set_macro("resethooks",[[\def\bfilehook{}\def\efilehook{}\def\blinehook{}\def\elinehook{}\def\bch{}\def\ech{}]],"global")

token.set_macro("hookson", tex.sprint(thirddata.handlecsv.hookson()) ,"global")

-- Corresponds callings of \resethooks macro in ConTeXt ie placing of \resetooks macro in string2print and its rewriting to ConTeXt
tex.sprint(token.get_macro("resethooks"))



-- Function for writing the command string to ConText
function H.string2context(str2ctx)
  local s = str2ctx
  s = gsub(s, "%%(.-)\n", "\n")
 context(s)
end


--------------------------------------------------------------------------------
-- ConTeXt Maker Block – Complete Definition of Makers (112 makers):
--------------------------------------------------------------------------------

local string2print = [[%
% --- State macros:
\newif\ifissetheader
\newif\ifnotsetheader
\newif\ifEOF
\newif\ifnotEOF
\newif\ifemptyline
\newif\ifnotemptyline
\newif\ifemptylinesmarking
\newif\ifemptylinesnotmarking

\let\lineaction\empty
%\def\resethooks{\ctxlua{context(thirddata.handlecsv.resethooks())}}
%\resethooks % -- DO IT NOW !!!

\def\hookson{\ctxlua{tex.sprint(thirddata.handlecsv.hookson())}}
\let\usehooks\hookson
\def\hooksoff{\ctxlua{tex.sprint(thirddata.handlecsv.hooksoff())}}

\def\setheader{\ctxlua{tex.sprint(thirddata.handlecsv.setheader())}}
\def\unsetheader{\ctxlua{tex.sprint(thirddata.handlecsv.unsetheader())}}
\let\resetheader\unsetheader

\def\setsep#1{\ctxlua{tex.sprint(thirddata.handlecsv.setsep('#1'))}}
\def\unsetsep{\ctxlua{tex.sprint(thirddata.handlecsv.unsetsep())}}
\let\resetsep\unsetsep

\def\setfiletoscan#1{\ctxlua{tex.sprint(thirddata.handlecsv.setfiletoscan('#1')); thirddata.handlecsv.opencsvfile()}}
\def\setcurrentcsvfile[#1]{\ctxlua{tex.sprint(thirddata.handlecsv.setgetcurrentcsvfile('#1'))}}

\def\numrows{\ctxlua{tex.sprint(thirddata.handlecsv.numrows())}}
\def\numrowsof[#1]{\ctxlua{tex.sprint(thirddata.handlecsv.numrowsof('#1'))}}
\def\numcols{\ctxlua{tex.sprint(thirddata.handlecsv.gNumCols[thirddata.handlecsv.gCurrentlyProcessedCSVFile])}}
\def\numcolsof[#1]{\ctxlua{tex.sprint(thirddata.handlecsv.gNumCols['#1'])}}
\def\currentcsvfile{\ctxlua{tex.sprint(thirddata.handlecsv.getcurrentcsvfilename())}}
\let\csvfilename\currentcsvfile

\def\numemptyrows{\ctxlua{tex.sprint(thirddata.handlecsv.numemptyrows())}}
\def\numnotemptyrows{\ctxlua{tex.sprint(thirddata.handlecsv.numnotemptyrows())}}

\def\thenumexpr#1{\the\numexpr(#1+0)}
\long\def\addto#1#2{\expandafter\def\expandafter#1\expandafter{#1#2}}
\long\def\eaddto#1#2{\edef#1{#1#2}}

\def\getcsvcell[#1,#2]{\ctxlua{tex.sprint(thirddata.handlecsv.getcellcontent(#1,#2))}}
\def\getcsvcellof[#1][#2,#3]{\ctxlua{tex.sprint(thirddata.handlecsv.getcellcontentof("#1",#2,#3))}}
\def\csvcell[#1,#2]{\getcsvcell[#1,\thenumexpr{#2+0}]}
\def\currentcsvcell#1{\getcsvcell[#1,\thenumexpr{\linepointer}]}
\let\currcell\currentcsvcell
\def\nextcsvcell#1{\ifnum\linepointer<\numrows{\getcsvcell[#1,\thenumexpr{\linepointer+1}]}\fi}
\let\nextcell\nextcsvcell
\def\previouscsvcell#1{\ifnum\linepointer>1{\getcsvcell[#1,\thenumexpr{\linepointer-1}]}\fi}
\let\prevcell\previouscsvcell

\def\colnameof[#1][#2]{\ctxlua{tex.sprint(thirddata.handlecsv.gColumnNames['#1'][#2])}}
\def\colname[#1]{\ctxlua{tex.sprint(thirddata.handlecsv.gColumnNames[thirddata.handlecsv.getcurrentcsvfilename()][#1])}}
\def\indexcolnameof[#1][#2]{\ctxlua{tex.sprint(thirddata.handlecsv.gColNames['#1'][#2])}}
\def\indexcolname[#1]{\ctxlua{tex.sprint(thirddata.handlecsv.gColNames[thirddata.handlecsv.getcurrentcsvfilename()][#1])}}
\def\xlscolname[#1]{\ctxlua{tex.sprint(thirddata.handlecsv.ar2colnum(#1))}}
\def\cxlscolname[#1]{\ctxlua{tex.sprint('c'..thirddata.handlecsv.ar2colnum(#1))}}
\def\texcolname[#1]{\ctxlua{tex.sprint(thirddata.handlecsv.tmn(thirddata.handlecsv.gColumnNames[thirddata.handlecsv.getcurrentcsvfilename()][#1]))}}
\def\columncontent[#1]{\getcsvcell[#1,\ctxlua{tex.sprint(thirddata.handlecsv.linepointer())}]}
\def\replacecontentin#1#2#3{\ctxlua{tex.sprint(thirddata.handlecsv.substitutecontentofcellofcurrentrow('#1','#2','#3'))}}
\def\numberxlscolname[#1]{\ctxlua{tex.sprint(thirddata.handlecsv.xls2ar(#1))}}
\def\columncontentof[#1][#2]{\ctxlua{tex.sprint(thirddata.handlecsv.getcellcontentof('#1',thirddata.handlecsv.gColNames['#1'][#2],thirddata.handlecsv.linepointerof('#1')))}}
\def\columncontent[#1]{\ctxlua{tex.sprint(thirddata.handlecsv.getcellcontent(thirddata.handlecsv.gColNames[thirddata.handlecsv.getcurrentcsvfilename()][#1],thirddata.handlecsv.linepointerof(thirddata.handlecsv.getcurrentcsvfilename())))}}

% MACROS FOR SETTING LINE POINTERS:
\def\setlinepointer#1{\ctxlua{thirddata.handlecsv.setlinepointer(#1)}}
\def\setlinepointerof[#1]#2{\ctxlua{thirddata.handlecsv.setlinepointerof('#1',#2)}}
\def\resetlinepointer{\ctxlua{tex.sprint(thirddata.handlecsv.resetlinepointer())}}
\def\resetlinepointerof[#1]{\ctxlua{tex.sprint(thirddata.handlecsv.resetlinepointerof('#1'))}}
\let\resetlineno\resetlinepointer
\let\resetsernumline\resetlinepointer

% MACROS FOR SETTING LINE COUNTERS:
\def\setnumline#1{\ctxlua{thirddata.handlecsv.setnumline(#1)}}
\def\resetnumline{\ctxlua{tex.sprint(thirddata.handlecsv.resetnumline())}}
\resetnumline
\def\linepointer{\ctxlua{tex.sprint(thirddata.handlecsv.linepointer())}}
\def\linepointerof[#1]{\ctxlua{tex.sprint(thirddata.handlecsv.linepointerof('#1'))}}
\let\lineno\linepointer
\let\sernumline\linepointer
\def\numline{\ctxlua{tex.sprint(thirddata.handlecsv.numline())}}
\def\addtonumline#1{\ctxlua{thirddata.handlecsv.addtonumline(#1)}}

\def\savelinepointer{\ctxlua{thirddata.handlecsv.savelinepointer()}}
\let\savelineno\savelinepointer
\def\setsavedlinepointer{\ctxlua{thirddata.handlecsv.setsavedlinepointer()}}
\let\setsavedlineno\setsavedlinepointer

\def\indexofnotemptyline#1{\ctxlua{tex.sprint(thirddata.handlecsv.indexofnotemptyline(#1))}}
\def\indexofemptyline#1{\ctxlua{tex.sprint(thirddata.handlecsv.indexofemptyline(#1))}}
\def\notmarkemptylines{\ctxlua{thirddata.handlecsv.notmarkemptylines()}}
\def\markemptylines{\ctxlua{thirddata.handlecsv.markemptylines()}}
\def\resetmarkemptylines{\ctxlua{thirddata.handlecsv.resetmarkemptylines()}}
\def\removeemptylines{\ctxlua{thirddata.handlecsv.removeemptylines()}}

% MACROS FOR SHIFTING ROW POINTERS AND LOOPS:
\def\nextlineof[#1]{\ctxlua{thirddata.handlecsv.nextlineof('#1')}}
\def\nextline{\ctxlua{thirddata.handlecsv.nextline()}}
\def\prevlineof[#1]{\ctxlua{thirddata.handlecsv.previouslineof('#1')}}
\def\prevline{\ctxlua{thirddata.handlecsv.previousline()}}
\def\nextnumline{\ctxlua{thirddata.handlecsv.nextnumline()}}
\def\nextrow{\nextline\readline}
\def\nextrowof[#1]{\nextlineof[#1]\readlineof[#1]{\ctxlua{tex.sprint(thirddata.handlecsv.linepointerof('#1'))}}}
\def\prevrow{\prevline\readline}
\def\prevrowof[#1]{\prevlineof[#1]\readlineof[#1]{\ctxlua{tex.sprint(thirddata.handlecsv.linepointerof('#1'))}}}
\def\exitlooptest{\ifEOF\exitloop\else\nextrow\fi}

% MACROS FOR OPENING/CLOSING CSV FILES:
\def\opencsvfile{\dosingleempty\doopencsvfile}
\def\doopencsvfile[#1]{\dosinglegroupempty\dodoopencsvfile}
\def\dodoopencsvfile#1{%
  \iffirstargument
    \ctxlua{thirddata.handlecsv.opencsvfile("#1")}
    \doifnot{\env{MainLinePointer}}{}{\setlinepointer{\env{MainLinePointer}}}
  \else
    \ctxlua{thirddata.handlecsv.opencsvfile()}
  \fi
}
\def\closecsvfile#1{\ctxlua{thirddata.handlecsv.closecsvfile("#1")}}

% MACROS FOR READING LINES:
\def\readline{\dosingleempty\doreadline}
\def\doreadline[#1]{\dosinglegroupempty\dodoreadline}
\def\dodoreadline#1{%
  \iffirstargument
    \ctxlua{thirddata.handlecsv.readline(#1)}
  \else
    \ctxlua{thirddata.handlecsv.readline(thirddata.handlecsv.gCurrentLinePointer[thirddata.handlecsv.gCurrentlyProcessedCSVFile])}
  \fi
}
\def\readlineof[#1]#2{\ctxlua{thirddata.handlecsv.readlineof('#1',#2)}}

% MACROS FOR PROCESSING PARAMETERS IN LOOPS:

\def\readandprocessparameters#1#2#3#4{%
  \edef\firstparam{#1}%
  \edef\secondparam{#2}%
  \edef\thirdparam{#3}%
  \def\fourthparam{#4}%\def\fourthparam{\if!#4!\else\removeunwantedspaces#4\fi}%
  \edef\paroperator{#2}%
  \ctxlua{
    local op='#2'
    local expressionisnotnumeric=not(type(tonumber('#1'))=='number' and type(tonumber('#3'))=='number')
        if (op == "==") and expressionisnotnumeric then op = "eq"
            elseif (op == "~=") and expressionisnotnumeric then op = "neq"
            elseif (op == "=<") then op = "<="
            elseif (op == "=>") then op = ">="
            elseif (op == "<>") then op = "~="
        end
    tex.sprint("\\def\\paroperator{"..op.."}")
  }%
}%
%


% LOOP MACROS:
\def\doloopfromto#1#2#3{\ctxlua{thirddata.handlecsv.doloopfromto([==[\thenumexpr{#1}]==],[==[\thenumexpr{#2}]==],[==[\detokenize{#3}]==])}}

\def\doloopforall{\dosinglegroupempty\doloopforAll}

\def\doloopforAll#1{
  \doifsomethingelse{#1}{
    \doloopfromto{1}{\numrows}{#1}
  }{
    \doloopfromto{1}{\numrows}{\lineaction}
  }
}

\def\doloopaction{\dotriplegroupempty\doloopAction}

\def\doloopAction#1#2#3{
  \opencsvfile
  \doifsomethingelse{#3}{
    \doloopfromto{#2}{#3}{#1}
  }{
    \doifsomethingelse{#2}{
      \doloopfromto{1}{#2}{#1}
    }{
      \doifsomethingelse{#1}{
        \doloopfromto{1}{\numrows}{#1}
      }{
        \doloopfromto{1}{\numrows}{\lineaction}
      }
    }
  }
}


\def\xdoloopif#1#2#3#4{\ctxlua{thirddata.handlecsv.xdoloopif([==[#1]==],[==[#2]==],[==[#3]==],[==[\detokenize{#4}]==])}}


\def\doloopif#1#2#3#4{
  \edef\tempnumline{\numline}
  \readandprocessparameters{#1}{#2}{#3}{#4}
  \removeunwantedspaces
  \ctxlua{
    local op='#2'
    local expressionisnotnumeric=not(type(tonumber('#1'))=='number' and type(tonumber('#3'))=='number')
        if (op == "==") and expressionisnotnumeric then op = "eq"
            elseif (op == "~=") and expressionisnotnumeric then op = "neq"
            elseif (op == "=<") then op = "<="
            elseif (op == "=>") then op = ">="
            elseif (op == "<>") then op = "~="
        end
        token.set_macro("paroperator",op)}
  \processaction[\paroperator][
    <=>{
      \doloopfromto{1}{\numrows}{
        \ctxlua{
          local a_num = tonumber('\luaescapestring{#1}') or 0
          local b_num = tonumber('\luaescapestring{#3}') or 0
          if a_num < b_num then   tex.sprint("\\fourthparam") else thirddata.handlecsv.addtonumline(-1) end
        }
      }
    },
    >=>{
      \doloopfromto{1}{\numrows}{
        \ctxlua{
          local a_num = tonumber('\luaescapestring{#1}') or 0
          local b_num = tonumber('\luaescapestring{#3}') or 0
          if a_num > b_num then tex.sprint("\\fourthparam") else thirddata.handlecsv.addtonumline(-1) end
        }
      }
    },
    ===>{
      \doloopfromto{1}{\numrows}{
        \ctxlua{
          local a_num = tonumber('\luaescapestring{#1}') or 0
          local b_num = tonumber('\luaescapestring{#3}') or 0
          if a_num == b_num then tex.sprint("\\fourthparam") else thirddata.handlecsv.addtonumline(-1) end
        }
      }
    },
    ~==>{
      \doloopfromto{1}{\numrows}{
        \ctxlua{
          local a_num = tonumber('\luaescapestring{#1}') or 0
          local b_num = tonumber('\luaescapestring{#3}') or 0
          if a_num ~= b_num then  tex.sprint("\\fourthparam") else thirddata.handlecsv.addtonumline(-1) end
        }
      }
    },
    >==>{
      \doloopfromto{1}{\numrows}{
        \ctxlua{
          local a_num = tonumber('\luaescapestring{#1}') or 0
          local b_num = tonumber('\luaescapestring{#3}') or 0
          if a_num >= b_num then tex.sprint("\\fourthparam") else thirddata.handlecsv.addtonumline(-1) end
        }
      }
    },
    <==>{
      \doloopfromto{1}{\numrows}{
        \ctxlua{
          local a_num = tonumber('\luaescapestring{#1}') or 0
          local b_num = tonumber('\luaescapestring{#3}') or 0
          if a_num <= b_num then  tex.sprint("\\fourthparam") else thirddata.handlecsv.addtonumline(-1) end
        }
      }
    },
    eq=>{
      \doloopfromto{1}{\numrows}{
        \ctxlua{
            local a_str = '\luaescapestring{#1}'
            local b_str = '\luaescapestring{#3}'
            if a_str == b_str then  tex.sprint("\\fourthparam") else thirddata.handlecsv.addtonumline(-1) end
        }
      }
    },
    neq=>{%
      \doloopfromto{1}{\numrows}{
        \ctxlua{
            local a_str = '\luaescapestring{#1}'
            local b_str = '\luaescapestring{#3}'
            if a_str ~= b_str then tex.sprint("\\fourthparam") else thirddata.handlecsv.addtonumline(-1) end
        }
      }
    },
    in=>{
      \doloopfromto{1}{\numrows}{
        \ctxlua{
          if string.find('\luaescapestring{#3}', '\luaescapestring{#1}') then tex.sprint("\\fourthparam") else thirddata.handlecsv.addtonumline(-1) end
        }
      }
    },
    ~in=>{
      \doloopfromto{1}{\numrows}{
        \ctxlua{
          if not string.find('\luaescapestring{#3}', '\luaescapestring{#1}') then tex.sprint("\\fourthparam") else thirddata.handlecsv.addtonumline(-1) end
        }
      }
    },
    repeatuntil=>{
      \doloop{
        \ctxlua{if '\luaescapestring{#1}'=='\luaescapestring{#3}' then tex.sprint('\\exitloop') else tex.sprint('\\ifEOF\\exitloop\\else\\fourthparam\\nextrow\\fi') end}%
      }
    },
    whiledo=>{
      \doloop{
        \ctxlua{if '\luaescapestring{#1}'~='\luaescapestring{#3}' then tex.sprint('\\exitloop') else tex.sprint('\\fourthparam\\ifEOF\\exitloop\\else\\nextrow\\fi') end}
      }
    }
  ]
\setnumline{\tempnumline}%
\removeunwantedspaces%
}%
%


\letvalue{doloopifnum}=\doloopif
\def\doloopuntil#1#2#3{\doloopif{#1}{repeatuntil}{#2}{#3}}
\letvalue{repeatuntil}=\doloopuntil
\def\doloopwhile#1#2#3{\doloopif{#1}{whiledo}{#2}{#3}}
\letvalue{whiledo}=\doloopwhile

\def\filelineaction{\dotriplegroupempty\dofilelineaction}
\def\dofilelineaction#1#2#3{%
  \doifelsenothing{#1}{\opencsvfile\doloopaction}{%
    \doifsomethingelse{#2}{\opencsvfile{#1}\doloopaction}{%
      \doifsomethingelse{#3}{\opencsvfile{#1}\doloopaction{\lineaction}{#2}}{%
        \opencsvfile{#1}\doloopaction{\lineaction}{#2}{#3}%
      }%
    }%
  }%
}
\def\doloopfornext#1#2{\ctxlua{thirddata.handlecsv.doloopfornext([==[\thenumexpr{#1}]==],[==[\detokenize{#2}]==])}}
]]

H.string2context(string2print)
-- End of module
