// AVA
// VOCAL INTERPRETOR
// VIAnswer.hpp

#ifndef VIANSWER_HPP_
# define VIANSWER_HPP_

# include <string>

class           VIAnswer {
private:
  // VIAnswer attributes
  std::string   answer;

public:
  // Ctor & Dtor
  VIAnswer();
  ~VIAnswer();

  // VIAnswer routines
  void          setAnswer(std::string);
  std::string   &getAnswer() const;
};

#endif // !VIANSWER_HPP_
