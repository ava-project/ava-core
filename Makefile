DEBUG		=	yes

CC		=	g++

RM		=	rm -fr

NAME		=	test

SRC		=	test.cpp	\

OBJ_DIR		=	obj/

SRC_DIR		=	src/

INC_DIR		=	includes/

#########################################################
#                        FLAGS                          #
#########################################################

CFLAGS		=	-W -Wall -Wextra -I$(INC_DIR)

CFLAGS		+=	-I/usr/local/include -I/usr/local/include/sphinxbase

CFLAGS		+=	-I/usr/local/include/pocketsphinx -std=c++11

LFLAGS		=	-lboost_system -lcrypto -lpthread

LFLAGS		+=	-L/usr/local/lib -lpocketsphinx -lsphinxbase -lsphinxad

ifeq ($(DEBUG),yes)

CFLAGS		+=	-g3

else

CFLAGS		+=	-O3

endif

#########################################################
#                        RULES                          #
#########################################################

BUILD_PRINT	=	\e[1;34mBuilding\e[0m \e[1;33m$<\e[0m

OBJS		=	$(patsubst %.cpp,${OBJ_DIR}%.o, $(SRC))

FIRST		:=	$(shell test -d $(OBJ_DIR) || mkdir $(OBJ_DIR))

$(OBJ_DIR)%.o	:	$(patsubst %.cpp, ${SRC_DIR}%.cpp, %.cpp)
			@echo -e "$(BUILD_PRINT)" && $(CC) $(CFLAGS) -c $< -o $@

$(NAME)	:	$(OBJS)
			$(CC) $(OBJS) -o $(NAME) $(LFLAGS)

all		:
			export LD_LIBRARY_PATH=/usr/local/lib
			@$(MAKE) --no-print-directory $(NAME)

clean		:
			$(RM) $(OBJS) $(OBJ_DIR)

fclean		:	clean
			$(RM) $(NAME)

re		:	fclean all

.PHONY		:	all clean fclean re
