# 📝 ToDoApp

Prosta i nowoczesna aplikacja typu **To-Do List**, umożliwiająca zarządzanie codziennymi zadaniami. Projekt został zbudowany z wykorzystaniem **FastAPI** po stronie backendu oraz **JavaScript, HTML i CSS** po stronie frontendu.

## 🚀 Funkcjonalności

👤 Zarządzanie użytkownikami
* Rejestracja nowych użytkowników
* Logowanie do aplikacji
* Bezpieczne przechowywanie danych uwierzytelniających
* Autoryzacja dostępu do zasobów użytkownika
* Obsługa sesji/tokenów dostępowych

✅ Zarządzanie zadaniami
* Dodawanie nowych zadań
* Edycja istniejących zadań
* Usuwanie zadań
* Oznaczanie zadań jako wykonane
* Wyświetlanie listy zadań przypisanych do zalogowanego użytkownika
* Kategorie i tagi zadań

---

## 🛠️ Technologie

### Backend

* Python 3.13
* FastAPI
* Uvicorn
* REST API
* JWT Authentication

### Frontend

* HTML5
* CSS3
* JavaScript (ES6+)

### Database

* SQLite

---

## 📂 Struktura projektu

```bash
ToDoApp/
|
├── main.py
├── models.py
├── database.py
└── requirements.txt
│
├── static/
│   ├── css
│   ├── js
│
├── routes/
│
├── templates/
|
|──tests/
|
└── README.md
```
🔐 System autoryzacji

Aplikacja wykorzystuje mechanizm uwierzytelniania użytkowników, dzięki któremu każdy użytkownik ma dostęp wyłącznie do własnych danych i zadań.

Proces działania:

1. Rejestracja nowego konta.
2. Logowanie do systemu.
3. Weryfikacja danych użytkownika.
4. Nadanie uprawnień dostępu.
5. Zarządzanie prywatną listą zadań.
---

## ⚙️ Instalacja

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/adam-91/todoapp.git
cd todoapp
```

### 2. Utwórz środowisko wirtualne

```bash
python -m venv venv
```

### 3. Aktywuj środowisko

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 4. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### 5. Uruchom backend

```bash
uvicorn main:app --reload
```

Backend będzie dostępny pod adresem:

```text
http://127.0.0.1:8000
```

Dokumentacja API:

```text
http://127.0.0.1:8000/docs
```

---

## 📡 Endpointy API

| Metoda | Endpoint          | Opis                              |
| ------ | ------------------| ----------------------------------|
| POST   | /auth             | create user                       |
| POST   | /auth/token       | JWT token                         |


| Metoda | Endpoint          | Opis                              |
| ------ | ------------------| ----------------------------------|
| GET    | /user             | Pobranie zalogowanego uzytkownika |
| POST   | /user             | Dodanie nowego zadania            |
| PUT    | /user/password    | Aktualizacja hasła                |
| PUT    | /user/name/{name} | Aktualizacja imienia              |
| PUT    | /user/emil/{email | Aktualizacja emaila               |

| Metoda | Endpoint          | Opis                              |
| ------ | ------------------| ----------------------------------|
| GET    | /activity         | Pobranie wszystkich zadań         |
| GET    | /activity/{id}    | Pobranie zadania                  |
| POST   | /activity/{id}    | Nowe zadanie hasła                |
| PUT    | /activity/{id}    | Aktualizacja zadania              |
| DELETE | /activity/{id}    | usunięcie/deaktywacja zadania     |

| Metoda | Endpoint          | Opis                              |
| ------ | ------------------| ----------------------------------|
| GET    | /categories       | Pobranie wszystkich kategorii     |
| GET    | /categories/{id}  | Pobranie kategorii                |
| POST   | /categories/{id}  | Stworzenie kategorii              |
| PUT    | /categories/{id}  | Aktualizacja kategorii            |
| DELETE | /categories/{id}  | usunięcie/deaktywacja kategorii   |

| Metoda | Endpoint          | Opis                              |
| ------ | ------------------| ----------------------------------|
| GET    | /types            | Pobranie wszystkich typów         |
| GET    | /types/{id}       | Pobranie typu                     |
| POST   | /types/{id}       | Stworzenie typu                   |
| PUT    | /types/{id}       | Aktualizacja typu                 |
| DELETE | /types/{id}       | Usunięcie/deaktywacja typu        |
---

## 🎯 Cel projektu

Projekt został stworzony w celu nauki:

* tworzenia REST API w FastAPI,
* komunikacji frontend–backend,
* obsługi żądań HTTP,
* zarządzania stanem aplikacji,
* organizacji kodu w aplikacjach webowych.

---

## 📸 Podgląd aplikacji

"in progras"

---

## 🔮 Możliwe rozszerzenia

 
* Resetowanie hasła
* Weryfikacja adresu e-mail
* Role użytkowników (User/Admin)
* Powiadomienia o terminach
* Dark Mode
* Aplikacja mobilna
---

## 👨‍💻 Autor

Projekt wykonany w celach edukacyjnych i rozwojowych.

**ToDoApp © 2026**
