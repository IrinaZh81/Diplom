import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from config import BASE_UI_URL, BASE_HD_URL


# Фикстура для инициализации и закрытия драйвера
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(50)
    yield driver
    driver.quit()


@allure.feature("Поиск на Кинопоиске")
@allure.story("Поиск по названию")
def test_search_by_title(driver):
    with allure.step("Перейти на главную страницу"):
        driver.get(BASE_UI_URL)
    movie_title = "Интерстеллар"

    step_msg = f"Ввести название фильма '{movie_title}' в поисковую строку"
    with allure.step(step_msg):
        search_input = driver.find_element(By.NAME, "kp_query")
        search_input.send_keys(movie_title)
        search_input.send_keys(Keys.RETURN)

    step_msg = f"Проверить, что результат содержит фильм '{movie_title}'"
    with allure.step(step_msg):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.PARTIAL_LINK_TEXT, movie_title)
                )
            )
            result_link = driver.find_element(
                By.PARTIAL_LINK_TEXT, movie_title
            )
            assert movie_title in result_link.text
        except Exception:
            raise


@allure.story("Поиск по фильму")
def test_search_by_genre(driver):
    with allure.step("Перейти на главную страницу"):
        driver.get(BASE_UI_URL)
    movie_title = "Интерстеллар"

    step_msg = f"Ввести название фильма '{movie_title}' в поисковую строку"
    with allure.step(step_msg):
        search_input = driver.find_element(By.NAME, "kp_query")
        search_input.send_keys(movie_title)
    movie = driver.find_element(By.ID, "suggest-item-film-258687")
    assert movie.is_displayed(), "Поле поиска не отображается"


@allure.title("Просмотр подробной информации о фильме")
def test_view_movie_details(driver):
    driver.get(BASE_UI_URL)
    search_bar = driver.find_element(
        By.CSS_SELECTOR,
        "input[placeholder='Фильмы, сериалы, персоны']"
    )
    search_bar.send_keys("Интерстеллар")
    search_bar.send_keys(Keys.ENTER)

    movie_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Интерстеллар"))
    )
    movie_link.click()

    movie_info = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[class*="styles_paragraph"]')
        )
    )

    assert movie_info.is_displayed(), (
        "Подробная информация о фильме не отображается"
    )


@allure.title("Проверка заголовка страницы Kinopoisk")
def test_header(driver):
    driver.get(BASE_HD_URL)
    element = driver.find_element(By.TAG_NAME, "h1")
    expected_text = "Фильмы и сериалы, премиум‑телеканалы по подписке"
    assert element.text == expected_text


@allure.title("Проверка информации об актерах")
def test_check_actor_info(driver):
    driver.get(BASE_UI_URL)
    # Переход на страницу фильма
    search_bar = driver.find_element(
        By.CSS_SELECTOR,
        "input[placeholder='Фильмы, сериалы, персоны']"
    )
    search_bar.send_keys("Интерстеллар")
    search_bar.send_keys(Keys.ENTER)

    movie_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Интерстеллар"))
    )
    movie_link.click()

    # Переход на страницу с главными ролями
    cast_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "В главных ролях"))
    )
    cast_link.click()

    # Ожидание заголовка "Актеры"
    xpath_locator = (
        "//a[@name='actor']/following-sibling::div[contains("
        "text(), 'Актеры')]"
    )
    actor_header = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, xpath_locator))
    )
    assert actor_header.is_displayed(), (
        "Заголовок 'Актеры' не отображается"
    )
