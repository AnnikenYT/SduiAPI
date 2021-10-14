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
            self.teachers.append(Teacher(teacher))
        # Lesson dates: {self.dates},

    def getRoom(self, room_number: int):
        try:
            return self.rooms[room_number-1]
        except:
            return Room({"id": "-1", "name": "No room found", "shortcut": "Empty Room"})


    def getTeacher(self, teacher_number: int):
        try:
            return self.teachers[teacher_number-1]
        except:
            return Teacher({"id": "-1", "name": "No teacher found", "shortcut": "No Teacher"})


    def __repr__(self) -> str:
        return f"Lesson ID: {self.id}, Lesson name: {self.name}, Lesson shortcut: {self.shortcut}, Lesson color: {self.color}, Lesson beginning: {self.begin}, Lesson end: {self.end}, Lesson Rooms: {self.rooms}, Lesson Teachers: {self.teachers}"       
    def __str__(self) -> str:
        return f"Lesson ID: {self.id}, Lesson name: {self.name}, Lesson shortcut: {self.shortcut}, Lesson color: {self.color}, Lesson beginning: {self.begin}, Lesson end: {self.end}, Lesson Rooms: {self.rooms}, Lesson Teachers: {self.teachers}"       

class Substitution(Lesson):
    def __init__(self, lessonData) -> None:
        Lesson.__init__(self, lessonData)
        
class Cancled(Lesson):
    def __init__(self, lessonData) -> None:
        Lesson.__init__(self, lessonData)

class RoomChange(Lesson):
    def __init__(self, lessonData) -> None:
        Lesson.__init__(self, lessonData)

# Hey you, snooping around in the code, huh?
# You might be wondering what this does.
# And if you think it doesnt do anything, youd be completely....
# ...right, actually.
# I have just created this, because I wanted to implement moved lessons,
# as the name suggests. But now im to lazy to actually write the code to
# implement it. Instead im sitting here, writing this comment.
# I don't know what you will do with this information, but here you go! :)
# Have a gread tay.
class MovedTo(Lesson):
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
