"""
Setting up commands for feedback
"""
from aiogram import types
from aiogram.dispatcher import FSMContext

from src.packages.bot.filters import GroupMember, ChatWithABot, ChatWithABotCallback, GroupMemberCallback
from src.packages.bot.keyboards import inline_buttons
from src.packages.bot.loader import dispatcher, bot
from src.packages.bot.states import CreateReview
from src.packages.loaders import env_variables


@dispatcher.message_handler(ChatWithABot(), GroupMember(), text="Обратная связь")
async def user_start(message: types.Message):
    """
    Reaction to the text /Обратная связь
    """
    await message.answer(
        "Вы можете посмотреть или оставить отзыв о работе нашего сервиса!",
        reply_markup=inline_buttons.feedback_keyboard,
    )


@dispatcher.callback_query_handler(ChatWithABotCallback(), GroupMemberCallback(), text="Оставить отзыв")
async def write_review(call: types.CallbackQuery):
    """
    Reaction to the text in inline button "Оставить отзыв" and running the state machine
    """
    await call.message.answer("Ваш отзыв будет опубликован в группе, ждем предложений и пожеланий:")
    await CreateReview.review_text.set()


@dispatcher.message_handler(state=CreateReview.review_text)
async def send_review_in_group(message: types.Message, state: FSMContext):
    """
    Shutting down the state machine and sending a message to the feedback chat
    """
    group_parameters = await message.bot.get_chat(env_variables.get("CHANNEL_FEEDBACK_ID"))
    answer = f"{message.text}\n\n[{message.from_user.username}]({message.from_user.url})"
    await bot.send_message(env_variables.get("CHANNEL_FEEDBACK_ID"), answer, parse_mode=types.ParseMode.MARKDOWN)
    await message.answer(
        "Спасибо, что оставили, отзыв о нашем сервисе, мы постараемся учесть все замечания и "
        "обязательно их добавить в следующем обновлении, чтобы стать ещё удобнее для вас!\n\n"
        f"Ваш отзыв будет опубликован в канале [{group_parameters.title}]({group_parameters.invite_link})!!!",
        parse_mode=types.ParseMode.MARKDOWN,
    )

    await state.finish()
