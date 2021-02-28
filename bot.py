import asyncio
import logging

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from utils import TestStates
import keyboards as kb

from config import TOKEN, PAY_TOKEN
loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage(), loop=loop)
dp.middleware.setup(LoggingMiddleware())

PRICES = [types.LabeledPrice(label='Machine time' , amount=4200000),
          types.LabeledPrice(label='holiday packaging' , amount=30000)]


TELEPORT_SHIPPING_OPTION = types.ShippingOption(id='teleporter' ,
                                                title='Wold teleport').add(types.LabeledPrice('teleport' , 1000000))

RUSSIAN_POST_SHIPPING_OPTION = types.ShippingOption(
    id='ru_post' , title='Russian post').add(
    types.LabeledPrice('Wooden box with shock absorbing suspension inside',100000)).add(
    types.LabeledPrice('Urgent departure (5-10 days)' , 500000))

PICKUP_SHIPPING_OPTION = types.ShippingOption(id='pickup' , title = 'pickup').add(
    types.LabeledPrice('pickup in Moskow' , 50000))




@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Hi!\nuse help, give list of commands' , reply_markup=kb.greet_kb)


@dp.message_handler(commands=['hi1'])
async def process_hi1_command(message: types.Message):
    await message.reply("change size of button" , reply_markup=kb.greet_kb1)

@dp.message_handler(commands=['hi2'])
async def process_hi2_command(message: types.Message):
    await message.reply("hide button after one click" , reply_markup=kb.greet_kb2)

@dp.message_handler(commands=['hi3'])
async def process_hi3_command(message: types.Message):
    await message.reply("more buttons..." , reply_markup=kb.markup3)


@dp.message_handler(commands=['hi4'])
async def process_hi4_command(message: types.Message):
    await message.reply("buttons in rows", reply_markup=kb.markup4)


@dp.message_handler(commands=['hi5'])
async def process_hi5_command(message: types.Message):
    await message.reply("more rows is button", reply_markup=kb.markup5)


@dp.message_handler(commands=['hi6'])
async def process_hi6_command(message: types.Message):
    await message.reply("give me your contact and location", reply_markup=kb.markup_request)

@dp.message_handler(commands=['hi7'])
async def process_hi7_command(message: types.Message):
    await message.reply("all methods", reply_markup=kb.markup_big)

@dp.message_handler(commands=['rm'])
async def process_rm_command(message: types.Message):
    await message.reply("remove keyboards", reply_markup=kb.ReplyKeyboardRemove())

@dp.message_handler(commands=['1'])
async def process_1_command(message: types.Message):
    await message.reply('first inline button' , reply_markup=kb.inline_kb1)

@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'button 1 is pressed!')

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 2:
        await bot.answer_callback_query(callback_query.id, text='second button pressed')
    elif code == 5:
        await bot.answer_callback_query(callback_query.id, text='button 5 is pressed' , show_alert= True)
    else:
        await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Inline button is pressed code={code}')


@dp.message_handler(commands=['2'])
async def process_command_2(message: types.Message):
    await message.reply('sending al buttons...' , reply_markup=kb.inline_kb_full)

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text(bold('list of commands:'),
               '/voice', '/photo', '/note', '/video', '/document',
               '/setstate' , '/terms' , '/buy' ,
               '/hi1' , '/hi2' ,'/hi3' , '/hi4' , '/hi5' ,'/hi6' ,
               '/hi7' , '/rm' , '/1' , '/2' ,  sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['voice'])
async def process_voice_command(message: types.Message):
    await bot.send_voice(message.from_user.id, open('demo-media/ogg/Rick_Astley_-_Never_Gonna_Give_You_Up.ogg' ,'rb') , reply_to_message_id=message.message_id)


@dp.message_handler(commands=['photo'])
async def process_photo_command(message: types.Message):
    await bot.send_photo(message.from_user.id, open('demo-media/pics/kitten0.jpg' ,'rb') , reply_to_message_id=message.message_id)


@dp.message_handler(commands=['video'])
async def process_video_command(message: types.Message):
    await bot.send_video(message.from_user.id, open('demo-media/videos/hedgehog.mp4' ,'rb') , reply_to_message_id=message.message_id)

@dp.message_handler(commands=['note'])
async def process_note_command(message: types.Message):
    await bot.send_video_note(message.from_user.id, open('demo-media/videoNotes/cute-puppy.mp4' ,'rb') , reply_to_message_id=message.message_id)


@dp.message_handler(commands=['document'])
async def process_document_command(message: types.Message):
    await bot.send_document(message.from_user.id, open('demo-media/files/very important text file.txt' ,'rb') , reply_to_message_id=message.message_id)

@dp.message_handler(state='*', commands=['setstate'])
async def process_setstate_command(message: types.Message):
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
    if not argument:
        await state.reset_state()
        return await message.reply('state is reset')

    if (not argument.isdigit()) or (int(argument) > len(TestStates.all())):
        return await message.reply('key is {} no valid'.format(argument))


    await state.set_state(TestStates.all()[int(argument)])
    await message.reply('state is changed', reply=False)


@dp.message_handler(state=TestStates.TEST_STATE_1)
async def first_state_case(message: types.Message):
    await message.reply('First State!', reply=False)


@dp.message_handler(state=TestStates.TEST_STATE_2)
async def second_state_case(message: types.Message):
    await message.reply('Second State!', reply=False)


@dp.message_handler(state=TestStates.TEST_STATE_3 | TestStates.TEST_STATE_4)
async def third_or_fourth_state_case(message: types.Message):
    await message.reply('Third or Fourth State!', reply=False)


@dp.message_handler(state=TestStates.all())
async def any_state_case(message: types.Message):
    await message.reply('Others State!', reply=False)

@dp.message_handler(commands=['terms'])
async def process_terms_command(message: types.Message):
    await message.reply('buy is time of machine' , reply=False)

@dp.message_handler(commands=['buy'])
async def process_buy_command(message: types.Message):
    await message.reply('1111 1111 1111 1026, 12/22, CVC 000   use this card' , reply=False)
    await bot.send_invoice(
        message.chat.id,
        title='Machine for change time',
        description="best time is machine",
        provider_token=PAY_TOKEN,
        currency='rub',
        photo_url='http://erkelzaar.tsudao.com/models/perrotta/TIME_MACHINE.jpg',
        photo_height=512,  # !=0/None, иначе изображение не покажется
        photo_width=512,
        photo_size=512,
        need_email = True,
        need_phone_number= True,
        is_flexible= True,  # True если конечная цена зависит от способа доставки
        prices=PRICES,
        start_parameter='time-machine-example',
        payload='some-invoice-payload-for-our-internal-use'
    )



@dp.shipping_query_handler()
async def process_shipping_query(shipping_query: types.ShippingQuery):
    print('shipping_query.shipping_address')
    print(shipping_query.shipping_address)

    if shipping_query.shipping_address.country_code == 'AU':
        return await bot.answer_shipping_query(shipping_query.id, ok = False, error_message='in Austral no shipping ')

    shipping_options = [TELEPORT_SHIPPING_OPTION]

    if shipping_query.shipping_address.country_code == 'RU':
        shipping_options.append(RUSSIAN_POST_SHIPPING_OPTION)

        if shipping_query.shipping_address.city == "Moskow":
            shipping_options.append(PICKUP_SHIPPING_OPTION)

    await bot.answer_shipping_query(shipping_query.id, ok = True, shipping_options=shipping_options)



@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    print ('order info')
    print(pre_checkout_query.order_info)

    if hasattr(pre_checkout_query.order_info, 'email') and (pre_checkout_query.order_info.email == 'vasya@pupkin.com'):

        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False, error_message='bad email')

    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok= True)



@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    print('successful_payment:')
    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f'{key} = {val}')

    await bot.send_message(message.chat.id,'Payment successful!')


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)