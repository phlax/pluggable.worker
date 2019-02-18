# distutils: define_macros=CYTHON_TRACE_NOGIL=1
# cython: linetrace=True

import asyncio
from importlib import import_module

from aioworker.worker cimport Worker

from pluggable.core.app cimport App
from pluggable.core.hooks cimport Hook
from pluggable.core.signals cimport Signals
from pluggable.core.log cimport ServerLog

from aiocouchdb.v1.server cimport Server


cdef class WorkerApp(App):

    @property
    def default_config(self):
        return ()

    cpdef create_hooks(self):
        self.hooks['auth.usermanager'] = Hook()
        self.hooks['auth.sessions'] = Hook()
        self.hooks['auth.data'] = Hook()
        self.hooks['auth.user'] = Hook()
        self.hooks['tasks'] = self.create_hook()
        self.hooks['worker'] = self.create_hook()
        self.hooks['data'] = Hook(sync=False)
        self.hooks['managers'] = Hook(sync=False)

    async def on_start(self) -> None:
        self.couchdb = Server(url_or_resource='http://couch:5984')
        self.logs = ServerLog(self)
        self.usermanager = self.hooks['auth.usermanager'].get(self)
        print("usermanager loaded")
        print(self.usermanager)
        self.sessions = self.hooks['auth.sessions'].get(self)
        self.authdata = self.hooks['auth.data'].get(self)
        self.data = {}
        await self.hooks['data'].gather(self.data)
        self.managers = {}
        await self.hooks['managers'].gather(self.managers)
        for task in self.hooks['tasks'].gather().values():
            import_module(task)

    async def on_exit(self):
        print("Eeek, leaving this ~mortal coil")

    def log(self, *msgs):
        print('app: ' + ' '.join(str(m) for m in msgs))

    async def on_job_request(self, request):
        print("Got job start from aioworker!", request.task)

    async def on_job_done(self, request, result, timing):
        print('TASK RUN (%s): %ss' % (request.task.name, timing))


class Py__WorkerApp(WorkerApp):
    pass


__all__ = ('tasks', 'WorkerApp', 'Py__WorkerApp')
