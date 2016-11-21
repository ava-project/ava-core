// AVA
// VOCAL INTERPRETOR
// CmdDictionnary.cpp

#include "CmdDictionnary.hpp"

CmdDictionnary::CmdDictionnary() {}

CmdDictionnary::CmdDictionnary(std::string &dictionnary) {
  cmds.push_back(dictionnary);
}

CmdDictionnary::~CmdDictionnary() {}

bool  CmdDictionnary::loadDictionnary(std::string &dictionnary) {
  cmds.push_back(dictionnary);
  return (true);
}

bool  CmdDictionnary::unloadDictionnary(std::string &dictionnary) {
  for (int i = 0 ; i < cmds.size() ; i++) {
    if (cmds[i] == dictionnary) {
      cmds.erase(i);
      return (true);
    }
  }
  return (false);
}

std::vector<std::string>  CmdDictionnary::getCmds() const {
  return cmds;
}
