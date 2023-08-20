from pandas import read_csv, DataFrame, Series

from dataclasses import dataclass
from typing import Optional

from misc.globals import settings

#convert user sheet names to sheet names in settings.json
sheetMasks = {
    "основа": "main",
    "резерв": "reserve"
}


#activity columns in main and reverse sheets are bit different
columns = {
    "main": ['[Lά] Branco Nostra пн.', 'вт.', 'ср.', 'чт.', 'пт.', 'сб.', 'вс.'],
    "reserve": ['[Lά] Branco Nostra 2 пн.', 'вт.', 'ср.', 'чт.', 'пт.', 'сб.', 'вс.']
}            

#week days by index
representValues = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

#maybe will be implemented later
#specialWords = ['-', 'отгул']


@dataclass
class SheetEntry:
    """
    Info about user activity.
    """
    nickname: str
    activity: list
    fullActivity: int

@dataclass
class WarnableMember:
    """
    Info about user who has lower activity than norm.
    """
    nickname: str
    activityShortage: int

class SheetParser:
    """
    Contains all methods for sheet parsing.
    """
    
    _dataFrameAllActivityColumn = "Общая активность "
    _dataFrameNicknamesColumn = "Ник "
    
    def __init__(self) -> None:

        #sheet DataFrame
        self._frame: DataFrame = None
        #sheet name
        self._sheet: str = ""
    
    def setFrame(self, sheet: str) -> bool:
        """
        Reads and saves sheet DataFrame.
        
        :param url: Sheet url.
        Returns: True if frame was successfully readed, else False.
        """
        
        sheets = settings.getSetting("sheets")
        try:
            
            self._sheet = sheetMasks[sheet]
            url = sheets[self._sheet]
            
        except KeyError:
            return False
        
        self._frame = read_csv(f"https://docs.google.com/spreadsheets/d/{url}/gviz/tq?tqx=out:csv", na_filter=False, converters = {i: str for i in range(100)})   
        return True
        
    def getActivityByName(self, name: str) -> Optional[SheetEntry]:
        """
        parses sheet DataFrame and gets activity by given name.
        
        :param name: member name.
        Returns: SheetEntry object if member in sheet, else None.
        """
        
        #empty name means that member has no nick in discord
        if name == "": return None
        
        #list of member activities
        activity = []
        #all members nicknames
        nicknamesColumn = self._frame[SheetParser._dataFrameNicknamesColumn]
        #looking member id
        memberId = -1
        
        #finding member id
        for i in range(len(nicknamesColumn)):
            
            member = nicknamesColumn[i]
            
            if member.lower() == name.lower():
                memberId = i
                break
        
        if memberId == -1:
            
            return None
        
        for column in columns[self._sheet]:
            
            content = self._frame[column][memberId]
            activity.append(content)
            
        return SheetEntry(
            nicknamesColumn[memberId],
            activity,
            self._frame[SheetParser._dataFrameAllActivityColumn][memberId]
        )
        
    def getMembersSortedByActivity(self, count: int) -> Optional[list[SheetEntry]]:
        """
        Parses DataFrame and sorts members by activity.
        
        :param count: count of members which will be sorted. if count equals -1 then all members will be included.
        Returns: sorted list of SheetEntries (activity list will be empty) if operation was successfull, else None.
        """
        
        #count can't be less than 1 except -1 which means that all rows will be parsed.
        if count != -1 and count <= 0:
            return None
        
        activityEntries = self._frame[SheetParser._dataFrameAllActivityColumn]
        nicknameEntries = self._frame[SheetParser._dataFrameNicknamesColumn]
        
        #normalized count which will be used in cycle
        actualCount = len(activityEntries) if count == -1 else count - 1
        
        sheetEntries: list[SheetEntry] = []
        for i in range(actualCount):
            
            nickname = nicknameEntries[i]
            
            #empty nickname means empty row
            if nickname == "": continue
            
            #sorting only by full activity so activity field is empty
            sheetEntries.append(
                SheetEntry(nickname, [], int(activityEntries[i]))
            )
        
        #sorting by full activity    
        sheetEntries.sort(reverse=True, key = lambda e: e.fullActivity)
        
        return sheetEntries[:actualCount + 1]
    
    def _getColumnByName(self, columnName: str) -> Series:
        """
        Gets column from frame by it's name
        
        Returns: column Series object.
        """
        
        return self._frame[columnName]
    
    def _isColumnFilled(self, column: Series) -> bool:
        """
        Checks that column is filled. Column needs to have at least one number to be filled.
        
        Returns: True if column is filled, else False.
        """
        
        for value in column:
            
            try:
                
                int(value)
                #at this point we can guarantee that value is int and column is filled.
                return True
            
            except:
                
                continue
        
        #column dont have any number values.
        return False
    
    def _getLastFilledDay(self) -> int:
        """
        Finds last day that is filled in sheet.
        
        Returns: index of last filled day if sheet have filld columns, else returns 0 (that equals to first column)
        """
        
        #get columns list for current sheet
        currentColumns = columns[self._sheet]
        
        #better to reverse columns list so we dont need to go through all list and just return first filled column index
        for i in reversed(range(len(currentColumns))):
            
            if self._isColumnFilled( self._frame[currentColumns[i]] ):
                return i       
            
        return 0
    
    def getWarnableMembers(self, day: str) -> Optional[list[WarnableMember]]:
        """
        Finds members in current DataFrame who has less than norm activity.
        
        :param day: day when need to find warnable members.
        """
        
        warnable = []
        
        if not day: return None
        
        #last is standard value when user is not specify it.
        if day == "last":
            
            #get last fiiled day
            dayIndex = self._getLastFilledDay()
            
            
        else:
            
            try:
                
                dayIndex = representValues.index(day.capitalize())
                
            except:
                #wrong day name
                return None
            
        
        membersNicknames = self._frame[SheetParser._dataFrameNicknamesColumn]
        
        currentSheetNorm = settings.getSetting("norms")[self._sheet]
        
        for i in range(len(membersNicknames)):
            
            currentMemberNickname = membersNicknames[i]
            
            currentSheetEntry: SheetEntry = self.getActivityByName(currentMemberNickname)
            
            if not currentSheetEntry: continue
                
            memberActive = currentSheetEntry.activity[dayIndex]
                
            try:
                
                memberActiveNumber = int(memberActive)
                
                if memberActiveNumber < currentSheetNorm:
                    
                    warnable.append(
                        WarnableMember(currentMemberNickname, currentSheetNorm - memberActiveNumber)
                    )
                
            except:
                continue
            
        return warnable