
from pluggable.core.app cimport App


cdef class WorkerApp(App):
     cdef public couchdb
     cdef public logs
     cdef public authdata
     cdef public usermanager
     cdef public data
     cdef public managers
