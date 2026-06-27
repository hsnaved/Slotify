from datetime import (
    datetime,
    timedelta,
    date,
    time
)
from app.utils.slot_types import GeneratedSlot
from typing import List
from app.enums.weekdays import WeekDay

def generate_slots(
    current_date: date,
    start_time: time,
    end_time: time,
    duration_minutes: int
) -> List[GeneratedSlot]:
    
    slots = []

    day_start = datetime.combine(
        current_date,
        start_time
    )

    day_end = datetime.combine(
        current_date,
        end_time
    )

    current_slot_start = day_start

    duration = timedelta(
        minutes=duration_minutes
    )

    while current_slot_start + duration <= day_end:

        current_slot_end = (
            current_slot_start + duration
        )

        slots.append(
            GeneratedSlot(
                start_datetime=current_slot_start,
                end_datetime=current_slot_end
            )
        )

        current_slot_start = current_slot_end

    return slots


WEEKDAY_MAPPING = {
    WeekDay.MONDAY: 0,
    WeekDay.TUESDAY: 1,
    WeekDay.WEDNESDAY: 2,
    WeekDay.THURSDAY: 3,
    WeekDay.FRIDAY: 4,
    WeekDay.SATURDAY: 5,
    WeekDay.SUNDAY: 6,
}


def generate_slots_for_rule(
    start_date,
    end_date,
    weekdays,
    start_time,
    end_time,
    duration_minutes
) -> List[GeneratedSlot]:
    all_slots = []

    current_date = start_date

    selected_weekdays = {
        WEEKDAY_MAPPING[day]
        for day in weekdays
    }

    while current_date <= end_date:

        if current_date.weekday() in selected_weekdays:

            daily_slots = generate_slots(
                current_date=current_date,
                start_time=start_time,
                end_time=end_time,
                duration_minutes=duration_minutes
            )

            all_slots.extend(daily_slots)

        current_date += timedelta(days=1)

    return all_slots

if __name__ == "__main__":
    slots = generate_slots_for_rule(
        start_date=date(2026, 7, 1),
        end_date=date(2026, 7, 7),
        weekdays=[
            
        ],
        start_time=time(9, 0),
        end_time=time(17, 0),
        duration_minutes=60
    )

    print(f"Generated {len(slots)} slots\n")

    for slot in slots:
        print(
            f"{slot.start_datetime}  -->  {slot.end_datetime}"
        )