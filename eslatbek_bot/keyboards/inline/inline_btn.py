from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime

def get_target_btn(target_id):
    
    target_btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Bajarildi", callback_data=f"done_{target_id}"),
                InlineKeyboardButton(text="Bajarilmadi", callback_data=f"not_done_{target_id}"),
            ]        
        ]
    )
    
    return target_btn

async def choose_weekday_btn(checked):
    weekday_btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Dushanba" if checked["monday"] else "Dushanba", callback_data="monday"),
                InlineKeyboardButton(text="✅ Seshanba" if checked["tuesday"] else "Seshanba", callback_data="tuesday"),                
            ],
            [
                InlineKeyboardButton(text="✅ Chorshanba" if checked["wednesday"] else "Chorshanba", callback_data="wednesday"),
                InlineKeyboardButton(text="✅ Payshanba" if checked["thursday"] else "Payshanba", callback_data="thursday"),                
            ],
            [
                InlineKeyboardButton(text="✅ Juma" if checked["friday"] else "Juma", callback_data="friday"),
                InlineKeyboardButton(text="✅ Shanba" if checked["saturday"] else "Shanba", callback_data="saturday"),                
            ],
            [
                InlineKeyboardButton(text="✅ Yakshanba" if checked["sunday"] else "Yakshanba", callback_data="sunday"),
            ],
            [
                InlineKeyboardButton(text="✅ Barchasini tanlash" if all(checked.values()) else "Barchasini tanlash", callback_data="all_weekdays"),
            ],
            [
                InlineKeyboardButton(text="Next ⏭", callback_data="choosen_weekdays"),
            ],
           
           
      
         
        ]
    )
    
    return weekday_btn

def choose_hours_btn():
    hours_btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="04:00", callback_data="04:00"),
                InlineKeyboardButton(text="05:00", callback_data="05:00"),
                InlineKeyboardButton(text="06:00", callback_data="06:00"),
                InlineKeyboardButton(text="07:00", callback_data="07:00"),
            ],
            [
                InlineKeyboardButton(text="08:00", callback_data="08:00"),
                InlineKeyboardButton(text="09:00", callback_data="09:00"),
                InlineKeyboardButton(text="10:00", callback_data="10:00"),
                InlineKeyboardButton(text="11:00", callback_data="11:00"),
            ],
            [
                InlineKeyboardButton(text="12:00", callback_data="12:00"),
                InlineKeyboardButton(text="13:00", callback_data="13:00"),
                InlineKeyboardButton(text="14:00", callback_data="14:00"),
                InlineKeyboardButton(text="15:00", callback_data="15:00"),
            ],
            [
                InlineKeyboardButton(text="16:00", callback_data="16:00"),
                InlineKeyboardButton(text="17:00", callback_data="17:00"),
                InlineKeyboardButton(text="18:00", callback_data="18:00"),
                InlineKeyboardButton(text="19:00", callback_data="19:00"),
            ],
            [
                InlineKeyboardButton(text="20:00", callback_data="20:00"),
                InlineKeyboardButton(text="21:00", callback_data="21:00"),
                InlineKeyboardButton(text="22:00", callback_data="22:00"),
                InlineKeyboardButton(text="23:00", callback_data="23:00"),
            ],
          
            
            [
                InlineKeyboardButton(text="Next ⏭", callback_data="choosen_hours"),
            ]
           
      
         
        ]
    )
    
    return hours_btn

def get_calendar(year, month):
    
    first_day = datetime.date(year, month, 1)
    last_day = datetime.date(year, month, 1)
    
    while last_day.month == month:
        last_day += datetime.timedelta(days=1)
    last_day -= datetime.timedelta(days=1)

    keyboard = InlineKeyboardMarkup(row_width=7,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton( text="<",  callback_data="previous_month") ,
                                            InlineKeyboardButton( text=f"{first_day.strftime('%B')} {first_day.year}", callback_data="ignore"),
                                            InlineKeyboardButton( text=">", callback_data="next_month" )
                                        ],
                                        
                                        [
                                            InlineKeyboardButton(text="Du", callback_data="ignore"),
                                            InlineKeyboardButton(text="Se", callback_data="ignore"),
                                            InlineKeyboardButton(text="Cho", callback_data="ignore"),
                                            InlineKeyboardButton(text="Pay", callback_data="ignore"),
                                            InlineKeyboardButton(text="Ju", callback_data="ignore"),
                                            InlineKeyboardButton(text="Shan", callback_data="ignore"),
                                            InlineKeyboardButton(text="Yak", callback_data="ignore"),
                                        ]
                                    ]
                                    )

    current_date = datetime.date(year, month, 1)

    while current_date.weekday() != 0:
        current_date -= datetime.timedelta(days=1)

    while current_date <= last_day:
        if current_date.month == month:
            day = current_date.day
            callback_data = f"select_day_{day}_{month}_{year}"
        else:
            day = " "
            callback_data = "ignore"
        keyboard.insert(InlineKeyboardButton(str(day), callback_data=callback_data))
        
        if current_date.weekday() == 6:
            keyboard.row() 
        current_date += datetime.timedelta(days=1)

    return keyboard



def target_delete_btn(target_id):
    
    target_btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ O'chirish", callback_data=f"delete_{target_id}"),
            ]        
        ]
    )
    
    return target_btn


def view_progress_target_btn(target_id):
    
    target_btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📈 Ko'rish", callback_data=f"view_progress_{target_id}"),
            ]        
        ]
    )
    
    return target_btn