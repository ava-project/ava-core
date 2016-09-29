// AVA
// VOCAL INTERPRETOR
// VIListen.hpp

#ifndef VILISTEN_HPP_
# define VILISTEN_HPP_

class   VIListen {
private:
  // VIListen attributes
  bool  isListening;

public:
  // Ctor & Dtor
  VIListen();
  ~VIListen();

  // VIListen routines
  bool  listen();
  bool  isListening() const;
  void  stopListening();
};

#endif // !VILISTEN_HPP_
