// AVA
// VOCAL INTERPRETOR
// CmdDaemon.cpp

CmdDaemon::CmdDaemon() {}

CmdDaemon::~CmdDaemon() {}

std::string   CmdDaemon::getLastCommand() const {
  return lastCommand;
}

void          CmdDaemon::setLastCommand(std::string const &command) {
  lastCommand = command;
}
