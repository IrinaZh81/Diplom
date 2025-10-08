import requests
import allure
from config import HEADERS, BASE_API_URL


@allure.title("Поиск фильмов по 2024 году")
@allure.description("Проверка получения списка фильмов 2024 года")
@allure.severity("critical")
def test_movies_2024():
    response = requests.get(
        f"{BASE_API_URL}/movie?page=1&limit=10&type=movie&year=2024",
        headers=HEADERS, timeout=10
    )

    assert response.status_code == 200, (
        f"Ожидался статус 200, получен {response.status_code}"
    )

    content_type = response.headers.get("Content-Type", "")
    assert content_type.startswith("application/json"), (
        "Ответ должен быть в формате JSON"
    )

    data = response.json()

    with allure.step("Проверка структуры ответа"):
        assert "docs" in data, "В ответе должно быть поле 'docs'"
        assert isinstance(data["docs"], list), "Поле 'docs' должно быть списком"
        assert len(data["docs"]) > 0, "Список фильмов не должен быть пустым"

    with allure.step("Проверка данных фильма"):
        first_movie = data["docs"][0]
        assert "id" in first_movie, "У фильма должен быть ID"
        has_name = "name" in first_movie or "alternativeName" in first_movie
        assert has_name, "У фильма должно быть название"
        assert "year" in first_movie, "У фильма должен быть год"
        expected_year = 2024
        actual_year = first_movie["year"]
        assert actual_year == expected_year, (
            f"Год фильма должен быть {expected_year}, получен {actual_year}"
        )


@allure.title("Поиск фильма по ID")
@allure.description("Проверка получения конкретного фильма по ID")
@allure.severity("critical")
def test_by_movie_id():
    movie_id = 1009536
    response = requests.get(
        f"{BASE_API_URL}/movie/{movie_id}", headers=HEADERS, timeout=10
    )

    assert response.status_code == 200, (
        f"Ожидался статус 200, получен {response.status_code}"
    )

    content_type = response.headers.get("Content-Type", "")
    assert content_type.startswith("application/json"), (
        "Ответ должен быть в формате JSON"
    )

    data = response.json()

    with allure.step("Проверка основных данных фильма"):
        assert "id" in data, "У фильма должен быть ID"
        assert data["id"] == movie_id, (
            f"ID фильма должен быть {movie_id}, получен {data['id']}"
        )
        has_name = "name" in data or "alternativeName" in data
        assert has_name, "У фильма должно быть название"
        assert "type" in data, "У фильма должен быть тип"


@allure.title("Поиск фильмов по названию")
@allure.description("Проверка поиска фильмов по названию 'Остров'")
@allure.severity("normal")
def test_by_name():
    url = (
        f"{BASE_API_URL}/movie/search?page=1&limit=10"
        f"&query=%D0%9E%D1%81%D1%82%D1%80%D0%BE%D0%B2"
    )
    response = requests.get(url, headers=HEADERS, timeout=10)

    assert response.status_code == 200, (
        f"Ожидался статус 200, получен {response.status_code}"
    )

    content_type = response.headers.get("Content-Type", "")
    assert content_type.startswith("application/json"), (
        "Ответ должен быть в формате JSON"
    )

    data = response.json()

    with allure.step("Проверка результатов поиска"):
        assert "docs" in data, "В ответе должно быть поле 'docs'"
        assert isinstance(data["docs"], list), "Поле 'docs' должно быть списком"
        assert len(data["docs"]) > 0, "Результаты поиска не должны быть пустыми"

        first_movie = data["docs"][0]
        movie_name = (
            first_movie.get("name", "")
            or first_movie.get("alternativeName", "")
        )
        assert movie_name, "У найденного фильма должно быть название"


@allure.title("Поиск актера по ID")
@allure.description("Проверка получения информации об актере")
@allure.severity("normal")
def test_by_actors():
    person_id = 37859
    response = requests.get(
        f"{BASE_API_URL}/person/{person_id}", headers=HEADERS, timeout=10
    )

    assert response.status_code == 200, (
        f"Ожидался статус 200, получен {response.status_code}"
    )

    content_type = response.headers.get("Content-Type", "")
    assert content_type.startswith("application/json"), (
        "Ответ должен быть в формате JSON"
    )

    data = response.json()

    with allure.step("Проверка данных актера"):
        assert "id" in data, "У актера должен быть ID"
        assert data["id"] == person_id, (
            f"ID актера должен быть {person_id}, получен {data['id']}"
        )
        has_name = "name" in data or "enName" in data
        assert has_name, "У актера должно быть имя"


@allure.title("Поиск рецензий на фильм")
@allure.description("Проверка получения рецензий на фильм")
@allure.severity("low")
def test_by_reviews():
    response = requests.get(
        f"{BASE_API_URL}/review?page=1&limit=10&movieId=397667",
        headers=HEADERS, timeout=10
    )

    assert response.status_code == 200, (
        f"Ожидался статус 200, получен {response.status_code}"
    )

    content_type = response.headers.get("Content-Type", "")
    assert content_type.startswith("application/json"), (
        "Ответ должен быть в формате JSON"
    )

    data = response.json()

    with allure.step("Проверка структуры ответа с рецензиями"):
        assert "docs" in data, "В ответе должно быть поле 'docs'"
        assert isinstance(data["docs"], list), "Поле 'docs' должно быть списком"

        if len(data["docs"]) > 0:
            first_review = data["docs"][0]
            assert "id" in first_review, "У рецензии должен быть ID"
            has_content = (
                "type" in first_review
                or "title" in first_review
                or "review" in first_review
            )
            assert has_content, "У рецензии должен быть контент"
