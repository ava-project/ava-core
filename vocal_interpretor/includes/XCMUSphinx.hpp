// AVA
// VOCAL INTERPRETOR
// XCMUSphinx.cpp

#ifndef XCMUSPHINX_HPP_
# define XCMUSPHINX_HPP_

# include "ADictionnary.hpp"
# include "CmdDictionnary.hpp"

class XCMUSphinx {
private:
  // XCMUSphinx attributes
  ADictionnary    CMU_dictionnary;
  CmdDictionnary  CMD_dictionnary;

public:
  // Ctor & Dtor
  XCMUSphinx();
  ~XCMUSphinx();

  // XCMUSphinx routines
  bool            loadLangDictionnary(std::string);
};

#endif // !XCMUSPHINX_HPP_
