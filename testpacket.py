from packet import Wrapper
from secrets import token, token2
import os

AnnikenAPI = Wrapper(TOKEN=token, TABLE_ID=305870)
""" VobAPI = Wrapper(TOKEN=token2, TABLE_ID=305516) """

print(AnnikenAPI.get_lessons_for_day(2))
os.remove("LAST_DOWNLOAD")
""" rint(VobAPI.get_lessons_for_day(1)) """