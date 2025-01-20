from aiogram.filters import Command, CommandStart, StateFilter, or_f
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from lexicon.lexicon import LEXICON
from keyboards.currencies_kb import create_currencies_keyboard
from database.database_get import get_data
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

# Создание роутера для обработки входящих сообщений
router = Router()
# Использование памяти для хранения состояний
storage = MemoryStorage()


# Класс для управления состояниями FSM калькулятора
class FSMCalculatorState(StatesGroup):
    enter_calculator = State()  # Состояние для ввода количества для калькулятора


# Обработчик команды /cancel
@router.message(Command(commands='cancel'))
async def process_cancel_command(message: Message, state: FSMContext):
    # Получаем текущее состояние пользователя
    cur_state = await state.get_state()
    if cur_state is None:
        await message.answer("Нечего отменять")
    else:
        # Очищаем состояние, если оно существует
        await state.clear()
        await message.answer("Действие отменено")


# Обработчик команды /start (первоначальное приветствие)
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON['/start'])  # Ответ с текстом из LEXICON


# Обработчик команды /help (выводит помощь)
@router.message(Command(commands='help'), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['/help'])  # Ответ с текстом из LEXICON


# Обработчик команды /currency (выводит информацию о валюте)
@router.message(Command(commands='currency'), StateFilter(default_state))
async def process_currency_command(message: Message):
    await message.answer(
        text=LEXICON['/currency'],  # Ответ с текстом из LEXICON
        reply_markup=create_currencies_keyboard()  # Клавиатура для выбора валюты
    )


# Обработчик команды /codes (выводит список валютных кодов)
@router.message(Command(commands='codes'), StateFilter(default_state))
async def process_codes_command(message: Message):
    await message.answer(
        text=LEXICON['/codes']  # Ответ с текстом из LEXICON
    )


# Обработчик коллбека от клавиатуры выбора валюты
@router.callback_query(or_f(StateFilter(default_state), FSMCalculatorState.enter_calculator))
async def process_currency_callback(callback_query: CallbackQuery, state: FSMContext):
    cur_state = await state.get_state()  # Получаем текущее состояние
    char_code = callback_query.data  # Получаем код валюты из данных коллбека
    all_data = get_data()  # Получаем все данные валют
    currency_data = None

    # Ищем информацию о валюте по ее коду
    for item in all_data:
        if item['Char_code'] == char_code:
            currency_data = item
            break

    if currency_data:
        if cur_state == FSMCalculatorState.enter_calculator.state:
            # Если пользователь в состоянии калькулятора, запросим ввод суммы для конвертации
            await state.update_data(selected_currency=currency_data)
            await callback_query.message.answer(f"Вы выбрали {currency_data['Name']} ({currency_data['Char_code']}).\n"
                "Введите количество рублей для конвертации в эту валюту")
            await callback_query.answer()
        else:
            # Если не в калькуляторе, выводим информацию о валюте
            await callback_query.message.answer(
                f"Информация о валюте {char_code}:\n"
                f"Название: {currency_data['Name']}\n"
                f"Номинал: {currency_data['Nominal']}\n"
                f"Курс: {currency_data['Value']}\n"
                f"Единичная стоимость: {currency_data['VunitRate']}"
            )
            await callback_query.answer()
    else:
        # Если не нашли информацию о валюте, сообщим пользователю
        await callback_query.message.answer(text="Не удалось найти информацию о выбранной валюте.")
        await callback_query.answer()


# Обработчик ввода количества для конвертации в валюту
@router.message(StateFilter(FSMCalculatorState.enter_calculator))
async def process_currency_calculation(message: Message, state: FSMContext):
    user_input = message.text  # Получаем текст, введенный пользователем

    # Проверяем, что введено корректное положительное число
    try:
        amount_in_rub = float(user_input)
        if amount_in_rub <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введите корректное положительное число.")
        return

    # Получаем данные о выбранной валюте из состояния
    data = await state.get_data()
    selected_currency = data.get("selected_currency")

    if not selected_currency:
        await message.answer("Произошла ошибка. Попробуйте снова.")
        return

    # Вычисляем количество валюты, которое можно получить за введенную сумму
    nominal = float(selected_currency['Nominal'])
    rate = float(selected_currency['Value'])

    currency_amount = (amount_in_rub * nominal) / rate

    # Отправляем результат пользователю
    await message.answer(
        f"На {amount_in_rub:.2f} рублей вы можете купить {currency_amount:.2f} {selected_currency['Name']} ({selected_currency['Char_code']})."
    )
    await state.clear()  # Очищаем состояние после выполнения


# Обработчик команды /calculator (запускает калькулятор для конвертации валют)
@router.message(Command(commands='calculator'), StateFilter(default_state))
async def process_calculator_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/calculator'],  # Ответ с текстом из LEXICON
                         reply_markup=create_currencies_keyboard()  # Клавиатура для выбора валюты
                         )
    await state.set_state(FSMCalculatorState.enter_calculator)  # Устанавливаем состояние калькулятора
