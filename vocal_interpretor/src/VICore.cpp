// AVA
// VOCAL INTERPRETOR
// VICore.cpp

#include "VICore.hpp"

VICore::VICore(CmdDaemon &daemon) : VI_cmd_daemon(daemon) {
}

VICore::~VICore() {}


XCMUSphinx  VICore::getXCMUSphinx() {
  return sphinxLibrary;
}

VIListen    VICore::getVIListen() {
  return VI_listen;
}

VIAnswer    VICore::getVIAnswer() {
  return VI_answer;
}

std::string   VICore::getCmdDaemon() {
  return VI_cmd_daemon.getLastCommand();
}
