// AVA
// VOCAL INTERPRETOR
// VIAnswer.cpp

#include "VIAnswer.hpp"

VIAnswer::VIAnswer() {}

VIAnswer::~VIAnswer() {}

std::string  VIAnswer::getAnswer() const {
  return answer;
}

void  VIAnswer::setAnswer(std::string &newAnswer) {
  answer = newAnswer;
}
