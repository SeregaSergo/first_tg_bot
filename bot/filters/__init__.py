from aiogram import Dispatcher
from .client_filters import isNotPrivate, isNotMember


def setup(dp: Dispatcher):
    dp.filters_factory.bind(isNotPrivate)
    dp.filters_factory.bind(isNotMember)