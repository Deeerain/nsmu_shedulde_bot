from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters

from bot.bot_instance import application

from . import common
from . import subscribers

application.add_handler(CommandHandler('start', common.wlecome))


application.add_handler(MessageHandler(
    filters.Text('Расписание (Сегодня)'), common.shedulde_today))
application.add_handler(MessageHandler(
    filters.Text('Расписание (Завтра)'), common.shedulde_tomorrow))

application.add_handler(CallbackQueryHandler(common.button))


subscriber_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Text(
        subscribers.SubsButtons.SUBSCIBE.value), subscribers.choise_specialization)],
    states={
        subscribers.SubscribesCommandState.CHOISE_SPECIALIZATION: [MessageHandler(
            filters.ALL, subscribers.ready_specialization)],
        subscribers.SubscribesCommandState.CHOISE_GROUP: [MessageHandler(filters.ALL, subscribers.ready_group)],
    },
    fallbacks=[MessageHandler(filters.Text(
        ['Подписаться', 'Отмена']), subscribers.subscribe_done)]
)

application.add_handler(MessageHandler(
    filters.Text("Подписка"), subscribers.subscribes))

application.add_handler(subscriber_conversation_handler)
