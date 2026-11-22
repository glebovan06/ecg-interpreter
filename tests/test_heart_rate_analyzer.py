import pytest
import allure
from ecg_interpreter.consts.consts import LOW_HEART_RATE, HIGH_HEART_RATE
from ecg_interpreter.ecg.heart_rate_analyser import (
    analyze_heart_rate,
    average_heart_rate,
    heart_rate_range,
)
from ecg_interpreter.models.interpretation import Diagnosis

# Константы для тестов
HR_BRADYCARDIA_EXTREME = 30
HR_BRADYCARDIA_BOUNDARY = LOW_HEART_RATE - 1
HR_NORMAL_MIDDLE = 85
HR_TACHYCARDIA_BOUNDARY = HIGH_HEART_RATE + 1
HR_TACHYCARDIA_EXTREME = 150
EXPECTED_AVERAGE_HR = 75.0


@allure.feature("Heart Rate Analyzer")
@allure.story("Analyze Heart Rate")
class TestAnalyzeHeartRate:

    @pytest.mark.parametrize(
        "heart_rate, expected",
        [
            (HR_BRADYCARDIA_EXTREME, Diagnosis.BRADYCARDIA),
            (HR_BRADYCARDIA_BOUNDARY, Diagnosis.BRADYCARDIA),
            (LOW_HEART_RATE, Diagnosis.NORMAL),
            (HR_NORMAL_MIDDLE, Diagnosis.NORMAL),
            (HIGH_HEART_RATE, Diagnosis.NORMAL),
            (HR_TACHYCARDIA_BOUNDARY, Diagnosis.TACHYCARDIA),
            (HR_TACHYCARDIA_EXTREME, Diagnosis.TACHYCARDIA),
        ],
        ids=[
            "extreme_bradycardia",
            "boundary_bradycardia",
            "boundary_normal_low",
            "normal_middle",
            "boundary_normal_high",
            "boundary_tachycardia",
            "extreme_tachycardia",
        ],
    )
    @allure.title("Классификация ЧСС")
    def test_analyze_heart_rate(self, heart_rate, expected):
        result = analyze_heart_rate(heart_rate)
        assert result == expected, (
            f"Когда ЧСС={heart_rate}: ожидали {expected}, получили {result}"
        )


@allure.feature("Heart Rate Analyzer")
@allure.story("Average Heart Rate")
class TestAverageHeartRate:

    @allure.title("Средний пульс для валидного набора измерений")
    @allure.severity(allure.severity_level.NORMAL)
    def test_average_positive(self, valid_ecg_dataset):
        result = average_heart_rate(valid_ecg_dataset)
        assert result == pytest.approx(EXPECTED_AVERAGE_HR), (
            f"Средний пульс должен быть {EXPECTED_AVERAGE_HR}, получено {result}"
        )

    @allure.title("Средний пульс для списка из одного измерения (граница размера)")
    def test_average_single_item_dataset(self, make_reading):
        # Явно показываем, что граница здесь — это размер списка = 1
        single_item_dataset = [make_reading(heart_rate=EXPECTED_AVERAGE_HR)]
        result = average_heart_rate(single_item_dataset)
        assert result == pytest.approx(EXPECTED_AVERAGE_HR), (
            f"Средний пульс для списка из одного элемента должен быть {EXPECTED_AVERAGE_HR}, получено {result}"
        )

    @allure.title("Пустой список вызывает ValueError")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_average_empty_raises(self, empty_ecg_dataset):
        with pytest.raises(ValueError, match="не может быть пустым"):
            average_heart_rate(empty_ecg_dataset)

    @allure.title("None вызывает ValueError")
    def test_average_none_raises(self):
        with pytest.raises(ValueError, match="не может быть пустым"):
            average_heart_rate(None)


@allure.feature("Heart Rate Analyzer")
@allure.story("Heart Rate Range")
class TestHeartRateRange:

    @allure.title("Диапазон пульса для валидного набора измерений")
    def test_range_positive(self, valid_ecg_dataset):
        min_hr, max_hr = heart_rate_range(valid_ecg_dataset)
        assert min_hr == pytest.approx(EXPECTED_AVERAGE_HR - 1), (
            f"Минимальная ЧСС должна быть {EXPECTED_AVERAGE_HR - 1}, получено {min_hr}"
        )
        assert max_hr == pytest.approx(EXPECTED_AVERAGE_HR + 1), (
            f"Максимальная ЧСС должна быть {EXPECTED_AVERAGE_HR + 1}, получено {max_hr}"
        )

    @allure.title("Пустой список вызывает ValueError")
    def test_range_empty_raises(self, empty_ecg_dataset):
        with pytest.raises(ValueError):
            heart_rate_range(empty_ecg_dataset)

    @allure.title("None вызывает TypeError")
    def test_range_none_raises(self):
        with pytest.raises(TypeError):
            heart_rate_range(None)