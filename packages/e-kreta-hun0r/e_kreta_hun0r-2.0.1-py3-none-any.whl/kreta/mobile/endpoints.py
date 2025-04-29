from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Literal, Optional

from ..utils.utils import filter_params, request_category, week_dates
from .models import (
    AnnouncedTest,
    ClassAverage,
    ClassMaster,
    ConsultingHour,
    Evaluation,
    Group,
    Guardian4T,
    Homework,
    LepEvent,
    Lesson,
    Note,
    NoticeBoardItem,
    Omission,
    SchoolYearCalendarEntry,
    Student,
    SubjectAverage,
    TimeTableWeek,
)

if TYPE_CHECKING:
    from datetime import datetime

    from ..idp.auth_session import Auth_Session

mobile_request = partial(
    request_category,
    "https://{institute_code}.e-kreta.hu/ellenorzo/v3/",
)


def delete_bank_account_number(
    session: Auth_Session,
) -> None:
    mobile_request(
        session,
        "DELETE",
        "sajat/Bankszamla",
    )


def delete_reservation(
    session: Auth_Session,
    uid: str,
) -> None:
    mobile_request(
        session,
        "DELETE",
        f"sajat/Fogadoorak/Idopontok/Jelentkezesek/{uid}",
    )


def download_attachment(
    session: Auth_Session,
    uid: str,
) -> bytes:
    return mobile_request(
        session,
        "GET",
        f"sajat/Csatolmany/{uid}",
    ).content


def get_announced_tests(
    session: Auth_Session,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
) -> list[AnnouncedTest]:
    params: dict[str, str] = filter_params(
        datumTol=from_date,
        datumIg=to_date,
    )

    return mobile_request(
        session,
        "GET",
        "sajat/BejelentettSzamonkeresek",
        model=list[AnnouncedTest],
        params=params,
    )


def get_class_average(
    session: Auth_Session,
    educationalTaskUid: str,
    subjectUid: Optional[str] = None,
) -> list[ClassAverage]:
    params: dict[str, str] = filter_params(
        oktatasiNevelesiFeladatUid=educationalTaskUid,
        tantargyUid=subjectUid,
    )

    return mobile_request(
        session,
        "GET",
        "sajat/Ertekelesek/Atlagok/OsztalyAtlagok",
        model=list[ClassAverage],
        params=params,
    )


def get_class_master(
    session: Auth_Session,
    Uids: Optional[list[str]] = None,
) -> list[ClassMaster]:
    params = filter_params(
        Uids=" ".join(Uids),
    )

    return mobile_request(
        session,
        "GET",
        "felhasznalok/Alkalmazottak/Tanarok/Osztalyfonokok",
        model=list[ClassMaster],
        params=params,
    )


def get_consulting_hour(
    session: Auth_Session,
    Uid: str,
) -> ConsultingHour:
    return mobile_request(
        session,
        "GET",
        f"sajat/Fogadoorak/{Uid}",
        model=ConsultingHour,
    )


def get_consulting_hours(
    session: Auth_Session,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
) -> list[ConsultingHour]:
    params: dict[str, str] = filter_params(
        datumTol=from_date,
        datumIg=to_date,
    )

    return mobile_request(
        session,
        "GET",
        "sajat/Fogadoorak",
        model=ConsultingHour,
        params=params,
    )


def get_device_state(
    session: Auth_Session,
) -> bool:
    return mobile_request(
        session,
        "GET",
        "TargyiEszkoz/IsEszkozKiosztva",
    ).json()


def get_evaluations(
    session: Auth_Session,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
) -> list[Evaluation]:
    params: dict[str, str] = filter_params(
        datumTol=from_date,
        datumIg=to_date,
    )

    return mobile_request(
        session,
        "GET",
        "sajat/Ertekelesek",
        model=list[Evaluation],
        params=params,
    )


def get_groups(
    session: Auth_Session,
) -> list[Group]:
    return mobile_request(
        session,
        "GET",
        "sajat/OsztalyCsoportok",
        model=list[Group],
    )


def get_guardian4t(
    session: Auth_Session,
) -> Guardian4T:
    return mobile_request(
        session,
        "GET",
        "sajat/GondviseloAdatlap",
        model=Guardian4T,
    )


def get_homework(
    session: Auth_Session,
    id: str,
) -> Homework:
    return mobile_request(
        session,
        "GET",
        f"sajat/HaziFeladatok/{id}",
        model=Homework,
    )


def get_homeworks(
    session: Auth_Session,
    from_date: datetime,
    to_date: Optional[datetime] = None,
) -> list[Homework]:
    params: dict[str, str] = filter_params(
        datumTol=from_date,
        datumIg=to_date,
    )

    return mobile_request(
        session,
        "GET",
        "sajat/HaziFeladatok",
        model=list[Homework],
        params=params,
    )


def get_lep_events(
    session: Auth_Session,
) -> list[LepEvent]:
    return mobile_request(
        session,
        "GET",
        "Lep/Eloadasok",
        model=LepEvent,
    )


def get_lesson(
    session: Auth_Session,
    LessonUid: str,
) -> Lesson:
    params: dict[str, str] = filter_params(
        ororendElemUid=LessonUid,
    )

    return mobile_request(
        session,
        "GET",
        "sajat/OrarendElem",
        model=Lesson,
        params=params,
    )


def get_lessons(
    session: Auth_Session,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
) -> list[Lesson]:
    params: dict[str, str] = filter_params(
        datumTol=from_date,
        datumIg=to_date,
    )

    return mobile_request(
        session,
        "GET",
        "sajat/OrarendElem",
        model=list[Lesson],
        params=params,
    )


def get_notes(
    session: Auth_Session,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
) -> list[Note]:
    params: dict[str, str] = filter_params(
        datumTol=from_date,
        datumIg=to_date,
    )

    return mobile_request(
        session,
        "GET",
        "sajat/Feljegyzesek",
        model=list[Note],
        params=params,
    )


def get_noticeboard_items(
    session: Auth_Session,
) -> list[NoticeBoardItem]:
    return mobile_request(
        session,
        "GET",
        "sajat/FaliujsagElemek",
        model=list[NoticeBoardItem],
    )


def get_ommissions(
    session: Auth_Session,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
) -> list[Omission]:
    params: dict[str, str] = filter_params(
        datumTol=from_date,
        datumIg=to_date,
    )

    return mobile_request(
        session,
        "GET",
        "sajat/Mulasztasok",
        model=list[Omission],
        params=params,
    )


def get_registration_state(
    session: Auth_Session,
) -> dict | str | int | list:
    return mobile_request(
        session,
        "GET",
        "TargyiEszkoz/IsRegisztralt",
    ).json()


def get_schoolyear_calendar(
    session: Auth_Session,
) -> list[SchoolYearCalendarEntry]:
    return mobile_request(
        session,
        "GET",
        "Intezmenyek/TanevRendjeElemek",
        model=list[SchoolYearCalendarEntry],
    )


def get_student(
    session: Auth_Session,
) -> Student:
    return mobile_request(
        session,
        "GET",
        "sajat/TanuloAdatlap",
        model=Student,
    )


def get_subject_average(
    session: Auth_Session,
    educationalTaskUid: str,
) -> list[SubjectAverage]:
    params: dict[str, str] = filter_params(
        oktatasiNevelesiFeladatUid=educationalTaskUid,
    )

    return mobile_request(
        session,
        "GET",
        "sajat/Ertekelesek/Atlagok/OsztalyAtlagok",
        model=list[SubjectAverage],
        params=params,
    )


def get_timetable_weeks(
    session: Auth_Session,
    date_in_first_week: datetime,
    weeks: Literal[1, 2, 3],
) -> list[TimeTableWeek]:
    start, end = week_dates(date_in_first_week, weeks)
    params: dict[str, str] = filter_params(
        orarendElemKezdoNapDatuma=start,
        orarendElemVegNapDatuma=end,
    )

    return mobile_request(
        session,
        "GET",
        "Intezmenyek/Hetirendek/Orarendi",
        model=list[TimeTableWeek],
        params=params,
    )


def post_bank_account_number(
    session: Auth_Session,
    bankAccountNumber: str,
    bankAccountOwnerName: str,
    bankAccountOwnerType: int,
    bankName: str,
) -> None:
    json = {
        "BankszamlaSzam": bankAccountNumber,
        "BankszamlaTulajdonosNeve": bankAccountOwnerName,
        "BankszamlaTulajdonosTipusId": bankAccountOwnerType,
        "SzamlavezetoBank": bankName,
    }

    mobile_request(
        session,
        "POST",
        "sajat/Bankszamla",
        json=json,
    )
    return None


def post_contact(session: Auth_Session, email: str, phone_number: str) -> None:
    data = {
        "email": email,
        "telefonszam": phone_number,
    }

    mobile_request(
        session,
        "POST",
        "sajat/Elerhetoseg",
        data=data,
    )
    return None


def post_covid_form(session: Auth_Session) -> None:
    mobile_request(
        session,
        "POST",
        "Bejelentes/Covid",
    )
    return None


def post_reservation(session: Auth_Session, uid: str) -> None:
    mobile_request(
        session,
        "POST",
        f"Fogadoorak/Idopontok/Jelentkezesek/{uid}",
    )
    return None


def post_teszek_registration(
    session: Auth_Session,
    dateOfBirth: datetime,
    firstname: str,
    firstnameOfBirth: str,
    isAszfAccepted: bool,
    mothersFirstname: str,
    mothersSurname: str,
    namePrefix: str,
    placeOfBirth: str,
    surname: str,
    surnameOfBirth: str,
) -> None:
    data = {
        "SzuletesiDatum": dateOfBirth,
        "Utonev": firstname,
        "SzuletesiUtonev": firstnameOfBirth,
        "IsElfogadottAszf": isAszfAccepted,
        "AnyjaUtonev": mothersFirstname,
        "AnyjaVezeteknev": mothersSurname,
        "Elotag": namePrefix,
        "SzuletesiHely": placeOfBirth,
        "Vezeteknev": surname,
        "SzuletesiVezeteknev": surnameOfBirth,
    }

    mobile_request(
        session,
        "POST",
        "TargyiEszkoz/Regisztracio",
        data=data,
    )
    return None


def update_guardian4T(
    session: Auth_Session,
    dateOfBirth: datetime,
    firstname: str,
    firstnameOfBirth: str,
    isAszfAccepted: bool,
    mothersFirstname: str,
    mothersSurname: str,
    namePrefix: str,
    placeOfBirth: str,
    surname: str,
    surnameOfBirth: str,
) -> None:
    data = {
        "SzuletesiDatum": dateOfBirth,
        "Utonev": firstname,
        "SzuletesiUtonev": firstnameOfBirth,
        "IsElfogadottAszf": isAszfAccepted,
        "AnyjaUtonev": mothersFirstname,
        "AnyjaVezeteknev": mothersSurname,
        "Elotag": namePrefix,
        "SzuletesiHely": placeOfBirth,
        "Vezeteknev": surname,
        "SzuletesiVezeteknev": surnameOfBirth,
    }

    mobile_request(
        session,
        "PUT",
        "sajat/GondviseloAdatlap",
        data=data,
    )
    return None


def update_LEP_event_permission(
    session: Auth_Session,
    eventId: int,
    isPermitted: bool,
) -> None:
    json = {
        "EloadasId": eventId,
        "Dontes": isPermitted,
    }

    mobile_request(
        session,
        "POST",
        "Lep/Eloadasok/GondviseloEngedelyezes",
        json=json,
    )
    return None
