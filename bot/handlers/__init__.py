from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters

from bot.bot_instance import application

from . import common
from . import subscribers
from . import start_handlers


start_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start_handlers.start)],
    states={
        start_handlers.State.SPECIALIZATION: [
            MessageHandler(filters.ALL, start_handlers.choise_specialization)
        ],
        start_handlers.State.GROUP: [
            MessageHandler(filters.ALL, start_handlers.choise_group)
        ]
    },
    fallbacks=[]
)

application.add_handler(start_conversation_handler)

# application.add_handler(MessageHandler(
#     filters.Text('Расписание (Сегодня)'), common.shedulde_today))
# application.add_handler(MessageHandler(
#     filters.Text('Расписание (Завтра)'), common.shedulde_tomorrow))

# application.add_handler(CallbackQueryHandler(common.button))


# subscriber_conversation_handler = ConversationHandler(
#     entry_points=[MessageHandler(filters.Text(
#         subscribers.SubsButtons.SUBSCIBE.value), subscribers.choise_specialization)],
#     states={
#         subscribers.SubscribesCommandState.CHOISE_SPECIALIZATION: [MessageHandler(
#             filters.ALL, subscribers.ready_specialization)],
#         subscribers.SubscribesCommandState.CHOISE_GROUP: [MessageHandler(filters.ALL, subscribers.ready_group)],
#     },
#     fallbacks=[MessageHandler(filters.Text(
#         ['Подписаться', 'Отмена']), subscribers.subscribe_done)]
# )

# application.add_handler(MessageHandler(
#     filters.Text("Подписка"), subscribers.subscribes))

# application.add_handler(subscriber_conversation_handler)
