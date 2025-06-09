import random 
from faker import Faker
from crud import *


fake = Faker('pt_BR')


def gerar_userprofile(n=10, k=150):
    return [{
        'iduser': i + k,
        "email": fake.email(),
        "password": fake.password(length=30),
        "handle": "@"+fake.user_name(),
        "photo": fake.user_name() + ".jpg",
        "siteaddress": fake.url() if random.random() < 0.9 else None,
        "biography": fake.sentence(nb_words=40, variable_nb_words=True) if random.random() < 0.9 else None
    } for i in range(n)]

def gerar_experience(n=10, k = 150):
    return [{
        "idexperience": i + k,
        "name": fake.company(),
        "experiencetype": random.choice(['Attraction', 'Restaurant', 'Museum', 'Destination', 'Hotel', 'Adventure']),  # exemplo de tipos
        "description": fake.sentence(nb_words=50, variable_nb_words=True) if random.random() < 0.8 else None,
        "siteaddress": fake.url() if random.random() < 0.9 else None,
        "phonenumber": fake.phone_number() if random.random() < 0.8 else None,
        "email": fake.company_email() if random.random() < 0.6 else None
    } for i in range(n)]

def gerar_experiencepicture(n=10, idexperience_range=(1, 10), k=150):
    return [{
        "idexperiencepicture": i + k,
        "photo": fake.city() + ".jpg",
        "alttext": fake.sentence(nb_words=40, variable_nb_words=True),
        "idexperience": random.randint(*idexperience_range) if random.random() < 0.9 else None
    } for i in range(n)]

def gerar_review(n=10, iduser_range=(1, 10), idexperience_range=(1, 10), k=150):
    return [{
        "idreview": i + k,
        "description": fake.text(max_nb_chars=150),
        "date": fake.date_between(start_date='-10y', end_date='today'),
        "score": random.randint(1, 5),
        "title": fake.sentence(nb_words=4) if random.random() < 0.6 else None,
        # "iduser": random.randint(*iduser_range) if random.random() < 0.95 else None,
        "iduser": 10 if random.random() < 0.95 else 4,
        # "idexperience": random.randint(*idexperience_range) if random.random() < 0.95 else None
        "idexperience": 10,
    } for i in range(n)]

def gerar_reviewpicture(n=10, idreview_range=(1, 10), k=150):
    return [{
        "idreviewpicture": i + k,
        "photo": fake.city() + ".jpg",
        "alttext": fake.sentence(nb_words=4, variable_nb_words=False),
        "idreview": random.randint(*idreview_range) if random.random() < 0.9 else None
    } for i in range(n)]

def gerar_schedule(n=10, idexperience_range=(1, 10), k=150):
    horarios = []
    for i in range(n):
        start_hour = random.randint(6, 18)
        end_hour = start_hour + random.randint(1, 5)
        horarios.append({
            "idschedule": i + k,
            "day": random.randint(0, 6),
            "startinghour": f"{start_hour:02d}:00",
            "endinghour": f"{end_hour:02d}:00",
            "idexperience": random.randint(*idexperience_range) if random.random() < 0.95 else None
        })
    return horarios

def gerar_subtypeexperience(n=10, k=150):
    return [{
        "idsubtypeexperience": i + k,
        "name": fake.word()
        } for i in range(n)]

def gerar_subtypeexperiencecategorizesexperience(n=10, idexperience_range=(1, 10), idsubtype_range=(1, 10)):
    return [{
        "idexperience": random.randint(*idexperience_range) if random.random() < 0.95 else None,
        "idsubtypeexperience": random.randint(*idsubtype_range) if random.random() < 0.95 else None
    } for _ in range(n)]


"""
if __name__ == "__main__":
    n = 1000
    k = 0

    # Geração principal
    dados_userprofile = gerar_userprofile(n=n, k=k)
    dados_experience = gerar_experience(n=n, k=k)
    dados_subtypeexperience = gerar_subtypeexperience(n=n, k=k)

    # # Inserir tabelas "principais" primeiro
    # for dado in dados_userprofile:  
    #     try:
    #         insert('userprofile', dado)
    #     except Exception as e:
    #         print(f"Erro ao inserir userprofile: {e}")

    # for dado in dados_experience:  
    #     try:
    #         insert('experience', dado)
    #     except Exception as e:
    #         print(f"Erro ao inserir experience: {e}")

    # for dado in dados_subtypeexperience:
    #     try:
    #         insert('subtypeexperience', dado)
    #     except Exception as e:
    #         print(f"Erro ao inserir subtypeexperience: {e}")

    # Extrair os ids inseridos
    idusers = [d["iduser"] for d in dados_userprofile]
    idexperiences = [d["idexperience"] for d in dados_experience]
    idsubtypes = [d["idsubtypeexperience"] for d in dados_subtypeexperience]

    # Gerar dependentes a partir dos ids já existentes
    dados_experiencepicture = gerar_experiencepicture(n=n, k=k, idexperience_range=(min(idexperiences), max(idexperiences)))
    dados_review = gerar_review(n=n, k=k, iduser_range=(min(idusers), max(idusers)), idexperience_range=(min(idexperiences), max(idexperiences)))
    idreviews = [d["idreview"] for d in dados_review]

    dados_reviewpicture = gerar_reviewpicture(n=n, k=k, idreview_range=(min(idreviews), max(idreviews)))
    dados_schedule = gerar_schedule(n=n, k=k, idexperience_range=(min(idexperiences), max(idexperiences)))
    dados_subtypeexperiencecategorizesexperience = gerar_subtypeexperiencecategorizesexperience(
        n=n,
        idexperience_range=(min(idexperiences), max(idexperiences)),
        idsubtype_range=(min(idsubtypes), max(idsubtypes))
    )

    # Inserir dependentes (linha por linha com tratamento de erro)
    for dado in dados_experiencepicture:
        try:
            insert('experiencepicture', dado)
        except Exception as e:
            print(f"Erro ao inserir experiencepicture: {e}")

    for dado in dados_review:
        try:
            insert('review', dado)
        except Exception as e:
            print(f"Erro ao inserir review: {e}")

    for dado in dados_reviewpicture:
        try:
            insert('reviewpicture', dado)
        except Exception as e:
            print(f"Erro ao inserir reviewpicture: {e}")

    for dado in dados_schedule:
        try:
            insert('schedule', dado)
        except Exception as e:
            print(f"Erro ao inserir schedule: {e}")

    for dado in dados_subtypeexperiencecategorizesexperience:
        try:
            insert('subtypeexperiencecategorizesexperience', dado)
        except Exception as e:
            print(f"Erro ao inserir subtypeexperiencecategorizesexperience: {e}")
if __name__ == "__main__":
    n = 1000
    k = 500
    # dados_reviewpicture = gerar_reviewpicture(n=n, k=k, idreview_range=(0, n + k))
    dados_review = gerar_review(n=n, k=k, iduser_range=(k, n+k), idexperience_range=(k, n+k))
    for dado in dados_review:
        print("asd")
        try:
            insert('review', dado)
        except Exception as e:
            print(f"Erro ao inserir review: {e}")
    # for dado in dados_reviewpicture:
    #     try:
    #         insert('reviewpicture', dado)
    #     except Exception as e:
    #         print(f"Erro ao inserir reviewpicture: {e}")

    # insert_many("reviewpicture", list_dicio=dados_reviewpicture)
"""

if __name__ == "__main__":
    n = 100000
    k = 60000 
    # Geração principal
    dados_userprofile = gerar_userprofile(n=n, k=k)
    dados_experience = gerar_experience(n=n, k=k)
    dados_subtypeexperience = gerar_subtypeexperience(n=n, k=k)

    # Inserir tabelas "principais" primeiro
    # insert_many("userprofile", list_dicio=dados_userprofile)
    # insert_many("experience", list_dicio=dados_experience)
    # insert_many("subtypeexperience", list_dicio=dados_subtypeexperience)

    # Extrair os ids inseridos
    idusers = [d["iduser"] for d in dados_userprofile]
    idexperiences = [d["idexperience"] for d in dados_experience]
    idsubtypes = [d["idsubtypeexperience"] for d in dados_subtypeexperience]

    # Gerar dependentes a partir dos ids já existentes
    # dados_experiencepicture = gerar_experiencepicture(n=n, k=k, idexperience_range=(min(idexperiences), max(idexperiences)))
    dados_review = gerar_review(n=n, k=k, iduser_range=(min(idusers), max(idusers)), idexperience_range=(min(idexperiences), max(idexperiences)))
    # idreviews = [d["idreview"] for d in dados_review]


    # dados_reviewpicture = gerar_reviewpicture(n=n, k=k, idreview_range=(min(idreviews), max(idreviews)))
    # dados_schedule = gerar_schedule(n=n, k=k, idexperience_range=(min(idexperiences), max(idexperiences)))
    # dados_subtypeexperiencecategorizesexperience = gerar_subtypeexperiencecategorizesexperience(
    #     n=n,
    #     idexperience_range=(min(idexperiences), max(idexperiences)),
    #     idsubtype_range=(min(idsubtypes), max(idsubtypes))
    # )

    # Inserir dependentes
    insert_many("review", list_dicio=dados_review)
    # insert_many("subtypeexperiencecategorizesexperience", list_dicio=dados_subtypeexperiencecategorizesexperience)
    # insert_many("experiencepicture", list_dicio=dados_experiencepicture)
    # insert_many("reviewpicture", list_dicio=dados_reviewpicture)
    # insert_many("schedule", list_dicio=dados_schedule)


