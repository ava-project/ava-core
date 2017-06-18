#include <Python.h>
#include <string>


std::string hello(char *what) {
  std::string hi("Hello, ");

  hi += what;
  return hi;
}

static PyObject * hello_wrapper(PyObject * self, PyObject * args)
{
  char *input;

  if (!PyArg_ParseTuple(args, "s", &input)) {
    return NULL;
  }

  return Py_BuildValue("s", hello(input));
}

static PyMethodDef HelloMethods[] = {
 { "hello_wrapper", (PyCFunction)hello_wrapper, METH_VARARGS, "Say Hello" },
 { NULL, NULL, 0, NULL }
};

static struct PyModuleDef Hello_world =
{
    PyModuleDef_HEAD_INIT,
    "Hello_world",
    "",
    -1,
    HelloMethods
};

PyMODINIT_FUNC PyInit_Hello_world(void)
{
    return PyModule_Create(&Hello_world);
}
