// TEST

#include <pocketshpinx.h>

int		main(int ac, char **av)
{
  ps_decoder_t	*ps = NULL;
  cmd_ln_t	*config = NULL;

  config = cmd_ln_init(NULL, ps_args(), TRUE,
		       "-hmm", MODELDIR "/en-us/en-us",
		       "-lm", MODELDIR "/en-us/en-us.lm.bin",
		       "-dict", MODELDIR "/en-us/cmudict-en-us.dict",
		       NULL);
  
  return (0);
}
