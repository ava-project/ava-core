// AVA
// VOCAL INTERPRETOR
// CmdDaemon.hpp

#ifndef CMDDAEMON_HPP_
# define CMDDAEMON_HPP_

class CmdDaemon {
private:
  // CmdDaemon attributes
  std::string   lastCommand;

public:
  // Ctor & Dtor
  CmdDaemon();
  ~CmdDaemon();

  // CmdDaemon routines
  std::string   getLastCommand() const;
  void          setLastCommand(std::string);
};

#endif // !CMDDAEMON_HPP_
