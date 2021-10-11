class Lesson:
    def __init__(self, lessonData) -> None:
        self.id        = lessonData["id"]
        self.dates     = lessonData["dates"]
        self.name      = lessonData["course"]["meta"]["displayname"]
        self.shortcut  = lessonData["course"]["meta"]["shortname"]
        self.color     = lessonData["course"]["meta"]["color"]
        self.begin     = lessonData["time_begins_at"]
        self.end       = lessonData["time_ends_at"]
        self.rooms     = []
        self.teachers  = []

        for room in lessonData["bookables"]:
            self.rooms.append(Room(room))
            
        for teacher in lessonData["teachers"]:
            self.rooms.append(Teacher(teacher))
    def __repr__(self) -> str:
        return f"Lesson ID: {self.id}, Lesson dates: {self.dates}, Lesson name: {self.name}, Lesson shortcut: {self.shortcut}, Lesson color: {self.color}, Lesson beginning: {self.begin}, Lesson end: {self.end}, Lesson Rooms: {self.rooms}, Lesson Teachers: {self.teachers}"       
    def __str__(self) -> str:
        return f"Lesson ID: {self.id}, Lesson dates: {self.dates}, Lesson name: {self.name}, Lesson shortcut: {self.shortcut}, Lesson color: {self.color}, Lesson beginning: {self.begin}, Lesson end: {self.end}, Lesson Rooms: {self.rooms}, Lesson Teachers: {self.teachers}"       

class Substitution(Lesson):
    def __init__(self, lessonData) -> None:
        Lesson.__init__(self, lessonData)

class Room:
    def __init__(self, roomData) -> None:
        self.id = roomData["id"]
        self.name = roomData["name"]
        self.shortcut = roomData["shortcut"]
        
    def __repr__(self) -> str:
        return f"{self.id, self.name, self.shortcut}"
    def __str__(self) -> str:
        return f"{self.id, self.name, self.shortcut}"

class Grade:
    def __init__(self, gradeData) -> None:
        self.id = gradeData["id"]
        self.name = gradeData["name"]
        self.shortcut = gradeData["shortcut"]
    def __repr__(self) -> str:
        return f"{self.id, self.name, self.shortcut}"
    def __str__(self) -> str:
        return f"{self.id, self.name, self.shortcut}"

class Teacher:
    def __init__(self, teacherData) -> None:
        self.id = teacherData["id"]
        self.name = teacherData["name"]
        self.shortcut = teacherData["shortcut"]
    
    def __repr__(self) -> str:
        return f"{self.id, self.name, self.shortcut}"
    def __str__(self) -> str:
        return f"{self.id, self.name, self.shortcut}"
