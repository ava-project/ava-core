#include <Python.h>
#include <string>


std::string say_hello(char *what) {
  return std::string("Hello, ") += what;
}

static PyObject *hello(PyObject * self, PyObject * args)
{
  char *input;

  if (!PyArg_ParseTuple(args, "s", &input)) {
    return NULL;
  }

  return Py_BuildValue("s", say_hello(input));
}

static PyMethodDef HelloMethods[] = {
 { "hello", (PyCFunction)hello, METH_VARARGS, "Say Hello" },
 { NULL, NULL, 0, NULL }
};

static struct PyModuleDef hello_world =
{
    PyModuleDef_HEAD_INIT,
    "hello_world",
    "",
    -1,
    HelloMethods
};

PyMODINIT_FUNC PyInit_hello_world(void)
{
    return PyModule_Create(&hello_world);
}
