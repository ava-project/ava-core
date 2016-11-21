// AVA
// VOCAL INTERPRETOR
// CmdDictionnary.hpp

#ifndef CMDDICTIONNARY_HPP_
# define CMDDICTIONNARY_HPP_

# include <vector>

class                       CmdDictionnary {
private:
  // CmdDictionnary attributes
  std::vector<std::string>  cmds;

public:
  // Ctor & Dtor
  CmdDictionnary();
  CmdDictionnary(std::string &);
  ~CmdDictionnary();

  // CmdDictionnary routines
  bool                      loadDictionnary(std::string &);
  bool                      unloadDictionnary(std::string &);
  std::vector<std::string>  getCmds() const;
};

#endif // !CMDDICTIONNARY_HPP_
