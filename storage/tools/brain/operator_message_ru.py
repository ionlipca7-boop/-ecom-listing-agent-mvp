"""Russian operator messages for Brain Hard-Gate dry-run V1.

Messages must be short, clear, safe, and operator-friendly.
They must not include secrets, tokens, stack traces, or raw environment values.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OperatorMessage:
    status: str
    message_ru: str


def message_for_status(status: str, reason: str = "") -> OperatorMessage:
    """Return safe Russian operator message for Brain decision."""
    safe_reason = (reason or "").replace("\r", " ").replace("\n", " ").strip()

    if status == "ALLOW":
        return OperatorMessage(
            status=status,
            message_ru="Разрешено: действие прошло проверку Brain Hard-Gate. Live-действия не запускались без отдельного разрешения.",
        )

    if status == "ALLOW_DRY_RUN_ONLY":
        return OperatorMessage(
            status=status,
            message_ru="Разрешено только как dry-run: реальный запуск не выполнялся, publish/server/live не тронуты.",
        )

    if status == "CHECK_REQUIRED":
        if safe_reason:
            return OperatorMessage(
                status=status,
                message_ru=f"Нужна проверка: {safe_reason}. Live-действия не запускались.",
            )
        return OperatorMessage(
            status=status,
            message_ru="Нужна проверка перед продолжением. Live-действия не запускались.",
        )

    if status == "BLOCK":
        if safe_reason:
            return OperatorMessage(
                status=status,
                message_ru=f"Блокировано: {safe_reason}. Действие остановлено, live-запуск не выполнялся.",
            )
        return OperatorMessage(
            status=status,
            message_ru="Блокировано: Brain Hard-Gate остановил действие. Live-запуск не выполнялся.",
        )

    return OperatorMessage(
        status="CHECK_REQUIRED",
        message_ru="Нужна проверка: неизвестный статус решения. Live-действия не запускались.",
    )


def message_for_missing_pointer() -> OperatorMessage:
    return OperatorMessage(
        status="CHECK_REQUIRED",
        message_ru="Нужна проверка: CURRENT_POINTER не найден или неполный. Продолжать без pointer нельзя.",
    )


def message_for_missing_approval() -> OperatorMessage:
    return OperatorMessage(
        status="BLOCK",
        message_ru="Блокировано: действие требует approval gate. Без подтверждения оператора live-действие не запускается.",
    )


def message_for_wrong_environment() -> OperatorMessage:
    return OperatorMessage(
        status="BLOCK",
        message_ru="Блокировано: действие запрошено не из той среды. Сервер/live/runtime не тронуты.",
    )


def message_for_verification_required() -> OperatorMessage:
    return OperatorMessage(
        status="CHECK_REQUIRED",
        message_ru="Требуется проверка результата: API-ответ не считается финальным без verify. Следующий шаг заблокирован до проверки.",
    )
