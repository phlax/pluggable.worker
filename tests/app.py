# -*- coding: utf-8 -*-

from unittest.mock import patch

import pytest

from aioworker.worker import Worker

from pluggable.worker.app import Py__WorkerApp as WorkerApp


class _MockWorker(Worker):
    pass


def MockWorker():
    return _MockWorker("BROKER")


def test_app_signature():
    with pytest.raises(TypeError):
        WorkerApp()


@patch('pluggable.worker.app.asyncio.get_event_loop')
@patch('pluggable.worker.app.Py__WorkerApp.setup_plugins')
@patch('pluggable.worker.app.Py__WorkerApp.create_hooks')
def test_app(hooks_m, plugins_m, aio_m):
    WorkerApp(MockWorker(), {"foo": "bar"})
    assert (
        [c[0] for c in hooks_m.call_args_list]
        == [()])
    assert (
        [c[0] for c in plugins_m.call_args_list]
        == [()])
    assert (
        [c[0] for c in aio_m.call_args_list]
        == [(), ()])
