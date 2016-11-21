// AVA
// VOCAL INTERPRETOR
// VICore.hpp

#ifndef VICORE_HPP_
# define VICORE_HPP_


# include <iostream>
# include <string>
# include "XCMUSphinx.hpp"
# include "VIListen.hpp"
# include "VIAnswer.hpp"
# include "CmdDaemon.hpp"

class         VICore {
private:
  // Core attributes
  XCMUSphinx  sphinxLibrary;
  VIListen    VI_listen;
  VIAnswer    VI_answer;
  CmdDaemon   VI_cmd_daemon;

public:
  // Ctor & Dtor
  VICore(CmdDaemon &);
  ~VICore();

  // Core routines
  XCMUSphinx  getXCMUSphinx();
  VIListen    getVIListen();
  VIAnswer    getVIAnswer();
  std::string getCmdDaemon();
};

#endif // !VICORE_HPP_
