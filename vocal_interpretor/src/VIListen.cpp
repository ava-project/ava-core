// AVA
// VOCAL INTERPRETOR
// VIListen.cpp

#include "VIListen.hpp"

VIListen::VIListen() {
  isListening = false;
}

VIListen::VIListen(bool const listen) {
  isListening = listen;
}

VIListen::~VIListen() {}

bool  VIListen::listen() {
  isListening = true;
}

bool  VIListen::isListening() const {
  return isListening;
}

void  VIListen::stopListening() {
  isListening = false;
}
