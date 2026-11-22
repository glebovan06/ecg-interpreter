import pytest
import allure
from ecg_interpreter.ecg.risk_analyser import risk_score


@allure.feature("Risk Analyzer")
@allure.story("Risk Score Calculation")
class TestRiskScore:

    @pytest.mark.parametrize(
        "fixture_name, expected_score",
        [
            # Для нормального ритма риск равен 0
            ("normal_data_ecg", 0.0),
            # Для брадикардии (URGENT + ЧСС-компонент) реальный риск = 6.0
            ("bradycardia_ecg", 6.0),
            # Для тахикардии реальный риск = 6.0
            ("tachycardia_ecg", 6.0),
            # Для инфаркта с нормальной ЧСС (90) риск тоже 0 из-за ограничения
            ("infarction_ecg", 0.0),
        ],
        ids=[
            "normal_reading",
            "bradycardia_reading",
            "tachycardia_reading",
            "infarction_reading_with_normal_hr",
        ]
    )
    @allure.title("Проверка значения риска для различных состояний")
    def test_risk_score_by_state(self, request, fixture_name, expected_score):
        reading = request.getfixturevalue(fixture_name)
        score = risk_score(reading)
        
        assert score == pytest.approx(expected_score), (
            f"Для {fixture_name} ожидали риск == {expected_score}, получено {score}. "
            "Проверьте формулу risk_score или ожидания."
        )

    @allure.title("Негатив: None вызывает ValueError")
    def test_risk_score_none_raises(self):
        with pytest.raises(ValueError):
            risk_score(None)