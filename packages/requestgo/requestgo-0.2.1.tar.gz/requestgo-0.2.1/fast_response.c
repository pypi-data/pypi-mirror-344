
#include <Python.h>

static PyObject* fast_status_code(PyObject* self, PyObject* args) {
    const char* raw;
    if (!PyArg_ParseTuple(args, "s", &raw)) return NULL;

    int code = 0;
    sscanf(raw, "HTTP/1.%*d %d", &code);
    return PyLong_FromLong(code);
}

static PyMethodDef FastMethods[] = {
    {"status_code", fast_status_code, METH_VARARGS, "Extract status code from raw HTTP"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef fastmodule = {
    PyModuleDef_HEAD_INIT,
    "fast_response", NULL, -1, FastMethods
};

PyMODINIT_FUNC PyInit_fast_response(void) {
    return PyModule_Create(&fastmodule);
}
